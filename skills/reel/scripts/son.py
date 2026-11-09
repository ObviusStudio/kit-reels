"""Le son d'un reel : le son choisi pour ce film, posé sous la voix, le master à -14 LUFS. Jamais un son calculé.

Usage :
  python3 son.py --video film.mp4 --voix voix/voix.wav --align voix/align.json -o final.mp4 LE_SON [--effets effets.json]
                 [--carte 12.4] [--style "warm lo-fi house, soft electric piano"] [--bpm 110]
  python3 son.py --piste --duree 13.26 --carte 11.73 --voix voix.wav -o son.wav LE_SON [--effets effets.json]
  python3 son.py --autotest

LE_SON se choisit à chaque projet, avec la personne ; il n'y en a pas par défaut :
  --compose                une musique composée pour ce film par ElevenLabs Music (music_v1), sur un plan à sections (intro,
                           groove, variation, outro qui résout), instrumentale, au style --style et au tempo --bpm ;
  --musique ta-piste.mp3   sa piste, libre de droits pour un usage commercial ;
  --sans-musique           pas de musique ;
et, en plus si elle les veut, --effets effets.json : des effets électro générés par ElevenLabs, un par animation,
[{"t": 1.2, "son": "whoosh"}, ...] ; sons : whoosh, impact, blip, glitch, frappe, montee, stab.

La musique se cale : sa tête muette sautée, son dernier son plein 0,5 s après le début de la carte de fin (--carte, par
défaut la fin du dernier mot d'align.json) ; 11 dB sous la voix, mesuré en LUFS (8 à 14 permis), 6 dB de plus sur la
carte. Les effets : deux à moins de 0,12 s, le plus important reste ; les prises alternent ; chacun sous la crête de la
voix, de 6 à 14 dB selon le son (3 au moins). Ce qui est généré (musique/, effets/, dossier courant) est gardé avec sa
demande : jamais repayé. Le tout revient à -14 LUFS intégré, la crête mesurée sur le film (-1 dBTP au plus), sans
réencoder la vidéo ; chaque couche s'écrit aussi seule, telle que mixée (<sortie>-musique.wav, <sortie>-effets.wav).
--piste écrit seulement le son ajouté, calé et réglé, à poser à volume 1 dans une composition qui porte déjà la voix.
Sans ELEVENLABS_API_KEY, ce qui n'est pas déjà généré ne l'est pas, et rien n'est calculé à sa place : le script le dit
et s'arrête.
"""
import array, hashlib, json, math, os, re, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

API = "https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192"
API_EFFETS = "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128"
STYLE = ("modern chill house, warm electric piano chords, round soft sub bass, gentle drums with tight hi-hats, "
         "optimistic and confident, polished modern production")
JAMAIS = ["vocals", "singing", "choir", "vocal chops", "spoken words", "whistling", "busy lead melody", "aggressive EDM drop",
          "heavy distortion", "cheesy corporate ukulele"]
