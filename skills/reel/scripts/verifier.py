"""Vérifie un reel fini, sur le fichier : format, durée, volume, musique sous la voix, images figées, débit et mots relus.

Usage :
  python3 verifier.py final.mp4 [--format 9:16] [--ips 30] [--align voix/align.json] [--mot équipe]
                      [--mots "Pilot,1500,L'IA"] [--absents "recommence"] [--sous-titres index.html --voix voix/voix.wav]
                      [--projet .] [--carte 2] [--face-camera] [--sans-musique]
  python3 verifier.py --autotest

--format : 9:16 (par défaut, 1080 x 1920), 4:5 (1080 x 1350), 1:1 (1080 x 1080) ou 16:9 (1920 x 1080).
--ips : la cadence choisie (30 par défaut du rendu, 60 pour le rendu premium) ; sans elle, 24 à 60 images/s.
--mot : le mot à commenter ; --mots : les noms et chiffres qui doivent être entendus justes ; --absents : les mots qui
ne doivent plus s'entendre (le raté coupé d'une prise face caméra). --sous-titres : la composition (balise
<script type="application/json" id="sous-titres">) ou voix/sous-titres.json : chaque groupe doit commencer à 0,2 s au
plus du mot entendu ; --voix, la voix seule (voix/voix.wav), pour lire le retour de la voix après un blanc. La voix est relue par la transcription de HyperFrames (npx hyperframes transcribe, en français ;
modèle Parakeet si installé, voir references/verifier.md). Puis les contrôles de porte_b.py (references/controles.md) :
l'image 0, une alerte sur les bandes hors de la zone du texte, la note de mouvement de chaque seconde (--carte : les secondes de
la carte de fin, non notées, 2 par défaut) et, avec --projet (le dossier du projet HyperFrames), le déterminisme et les tirets
longs de la composition. --face-camera : le film d'une prise face caméra ; la note de mouvement s'y dit pour mémoire,
son seuil venant de films de motion sans voix (references/sources.md, C10). Chaque ligne dit OK ou À REVOIR ; la dernière dit VERIF_OK, ou VERIF_A_REVOIR et le nombre de défauts. --sans-musique : le son choisi pour ce film n'a pas de musique (des effets seuls, ou la voix seule) :
les silences entre les phrases sont voulus, une ligne INFO les dit au lieu d'un défaut.
"""
import contextlib, difflib, importlib.util, io, json, math, os, re, subprocess, sys, tempfile, unicodedata

HF = ["npx", "--yes", "hyperframes@0.8.167"]
FORMATS = {"9:16": (1080, 1920), "4:5": (1080, 1350), "1:1": (1080, 1080), "16:9": (1920, 1080)}
ECART_SOUS_TITRE, PART_RETROUVEE = 0.2, 0.9
_spec = importlib.util.spec_from_file_location("voix", os.path.join(os.path.dirname(os.path.abspath(__file__)), "voix.py"))
voix = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(voix)          # la mesure d'énergie de la voix, partagée avec voix.py et prise.py
_spec = importlib.util.spec_from_file_location("porte_b", os.path.join(os.path.dirname(os.path.abspath(__file__)), "porte_b.py"))
porte_b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(porte_b)       # image 0, zones, note de mouvement, déterminisme, tirets (references/controles.md)


def sortie(*cmd):
    s = subprocess.run(list(cmd), capture_output=True, text=True)
    return s.returncode, s.stdout + s.stderr


def sans_accents(m):
    m = unicodedata.normalize("NFD", m.lower().replace("’", "'"))
    m = re.sub(r"[^a-z0-9']", "", "".join(c for c in m if unicodedata.category(c) != "Mn"))
    # « l'énergie » vaut « énergie » ; pas « t'équipes », que la transcription entend pour « Commente « équipe » »
    return re.sub(r"^(?:l|d|qu)'(?=\w)", "", m)


NOMBRES = {"zero": "0", "un": "1", "une": "1", "deux": "2", "trois": "3", "quatre": "4", "cinq": "5", "six": "6", "sept": "7",
           "huit": "8", "neuf": "9", "dix": "10", "onze": "11", "douze": "12", "treize": "13", "quatorze": "14", "quinze": "15",
           "seize": "16", "vingt": "20", "trente": "30", "quarante": "40", "cinquante": "50", "soixante": "60", "cent": "100"}


