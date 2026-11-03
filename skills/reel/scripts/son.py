"""Le son d'un reel : une musique sous la voix qui se baisse quand elle parle, un bruitage par information, le master à -14 LUFS.

Usage :
  python3 son.py --video film.mp4 --voix voix/voix.wav --align voix/align.json -o final.mp4
                 [--musique ta-piste.mp3] [--bpm 110] [--bruitages bruitages.json] [--sans-musique]
  python3 son.py --autotest

--musique : ta piste, libre de droits pour un usage commercial. Sans elle, une musique douce est fabriquée ici, au tempo
--bpm (accords, basse, pied et charleston de synthèse) : libre de droits, puisqu'elle est calculée sur ta machine.
bruitages.json : [{"t": 1.2, "son": "pop"}, {"t": 6.3, "son": "souffle"}] ; sons : pop, souffle, tic. Un son par
information qui arrive à l'image, jamais sur une coupe vide.

Niveaux : la musique à -18 LUFS seule, 8 dB plus bas quand la voix parle (donc 12 dB sous la voix), les bruitages sous la
voix, et le tout ramené à -14 LUFS intégré et -1 dBTP au plus. La vidéo n'est pas réencodée.
"""
import array, json, math, os, random, subprocess, sys, tempfile, wave

TAUX = 22050
BAISSE = 10 ** (-8 / 20)        # gain de la musique quand la voix parle
RAMPE = 0.15                    # secondes pour descendre ou remonter
FUSION = 0.4                    # deux mots séparés de moins de 0,4 s : la musique reste baissée entre eux


def ffmpeg(*args):
    s = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", *args], capture_output=True, text=True)
    if s.returncode:
        raise RuntimeError(s.stderr[-800:])
    return s.stderr


def duree(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True, check=True).stdout)


def plages_voix(align):
    """Les moments où la voix parle, mots voisins fusionnés : [(début, fin), ...]."""
    mots = sorted((m["start"], m["end"]) for sc in align["scenes"] for m in sc["mots"])
    plages = []
    for a, b in mots:
        if plages and a - plages[-1][1] < FUSION:
            plages[-1][1] = max(plages[-1][1], b)
        else:
            plages.append([a, b])
    return [(round(a, 3), round(b, 3)) for a, b in plages]


def expression_gain(plages):
    """Expression ffmpeg du gain de la musique : 1 hors voix, BAISSE pendant la voix, rampes de RAMPE s."""
    if not plages:
        return "1"
    r = RAMPE
    d = [f"clip(min((t-{a - r:.3f})/{r},({b + r:.3f}-t)/{r}),0,1)" for a, b in plages]
    m = d[0]
    for x in d[1:]:
        m = f"max({m},{x})"
    return f"1-{1 - BAISSE:.4f}*{m}"


def note(n):                                   # numéro MIDI -> fréquence
    return 440 * 2 ** ((n - 69) / 12)


