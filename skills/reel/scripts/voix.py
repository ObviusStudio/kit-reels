"""La voix d'un reel, scène par scène, avec ElevenLabs v3 : générée, mesurée, reprise si elle va trop vite, nettoyée, à -14 LUFS.

Usage :
  python3 voix.py scenes.json [-o voix/]
  python3 voix.py --voix-dispo           liste les voix de ton compte (nom et identifiant)
  python3 voix.py --enregistrement prise.m4a [-o voix/] [--coupes coupes.json]   ta propre voix, nettoyée et transcrite
  python3 voix.py --autotest             contrôle les calculs, sans réseau

scenes.json :
  {"voix": "<identifiant ElevenLabs, Théo par défaut>", "ton": "excited",
   "scenes": [{"id": "s01", "texte": "Ta première phrase. Ta deuxième."}, ...]}

Une scène = 2 à 4 phrases dites d'un souffle. Le texte s'écrit pour être dit : chiffres en chiffres, le mot à commenter
en minuscules entre guillemets (« équipe ») ; en capitales, la voix le lit à l'anglaise.

Sorties dans le dossier -o : voix.wav (la piste nettoyée, -14 LUFS), align.json (les temps de chaque mot),
sous-titres.json (les groupes d'une ligne, calés sur ces temps), rapport.json (débit de chaque scène, reprises), et
cache/ (une scène déjà payée n'est jamais refacturée). La clé est lue dans ELEVENLABS_API_KEY, jamais affichée ni écrite.
--coupes : la liste de coupes d'une prise face caméra (prise.py) ; aucun sous-titre n'est à cheval sur une coupe.
"""
import array, base64, hashlib, json, math, os, re, subprocess, sys, urllib.error, urllib.request

THEO = "NBjtCdChq5Ph56VnCM8Z"          # Théo, voix française de la bibliothèque ElevenLabs
MODELE = "eleven_v3"
REGLAGES = {"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": True}
TROP_VITE = 200                         # mots par minute : au-dessus, on reprend la scène
BLANC = 0.25                            # secondes entre deux scènes (pauses de 0,1 à 0,5 s)
SOUS_TITRE_CAR, SOUS_TITRE_MIN, FIN_APRES, COLLE = 18, 0.8, 0.15, 0.4   # une ligne à 76 px ; 0,8 s pour lire
ENERGIE_SR, PAS, SOUS_P95 = 16000, 0.01, 30   # trames de 10 ms ; parole : 30 dB sous le 95e centile du fichier
MARGE, GARDE, RETOUR = 5, 0.10, 0.6           # 50 ms autour du son ; pause gardée sous 0,10 + 2 x 0,05 = 0,20 s, le
                                              # trou interdit du montage (0,18 laissait passer 0,23 s, vu) ; un sous-titre dans un blanc
                                              # se pose sur le retour de la voix s'il arrive dans les 0,6 s
CHAINE = "afftdn=nf=-25,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=60,equalizer=f=3200:t=q:w=1.2:g=2"


def mots(texte):
    """Les mots dits : sans les balises de ton (« [excited] ») ni la ponctuation seule."""
    return [m for m in re.split(r"\s+", re.sub(r"\[[^\]]*\]", " ", texte)) if re.search(r"\w", m)]


def avec_pauses(texte):
    """Seconde prise : une pause écrite « … » entre les phrases (v3 ignore le SSML, le rythme passe par la ponctuation)."""
    t = re.sub(r"([.?!])\s+(?=\S)", r"\1… ", texte.strip())
    if t == texte.strip():                       # une seule phrase : la pause va après la première virgule
        t = texte.strip().replace(", ", ",… ", 1)
    return t


def debit(n_mots, duree):
    return round(n_mots / duree * 60) if duree > 0 else 0


class Echec(Exception):
    pass