def entendu(mot, transcrit):
    """Le mot (ou le groupe de mots) se retrouve-t-il dans la transcription ? Accents, casse et ponctuation ignorés ;
    un nombre écrit « 1 500 » vaut « 1500 »."""
    cible = [sans_accents(x) for x in re.sub(r"(\d)\s+(?=\d{3}\b)", r"\1", mot).split()]
    cible = [x for x in cible if x]
    t = [sans_accents(x) for x in re.sub(r"(\d)\s+(?=\d{3}\b)", r"\1", transcrit).split()]
    t = [x for x in t if x]
    # un nom anglais dit à la française s'écrit avec une lettre de plus (« Pilot » transcrit « Pilote ») : toléré
    # un nombre dit en lettres vaut le même en chiffres (« quatre » transcrit « 4 », et l'inverse)
    chiffre = lambda x: NOMBRES.get(x, x)
    pareil = lambda a, b: chiffre(a) == chiffre(b) or (a.startswith(b) and len(a) - len(b) <= 1 and not b.isdigit())
    return any(all(pareil(t[i + k], c) for k, c in enumerate(cible)) for i in range(len(t) - len(cible) + 1)) if cible else False


def lire_format(texte):
    v = dict(re.findall(r"^(\w+)=(.+)$", texte, re.M))
    num, den = v.get("r_frame_rate", "0/1").split("/")
    debit = v.get("bit_rate", "N/A")
    return {"largeur": int(v.get("width", 0)), "hauteur": int(v.get("height", 0)), "ips": round(int(num) / int(den), 2),
            "codec": v.get("codec_name", ""), "duree": float(v.get("duration", 0)),
            "debit": int(debit) if debit.isdigit() else 0}