SECTIONS = {   # les styles de chaque section, repris du plan de la musique du 09/11/2026, sans son genre
    "Intro": (["sparse intro", "soft kick enters", "anticipation"], ["full drums"]),
    "Groove": (["full groove", "steady beat", "warm bassline", "subtle percussion"], ["melodic lead"]),
    "Variation": (["same groove with brighter chords", "light new texture", "slow build of energy"], ["drop", "breakdown silence"]),
    "Outro": (["uplifting final phrase", "chords open up", "clean resolved ending on the tonic", "last chord rings out"],
              ["fade to silence too early", "abrupt cut"]),
}
# les effets électro de la v7 du 09/11/2026 : (durée en s, prompt, prises, dB sous la crête de la voix, tirés de ses volumes)
PALETTE = {
    "whoosh": (0.9, "Short modern electronic whoosh transition, airy filtered synth swoosh passing quickly from left to right "
                    "with a soft digital tail, clean, punchy, no music", 2, 11),
    "impact": (0.8, "Punchy modern electro impact hit for a title reveal, tight deep sub bass thump with a crisp digital "
                    "transient click on top, short, no long reverb tail, no music", 2, 8),
    "blip": (0.5, "Short clean digital user interface blip, modern tech app notification click, crisp high pitched synth pip, "
                  "very short, no music", 2, 12),
    "glitch": (0.6, "Short modern digital glitch stutter sound effect, crisp electronic data glitch with tiny bit crushed "
                    "clicks, tech, no music", 2, 11),
    "frappe": (1.0, "Fast soft modern keyboard typing burst, clean low profile mechanical keys, digital and crisp, close "
                    "microphone, no music", 1, 14),
    "montee": (1.4, "Short electronic riser building tension, rising filtered synth noise sweep that accelerates and stops "
                    "abruptly at the peak, modern, no melody", 1, 9),
    "stab": (1.5, "Modern electro synth stab chord hit for an end card, bright and confident, single hit with a short "
                  "shimmering digital tail, no drums, no melody", 2, 6),
}
PRIORITE = ("montee", "stab", "frappe", "glitch", "impact", "whoosh", "blip")   # deux effets à moins de 0,12 s : le premier reste
ECART_EFFETS, SOUS_CRETE = 0.12, 3.0   # s entre deux effets ; dB au moins sous la crête de la voix
SOUS_VOIX, PERMIS, RELEVE = 11.0, (8.0, 14.0), 6.0   # dB sous la voix, en LUFS ; dB de plus sur la carte de fin
RAMPE, FONDU, AVANT = 0.3, 0.8, 0.5   # s : montée sur la carte, fondu final ; la carte arrive 0,5 s avant le dernier son plein :
TRAME = 0.05                          # le dernier accord tombe sur la carte, sa première moitié reste relevée (essai du 09/11)
ENTREE = 0.15                         # s de fondu d'entrée : lue en plein groove, la musique démarrait d'un front, crête à -0,75 dBTP
CHOIX = """Le son de ce film se choisit à chaque projet : demande à la personne ce qu'elle veut, puis relance avec un seul de ces choix :
  --compose                une musique composée pour ce film (ElevenLabs Music) ;
  --musique ta-piste.mp3   sa piste, libre de droits pour un usage commercial ;
  --sans-musique           pas de musique ;
et, en plus si elle les veut : --effets effets.json, des effets électro calés sur les animations (ElevenLabs)."""
SANS_CLE = """Pas de clé ElevenLabs (ELEVENLABS_API_KEY) : {quoi}, et rien n'est calculé à sa place.
Trois choix :
  1. ta clé : crée-la sur https://elevenlabs.io/app/settings/api-keys, puis ajoute toi-même la ligne
     export ELEVENLABS_API_KEY=... à ton ~/.zshrc, et relance ;
  2. ta piste, libre de droits pour un usage commercial : --musique ta-piste.mp3 ;
  3. sans musique ni effet : --sans-musique, sans --effets (un son s'ajoute dans l'appli, à la publication)."""


def ffmpeg(*args):
    s = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", *args], capture_output=True, text=True)
    if s.returncode:
        raise RuntimeError(s.stderr[-800:])
    return s.stderr


def sonde(f, champ):
    return subprocess.run(["ffprobe", "-v", "error", *champ, "-of", "csv=p=0", f], capture_output=True, text=True, check=True).stdout


def duree(f):
    return float(sonde(f, ["-show_entries", "format=duration"]))


def stereo(f):
    """Le filtre qui lit un son mono à plein niveau sur les deux canaux, comme un lecteur le joue."""
    return "pan=stereo|c0=c0|c1=c0" if sonde(f, ["-select_streams", "a:0", "-show_entries", "stream=channels"]).strip() == "1" else "anull"


def lufs(f, debut, long):
    """Sonie intégrée d'une fenêtre, -70 pour un silence."""
    e = ffmpeg("-ss", f"{debut:.3f}", "-t", f"{long:.3f}", "-i", f, "-vn", "-af", stereo(f) + ",ebur128", "-f", "null", "-")
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
    return max(float(m[-1]), -70.0) if m else -70.0


def crete(f):
    """La crête d'échantillon d'un fichier, en dBFS."""
    return float(re.findall(r"max_volume: (-?[\d.]+) dB", ffmpeg("-i", f, "-af", "volumedetect", "-f", "null", "-"))[-1])


def enveloppe(f):
    """Le niveau de la piste en dB, par trames de 50 ms (mono, 8 kHz)."""
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x, n = array.array("h"), int(8000 * TRAME)
    x.frombytes(pcm)
    return [10 * math.log10(sum(v * v for v in x[i:i + n]) / n / 32768 ** 2 + 1e-12) for i in range(0, len(x) - n + 1, n)]