def energie(chemin):
    """Énergie en dB par trame de 10 ms (son lu en mono 16 kHz), et le seuil de parole de ce fichier."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", chemin, "-vn", "-ac", "1", "-ar", str(ENERGIE_SR), "-f", "s16le", "-"],
                       capture_output=True)
    if r.returncode:
        raise Echec(f"son illisible : {chemin} ({r.stderr.decode(errors='replace').strip()[-200:]})")
    a = array.array("h")
    a.frombytes(r.stdout[:len(r.stdout) // 2 * 2])
    if sys.byteorder == "big":
        a.byteswap()
    h = int(ENERGIE_SR * PAS)
    db = [10 * math.log10(max(sum(x * x for x in a[i:i + h]) / h, 1e-12) / 32768 ** 2) for i in range(0, len(a) - h + 1, h)]
    if not db:
        raise Echec(f"aucun son dans {chemin}")
    return db, sorted(db)[int(len(db) * 0.95)] - SOUS_P95


def passages(db, seuil):
    """Les passages parlés (début, fin) en secondes, mesurés sur l'énergie, jamais sur les dates des mots."""
    on = [d >= seuil for d in db]
    on = [any(on[max(0, i - MARGE):i + MARGE + 1]) for i in range(len(on))]
    segs, st = [], None
    for i, v in enumerate(on + [False]):
        if v and st is None:
            st = i
        if not v and st is not None:
            segs.append([st, i])
            st = None
    fus = []
    for x, y in segs:
        if fus and (x - fus[-1][1]) * PAS < GARDE:
            fus[-1][1] = y
        else:
            fus.append([x, y])
    return [(round(x * PAS, 3), round(y * PAS, 3)) for x, y in fus]


def caler(groupes_, chemin_voix):
    """Les dates des mots (l'alignement d'ElevenLabs, la transcription) tombent trop tôt ou trop tard après un blanc
    (mesuré : jusqu'à 0,33 s). Un groupe qui commence dans un blanc de la voix se pose sur son retour, lu sur l'énergie."""
    db, seuil = energie(chemin_voix)
    ps = passages(db, seuil)
    for k, g in enumerate(groupes_):
        if any(a <= g["start"] < b for a, b in ps):
            continue
        retour = next((a + MARGE * PAS for a, b in ps if a >= g["start"]), None)
        if retour is None or retour - g["start"] > RETOUR:
            continue
        if k and abs(groupes_[k - 1]["end"] - g["start"]) < 1e-6:
            groupes_[k - 1]["end"] = round(retour, 3)
        g["start"] = round(retour, 3)
        suivant = groupes_[k + 1]["start"] if k + 1 < len(groupes_) else math.inf
        g["end"] = round(min(max(g["end"], retour + SOUS_TITRE_MIN), suivant), 3)
    return groupes_


def texte_groupe(g):
    return re.sub(r"[.,;:…]+$", "", " ".join(x["w"] for x in g))


# un groupe ne finit pas sur ces petits mots : ils appellent le suivant (« ton | panier », « se | remplit »)
PETITS = set("le la les l' un une des du de d' à au aux en et ou mais que qu' qui pour par sur sous dans avec sans ce cet cette "
             "ces mon ma mes ton ta tes son sa ses notre votre leur leurs je tu il elle on nous vous ils elles se me te ne n' "
             "y c' j' s' t' m' est chaque tous toutes très".split())


def cout(g):
    """Le prix d'un groupe : trop court pour être lu, trop de mots, une fin sur un petit mot, une ponctuation au milieu."""
    duree = g[-1]["end"] - g[0]["start"] + FIN_APRES
    fin = re.sub(r"[^\w']", "", g[-1]["w"].lower())
    milieu = sum(x["w"][-1] in ",.;:!?…" for x in g[:-1])
    return 1 + 12 * max(0, SOUS_TITRE_MIN - duree) / SOUS_TITRE_MIN + 3 * max(0, len(g) - 3) + 4 * (fin in PETITS) + 3 * milieu