def lire_volume(texte):
    """Sortie de ebur128=peak=true : volume intégré (LUFS) et crête vraie (dBTP) du résumé."""
    resume = texte[texte.rindex("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", resume).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", resume).group(1))


def lire_silences(texte):
    debuts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", texte)]
    durees = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", texte)]
    return list(zip(debuts, durees))


def lire_figees(texte):
    debuts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", texte)]
    durees = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", texte)]
    return list(zip(debuts, durees))


def debits(align):
    return [(sc["id"], round(len(sc["mots"]) / (sc["end"] - sc["start"]) * 60)) for sc in align["scenes"] if sc["end"] > sc["start"]]


def transcrire(film):
    """Les mots entendus dans le film : [{"text", "start", "end"}], ou None et l'erreur."""
    with tempfile.TemporaryDirectory() as d:
        code, txt = sortie("ffmpeg", "-v", "error", "-y", "-i", film, "-vn", "-ac", "1", "-ar", "16000", os.path.join(d, "voix.wav"))
        code, txt = sortie(*HF, "transcribe", os.path.join(d, "voix.wav"), "-d", d, "-l", "fr")
        p = os.path.join(d, "transcript.json")
        if not os.path.exists(p):
            return None, txt[-300:]
        return json.load(open(p)), ""


def lire_sous_titres(chemin):
    """Les groupes affichés [{"text", "start", "end"}] : la balise JSON de la composition, ou un fichier .json."""
    texte = open(chemin, encoding="utf-8").read()
    if chemin.endswith(".html"):
        m = re.search(r'<script type="application/json" id="sous-titres">(.*?)</script>', texte, re.S)
        if not m:
            raise ValueError("pas de balise <script type=\"application/json\" id=\"sous-titres\"> dans " + chemin)
        texte = m.group(1)
    return json.loads(texte)


def calage(groupes, entendus, parole=()):
    """Part des mots de sous-titres retrouvés dans la voix entendue, et le plus grand écart de début de groupe (s).
    Après un blanc, la transcription date le mot trop tôt (mesuré : jusqu'à 0,32 s) : l'écart s'y lit sur l'énergie de la
    voix seule (parole : ses passages, voix.passages), au retour de la voix. En parole continue, sur le mot entendu."""
    aff = [(sans_accents(m), g["start"] if i == 0 else None) for g in groupes for i, m in enumerate(g["text"].split())]
    aff = [a for a in aff if a[0]]
    ent = [(sans_accents(w["text"]), w["start"]) for w in entendus]
    ent = [e for e in ent if e[0]]
    sm = difflib.SequenceMatcher(a=[a[0] for a in aff], b=[e[0] for e in ent], autojunk=False)
    vus = {i + k: j + k for i, j, n in sm.get_matching_blocks() for k in range(n)}
    retours = [a + voix.MARGE * voix.PAS for a, b in parole]
    ecarts = []
    for i, (_, t) in enumerate(aff):
        if t is None:
            continue
        proches = [r for r in retours if t - ECART_SOUS_TITRE <= r <= t + 0.05]
        if parole and not any(a <= t < b for a, b in parole):      # affiché dans un blanc : jusqu'au retour de la voix
            ecarts.append(next((r for r in retours if r >= t), math.inf) - t)
        elif proches:                                               # posé sur le retour de la voix
            ecarts.append(min(abs(t - r) for r in proches))
        elif i in vus:
            ecarts.append(abs(t - ent[vus[i]][1]))
    return (len(vus) / len(aff) if aff else 0.0), (max(ecarts) if ecarts else None)


def lignes_porte_b(resultats, face_camera=False):
    """Les contrôles de porte_b.py, dans leur ordre ; sur une prise face caméra, la note de mouvement (la troisième) passe en
    INFO : son seuil vient de films de motion sans voix (C10), une tête qui parle bouge moins."""
    return [("INFO" if face_camera and k == 2 else ok, texte) for k, (ok, texte) in enumerate(resultats)]


def verifier(film, align=None, mot=None, mots=(), format_="9:16", ips=None, absents=(), sous_titres=None, voix_seule=None,
             projet=None, carte=porte_b.CARTE, face_camera=False, sans_musique=False):
    defauts = []
    def ligne(ok, texte):
        print(("OK        " if ok else "À REVOIR  ") + texte)
        if not ok:
            defauts.append(texte)
    _, t = sortie("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                  "stream=codec_name,width,height,r_frame_rate,bit_rate:format=duration", "-of", "default=nw=1", film)
    f = lire_format(t)
    lw, lh = FORMATS[format_]
    ligne((f["largeur"], f["hauteur"]) == (lw, lh), f"format {f['largeur']} x {f['hauteur']} (attendu {lw} x {lh}, {format_})")
    cadence = f["ips"] == ips if ips else 24 <= f["ips"] <= 60
    ligne(f["codec"] == "h264" and cadence, f"vidéo {f['codec']} à {f['ips']} images/s (attendu {ips or '24 à 60'}), "
          f"{f['debit'] / 1e6:.1f} Mbit/s")
    ligne(8 <= f["duree"] <= 90, f"durée {f['duree']:.1f} s (8 à 90 s)")
    _, t = sortie("ffmpeg", "-nostats", "-i", film, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-")
    i, crete = lire_volume(t)
    ligne(-15 <= i <= -13, f"volume {i} LUFS (visé -14)")
    ligne(crete <= -0.5, f"crête {crete} dBTP (au plus -1, tolérance 0,5)")
    _, t = sortie("ffmpeg", "-nostats", "-i", film, "-vn", "-af", "silencedetect=noise=-45dB:d=0.4", "-f", "null", "-")
    trous = [(a, b) for a, b in lire_silences(t) if a < f["duree"] - 1.0]
    if sans_musique:   # le son choisi pour ce film n'a pas de musique : les silences entre les phrases sont voulus
        print("INFO      sans musique (choix du projet) : " + (f"{len(trous)} silence(s) de 0,4 s ou plus, non comptés : " + ", ".join(
            f"{a:.1f} s ({b:.1f} s)" for a, b in trous[:5]) if trous else "aucun silence de 0,4 s ou plus"))
    else:
        ligne(not trous, "musique sous la voix, aucun trou de silence" if not trous else
              "trous de silence (pas de musique ?) à " + ", ".join(f"{a:.1f} s ({b:.1f} s)" for a, b in trous[:5]))
    _, t = sortie("ffmpeg", "-nostats", "-i", film, "-an", "-vf", "freezedetect=n=0.003:d=1.0", "-f", "null", "-")
    fig = [(a, b) for a, b in lire_figees(t) if a < f["duree"] - 2.0]   # la carte de fin peut tenir
    ligne(not fig, "aucune image figée plus d'une seconde" if not fig else
          "images figées à " + ", ".join(f"{a:.1f} s ({b:.1f} s)" for a, b in fig[:5]))
    if align:
        al = json.load(open(align))
        vite = [f"{s} ({d} mots/min)" for s, d in debits(al) if d > 200]
        if al.get("voix") == "enregistrement":            # ta prise : ton débit, qu'on ne refait pas ; dit pour mémoire
            print("INFO      débit de ta prise : " + ", ".join(f"{s} {d} mots/min" for s, d in debits(al)))
        else:
            ligne(not vite, "débit de chaque scène sous 200 mots/min" if not vite else "scènes trop rapides : " + ", ".join(vite))
    if mot or mots or absents or sous_titres:
        entendus, erreur = transcrire(film)
        if entendus is None:
            ligne(False, "voix non relue : la transcription a échoué (" + erreur.strip()[:120] + ")")
        else:
            texte = " ".join(w["text"] for w in entendus)
            for m in ([mot] if mot else []) + list(mots):
                ligne(entendu(m, texte), f"« {m} » entendu" if entendu(m, texte) else f"« {m} » pas entendu dans la voix")
            for m in absents:
                ligne(not entendu(m, texte), f"« {m} » coupé" if not entendu(m, texte) else f"« {m} » encore entendu : la coupe l'a laissé")
            if sous_titres:
                groupes = lire_sous_titres(sous_titres)
                parole = voix.passages(*voix.energie(voix_seule)) if voix_seule else ()
                # témoins : les mêmes sous-titres avancés puis retardés de 0,3 s doivent être refusés, sinon la mesure ne prouve rien
                temoins = [calage([dict(g, start=g["start"] + d) for g in groupes], entendus, parole)[1] for d in (-0.3, 0.3)]
                part, ecart = calage(groupes, entendus, parole)
                vu = all(x is not None and x > ECART_SOUS_TITRE for x in temoins)
                ok = vu and part >= PART_RETROUVEE and ecart is not None and ecart <= ECART_SOUS_TITRE
                nb = lambda x: "?" if x is None else f"{x:.2f}"
                ligne(ok, f"sous-titres : {len(groupes)} groupes, {part:.0%} des mots entendus, écart max {nb(ecart)} s "
                      f"(au plus {ECART_SOUS_TITRE} s, mesuré {'sur la voix seule' if voix_seule else 'sur la transcription'} ; "
                      f"témoins à -0,3 et +0,3 s : {nb(temoins[0])} et {nb(temoins[1])} s{'' if vu else ', pas vus'})")
    for ok, texte in lignes_porte_b(porte_b.controles(film, format_, projet, carte), face_camera):
        if ok == "INFO":
            print("INFO      " + texte + " (prise face caméra : pour mémoire)")
        else:
            ligne(ok, texte)
    print("VERIF_OK" if not defauts else f"VERIF_A_REVOIR {len(defauts)}")
    return not defauts


def autotest():
    assert entendu("équipe", "Commente Équipe, et je t'envoie le lien")
    assert not entendu("équipe", "Comment t'équipes et je t'envoie")
    assert entendu("1 500", "plus de 1500 sites") and entendu("L'IA", "L’IA ne décide pas")
    assert entendu("énergie", "sur l'énergie de ma voix") and not entendu("énergie", "sur l'énergique")
    assert not entendu("Pilot", "Kilo lit les annonces") and entendu("Pilot", "Pilote lit les annonces")
    assert not entendu("15", "150 sites")
    assert entendu("quatre", "4 PME sur 10") and entendu("4", "quatre PME") and not entendu("quatre", "5 PME")
    f = lire_format("codec_name=h264\nwidth=1080\nheight=1920\nr_frame_rate=30/1\nbit_rate=N/A\nduration=41.2\n")
    assert f == {"largeur": 1080, "hauteur": 1920, "ips": 30.0, "codec": "h264", "duree": 41.2, "debit": 0}, f
    assert lire_format("width=1920\nheight=1080\nr_frame_rate=60/1\nbit_rate=24000000\n")["debit"] == 24000000
    assert FORMATS["4:5"] == (1080, 1350) and FORMATS["16:9"] == (1920, 1080)
    ent = [{"text": "Le", "start": 1.0}, {"text": "lait", "start": 1.2}, {"text": "est", "start": 1.5}, {"text": "au", "start": 1.7},
           {"text": "fond.", "start": 1.9}]
    g = [{"text": "Le lait", "start": 1.05}, {"text": "est au fond", "start": 1.45}]
    part, ecart = calage(g, ent)
    assert part == 1.0 and abs(ecart - 0.05) < 1e-9, (part, ecart)
    part, ecart = calage([dict(x, start=x["start"] + 0.3) for x in g], ent)
    assert ecart > ECART_SOUS_TITRE, ecart                       # le témoin décalé est vu
    # après un blanc, la transcription date « ton » à 6,64 s ; la voix revient à 6,96 s (mesuré sur l'essai 3D)
    ent2, g2, parole = [{"text": "ton", "start": 6.64}], [{"text": "ton", "start": 6.96}], [(6.91, 7.88)]
    assert abs(calage(g2, ent2)[1] - 0.32) < 1e-9                                                # sans la voix : refusé à tort
    assert abs(calage(g2, ent2, parole)[1]) < 1e-9                                                # sur la voix : juste
    assert abs(calage([{"text": "ton", "start": 6.66}], ent2, parole)[1] - 0.30) < 1e-9          # affiché dans le blanc : vu
    with tempfile.TemporaryDirectory() as d:
        h = os.path.join(d, "index.html")
        open(h, "w").write('<script type="application/json" id="sous-titres">[{"text": "Le lait", "start": 1.05, "end": 1.4}]</script>')
        assert lire_sous_titres(h)[0]["text"] == "Le lait"
    eb = "t: 1 ...\n[Parsed_ebur128_0 @ x] Summary:\n\n  Integrated loudness:\n    I:         -14.2 LUFS\n  True peak:\n    Peak:       -1.3 dBFS\n"
    assert lire_volume(eb) == (-14.2, -1.3)
    assert lire_silences("silence_start: 3.5\n... silence_end: 4.1 | silence_duration: 0.6\n") == [(3.5, 0.6)]
    assert lire_figees("lavfi.freezedetect.freeze_start: 10.2\nlavfi.freezedetect.freeze_duration: 1.4\n") == [(10.2, 1.4)]
    assert debits({"scenes": [{"id": "s1", "start": 0, "end": 3, "mots": [0] * 12}]}) == [("s1", 240)]
    r = [(True, "image 0"), (True, "zones"), (False, "secondes faibles : 1-2 s")]
    assert [x[0] for x in lignes_porte_b(r)] == [True, True, False]                 # un film de motion : la seconde molle compte
    assert [x[0] for x in lignes_porte_b(r, face_camera=True)] == [True, True, "INFO"]  # une prise face caméra : pour mémoire
    # témoin sans musique : une voix de 8,5 s qui se tait 1,5 s ; sans --sans-musique, ce silence est un défaut ; avec, une ligne INFO
    with tempfile.TemporaryDirectory() as d:
        film, sans, avec = os.path.join(d, "voix.mp4"), io.StringIO(), io.StringIO()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=d=8.5:s=360x450:r=30,scale=1080:1350", "-f", "lavfi",
                        "-i", "sine=f=220:d=8.5", "-af", "volume='if(between(t,3,4.5),0,1)':eval=frame", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-shortest", film], check=True)
        with contextlib.redirect_stdout(sans):
            verifier(film, format_="4:5", ips=30)
        with contextlib.redirect_stdout(avec):
            verifier(film, format_="4:5", ips=30, sans_musique=True)
    assert "À REVOIR  trous de silence" in sans.getvalue(), sans.getvalue()
    assert "INFO      sans musique" in avec.getvalue() and "trous de silence" not in avec.getvalue(), avec.getvalue()
    print("témoin sans musique : refusé sans l'option, accepté avec")
    print("autotest vérification : 23 contrôles passés")
    porte_b.autotest()


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--autotest"]:
        autotest()
        sys.exit()
    if not a or a[0].startswith("-"):
        sys.exit(__doc__)
    def opt(k):
        return a[a.index(k) + 1] if k in a else None
    liste = lambda k: [m.strip() for m in (opt(k) or "").split(",") if m.strip()]
    if (opt("--format") or "9:16") not in FORMATS:
        sys.exit("--format : " + ", ".join(FORMATS))
    ok = verifier(a[0], opt("--align"), opt("--mot"), liste("--mots"), opt("--format") or "9:16",
                  float(opt("--ips")) if opt("--ips") else None, liste("--absents"), opt("--sous-titres"), opt("--voix"),
                  opt("--projet"), float(opt("--carte")) if opt("--carte") else porte_b.CARTE, "--face-camera" in a, "--sans-musique" in a)
    sys.exit(0 if ok else 1)