def reperes(env):
    """La fin de la tête muette (le premier son, moins une trame) et la fin du dernier son plein (4 dB sous le 95e centile)."""
    ref = sorted(env)[int(0.95 * (len(env) - 1))]
    tete = next(i for i, v in enumerate(env) if v >= ref - 30)
    return max(0, tete - 1) * TRAME, max(i for i, v in enumerate(env) if v >= ref - 4) * TRAME


def caler(tete, accord, carte):
    """Où lire la piste au début du film, et quand elle y entre : 0, sauf une piste trop courte, qui entre plus tard."""
    debut = round(accord - AVANT - carte, 3)
    return (debut, 0.0) if debut >= tete else (tete, round(tete - debut, 3))


def plan(duree_film, carte, bpm=110, style=None):
    """Le plan de composition : l'intro (4 s) et le milieu couvrent le film jusqu'à 1 s après la carte, l'outro qui résout
    dure le reste de la carte et 8 s de plus, pour que le dernier accord ait la place de résonner. En secondes entières : un
    film rendu de nouveau, à quelques images près, retrouve le même plan, donc la même musique, sans la repayer."""
    intro, outro = 4, math.ceil(duree_film - carte) + 8
    milieu = max(6, math.ceil(carte) + 1 - intro)
    if intro + milieu + outro > 600:
        raise ValueError(f"film de {duree_film:.0f} s : une composition dure 600 s au plus")
    k = max(2, math.ceil(milieu / 110))   # 120 s au plus par section
    parts = [milieu // k + (1 if i < milieu % k else 0) for i in range(k)]
    noms = ["Intro"] + [("Groove", "Variation")[i % 2] + (f" {i // 2 + 1}" if i > 1 else "") for i in range(k)] + ["Outro"]
    sections = []
    for nom, s in zip(noms, [intro] + parts + [outro]):
        pos, neg = SECTIONS[nom.split()[0]]
        sections.append({"section_name": nom, "positive_local_styles": pos, "negative_local_styles": neg,
                         "duration_ms": s * 1000, "lines": []})
    styles = [x.strip() for x in (style or STYLE).split(",") if x.strip()]
    return {"composition_plan": {"positive_global_styles": styles + [f"{bpm} BPM", "instrumental", "leaves room for a spoken voiceover"],
                                 "negative_global_styles": JAMAIS, "sections": sections},
            "model_id": "music_v1", "respect_sections_durations": True}


def cache(url, corps, extra=""):
    return hashlib.sha256((url + json.dumps(corps, sort_keys=True, ensure_ascii=False) + extra).encode()).hexdigest()[:12]


def demander(url, corps, chemin, quoi, cote):
    """Le son de cette demande, gardé dans chemin : repris s'il y est déjà (rien de payé), sinon demandé à ElevenLabs. Rend
    (chemin, payé)."""
    if os.path.isfile(chemin) and os.path.getsize(chemin) > 0:
        return chemin, False
    cle = os.environ.get("ELEVENLABS_API_KEY")
    if not cle:
        sys.exit(SANS_CLE.format(quoi=quoi))
    req = urllib.request.Request(url, data=json.dumps(corps).encode(), headers={"xi-api-key": cle, "Content-Type": "application/json"})
    for essai in range(3):   # une coupure du réseau ne se relance pas : la demande a pu être payée
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                audio = r.read()
            break
        except urllib.error.HTTPError as err:
            detail = err.read().decode(errors="replace")[:300]
            if err.code in (429, 500, 502, 503) and essai < 2:
                time.sleep(10 * (essai + 1))
                continue
            sys.exit(f"ElevenLabs refuse ({err.code}) : {detail}")
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin + ".part", "wb") as f:
        f.write(audio)
    os.replace(chemin + ".part", chemin)
    json.dump(corps, open(chemin[:-4] + cote, "w"), ensure_ascii=False, indent=1)
    return chemin, True


def composer(corps, dossier="musique"):
    """La musique de ce plan : reprise si elle est déjà composée, sinon composée par ElevenLabs Music."""
    mp3 = os.path.join(dossier, f"musique-{cache(API, corps)}.mp3")
    s = sum(x["duration_ms"] for x in corps["composition_plan"]["sections"]) / 1000
    if not os.path.isfile(mp3):
        print(f"composition par ElevenLabs Music : {s:.0f} s, {len(corps['composition_plan']['sections'])} sections")
    chemin, paye = demander(API, corps, mp3, "la musique du film ne peut pas être composée", "-plan.json")
    print(f"musique composée : {chemin} ({os.path.getsize(chemin) // 1024} Ko), son plan à côté" if paye else
          f"musique reprise : {chemin}, déjà composée pour ce plan (rien de payé)")
    return chemin