def groupes(scenes, coupures=()):
    """Sous-titres d'une ligne (18 caractères au plus, 4 mots au plus), jamais à cheval sur une scène ou une coupe,
    découpés au moindre coût (voir cout). Un groupe finit au début du suivant si celui-ci suit de moins de 0,4 s, sinon
    0,15 s après son dernier mot (au moins 0,8 s après son début), sans passer la coupe suivante.
    -> [{"text", "start", "end"}]"""
    coupures = sorted(coupures)
    morceau = lambda w: sum(c <= (w["start"] + w["end"]) / 2 for c in coupures)
    tous = []
    for sc in scenes:
        ms = sc["mots"]
        runs, i = [], 0
        while i < len(ms):
            j = i + 1
            while j < len(ms) and morceau(ms[j]) == morceau(ms[i]):
                j += 1
            runs.append(ms[i:j])
            i = j
        for run in runs:
            # meilleur découpage du morceau : best[k] = (coût, groupes) pour ses k premiers mots
            best = [(0, [])] + [None] * len(run)
            for k in range(1, len(run) + 1):
                for n in range(1, 5):
                    g = run[k - n:k] if n <= k else None
                    if not g or (n > 1 and len(texte_groupe(g)) > SOUS_TITRE_CAR) or best[k - n] is None:
                        continue
                    c = best[k - n][0] + cout(g)
                    if best[k] is None or c < best[k][0]:
                        best[k] = (c, best[k - n][1] + [g])
            n = morceau(run[0])
            limite = sc["end"] + FIN_APRES if n == len(coupures) else min(coupures[n], sc["end"] + FIN_APRES)
            tous += [(g, limite) for g in best[-1][1]]
    sortie = []
    for k, (g, limite) in enumerate(tous):
        debut, fin = g[0]["start"], max(g[-1]["end"] + FIN_APRES, g[0]["start"] + SOUS_TITRE_MIN)
        suivant = tous[k + 1][0][0]["start"] if k + 1 < len(tous) else None
        if suivant is not None and suivant - g[-1]["end"] < COLLE:
            fin = suivant
        fin = min([fin, limite] + ([suivant] if suivant is not None else []))
        sortie.append({"text": texte_groupe(g), "start": round(debut, 3), "end": round(fin, 3)})
    return sortie


def ecrire_sous_titres(scenes, sortie, coupures=()):
    g = caler(groupes(scenes, coupures), os.path.join(sortie, "voix.wav"))
    json.dump(g, open(os.path.join(sortie, "sous-titres.json"), "w"), ensure_ascii=False, indent=1)
    print(f"sous-titres.json : {len(g)} groupes d'une ligne, calés sur la voix")


def mots_alignes(ali, decalage):
    """Alignement caractère par caractère d'ElevenLabs -> [{"w", "start", "end"}], balises de ton retirées."""
    car, deb, fin = ali["characters"], ali["character_start_times_seconds"], ali["character_end_times_seconds"]
    sortie, cur = [], None
    for c, d, f in zip(car, deb, fin):
        if c.isspace():
            if cur:
                sortie.append(cur)
            cur = None
            continue
        if cur is None:
            cur = {"w": "", "start": round(d + decalage, 3), "end": 0}
        cur["w"] += c
        cur["end"] = round(f + decalage, 3)
    if cur:
        sortie.append(cur)
    garde = []
    for m in sortie:
        if re.fullmatch(r"\[[^\]]*\][.,]?", m["w"]):
            continue
        if not re.search(r"\w", m["w"]):              # « ? » détaché par l'espace française : collé au mot d'avant
            if garde:
                garde[-1]["w"] += " " + m["w"]
                garde[-1]["end"] = m["end"]
            continue
        garde.append(m)
    return garde


def duree_parole(ali):
    """Du premier au dernier caractère dit, balises comprises à durée nulle."""
    car = ali["characters"]
    idx = [i for i, c in enumerate(car) if not c.isspace()]
    if not idx:
        return 0.0
    return ali["character_end_times_seconds"][idx[-1]] - ali["character_start_times_seconds"][idx[0]]