def musique_calculee(chemin, secondes, bpm):
    """Accords la mineur, fa, do, sol (2 mesures chacun), basse, pied sur les temps, charleston à contretemps."""
    accords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]]
    temps = 60 / bpm
    mesure = 4 * temps
    n = int(secondes * TAUX)
    rnd = random.Random(7)                     # graine fixe : la même musique à chaque passage
    sortie = array.array("h")
    prec_bruit = 0.0
    for i in range(n):
        t = i / TAUX
        acc = accords[int(t // (2 * mesure)) % 4]
        dans = t % (2 * mesure)
        env = min(1.0, dans / 0.6) * min(1.0, (2 * mesure - dans) / 0.4)
        nappe = sum(math.sin(2 * math.pi * note(k) * t) + 0.5 * math.sin(2 * math.pi * note(k) * 1.003 * t) for k in acc) / 6
        basse = math.sin(2 * math.pi * note(acc[0] - 12) * t) * 0.5
        tb = t % temps
        pied = math.sin(2 * math.pi * (45 + 55 * math.exp(-tb * 30)) * tb) * math.exp(-tb * 9) if tb < 0.3 else 0.0
        tc = (t + temps / 2) % temps
        bruit = rnd.uniform(-1, 1)
        haut = bruit - prec_bruit                 # passe-haut grossier : le souffle devient charleston
        prec_bruit = bruit
        charl = haut * math.exp(-tc * 60) * 0.25 if tc < 0.06 else 0.0
        x = 0.30 * env * nappe + 0.22 * env * basse + 0.45 * pied + charl
        sortie.append(int(max(-1.0, min(1.0, x * 0.8)) * 32767))
    with wave.open(chemin, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TAUX)
        w.writeframes(sortie.tobytes())


def bruitage(son, rnd):
    """Un bruitage court, calculé : pop (note qui monte), souffle (bruit qui enfle et retombe), tic (clic)."""
    if son == "pop":
        d = 0.09
        return [math.sin(2 * math.pi * (700 + 900 * i / (d * TAUX)) * i / TAUX) * math.exp(-i / TAUX * 35) for i in range(int(d * TAUX))]
    if son == "souffle":
        d, p, y = 0.4, 0.0, []
        for i in range(int(d * TAUX)):
            b = rnd.uniform(-1, 1)
            p = 0.85 * p + 0.15 * b                 # passe-bas : un souffle, pas un grésillement
            y.append(p * math.sin(math.pi * i / (d * TAUX)) * 1.6)
        return y
    if son == "tic":
        return [rnd.uniform(-1, 1) * math.exp(-i / TAUX * 400) for i in range(int(0.02 * TAUX))]
    raise ValueError(f"bruitage inconnu : {son} (pop, souffle, tic)")


def piste_bruitages(chemin, secondes, liste):
    rnd = random.Random(11)
    x = [0.0] * int(secondes * TAUX)
    for b in liste:
        debut = int(b["t"] * TAUX)
        for k, v in enumerate(bruitage(b["son"], rnd)):
            if debut + k < len(x):
                x[debut + k] += v * 0.5
    with wave.open(chemin, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TAUX)
        w.writeframes(array.array("h", (int(max(-1.0, min(1.0, v)) * 32767) for v in x)).tobytes())


def loudnorm_deux_passes(entree_args, filtre, cible, sortie_args):
    m = ffmpeg(*entree_args, "-filter_complex", filtre + f",loudnorm=I={cible}:TP=-1:LRA=11:print_format=json[o]",
               "-map", "[o]", "-f", "null", "-")
    j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    ln = (f"loudnorm=I={cible}:TP=-1:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    ffmpeg(*entree_args, "-filter_complex", filtre + "," + ln + "[o]", "-map", "[o]", *sortie_args)


def mixer(video, voix, align, sortie, musique=None, bpm=110, bruitages=None, sans_musique=False):
    d = duree(video)
    tmp = tempfile.mkdtemp(prefix="son-")
    entrees, branches, n = ["-i", voix], ["[0:a]aresample=48000,apad[v]"], 1
    if not sans_musique:
        piste = os.path.join(tmp, "musique-18.wav")
        source = musique
        if not source:
            source = os.path.join(tmp, "musique.wav")
            musique_calculee(source, d + 1, bpm)
        # la musique seule à -18 LUFS, avant le mixage
        loudnorm_deux_passes(["-i", source], f"[0:a]atrim=0:{d:.3f},aresample=48000", -18, ["-ar", "48000", "-c:a", "pcm_s16le", piste])
        gain = expression_gain(plages_voix(json.load(open(align))))
        entrees += ["-i", piste]
        branches.append(f"[{n}:a]volume='{gain}':eval=frame,afade=t=out:st={max(0, d - 1):.3f}:d=1[m]")
        n += 1
    if bruitages:
        pb = os.path.join(tmp, "bruitages.wav")
        piste_bruitages(pb, d, json.load(open(bruitages)))
        entrees += ["-i", pb]
        branches.append(f"[{n}:a]aresample=48000,volume=0.5[b]")
        n += 1
    noms = "[v]" + ("[m]" if not sans_musique else "") + ("[b]" if bruitages else "")
    filtre = ";".join(branches) + f";{noms}amix=inputs={n}:normalize=0:duration=first,atrim=0:{d:.3f}"
    audio = os.path.join(tmp, "master.wav")
    loudnorm_deux_passes(entrees, filtre, -14, ["-ar", "48000", "-c:a", "pcm_s16le", audio])
    ffmpeg("-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", "-shortest", sortie)
    print(f"{sortie} : {d:.1f} s, musique {'aucune' if sans_musique else (os.path.basename(musique) if musique else f'calculée à {bpm} BPM')}, "
          f"{len(json.load(open(bruitages))) if bruitages else 0} bruitage(s), master visé -14 LUFS / -1 dBTP")
    print("SON_OK")


def autotest():
    al = {"scenes": [{"mots": [{"start": 0.0, "end": 0.4}, {"start": 0.6, "end": 1.0}, {"start": 2.0, "end": 2.5}]}]}
    assert plages_voix(al) == [(0.0, 1.0), (2.0, 2.5)], plages_voix(al)
    g = expression_gain([(1.0, 2.0)])
    t = 1.5                                          # en pleine voix : la musique est à BAISSE
    v = eval(g.replace("clip", "_clip").replace("t-", f"{t}-").replace("-t)", f"-{t})"),
             {"_clip": lambda x, a, b: max(a, min(b, x)), "min": min, "max": max})
    assert abs(v - BAISSE) < 1e-3, v
    assert expression_gain([]) == "1"
    rnd = random.Random(1)
    assert all(len(bruitage(s, rnd)) > 0 for s in ("pop", "souffle", "tic"))
    try:
        bruitage("klaxon", rnd)
        raise AssertionError("bruitage inconnu accepté")
    except ValueError:
        pass
    with tempfile.TemporaryDirectory() as d:          # bout en bout : 3 s de vidéo, une voix, la musique calculée
        vid, vx, ali, out = (os.path.join(d, x) for x in ("v.mp4", "voix.wav", "align.json", "final.mp4"))
        ffmpeg("-f", "lavfi", "-i", "color=c=black:s=108x192:d=3:r=30", "-c:v", "libx264", "-pix_fmt", "yuv420p", vid)
        ffmpeg("-f", "lavfi", "-i", "sine=f=220:d=1.5", "-af", "apad=pad_dur=1.5", "-ar", "48000", vx)
        json.dump({"scenes": [{"mots": [{"start": 0.0, "end": 1.5}]}]}, open(ali, "w"))
        bj = os.path.join(d, "b.json")
        json.dump([{"t": 2.0, "son": "pop"}], open(bj, "w"))
        mixer(vid, vx, ali, out, bpm=110, bruitages=bj)
        e = ffmpeg("-i", out, "-af", "ebur128", "-f", "null", "-")
        i = float(e[e.rindex("I:"):].split()[1])
        assert -15.5 < i < -12.5, i                    # sur 3 s, loudnorm vise -14 sans l'atteindre au dixième
    print("autotest son : 6 contrôles passés")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--autotest"]:
        autotest()
        sys.exit()
    def opt(k, defaut=None):
        return a[a.index(k) + 1] if k in a else defaut
    if not ("--video" in a and "--voix" in a and "--align" in a and "-o" in a):
        sys.exit(__doc__)
    mixer(opt("--video"), opt("--voix"), opt("--align"), opt("-o"), opt("--musique"), int(opt("--bpm", 110)),
          opt("--bruitages"), "--sans-musique" in a)