def prise_effet(nom, k, dossier="effets"):
    """La prise k de l'effet nom : reprise si elle est déjà générée, sinon générée par ElevenLabs. Rend (chemin, payé)."""
    corps = {"text": PALETTE[nom][1], "duration_seconds": PALETTE[nom][0]}
    mp3 = os.path.join(dossier, f"{nom}-{k}-{cache(API_EFFETS, corps, str(k))}.mp3")
    return demander(API_EFFETS, corps, mp3, "les effets ne peuvent pas être générés", "-demande.json")


def fin_de_voix(align):
    return max(m["end"] for sc in json.load(open(align))["scenes"] for m in sc["mots"])


def poser(source, d, carte, voix, sortie):
    """La musique calée sur le film et réglée sur la voix, en wav stéréo 48 kHz de d secondes : 11 dB sous la voix (LUFS),
    6 dB de plus sur la carte de fin, fondu final. Rend la phrase du compte rendu."""
    tete, accord = reperes(enveloppe(source))
    debut, entree = caler(tete, accord, carte)
    brute = sortie + ".brute.wav"
    ffmpeg("-i", source, "-af", f"atrim=start={debut:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={ENTREE},adelay={entree * 1000:.0f}:all=1,"
           f"apad,atrim=0:{d:.3f},aresample=48000,{stereo(source)}", "-c:a", "pcm_s16le", brute)
    v = lufs(voix, 0, carte)
    g1 = 10 ** ((v - SOUS_VOIX - lufs(brute, 0, carte)) / 20)
    g2 = g1 * 10 ** (RELEVE / 20)
    gain = f"if(lt(t,{carte:.3f}),{g1:.5f},{g1:.5f}+{g2 - g1:.5f}*min(1,(t-{carte:.3f})/{RAMPE}))"
    e = ffmpeg("-i", brute, "-af", f"volume='{gain}':eval=frame,afade=t=out:st={max(0, d - FONDU):.3f}:d={FONDU},volumedetect",
               "-c:a", "pcm_s16le", sortie)
    os.remove(brute)
    pic = float(re.findall(r"max_volume: (-?[\d.]+) dB", e)[-1])
    ecart = v - lufs(sortie, 0, carte)
    if pic > -0.1 or not PERMIS[0] <= ecart <= PERMIS[1]:
        sys.exit(f"{sortie} : musique à {ecart:.1f} dB sous la voix ({PERMIS[0]:g} à {PERMIS[1]:g} attendus), crête {pic} dB : "
                 "la piste est trop faible pour être réglée sans saturer")
    fin = duree(source) - debut + entree
    return (f"musique {os.path.basename(source)} lue de {debut:.2f} s" + (f", entrée à {entree:.2f} s du film (piste trop courte)" if entree else "")
            + f", dernier son plein à {accord - debut + entree:.2f} s du film (carte à {carte:.2f} s)"
            + (f", finie {d - fin:.2f} s avant le film" if fin < d else "")
            + f" ; {ecart:.1f} dB sous la voix (LUFS), +{RELEVE:g} dB sur la carte")


def choisir_effets(liste, d):
    """Les effets gardés : dans le film, deux à moins de 0,12 s départagés par PRIORITE ; la prise de chacun alterne."""
    inconnus = sorted({e["son"] for e in liste} - set(PALETTE))
    if inconnus:
        raise ValueError(f"effet inconnu : {', '.join(inconnus)} (sons : {', '.join(PALETTE)})")
    garde = []
    for e in sorted(liste, key=lambda e: (PRIORITE.index(e["son"]), e["t"])):
        if 0 <= e["t"] <= d - 0.2 and all(abs(e["t"] - g["t"]) >= ECART_EFFETS for g in garde):
            garde.append(dict(e))
    garde.sort(key=lambda e: e["t"])
    vus = {}
    for e in garde:   # jamais deux fois la même prise d'un son de suite
        e["prise"] = vus.get(e["son"], 0) % PALETTE[e["son"]][2] + 1
        vus[e["son"]] = vus.get(e["son"], 0) + 1
    return garde


