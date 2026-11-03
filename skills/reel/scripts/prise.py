"""Monter ta prise face caméra : les coupes sur l'énergie de ta voix, la voix montée nettoyée et transcrite, les
sous-titres calés sur elle, et le contrôle des blancs.

Usage :
  python3 prise.py couper prise.mp4 [--garder 2,3,5] [-o coupes.json]
  python3 prise.py monter prise.mp4 coupes.json [-o voix/]
  python3 prise.py pauses voix/voix.wav prise.mp4
  python3 prise.py --autotest

couper : mesure l'énergie de la voix par trames de 10 ms, garde chaque passage parlé avec 50 ms de marge autour du son
(un blanc de moins de 0,20 s reste dans le passage, un plus long le coupe), retire les bribes (moins de 0,15 s, aucun mot), et transcrit
chaque passage pour l'afficher. Sans --garder, tous les passages vont dans coupes.json ; relis la liste, puis relance
avec --garder et les numéros à garder (le raté et le faux départ sautent, jamais une phrase sans l'accord de la
personne). Les dates de la transcription ne posent jamais la coupe : elles avalent les silences.
monter : la voix des passages gardés, mise bout à bout, nettoyée à -14 LUFS et retranscrite (voix.py --enregistrement) :
voix/voix.wav, voix/align.json et voix/sous-titres.json, sur le temps du montage, aucun sous-titre à cheval sur une
coupe ; puis voix/plages.html, les balises <video> de chaque passage pour la composition ; puis le contrôle pauses.
pauses : aucun trou de 0,20 s ou plus dans la voix montée. Son témoin, la prise brute, doit en avoir : sinon la mesure
ne prouve rien. Dernière ligne : PAUSES_OK ou PAUSES_A_REVOIR.
Bibliothèque standard de Python, ffmpeg, et npx hyperframes@0.8.167 transcribe (Parakeet si installé).
"""
import array, importlib.util, json, math, os, subprocess, sys, tempfile, wave

HF = ["npx", "--yes", "hyperframes@0.8.167"]
BRIBE, TROU = 0.15, 0.20                # bribe sans mot retirée ; trou interdit dans la voix montée
ICI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("voix", os.path.join(ICI, "voix.py"))
voix = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(voix)          # la mesure d'énergie de la voix est partagée : voix.energie, voix.passages
energie, passages, SR, PAS, Echec = voix.energie, voix.passages, voix.ENERGIE_SR, voix.PAS, voix.Echec


def ffmpeg(*args):
    s = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-y", *map(str, args)], capture_output=True)
    if s.returncode:
        raise Echec(s.stderr.decode(errors="replace")[-600:])
    return s


def trous(db, seuil, tete=0.15):
    """Silences de 0,20 s ou plus après la tête, hors silence final : [(début, durée)]."""
    out, st = [], None
    for i, d in enumerate(db + [math.inf]):
        if d < seuil and st is None:
            st = i
        if d >= seuil and st is not None:
            if (i - st) * PAS >= TROU and st * PAS > tete and i < len(db):
                out.append((round(st * PAS, 2), round((i - st) * PAS, 2)))
            st = None
    return out


def transcrire(wav):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([*HF, "transcribe", wav, "-d", d, "-l", "fr"], capture_output=True, text=True)
        p = os.path.join(d, "transcript.json")
        return " ".join(w["text"] for w in json.load(open(p))) if os.path.exists(p) else ""


def couper(prise, garder=None, sortie="coupes.json"):
    liste = []
    with tempfile.TemporaryDirectory() as d:
        # l'énergie se lit sur la prise nettoyée comme le sera la voix montée : sur la brute, le bruit de pièce remplit
        # les pauses (mesuré : une virgule de 0,23 s dans la voix montée, invisible dans la prise brute)
        propre = os.path.join(d, "propre.wav")
        ffmpeg("-v", "error", "-i", prise, "-vn", "-af", voix.CHAINE, "-ac", "1", "-ar", SR, propre)
        segs = passages(*energie(propre))
        for k, (a, b) in enumerate(segs, 1):
            w = os.path.join(d, f"p{k}.wav")
            ffmpeg("-v", "error", "-ss", a, "-to", b, "-i", prise, "-vn", "-ac", "1", "-ar", SR, w)
            texte = transcrire(w)
            bribe = b - a < BRIBE and not texte
            garde = not bribe and (garder is None or k in garder)
            print(f"{k:>3}  {a:7.2f} à {b:7.2f} s  ({b - a:4.2f} s)  {'gardé ' if garde else 'bribe ' if bribe else 'coupé '} « {texte} »")
            if garde:
                liste.append({"source": os.path.basename(prise), "in": a, "out": b, "raison": f"passage {k} : « {texte} »"})
    json.dump(liste, open(sortie, "w"), ensure_ascii=False, indent=1)
    print(f"{sortie} : {len(liste)} passage(s) gardé(s) sur {len(segs)}, {sum(p['out'] - p['in'] for p in liste):.2f} s montées")
    print("COUPES_OK" if liste else "COUPES_VIDES")


def plages_html(coupes):
    """Une balise <video> muette par passage ; data-cadrage alterne 100 et 108 % à chaque coupe (le jump cut se lit voulu)."""
    lignes, t = [], 0.0
    for k, p in enumerate(coupes, 1):
        d = p["out"] - p["in"]
        lignes.append(f'<div class="plan" id="w{k}" data-cadrage="{100 if k % 2 else 108}"><video id="p{k}" class="clip" '
                      f'src="{p["source"]}" data-start="{t:.3f}" data-duration="{d:.3f}" data-media-start="{p["in"]:.3f}" '
                      f'data-track-index="0" muted playsinline></video></div>')
        t += d
    return lignes, round(t, 3)