def cle_cache(voix, texte, reglages, modele):
    return hashlib.sha256(json.dumps([voix, texte, reglages, modele], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def appel(url, corps=None):
    cle = os.environ.get("ELEVENLABS_API_KEY")
    if not cle:
        sys.exit("Pas de clé : mets ta clé ElevenLabs dans ELEVENLABS_API_KEY (voir references/voix.md, section 4).")
    req = urllib.request.Request(url, data=json.dumps(corps).encode() if corps is not None else None,
                                 headers={"xi-api-key": cle, "Content-Type": "application/json"})
    for essai in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as err:
            detail = err.read().decode(errors="replace")[:300]
            if err.code in (429, 500, 502, 503) and essai < 3:
                __import__("time").sleep(4 * (essai + 1))
                continue
            sys.exit(f"ElevenLabs refuse ({err.code}) : {detail}")
        except OSError as err:
            if essai == 3:
                raise
            print("réseau, nouvelle tentative :", type(err).__name__)
            __import__("time").sleep(3 * (essai + 1))


def prise(voix, texte, cache):
    """Une prise : mp3 et alignement, depuis le cache si ce texte a déjà été payé."""
    k = cle_cache(voix, texte, REGLAGES, MODELE)
    mp3, js = os.path.join(cache, k + ".mp3"), os.path.join(cache, k + ".json")
    paye = 0
    if not os.path.exists(mp3):
        paye = len(texte)
        r = appel(f"https://api.elevenlabs.io/v1/text-to-speech/{voix}/with-timestamps?output_format=mp3_44100_128",
                  {"text": texte, "model_id": MODELE, "voice_settings": REGLAGES})
        open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
        json.dump(r["alignment"], open(js, "w"))
    return mp3, json.load(open(js)), paye


def ffmpeg(*args):
    s = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", *args], capture_output=True, text=True)
    if s.returncode:
        raise RuntimeError(s.stderr[-600:])
    return s.stderr


def duree_fichier(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True, check=True).stdout)


def loudnorm_mesure(stderr):
    return json.loads(stderr[stderr.rindex("{"):stderr.rindex("}") + 1])


def nettoyer(brut, final):
    """Chaîne voix (débruitage, coupe-bas, compression, présence) puis -14 LUFS et -1,5 dBTP en deux passes."""
    m = loudnorm_mesure(ffmpeg("-i", brut, "-af", CHAINE + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"))
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    ffmpeg("-i", brut, "-af", CHAINE + "," + ln, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", final)


def fabriquer(conf_path, sortie):
    conf = json.load(open(conf_path, encoding="utf-8"))
    voix, ton = conf.get("voix") or THEO, conf.get("ton", "excited")
    cache = os.path.join(sortie, "cache")
    os.makedirs(cache, exist_ok=True)
    tete = f"[{ton}] " if ton else ""
    rapport, liste, scenes, t, caracteres = [], [], [], 0.0, 0
    blanc = os.path.join(cache, "blanc.wav")
    ffmpeg("-f", "lavfi", "-t", str(BLANC), "-i", "anullsrc=r=44100:cl=mono", "-c:a", "pcm_s16le", blanc)
    for i, sc in enumerate(conf["scenes"]):
        n = len(mots(sc["texte"]))
        mp3, ali, c = prise(voix, tete + sc["texte"], cache)
        caracteres += c
        d = debit(n, duree_parole(ali))
        prises = [(d, mp3, ali)]
        if d > TROP_VITE:                                   # reprise, une fois, avec des pauses écrites
            mp3b, alib, c = prise(voix, tete + avec_pauses(sc["texte"]), cache)
            caracteres += c
            prises.append((debit(n, duree_parole(alib)), mp3b, alib))
        d, mp3, ali = min(prises, key=lambda p: p[0])
        wav = os.path.join(cache, f"{sc['id']}.wav")
        ffmpeg("-i", mp3, "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", wav)
        if i:
            liste.append(blanc)
            t += BLANC
        liste.append(wav)
        duree = duree_fichier(wav)
        scenes.append({"id": sc["id"], "start": round(t, 3), "end": round(t + duree, 3), "texte": sc["texte"], "mots": mots_alignes(ali, t)})
        rapport.append({"id": sc["id"], "mots": n, "mots_par_min": d, "prises": len(prises),
                        "a_raccourcir": d > TROP_VITE})
        t += duree
    lst = os.path.join(cache, "liste.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in liste))
    brut = os.path.join(cache, "voix-brute.wav")
    ffmpeg("-f", "concat", "-safe", "0", "-i", lst, "-c:a", "pcm_s16le", brut)
    nettoyer(brut, os.path.join(sortie, "voix.wav"))
    total = sum(r["mots"] for r in rapport)
    json.dump({"duree": round(t, 3), "voix": voix, "modele": MODELE, "scenes": scenes},
              open(os.path.join(sortie, "align.json"), "w"), ensure_ascii=False, indent=1)
    ecrire_sous_titres(scenes, sortie)
    bilan = {"duree_s": round(t, 2), "mots": total, "mots_par_min": debit(total, t), "caracteres_payes": caracteres,
             "scenes": rapport}
    json.dump(bilan, open(os.path.join(sortie, "rapport.json"), "w"), ensure_ascii=False, indent=1)
    for r in rapport:
        alerte = "  À RACCOURCIR : trop rapide même après reprise (raccourcis la phrase, ou coupe la scène en deux)" if r["a_raccourcir"] else ""
        print(f"{r['id']} : {r['mots']} mots, {r['mots_par_min']} mots/min, {r['prises']} prise(s){alerte}")
    print(f"voix.wav : {bilan['duree_s']} s, {bilan['mots_par_min']} mots/min en moyenne, {caracteres} caractères "
          f"payés à ElevenLabs cette fois (le cache ne refacture rien)")
    print("VOIX_OK" if not any(r["a_raccourcir"] for r in rapport) else "VOIX_A_RACCOURCIR")


def scenes_depuis_mots(mots_t, coupure=0.7):
    """Mots transcrits [{"text", "start", "end"}] -> scènes coupées aux pauses de plus de `coupure` s."""
    scenes = []
    for m in mots_t:
        if not scenes or m["start"] - scenes[-1]["end"] > coupure:
            scenes.append({"id": f"s{len(scenes) + 1:02d}", "start": m["start"], "end": m["end"], "texte": "", "mots": []})
        sc = scenes[-1]
        sc["mots"].append({"w": m["text"], "start": m["start"], "end": m["end"]})
        sc["end"], sc["texte"] = m["end"], (sc["texte"] + " " + m["text"]).strip()
    return scenes


def depuis_enregistrement(prise, sortie, coupures=()):
    """Ta propre voix : nettoyée, à -14 LUFS, transcrite pour avoir les temps des mots (align.json) et les sous-titres."""
    import tempfile
    os.makedirs(sortie, exist_ok=True)
    voix = os.path.join(sortie, "voix.wav")
    nettoyer(prise, voix)
    with tempfile.TemporaryDirectory() as d:
        ffmpeg("-i", voix, "-ac", "1", "-ar", "16000", os.path.join(d, "v.wav"))
        s = subprocess.run(["npx", "--yes", "hyperframes@0.8.167", "transcribe", os.path.join(d, "v.wav"), "-d", d, "-l", "fr"],
                           capture_output=True, text=True)
        p = os.path.join(d, "transcript.json")
        if not os.path.exists(p):
            sys.exit("Transcription impossible : " + (s.stdout + s.stderr)[-300:])
        mots_t = json.load(open(p))
    scenes, t = scenes_depuis_mots(mots_t), duree_fichier(voix)
    json.dump({"duree": round(t, 3), "voix": "enregistrement", "modele": None, "scenes": scenes},
              open(os.path.join(sortie, "align.json"), "w"), ensure_ascii=False, indent=1)
    ecrire_sous_titres(scenes, sortie, coupures)
    for sc in scenes:
        print(f"{sc['id']} : {len(sc['mots'])} mots, {debit(len(sc['mots']), sc['end'] - sc['start'])} mots/min")
    print(f"voix.wav : {t:.1f} s, {debit(len(mots_t), t)} mots/min en moyenne")
    print("VOIX_OK")


def voix_dispo():
    for v in appel("https://api.elevenlabs.io/v1/voices")["voices"]:
        print(f"{v['voice_id']}  {v['name']}  ({v.get('category', '?')})")


def autotest():
    assert mots("[excited] Qui a vu quoi ? Qui a aimé quoi ?") == ["Qui", "a", "vu", "quoi", "Qui", "a", "aimé", "quoi"]
    assert avec_pauses("Qui a vu quoi ? Plus personne ne suit.") == "Qui a vu quoi ?… Plus personne ne suit."
    assert avec_pauses("Il lit tout, et vire les doublons.") == "Il lit tout,… et vire les doublons."
    assert debit(12, 3.0) == 240 and debit(5, 0) == 0
    ali = {"characters": list("[excited] Oui, va."), "character_start_times_seconds": [0] * 10 + [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
           "character_end_times_seconds": [0] * 10 + [0.1, 0.2, 0.3, 0.35, 0.5, 0.6, 0.7, 0.8]}
    m = mots_alignes(ali, 2.0)
    assert [x["w"] for x in m] == ["Oui,", "va."] and m[0]["start"] == 2.0 and m[1]["end"] == 2.8, m
    assert abs(duree_parole(ali) - 0.8) < 1e-9
    assert cle_cache("a", "b", REGLAGES, MODELE) == cle_cache("a", "b", dict(REGLAGES), MODELE) != cle_cache("a", "c", REGLAGES, MODELE)
    sortie = "Input Integrated: x\n{\n\"input_i\" : \"-20.1\"\n}\n"
    assert loudnorm_mesure(sortie)["input_i"] == "-20.1"
    sc = scenes_depuis_mots([{"text": "Un", "start": 0.0, "end": 0.2}, {"text": "deux.", "start": 0.3, "end": 0.6},
                             {"text": "Trois", "start": 1.6, "end": 1.9}])
    assert [(s["id"], s["texte"], s["end"]) for s in sc] == [("s01", "Un deux.", 0.6), ("s02", "Trois", 1.9)], sc
    m = lambda w, a, b: {"w": w, "start": a, "end": b}
    sc = [{"start": 0, "end": 3.0, "mots": [m("Je", 0.0, 0.1), m("dépose", 0.12, 0.4), m("ma", 0.42, 0.5), m("vidéo,", 0.52, 0.9),
                                           m("et", 1.0, 1.1), m("il", 1.12, 1.2), m("coupe", 1.22, 1.5), m("tout.", 1.52, 2.9)]}]
    g = groupes(sc)
    assert [x["text"] for x in g] == ["Je dépose ma vidéo", "et il coupe tout"], g      # 4 mots plutôt qu'un groupe trop court
    assert g[0]["end"] == g[1]["start"] == 1.0 and g[-1]["end"] == 3.05, g               # collé au suivant ; fin de scène
    assert all(len(x["text"]) <= SOUS_TITRE_CAR for x in g)
    g = groupes(sc, coupures=[0.95])                                                       # une coupe après « vidéo, »
    assert g[0]["text"] == "Je dépose ma vidéo" and g[0]["end"] <= 0.95 and g[1]["start"] == 1.0, g
    assert [x["text"] for x in groupes([{"start": 0, "end": 1, "mots": [m("anticonstitutionnel", 0, 0.5), m("vraiment", 0.5, 1)]}])] == ["anticonstitutionnel", "vraiment"]
    sc = [{"start": 0, "end": 2.4, "mots": [m("Et", 0.0, 0.1), m("au", 0.12, 0.2), m("passage…", 0.22, 1.0), m("ton", 1.1, 1.3),
                                           m("panier", 1.32, 1.7), m("se", 1.72, 1.8), m("remplit.", 1.82, 2.3)]}]
    assert [x["text"] for x in groupes(sc)] == ["Et au passage", "ton panier", "se remplit"], groupes(sc)   # ni « se » en fin, ni un mot seul
    ali = {"characters": list("lait ?"), "character_start_times_seconds": [0, .1, .2, .3, .4, .5], "character_end_times_seconds": [.1, .2, .3, .4, .5, .6]}
    assert [(x["w"], x["end"]) for x in mots_alignes(ali, 0)] == [("lait ?", 0.6)]
    import tempfile, wave
    with tempfile.TemporaryDirectory() as d:                  # un mot à 0,5 s, un blanc, un mot dont la voix revient à 1,5 s
        w = os.path.join(d, "voix.wav")
        with wave.open(w, "wb") as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(ENERGIE_SR)
            son = [(0.5 <= k / ENERGIE_SR < 1.0 or 1.5 <= k / ENERGIE_SR < 2.2) for k in range(int(2.5 * ENERGIE_SR))]
            f.writeframes(array.array("h", (int(9000 * math.sin(k * 0.09)) if s else 0 for k, s in enumerate(son))).tobytes())
        g = caler([{"text": "un", "start": 0.5, "end": 1.2}, {"text": "deux", "start": 1.2, "end": 2.3}], w)
        assert g[1]["start"] == 1.5 and g[0]["end"] == 1.5 and g[0]["start"] == 0.5, g    # posé sur le retour de la voix
    print("autotest voix : 16 contrôles passés")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--autotest"]:
        autotest()
    elif a == ["--voix-dispo"]:
        voix_dispo()
    elif a and a[0] == "--enregistrement" and len(a) >= 2:
        coupes = json.load(open(a[a.index("--coupes") + 1])) if "--coupes" in a else []
        bornes = [round(sum(p["out"] - p["in"] for p in coupes[:k + 1]), 3) for k in range(len(coupes) - 1)]
        depuis_enregistrement(a[1], a[a.index("-o") + 1] if "-o" in a else "voix", bornes)
    elif a and a[0].endswith(".json"):
        fabriquer(a[0], a[a.index("-o") + 1] if "-o" in a else "voix")
    else:
        sys.exit(__doc__)