def poser_effets(liste, d, voix, sortie):
    """Les effets posés à leurs instants, en wav stéréo 48 kHz de d secondes, chacun sous la crête de la voix (PALETTE), le
    tout à SOUS_CRETE dB au moins dessous. Rend (la phrase du compte rendu, les effets gardés)."""
    garde, vc, tmp, payes = choisir_effets(liste, d), crete(voix), tempfile.mkdtemp(prefix="effets-"), 0
    prises, entrees, graphe, labels = {}, [], [], []
    for e in garde:
        cle = (e["son"], e["prise"])
        if cle not in prises:   # la tête muette retirée : l'effet part à son instant
            src, paye = prise_effet(*cle)
            payes += paye
            net = os.path.join(tmp, f"{e['son']}-{e['prise']}.wav")
            ffmpeg("-i", src, "-af", "silenceremove=start_periods=1:start_threshold=-50dB,aresample=48000,aformat=channel_layouts=stereo",
                   "-c:a", "pcm_s16le", net)
            prises[cle] = (net, vc - PALETTE[e["son"]][3] - crete(net), [])
        prises[cle][2].append(e["t"])
    for i, (net, gain, instants) in enumerate(prises.values()):
        entrees += ["-i", net]
        graphe.append(f"[{i}:a]asplit={len(instants)}" + "".join(f"[s{i}_{j}]" for j in range(len(instants))) if len(instants) > 1
                      else f"[{i}:a]anull[s{i}_0]")
        for j, t in enumerate(instants):
            graphe.append(f"[s{i}_{j}]adelay={round(t * 1000)}:all=1,volume={gain:.2f}dB[e{i}_{j}]")
            labels.append(f"[e{i}_{j}]")
    if labels:
        brute = os.path.join(tmp, "effets.wav")
        ffmpeg(*entrees, "-filter_complex", ";".join(graphe) + ";" + "".join(labels)
               + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,apad=whole_dur={d:.3f}[o]", "-map", "[o]",
               "-t", f"{d:.3f}", "-ar", "48000", "-c:a", "pcm_s16le", brute)   # apad,atrim après un asplit ne finit jamais
        trop = crete(brute) - (vc - SOUS_CRETE)   # deux effets qui se chevauchent s'additionnent : ramenés sous la limite
        ffmpeg("-i", brute, "-af", f"volume={-(trop + 0.1) if trop > 0 else 0.0:.2f}dB", "-c:a", "pcm_s16le", sortie)
    else:
        ffmpeg("-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={d:.3f}", "-c:a", "pcm_s16le", sortie)
    shutil.rmtree(tmp)
    sous = vc - crete(sortie) if labels else None
    compte = ", ".join(f"{sum(1 for e in garde if e['son'] == s)} {s}" for s in PALETTE if any(e["son"] == s for e in garde))
    return (f"{len(garde)} effets électro ({compte or 'aucun'})" + (f", crêtes {sous:.1f} dB sous celle de la voix" if labels else "")
            + (f", {payes} prise(s) générée(s) par ElevenLabs" if payes else ", prises reprises sans rien payer")), garde


def couches(musique, effets, d, carte, voix, base, bpm=110, style=None):
    """Le son ajouté, une couche par fichier (base-musique.wav, base-effets.wav) : [(chemin, phrase)]. musique : None (pas de
    musique), "compose" ou le chemin d'une piste fournie."""
    faites = []
    if musique:
        source = composer(plan(d, carte, bpm, style)) if musique == "compose" else musique
        faites.append((base + "-musique.wav", poser(source, d, carte, voix, base + "-musique.wav")))
    if effets:
        faites.append((base + "-effets.wav", poser_effets(json.load(open(effets)), d, voix, base + "-effets.wav")[0]))
    return faites