def pauses(montee, brute):
    t = trous(*energie(brute))
    print(f"témoin, prise brute : {len(t)} trou(s) de {TROU:.2f} s ou plus")
    if not t:
        raise Echec("le témoin n'a aucun trou : la mesure ne prouve rien sur cette prise")
    v = trous(*energie(montee))
    print(f"voix montée : {len(v)} trou(s) {v}")
    print("PAUSES_OK" if not v else "PAUSES_A_REVOIR")
    return not v


def monter(prise, coupes_json, sortie="voix"):
    coupes = json.load(open(coupes_json, encoding="utf-8"))
    if not coupes or not all(p["out"] > p["in"] for p in coupes):
        raise Echec(f"{coupes_json} : des passages avec in et out attendus")
    os.makedirs(sortie, exist_ok=True)
    brute = os.path.join(sortie, "voix-montee-brute.wav")
    morceaux = "".join(f"[0:a]atrim={p['in']}:{p['out']},asetpts=N/SR/TB[a{i}];" for i, p in enumerate(coupes))
    ffmpeg("-v", "error", "-i", prise, "-filter_complex", morceaux + "".join(f"[a{i}]" for i in range(len(coupes)))
           + f"concat=n={len(coupes)}:v=0:a=1[o]", "-map", "[o]", "-ac", "1", "-ar", 48000, brute)
    s = subprocess.run([sys.executable, os.path.join(ICI, "voix.py"), "--enregistrement", brute, "-o", sortie, "--coupes", coupes_json],
                       capture_output=True, text=True)
    print(s.stdout.strip())
    if s.returncode or "VOIX_OK" not in s.stdout:
        raise Echec("voix montée : " + (s.stdout + s.stderr)[-400:])
    lignes, total = plages_html(coupes)
    open(os.path.join(sortie, "plages.html"), "w").write(
        f"<!-- {len(coupes)} plages de {os.path.basename(coupes_json)}, {total} s : copie {coupes[0]['source']} dans le projet -->\n"
        + "\n".join(lignes) + "\n")
    print(f"plages.html : {len(lignes)} plages, {total} s, cadrage alterné 100 / 108 %")
    ok = pauses(os.path.join(sortie, "voix.wav"), prise)
    print("PRISE_OK" if ok else "PRISE_A_REVOIR")
    return ok


def ecrire_wav(chemin, morceaux):
    """morceaux : [(durée, amplitude)] d'un son à 220 Hz ; amplitude 0 = silence (bruit de fond très bas)."""
    a, k = array.array("h"), 0
    for duree, amp in morceaux:
        for _ in range(int(duree * SR)):
            a.append(int(32767 * (amp * math.sin(2 * math.pi * 220 * k / SR) + 0.0003 * math.sin(k * 0.7))))
            k += 1
    with wave.open(chemin, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(a.tobytes())


def autotest():
    with tempfile.TemporaryDirectory() as d:
        brute, montee, bribe = (os.path.join(d, x) for x in ("brute.wav", "montee.wav", "bribe.wav"))
        ecrire_wav(brute, [(0.5, 0), (1.0, 0.3), (0.8, 0), (1.2, 0.3), (0.12, 0), (0.6, 0.3), (0.7, 0)])
        db, seuil = energie(brute)
        p = passages(db, seuil)
        assert len(p) == 2 and abs(p[0][0] - 0.45) < 0.02 and abs(p[0][1] - 1.55) < 0.02, p   # 50 ms autour du son
        assert abs(p[1][1] - (0.5 + 1 + 0.8 + 1.2 + 0.12 + 0.6 + 0.05)) < 0.02, p              # la respiration de 0,12 s reste
        ecrire_wav(bribe, [(0.5, 0), (1.0, 0.3), (0.23, 0), (1.0, 0.3), (0.5, 0)])
        assert len(passages(*energie(bribe))) == 2                                              # une pause de 0,23 s coupe
        assert [round(x[1], 1) for x in trous(db, seuil)] == [0.8], trous(db, seuil)           # le blanc de 0,8 s ; la tête et la respiration ne comptent pas
        ecrire_wav(montee, [(0.05, 0), (1.0, 0.3), (0.1, 0), (1.9, 0.3), (0.05, 0)])
        assert pauses(montee, brute)                                                            # 0,1 s au joint : une respiration
        assert not pauses(brute, brute)                                                         # la prise brute, elle, a un trou
        ecrire_wav(bribe, [(1.0, 0.3)])
        try:
            pauses(montee, bribe)
            raise AssertionError("un témoin sans trou est accepté")
        except Echec:
            pass
        l, t = plages_html([{"source": "prise.mp4", "in": 0.45, "out": 1.55}, {"source": "prise.mp4", "in": 2.25, "out": 4.27}])
        assert t == 3.12 and 'data-start="1.100"' in l[1] and 'data-media-start="2.250"' in l[1], l
        assert 'data-cadrage="100"' in l[0] and 'data-cadrage="108"' in l[1]
    print("autotest prise : 9 contrôles passés")


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, defaut=None: a[a.index(k) + 1] if k in a else defaut
    try:
        if a == ["--autotest"]:
            autotest()
        elif a[:1] == ["couper"] and len(a) >= 2:
            g = opt("--garder")
            couper(a[1], {int(x) for x in g.split(",")} if g else None, opt("-o", "coupes.json"))
        elif a[:1] == ["monter"] and len(a) >= 3:
            sys.exit(0 if monter(a[1], a[2], opt("-o", "voix")) else 1)
        elif a[:1] == ["pauses"] and len(a) == 3:
            sys.exit(0 if pauses(a[1], a[2]) else 1)
        else:
            sys.exit(__doc__)
    except Echec as e:
        print("ÉCHEC", e)
        sys.exit(1)
