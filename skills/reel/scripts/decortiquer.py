#!/usr/bin/env python3
"""Décortiquer le reel qu'on refait : le fichier, ses planches d'images, ses mots et ses coupes, tout dans DECORTIQUE.md.

Usage :
  python3 scripts/decortiquer.py <lien ou fichier.mp4> -o reference/ [--langue en] [--ips 2]
  python3 scripts/decortiquer.py --mots <dossier ou mots.json> <début> <fin>     les mots d'un passage, en secondes ou m:ss (0 11.5 ; 1:07.2 1:42) : « N mots, D s (M par minute) »
  python3 scripts/decortiquer.py --sept-mots <transcription de l'original> <ton script>     aucune suite de 7 mots reprise : SEPT_MOTS_OK
  python3 scripts/decortiquer.py --selftest

DECORTIQUE.md donne aussi `## Les plans` (un plan entre deux coupes : début, durée, mots dits, images plans/NN.jpg à 720 px) et l'ouverture mesurée.
Le reel reste dans ce dossier : il sert à lire la structure, il ne va jamais dans ton film (references/refaire.md).
"""
import argparse, bisect, glob, statistics, json, os, re, shutil, subprocess, sys, tempfile, time, unicodedata, urllib.parse, urllib.request

HF = ["npx", "--yes", "hyperframes@0.8.167"]