def loudnorm_deux_passes(entree_args, filtre, cible, sortie_args):
    m = ffmpeg(*entree_args, "-filter_complex", filtre + f",loudnorm=I={cible}:TP=-1.5:LRA=11:print_format=json[o]",
               "-map", "[o]", "-f", "null", "-")
    j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    ln = (f"loudnorm=I={cible}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    ffmpeg(*entree_args, "-filter_complex", filtre + "," + ln + "[o]", "-map", "[o]", *sortie_args)


def mixer(video, voix, align, sortie, musique=None, effets=None, bpm=110, style=None, carte=None):
    d = duree(video)
    if musique and carte is None:
        carte = fin_de_voix(align)
    faites = couches(musique, effets, d, carte, voix, os.path.splitext(sortie)[0], bpm, style)
    entrees = ["-i", voix] + [x for chemin, _ in faites for x in ("-i", chemin)]
    filtre = (f"[0:a]aresample=48000,{stereo(voix)},apad[v];[v]" + "".join(f"[{k + 1}:a]" for k in range(len(faites)))
              + f"amix=inputs={len(faites) + 1}:normalize=0:duration=first,atrim=0:{d:.3f}" if faites else
              f"[0:a]aresample=48000,{stereo(voix)},apad,atrim=0:{d:.3f}")
    tmp = tempfile.mkdtemp(prefix="son-")
    audio = os.path.join(tmp, "master.wav")
    loudnorm_deux_passes(entrees, filtre, -14, ["-ar", "48000", "-c:a", "pcm_s16le", audio])
    for essai in range(3):   # l'AAC ajoute de la crête (09/11/2026 : -0,7 dBTP pour -1,5 visés) : mesurée sur le film, rabotée
        ffmpeg("-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "-shortest", sortie)
        e = ffmpeg("-i", sortie, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-")
        i, pic = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
        if pic <= -1.0:
            break
        ffmpeg("-i", audio, "-af", f"volume={-1.1 - pic:.2f}dB", "-c:a", "pcm_s16le", audio + f".{essai}.wav")
        audio += f".{essai}.wav"
    shutil.rmtree(tmp)
    dit = " ; ".join(p for _, p in faites) or "ni musique ni effet"
    print(f"{sortie} : {d:.1f} s ; {dit} ; master {i} LUFS, crête {pic} dBTP (mesurés sur le film)")
    print("SON_OK")


def autotest():
    n = 0
    p = plan(30.0, 27.5)
    s = p["composition_plan"]["sections"]
    assert [x["section_name"] for x in s] == ["Intro", "Groove", "Variation", "Outro"], s
    assert sum(x["duration_ms"] for x in s) == 40000 and all(3000 <= x["duration_ms"] <= 120000 for x in s), s
    assert p["model_id"] == "music_v1" and "vocals" in p["composition_plan"]["negative_global_styles"], p
    assert "110 BPM" in p["composition_plan"]["positive_global_styles"] and "instrumental" in p["composition_plan"]["positive_global_styles"]
    assert "lo-fi" in plan(30.0, 27.5, 90, "lo-fi hip hop, mellow piano")["composition_plan"]["positive_global_styles"][0]
    n += 1
    assert plan(13.26, 11.73) == plan(13.30, 11.70), "un film rendu de nouveau doit retrouver le même plan"
    n += 1
    s = plan(400, 395)["composition_plan"]["sections"]
    assert len(s) == 6 and all(3000 <= x["duration_ms"] <= 120000 for x in s) and s[3]["section_name"] == "Groove 2", s
    n += 1
    try:
        plan(700, 695)
        raise AssertionError("une composition de plus de 600 s acceptée")
    except ValueError:
        n += 1
    assert caler(0.95, 9.5, 6.0) == (3.0, 0.0) and caler(2.0, 7.0, 6.0) == (2.0, 1.5), (caler(0.95, 9.5, 6.0), caler(2.0, 7.0, 6.0))
    n += 1
    ev = [{"t": 1.0, "son": "whoosh"}, {"t": 1.05, "son": "impact"}, {"t": 2.0, "son": "whoosh"}, {"t": 3.0, "son": "whoosh"},
          {"t": 4.0, "son": "whoosh"}, {"t": 7.9, "son": "blip"}]   # la prise 1 du whoosh sert deux fois
    assert [(e["t"], e["son"], e["prise"]) for e in choisir_effets(ev, 8.0)] == [(1.05, "impact", 1), (2.0, "whoosh", 1),
                                                                                 (3.0, "whoosh", 2), (4.0, "whoosh", 1)], choisir_effets(ev, 8.0)
    n += 1
    try:
        choisir_effets([{"t": 1.0, "son": "klaxon"}], 8.0)
        raise AssertionError("un effet inconnu accepté")
    except ValueError:
        n += 1
    ici, cle = os.getcwd(), os.environ.pop("ELEVENLABS_API_KEY", None)   # rien ne se paie dans l'autotest
    with tempfile.TemporaryDirectory() as dd:
        os.chdir(dd)
        try:
            # une musique fabriquée : 1 s muette, un son plein jusqu'à 9 s, puis un dernier accord qui s'éteint
            ffmpeg("-f", "lavfi", "-i", "anoisesrc=d=12:c=pink:a=0.1:seed=3", "-af",
                   "volume='if(lt(t,1),0,exp(-max(0,t-9)/1.2))':eval=frame,aformat=channel_layouts=stereo", "-ar", "48000", "piste.wav")
            tete, accord = reperes(enveloppe("piste.wav"))
            assert 0.85 <= tete <= 1.0 and 9.2 <= accord <= 9.9, (tete, accord)
            n += 1
            ffmpeg("-f", "lavfi", "-i", "sine=f=330:d=6", "-af", "volume=-4dB,apad=whole_dur=8", "-ar", "48000", "voix.wav")
            dit = poser("piste.wav", 8.0, 6.0, "voix.wav", "posee.wav")
            v, m = lufs("voix.wav", 0, 6.0), lufs("posee.wav", 0, 6.0)
            debut = caler(tete, accord, 6.0)[0]   # le gain, lu à la même place dans la piste : sous la voix, puis sur la carte
            g1 = m - lufs("piste.wav", debut, 6.0)
            g2 = lufs("posee.wav", 6.4, 0.5) - lufs("piste.wav", debut + 6.4, 0.5)
            assert 10.5 <= v - m <= 11.5 and abs(g2 - g1 - RELEVE) < 0.3 and abs(duree("posee.wav") - 8.0) < 0.05, (v, m, g1, g2, dit)
            n += 1
            corps = plan(8.0, 6.0)
            try:
                composer(corps)
                raise AssertionError("sans clé, une musique a été rendue")
            except SystemExit as e:
                assert all(x in str(e) for x in ("ELEVENLABS_API_KEY", "--musique", "--sans-musique")), e
                assert not os.path.exists("musique"), "sans clé, un dossier a été écrit"
            n += 1
            os.makedirs("musique")
            shutil.copy("piste.wav", f"musique/musique-{cache(API, corps)}.mp3")
            assert composer(corps) == f"musique/musique-{cache(API, corps)}.mp3", "la musique déjà composée n'est pas reprise sans clé"
            n += 1
            # des prises d'effets fabriquées, rangées comme si ElevenLabs les avait générées : 0,1 s muette puis le son
            os.makedirs("effets")
            for nom, k, src in (("whoosh", 1, "anoisesrc=d=0.4:c=pink:seed=1"), ("whoosh", 2, "anoisesrc=d=0.4:c=pink:seed=2"),
                                ("impact", 1, "sine=f=80:d=0.3")):
                corps_e = {"text": PALETTE[nom][1], "duration_seconds": PALETTE[nom][0]}
                ffmpeg("-f", "lavfi", "-i", src, "-af", "adelay=100:all=1,aformat=channel_layouts=stereo", "-ar", "48000", "-f", "wav",
                       f"effets/{nom}-{k}-{cache(API_EFFETS, corps_e, str(k))}.mp3")
            dit, garde = poser_effets(ev, 8.0, "voix.wav", "effets.wav")
            vc, pe = crete("voix.wav"), crete("effets.wav")
            depart = float(re.findall(r"silence_end: ([\d.]+)", ffmpeg("-i", "effets.wav", "-af", "silencedetect=n=-50dB:d=0.5", "-f", "null", "-"))[0])
            fen = float(re.findall(r"max_volume: (-?[\d.]+) dB", ffmpeg("-ss", "1.0", "-t", "0.5", "-i", "effets.wav", "-af",
                                                                       "volumedetect", "-f", "null", "-"))[-1])
            assert len(garde) == 4 and abs(depart - 1.05) < 0.03 and vc - pe >= SOUS_CRETE - 0.05, (depart, vc, pe, dit)
            assert abs(vc - fen - PALETTE["impact"][3]) < 0.6 and abs(duree("effets.wav") - 8.0) < 0.05, (vc, fen)
            n += 1
            try:
                poser_effets([{"t": 1.0, "son": "glitch"}], 8.0, "voix.wav", "glitch.wav")
                raise AssertionError("sans clé, un effet a été généré")
            except SystemExit as e:
                assert "ELEVENLABS_API_KEY" in str(e) and not any(f.startswith("glitch") for f in os.listdir("effets")), e
            n += 1
            ffmpeg("-f", "lavfi", "-i", "color=c=black:s=108x192:d=8:r=30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "v.mp4")
            json.dump({"scenes": [{"mots": [{"start": 0.0, "end": 3.0}, {"start": 3.2, "end": 6.0}]}]}, open("align.json", "w"))
            json.dump(ev, open("effets.json", "w"))
            for musique, effets, couches_attendues in (("piste.wav", None, ["final-musique.wav"]), (None, "effets.json", ["final-effets.wav"])):
                for f in ("final-musique.wav", "final-effets.wav"):
                    if os.path.exists(f):
                        os.remove(f)
                mixer("v.mp4", "voix.wav", "align.json", "final.mp4", musique=musique, effets=effets)
                e = ffmpeg("-i", "final.mp4", "-af", "ebur128=peak=true", "-f", "null", "-")
                i, p = float(e[e.rindex("I:"):].split()[1]), float(e[e.rindex("Peak:"):].split()[1])
                assert -15.5 < i < -12.5 and p <= -1.0, (musique, effets, i, p)
                assert [f for f in ("final-musique.wav", "final-effets.wav") if os.path.isfile(f)] == couches_attendues, couches_attendues
                assert sonde("final.mp4", ["-select_streams", "a:0", "-show_entries", "stream=channels"]).strip() == "2"
                n += 1
            for args, attendu in ((["--video", "v.mp4", "--bruitages", "b.json"], "option inconnue : --bruitages"),
                                  (["--video", "v.mp4", "--voix", "voix.wav", "--align", "align.json", "-o", "x.mp4"], "se choisit à chaque projet"),
                                  (["--video", "v.mp4", "--voix", "voix.wav", "--align", "align.json", "-o", "x.mp4", "--compose",
                                    "--sans-musique"], "se choisit à chaque projet")):
                r = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), *args], capture_output=True, text=True)
                assert r.returncode and attendu in r.stderr and not os.path.exists("x.mp4"), (args, r.stderr)
                n += 1
        finally:
            os.chdir(ici)
            if cle:
                os.environ["ELEVENLABS_API_KEY"] = cle
    print(f"autotest son : {n} contrôles passés")


AVEC_VALEUR = {"--video", "--voix", "--align", "-o", "--musique", "--effets", "--bpm", "--style", "--carte", "--duree"}


def main(a):
    if a == ["--autotest"]:
        return autotest()
    v, drapeaux, i = {}, set(), 0
    while i < len(a):
        if a[i] in AVEC_VALEUR and i + 1 < len(a):
            v[a[i]], i = a[i + 1], i + 2
        elif a[i] in ("--compose", "--sans-musique", "--piste"):
            drapeaux.add(a[i])
            i += 1
        else:
            sys.exit(f"option inconnue : {a[i]} (plus aucun bruitage calculé depuis le 09/11/2026)\n\n{__doc__}")
    choix = [c for c in ("--compose", "--musique", "--sans-musique") if c in drapeaux or c in v]
    if len(choix) != 1:
        sys.exit(CHOIX)
    musique = {"--compose": "compose", "--musique": v.get("--musique"), "--sans-musique": None}[choix[0]]
    bpm, style, effets = int(v.get("--bpm", 110)), v.get("--style"), v.get("--effets")
    if "--piste" in drapeaux:
        if not all(k in v for k in ("--duree", "--voix", "-o") + (("--carte",) if musique else ())):
            sys.exit(__doc__)
        if not musique and not effets:
            sys.exit("--piste --sans-musique sans --effets : rien à poser.")
        d = float(v["--duree"])
        tmp = tempfile.mkdtemp(prefix="piste-")
        faites = couches(musique, effets, d, float(v["--carte"]) if musique else None, v["--voix"], os.path.join(tmp, "son"), bpm, style)
        if len(faites) == 1:
            shutil.copy(faites[0][0], v["-o"])
        else:
            ffmpeg("-i", faites[0][0], "-i", faites[1][0], "-filter_complex", "amix=inputs=2:normalize=0", "-c:a", "pcm_s16le", v["-o"])
        shutil.rmtree(tmp)
        print(f"{v['-o']} : {d:.2f} s ; {' ; '.join(p for _, p in faites)} ; à poser à volume 1, sur sa propre piste : "
              f'<audio id="musique" class="clip" src="{v["-o"]}" data-start="0" data-duration="{d:.3f}" data-track-index="11" data-volume="1"></audio>')
        print("SON_OK")
        return
    if not all(k in v for k in ("--video", "--voix", "--align", "-o")):
        sys.exit(__doc__)
    mixer(v["--video"], v["--voix"], v["--align"], v["-o"], musique, effets, bpm, style, float(v["--carte"]) if "--carte" in v else None)


if __name__ == "__main__":
    main(sys.argv[1:])