def sortie(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def api(chemin, lien, cle):
    q = urllib.request.Request(f"https://api.scrapecreators.com{chemin}?" + urllib.parse.urlencode({"url": lien}), headers={"x-api-key": cle})
    return json.load(urllib.request.urlopen(q, timeout=60))


def jour(t):
    return time.strftime("%Y-%m-%d", time.gmtime(t)) if t else None


def par_scrapecreators(lien, cle):
    """L'adresse du fichier vidéo et les chiffres du reel, lus par l'API ScrapeCreators ; None hors Instagram et TikTok."""
    if "instagram.com" in lien:
        d = api("/v1/instagram/post", lien, cle).get("data", {})
        d = d.get("xdt_shortcode_media", d)
        com = d.get("edge_media_to_parent_comment") or d.get("edge_media_to_comment") or {}
        return d.get("video_url"), {"compte": (d.get("owner") or {}).get("username"), "date": jour(d.get("taken_at_timestamp")),
                                    "vues": d.get("video_play_count") or d.get("video_view_count"),
                                    "j'aime": (d.get("edge_media_preview_like") or {}).get("count"), "commentaires": com.get("count"), "lien": lien}
    if "tiktok.com" in lien:
        d = api("/v2/tiktok/video", lien, cle).get("aweme_detail", {})
        s, adresses = d.get("statistics", {}), ((d.get("video") or {}).get("play_addr") or {}).get("url_list") or [None]
        return adresses[0], {"compte": (d.get("author") or {}).get("unique_id"), "date": jour(d.get("create_time")), "vues": s.get("play_count"),
                             "j'aime": s.get("digg_count"), "commentaires": s.get("comment_count"), "lien": lien}
    return None


def recuperer(source, dossier):
    """Le fichier du reel dans <dossier> et ce que dit sa page ; un lien passe par ScrapeCreators si la clé est là, sinon par yt-dlp."""
    if os.path.isfile(source):
        cible = os.path.join(dossier, "reel" + os.path.splitext(source)[1])
        shutil.copyfile(source, cible)
        return cible, {}
    if not re.match(r"https?://", source):
        sys.exit("Ni un fichier ni un lien : " + source)
    cle = os.environ.get("SCRAPECREATORS_API_KEY")
    if cle:
        try:
            r = par_scrapecreators(source, cle)
            if r and r[0]:
                cible = os.path.join(dossier, "reel.mp4")
                with urllib.request.urlopen(urllib.request.Request(r[0], headers={"User-Agent": "Mozilla/5.0"}), timeout=120) as f, open(cible, "wb") as o:
                    shutil.copyfileobj(f, o)
                return cible, r[1]
        except Exception as e:  # clé refusée, crédits épuisés, reel supprimé : on tente yt-dlp
            print(f"ScrapeCreators n'a pas rendu la vidéo ({e}) : j'essaie yt-dlp.", file=sys.stderr)
    if not shutil.which("yt-dlp"):
        sys.exit("Pour un lien, il faut une clé ScrapeCreators (SCRAPECREATORS_API_KEY) ou yt-dlp (brew install yt-dlp) ; sinon, donne le fichier de la vidéo.")
    code, txt = sortie("yt-dlp", "-q", "--no-warnings", "-f", "mp4/best", "-o", os.path.join(dossier, "reel.%(ext)s"), "--write-info-json", source)
    films = [f for f in glob.glob(os.path.join(dossier, "reel.*")) if not f.endswith(".json")]
    if code or not films:
        sys.exit("Le lien ne se télécharge pas (compte privé, connexion demandée) : enregistre l'écran de ton téléphone et donne le fichier.\n" + txt[-300:])
    info = os.path.join(dossier, "reel.info.json")
    meta = json.load(open(info, encoding="utf-8")) if os.path.exists(info) else {}
    return films[0], {"compte": meta.get("channel") or meta.get("uploader"), "date": meta.get("upload_date"), "vues": meta.get("view_count"),
                      "j'aime": meta.get("like_count"), "commentaires": meta.get("comment_count"), "lien": meta.get("webpage_url")}


def duree(film):
    code, txt = sortie("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", film)
    return float(txt.strip())


def format_(film):
    code, txt = sortie("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate", "-of", "csv=p=0", film)
    l, h, r = txt.strip().split(",")[:3]
    n, d = r.split("/")
    return f"{l} x {h}, {float(n) / float(d):.0f} i/s"


def silences(film):
    """Les passages de plus de 0,5 s sous -40 dB : [(début, fin)]. Vide si le son ne s'arrête jamais, ou s'il n'y a pas de son."""
    code, txt = sortie("ffmpeg", "-hide_banner", "-i", film, "-vn", "-af", "silencedetect=n=-40dB:d=0.5", "-f", "null", "-")
    debuts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", txt)]
    fins = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", txt)]
    return list(zip(debuts, fins + [duree(film)]))


def coupes(film, seuil=0.15):  # à 0,3 un plan qui n'occupe qu'une partie de l'écran passait sous le seuil : 2 coupes vues sur 9 (07/11)
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "s.txt")
        subprocess.run(["ffmpeg", "-v", "error", "-i", film, "-vf", f"select='gte(scene,0)',metadata=print:key=lavfi.scene_score:file={f}", "-f", "null", "-"], check=True)
        blocs = open(f).read().split("frame:")[1:]
    v = [(float(re.search(r"pts_time:([0-9.]+)", x).group(1)), float(re.search(r"scene_score=([0-9.]+)", x).group(1))) for x in blocs]
    brut = [a for a, b in v if b > seuil]
    return [a for k, a in enumerate(brut) if not k or a - brut[k - 1] > 0.15]  # une coupe sur plusieurs images compte une fois


def planches(film, dossier, ips=2):
    os.makedirs(dossier, exist_ok=True)
    base, tuiles = f"fps={ips}:round=up,scale=320:-2", "tile=5x3:padding=4:color=white"  # round=up : la vraie image 0, et chaque temps juste
    temps = "drawtext=text='%{pts\\:hms}':x=4:y=h-24:fontsize=15:fontcolor=yellow:box=1:boxcolor=black@0.7"
    for filtre in (f"{base},{temps},{tuiles}", f"{base},{tuiles}"):  # un ffmpeg sans police refuse drawtext : le temps se lit alors à l'image k = k / ips
        code, _ = sortie("ffmpeg", "-v", "error", "-y", "-i", film, "-vf", filtre, os.path.join(dossier, "p%02d.jpg"))
        if not code:
            break
    return sorted(glob.glob(os.path.join(dossier, "*.jpg")))


def mots(film, dossier, langue):
    """Les mots entendus ; une vidéo sans voix, ou sans transcription disponible, rend une liste vide et le dit."""
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "voix.wav")
        code, txt = sortie("ffmpeg", "-v", "error", "-y", "-i", film, "-vn", "-ac", "1", "-ar", "16000", wav)
        if code:
            return [], "aucune piste son"
        code, txt = sortie(*HF, "transcribe", wav, "-d", d, "-l", langue)
        p = os.path.join(d, "transcript.json")
        if not os.path.exists(p):
            return [], "transcription impossible : " + txt[-200:].strip()
        m = json.load(open(p))
    json.dump(m, open(os.path.join(dossier, "mots.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return m, ""


def mots_du_plan(ms, a, b):
    """Les mots dont le milieu (début + fin) / 2 tombe dans [a, b[ : chaque mot appartient ainsi à un seul passage."""
    return [m for m in ms if a <= (m["start"] + m["end"]) / 2 < b]


def plans(film, dossier, c, d, ms):
    """Un plan entre deux coupes consécutives (le premier dès 0, le dernier jusqu'à la fin) : numéro, début, durée, mots, images.
    Images : plans/NN.jpg au milieu du plan, à 720 px de large (le texte à l'écran se lit) ; au-delà de 2 s, NN-a.jpg (début + 0,15 s) et NN-b.jpg (fin - 0,2 s)."""
    os.makedirs(os.path.join(dossier, "plans"), exist_ok=True)
    bornes, rendu = [0.0] + list(c) + [d], []
    for k in range(len(bornes) - 1):
        a, b = bornes[k], bornes[k + 1]
        nom = f"{k + 1:02d}"
        temps = [(nom, (a + b) / 2)] + ([(nom + "-a", a + 0.15), (nom + "-b", b - 0.2)] if b - a > 2 else [])
        for n, t in temps:
            sortie("ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", film, "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "3", os.path.join(dossier, "plans", n + ".jpg"))
        rendu.append({"n": k + 1, "debut": a, "duree": b - a, "mots": mots_du_plan(ms, a, b if k < len(bornes) - 2 else float("inf")),  # le dernier plan prend tout ce qui reste
                      "images": ["plans/" + n + ".jpg" for n, _ in temps]})
    return rendu


def ouverture(c, ms, limite=3.0):
    """(coupes avant 3 s, temps du premier mot ou None, mots des 3 premières secondes)."""
    return sum(1 for t in c if t < limite), min((m["start"] for m in ms), default=None), mots_du_plan(ms, 0, limite)


def texte_mots(ms):
    return " ".join(m["text"].strip() for m in ms)


def decortiquer(source, dossier, langue="en", transcrire=True, ips=2, mots_donnes=None):
    os.makedirs(dossier, exist_ok=True)
    film, meta = recuperer(source, dossier)
    d, c, pl = duree(film), coupes(film), planches(film, os.path.join(dossier, "planches"), ips)
    calme = silences(film)
    ms, note = mots(film, dossier, langue) if transcrire else (mots_donnes or [], "transcription non demandée")
    texte = texte_mots(ms)
    pls, (avant, premier, trois) = plans(film, dossier, c, d, ms), ouverture(c, ms)
    durees = [p["duree"] for p in pls]
    open(os.path.join(dossier, "transcription.txt"), "w", encoding="utf-8").write(texte + "\n")
    chiffres = " · ".join(f"{k} : {v}" for k, v in meta.items() if v)
    lignes = ["# Le reel décortiqué", "", f"Source : {source}", *([chiffres] if chiffres else []), "",
              f"- Durée : {d:.2f} s ; format : {format_(film)}", f"- Coupes : {len(c)} ({len(c) / d * 60:.0f} par minute) : " + " ; ".join(f"{t:.2f}" for t in c),
              "- Silences (plus de 0,5 s sous -40 dB) : " + (" ; ".join(f"{a:.2f} à {b:.2f}" for a, b in calme) or "aucun"),
              f"- Planches : {len(pl)} dans planches/, {ips} images par seconde, de gauche à droite puis de haut en bas, le temps en bas à gauche",
              f"- Les mots ({langue}) : {len(ms)}, soit {len(ms) / d * 60:.0f} par minute" + (f" ({note})" if note else "") + " ; texte dans transcription.txt, temps dans mots.json ; recoupe-les avec l'écran, surtout les noms et les chiffres",
              f"- Plans : {len(pls)}, durée médiane {statistics.median(durees):.2f} s (le plus court {min(durees):.2f} s, le plus long {max(durees):.2f} s)",
              f"- Ouverture : {avant} coupes avant 3 s ; premier mot à " + (f"{premier:.2f} s" if premier is not None else "aucun mot") + " ; les mots des 3 premières secondes : " + (f"« {texte_mots(trois)} »" if trois else "aucun mot"), "",
              "## Ce qui se dit", "", texte or "(rien)", "",
              "## Les plans", "", "Un plan entre deux coupes : numéro · début · durée · mots dits (par leur milieu) · images (plans/NN.jpg au milieu, -a au début et -b à la fin pour un plan de plus de 2 s). Les coupes sont un plancher (voir references/refaire.md).", "",
              *(f"- {p['n']} · {p['debut']:.2f} s · {p['duree']:.2f} s · " + (f"« {texte_mots(p['mots'])} »" if p["mots"] else "aucun mot") + " · " + ", ".join(p["images"]) for p in pls), "",
              # aucun tableau vide : en essai, deux Claude sur quatre écrivaient le leur plus bas, sous le mauvais titre
              "À ajouter à la fin de ce fichier, à partir de `## Les plans` et des images, en regardant les planches : `## Plan par plan` puis `## Le moule` (references/refaire.md, section 2).", ""]
    open(os.path.join(dossier, "DECORTIQUE.md"), "w", encoding="utf-8").write("\n".join(lignes))
    print(f"DECORTIQUE_OK {os.path.join(dossier, 'DECORTIQUE.md')} · {d:.1f} s · {len(c)} coupes · {len(pls)} plans · {len(pl)} planches · {len(ms)} mots" + (f" ({note})" if note else ""))
    return d, c, pl


def normaliser(t):
    t = unicodedata.normalize("NFD", t.lower())
    return re.findall(r"[a-z0-9]+", "".join(x for x in t if not unicodedata.combining(x)))


def sept_mots(original, script):
    """Les suites de 7 mots de l'original qu'on retrouve dans le script."""
    a, b = normaliser(original), normaliser(script)
    deja = {tuple(b[i:i + 7]) for i in range(len(b) - 6)}
    return [" ".join(a[i:i + 7]) for i in range(len(a) - 6) if tuple(a[i:i + 7]) in deja]


def temps_en_secondes(t):
    """« 67.2 » ou « 1:07.2 » : des secondes."""
    m, _, s = t.rpartition(":")
    return (int(m) * 60 if m else 0) + float(s)


def mots_du_passage(chemin, debut, fin):
    """Les mots d'un passage de mots.json (le fichier ou son dossier) : (liste, durée en s)."""
    fichier = os.path.join(chemin, "mots.json") if os.path.isdir(chemin) else chemin
    if not os.path.isfile(fichier):
        sys.exit("Pas de mots.json : " + chemin)
    a, b = temps_en_secondes(debut), temps_en_secondes(fin)
    if b <= a:
        sys.exit("La fin doit suivre le début.")
    return mots_du_plan(json.load(open(fichier, encoding="utf-8")), a, b), b - a


def selftest():
    with tempfile.TemporaryDirectory() as d:
        couleurs = "".join(f"color=c={c}:s=270x480:d={2 if c != 'white' else 3}:r=30[{c}];" for c in ("red", "blue", "white"))
        film = os.path.join(d, "trois.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-filter_complex", couleurs + "[red][blue][white]concat=n=3:v=1[v]", "-map", "[v]", film], check=True)
        faux = [{"id": f"w{k}", "text": t, "start": a, "end": b} for k, (t, a, b) in enumerate((("un", 0.5, 0.9), ("deux", 1.8, 2.4), ("trois", 3.9, 4.3), ("quatre", 5.0, 5.5)))]
        duree_, c, pl = decortiquer(film, os.path.join(d, "a"), transcrire=False, mots_donnes=faux)
        assert abs(duree_ - 7) < 0.2 and len(c) == 2 and abs(c[0] - 2) < 0.2 and abs(c[1] - 4) < 0.2, (duree_, c)
        md = open(os.path.join(d, "a", "DECORTIQUE.md"), encoding="utf-8").read()
        assert pl and "`## Plan par plan`" in md and "|---|" not in md and "270 x 480, 30 i/s" in md, md
        pls = plans(film, os.path.join(d, "p"), c, duree_, faux)  # 3 plans de 2, 2 et 3 s ; « deux » (milieu 2,1) et « trois » (milieu 4,1) chevauchent une coupe
        assert [p["n"] for p in pls] == [1, 2, 3] and all(abs(p["duree"] - e) < 0.2 for p, e in zip(pls, (2, 2, 3))), pls
        assert [[m["text"] for m in p["mots"]] for p in pls] == [["un"], ["deux"], ["trois", "quatre"]], pls
        assert sum(len(p["mots"]) for p in pls) == len(faux)  # chaque mot dans un seul plan
        vus = sorted(os.listdir(os.path.join(d, "p", "plans")))
        assert vus == ["01.jpg", "02.jpg", "03-a.jpg", "03-b.jpg", "03.jpg"], vus  # -a et -b seulement pour le plan de plus de 2 s
        for v in vus:
            assert format_(os.path.join(d, "p", "plans", v)).startswith("720 x "), v
        assert ouverture(c, faux) == (1, 0.5, faux[:2]), ouverture(c, faux)
        assert ouverture([], []) == (0, None, [])  # témoin : sans mot, rien n'est inventé
        for morceau in ("- Plans : 3, durée médiane 2.0", "- Ouverture : 1 coupes avant 3 s ; premier mot à 0.50 s ; les mots des 3 premières secondes : « un deux »", " s · « trois quatre » · plans/03.jpg, plans/03-a.jpg, plans/03-b.jpg"):
            assert morceau in md, morceau
        assert "## Les plans" in md
        # --mots : le comptage par le milieu, en secondes ou en m:ss
        os.makedirs(os.path.join(d, "m"))
        json.dump([{"id": "0", "text": "un", "start": 60.0, "end": 61.0}, {"id": "1", "text": "deux", "start": 67.0, "end": 67.6}, {"id": "2", "text": "trois", "start": 71.9, "end": 72.5}], open(os.path.join(d, "m", "mots.json"), "w"))
        assert temps_en_secondes("1:07.2") == 67.2 and temps_en_secondes("11.5") == 11.5 and temps_en_secondes("0") == 0
        sel, dur = mots_du_passage(os.path.join(d, "m"), "1:07.2", "1:42")
        assert [m["text"] for m in sel] == ["deux", "trois"] and abs(dur - 34.8) < 1e-9, sel
        assert [m["text"] for m in mots_du_passage(os.path.join(d, "m", "mots.json"), "60", "67.2")[0]] == ["un"]  # « deux » (milieu 67,3) est au-delà
        assert mots_du_passage(os.path.join(d, "m"), "0", "11.5")[0] == []  # témoin : aucun mot dans ce passage
        sortie_ = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "--mots", os.path.join(d, "m"), "0", "11.5"], capture_output=True, text=True)
        assert sortie_.returncode == 0 and sortie_.stdout.startswith("0 mots, 11.5 s (0 par minute)"), sortie_
        uni = os.path.join(d, "uni.mp4")  # témoin : sans changement de plan, aucune coupe
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=red:s=270x480:d=3:r=30", uni], check=True)
        assert decortiquer(uni, os.path.join(d, "b"), transcrire=False)[1] == []
        # un lien avec la clé : ScrapeCreators donne l'adresse du fichier et les chiffres (réponses enregistrées, sans réseau)
        global api
        vrai, adresse = api, "file://" + uni
        reponses = {"/v1/instagram/post": {"data": {"xdt_shortcode_media": {"video_url": adresse, "video_play_count": 6669525, "owner": {"username": "compte"},
                                                                             "taken_at_timestamp": 1759622400, "edge_media_to_parent_comment": {"count": 1004}}}},
                    "/v2/tiktok/video": {"aweme_detail": {"video": {"play_addr": {"url_list": [adresse]}}, "statistics": {"play_count": 12, "comment_count": 3}}}}
        api, os.environ["SCRAPECREATORS_API_KEY"] = (lambda chemin, lien, cle: reponses[chemin]), "essai"
        try:
            f, m = recuperer("https://www.instagram.com/reel/X/", os.path.join(d, "a"))
            assert os.path.getsize(f) == os.path.getsize(uni) and m["vues"] == 6669525 and m["commentaires"] == 1004 and m["date"] == "2025-10-05", m
            assert recuperer("https://www.tiktok.com/@x/video/1", os.path.join(d, "b"))[1]["vues"] == 12
            assert par_scrapecreators("https://www.youtube.com/shorts/x", "essai") is None  # témoin : YouTube passe par yt-dlp
        finally:
            api = vrai
            del os.environ["SCRAPECREATORS_API_KEY"]
    with tempfile.TemporaryDirectory() as d:  # 2 s de son puis 2 s de silence : un silence, de 2 à 4 s ; un son continu : aucun
        for nom, expr, attendu in (("coupe", "if(lt(t,2),sin(2*PI*440*t),0)", 1), ("continu", "sin(2*PI*440*t)", 0)):
            s = os.path.join(d, nom + ".mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=red:s=270x480:d=4:r=30", "-f", "lavfi", "-i", f"aevalsrc='{expr}':d=4", "-shortest", s], check=True)
            v = silences(s)
            assert len(v) == attendu and (not v or abs(v[0][0] - 2) < 0.2), (nom, v)
    phrase = "le metier le mieux paye du pays n est pas celui que tu crois"
    assert sept_mots(phrase, "Écoute : le métier le mieux payé du pays n'est pas le tien")
    assert not sept_mots(phrase, "la boulangerie la plus rentable du quartier ouvre seulement le matin")
    print("DECORTIQUER_OK")


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:2] == ["--mots"] and len(sys.argv) == 5:
        sel, dur = mots_du_passage(*sys.argv[2:5])
        print(f"{len(sel)} mots, {dur:g} s ({len(sel) / dur * 60:.0f} par minute)")
        if sel:
            print(texte_mots(sel))
        return
    if sys.argv[1:2] == ["--sept-mots"]:
        repris = sept_mots(open(sys.argv[2], encoding="utf-8").read(), open(sys.argv[3], encoding="utf-8").read())
        for r in repris:
            print("repris :", r)
        print("SEPT_MOTS_KO" if repris else "SEPT_MOTS_OK")
        return sys.exit(1 if repris else 0)
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("-o", dest="dossier", required=True)
    p.add_argument("--langue", default="en")
    p.add_argument("--ips", type=int, default=2)
    a = p.parse_args()
    decortiquer(a.source, a.dossier, a.langue, ips=a.ips)


if __name__ == "__main__":
    main()
