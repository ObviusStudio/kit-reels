"""Images et vidéos libres de droit : chercher, prendre avec sa licence notée, contrôler.

Usage :
  python3 banque.py chercher "<mots concrets, en anglais de préférence>" [--type photo|video] [--banques pexels,pixabay,openverse]
                    [--vertical] [-n 5] [--apercus <dossier>]
  python3 banque.py prendre <banque>:<type>:<id> -o <dossier>
  python3 banque.py noter <fichier> --banque <nom> --page <adresse> --auteur "<nom>" [--licence "<nom>" --licence-url <adresse>]
  python3 banque.py controler <dossier>
  python3 banque.py --autotest

Banques : Pexels (photos, vidéos ; clé gratuite dans PEXELS_API_KEY), Pixabay (photos, vidéos ; clé gratuite dans
PIXABAY_API_KEY), Openverse (images de Wikimedia Commons, Flickr, musées : CC0, domaine public ou CC BY seulement ; sans
clé). Unsplash se prend à la main sur son site, puis se note par `noter` : son API demande des images liées à leur
adresse, pas des fichiers téléchargés par un script. Une banque sans sa clé est sautée, et le message dit à Claude de demander à la personne sa clé gratuite.
Chaque fichier pris est noté dans <dossier>/banque.json : banque, page, auteur, licence, crédit exigé ou non, date,
taille mesurée. `controler` rend BANQUE_OK quand chaque image ou vidéo du dossier y est notée avec sa page et sa licence.
Les clés ne s'affichent ni ne s'écrivent jamais. Licences relues le 03/11/2026 : references/illustrations.md, section 5.
"""
import datetime, json, os, shutil, subprocess, sys, tempfile, urllib.error, urllib.parse, urllib.request

UA = {"User-Agent": "kit-reels-banque/1.0"}
CLES = {"pexels": ("PEXELS_API_KEY", "https://www.pexels.com/api/"),
        "pixabay": ("PIXABAY_API_KEY", "https://pixabay.com/api/docs/")}
LICENCES = {"pexels": ("Licence Pexels", "https://www.pexels.com/license/"),
            "pixabay": ("Content License de Pixabay", "https://pixabay.com/service/license-summary/"),
            "unsplash": ("Licence Unsplash", "https://unsplash.com/license")}
OPENVERSE_PERMISES = ("cc0", "pdm", "by")   # ni BY-SA (le film devrait suivre sa licence), ni NC, ni ND
MEDIAS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".mov", ".webm", ".m4v")
NOTES = "banque.json"


def lire_json(url, entetes=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **(entetes or {})}), timeout=30) as r:
        return json.load(r)


def cle(banque):
    nom, ou = CLES[banque]
    v = os.environ.get(nom)
    if not v:
        print(f"{banque} sautée : {nom} absente. Demande à la personne sa clé gratuite ({ou}), qu'elle ajoute elle-même "
              f"à son environnement : export {nom}=<sa clé>", file=sys.stderr)
    return v


def choisir(fichiers):
    """(largeur, hauteur, url) : le plus petit dont le petit côté fait 1080 au moins, sinon le plus grand."""
    assez = [f for f in fichiers if min(f[0], f[1]) >= 1080]
    return min(assez, key=lambda f: f[0] * f[1]) if assez else max(fichiers, key=lambda f: f[0] * f[1])


def fiche(**k):
    base = dict(duree=None, credit=None, source=None, ia=False, auteur_url=None)
    return {**base, **k}


def pexels_photo(p):
    nom, url = LICENCES["pexels"]
    return fiche(ref=f"pexels:photo:{p['id']}", banque="Pexels", type="photo", page=p["url"], auteur=p["photographer"],
                 auteur_url=p.get("photographer_url"), largeur=p["width"], hauteur=p["height"],
                 apercu=p["src"]["medium"], fichier_url=p["src"]["original"], licence=nom, licence_url=url)


def pexels_video(v):
    nom, url = LICENCES["pexels"]
    l, h, lien = choisir([(f["width"], f["height"], f["link"]) for f in v["video_files"] if f.get("width")])
    return fiche(ref=f"pexels:video:{v['id']}", banque="Pexels", type="video", page=v["url"], auteur=v["user"]["name"],
                 auteur_url=v["user"].get("url"), largeur=l, hauteur=h, duree=v.get("duration"), apercu=v.get("image"),
                 fichier_url=lien, licence=nom, licence_url=url)


def pixabay_photo(h):
    nom, url = LICENCES["pixabay"]
    return fiche(ref=f"pixabay:photo:{h['id']}", banque="Pixabay", type="photo", page=h["pageURL"], auteur=h["user"],
                 auteur_url=h.get("userURL") or f"https://pixabay.com/users/{h['user']}-{h['user_id']}/",
                 largeur=h["imageWidth"], hauteur=h["imageHeight"], apercu=h.get("previewURL"),
                 fichier_url=h["largeImageURL"], licence=nom, licence_url=url, ia=bool(h.get("isAiGenerated")))


def pixabay_video(h):
    nom, url = LICENCES["pixabay"]
    tailles = [x for x in h["videos"].values() if x.get("url") and x.get("width")]
    l, ht, lien = choisir([(x["width"], x["height"], x["url"]) for x in tailles])
    return fiche(ref=f"pixabay:video:{h['id']}", banque="Pixabay", type="video", page=h["pageURL"], auteur=h["user"],
                 auteur_url=h.get("userURL"), largeur=l, hauteur=ht, duree=h.get("duration"),
                 apercu=next((x.get("thumbnail") for x in tailles if x.get("thumbnail")), None),
                 fichier_url=lien, licence=nom, licence_url=url, ia=bool(h.get("isAiGenerated")))


def openverse(r):
    lic, ver = r["license"].lower(), r.get("license_version") or ""
    nom = {"cc0": "CC0 1.0", "pdm": "Marque du domaine public"}.get(lic, f"CC {lic.upper()} {ver}".strip())
    return fiche(ref=f"openverse:photo:{r['id']}", banque="Openverse", type="photo", page=r["foreign_landing_url"],
                 auteur=r.get("creator") or "inconnu", auteur_url=r.get("creator_url"), largeur=r.get("width"),
                 hauteur=r.get("height"), apercu=r.get("thumbnail"), fichier_url=r["url"], licence=nom,
                 licence_url=r.get("license_url"), source=r.get("source"),
                 credit=r.get("attribution") if lic not in ("cc0", "pdm") else None, licence_code=lic)


def garder(f, vertical=False):
    """Écarte ce qui est marqué généré par IA, une licence Openverse non permise, et l'horizontal si --vertical."""
    if f["ia"] or (f["banque"] == "Openverse" and f.get("licence_code") not in OPENVERSE_PERMISES):
        return False
    return not (vertical and f["largeur"] and f["hauteur"] and f["hauteur"] <= f["largeur"])


def requete(banque, typ, q=None, ident=None, n=10, vertical=False):
    """Une recherche (q) ou une fiche (ident) ; rend une liste de fiches."""
    if banque == "pexels":
        k = cle("pexels")
        if not k:
            return []
        e = {"Authorization": k}
        if typ == "video":
            if ident:
                return [pexels_video(lire_json(f"https://api.pexels.com/videos/videos/{ident}", e))]
            p = {"query": q, "per_page": n, **({"orientation": "portrait"} if vertical else {})}
            return [pexels_video(v) for v in lire_json("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(p), e)["videos"]]
        if ident:
            return [pexels_photo(lire_json(f"https://api.pexels.com/v1/photos/{ident}", e))]
        p = {"query": q, "per_page": n, **({"orientation": "portrait"} if vertical else {})}
        return [pexels_photo(x) for x in lire_json("https://api.pexels.com/v1/search?" + urllib.parse.urlencode(p), e)["photos"]]
    if banque == "pixabay":
        k = cle("pixabay")
        if not k:
            return []
        p = {"key": k, "safesearch": "true", **({"id": ident} if ident else {"q": q, "per_page": max(3, min(n, 200))})}
        if typ == "video":
            return [pixabay_video(h) for h in lire_json("https://pixabay.com/api/videos/?" + urllib.parse.urlencode(p))["hits"]]
        p["image_type"] = "photo"
        if vertical and not ident:
            p["orientation"] = "vertical"
        return [pixabay_photo(h) for h in lire_json("https://pixabay.com/api/?" + urllib.parse.urlencode(p))["hits"]]
    if banque == "openverse":
        if typ == "video":
            return []                                   # Openverse n'a pas de vidéos
        if ident:
            return [openverse(lire_json(f"https://api.openverse.org/v1/images/{ident}/"))]
        p = {"q": q, "license": ",".join(OPENVERSE_PERMISES), "page_size": n, **({"aspect_ratio": "tall"} if vertical else {})}
        return [openverse(r) for r in lire_json("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(p))["results"]]
    raise ValueError(f"banque inconnue : {banque} (pexels, pixabay, openverse ; Unsplash à la main, puis noter)")


def telecharger(url, chemin):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r, open(chemin, "wb") as o:
        shutil.copyfileobj(r, o)


def mesurer(chemin):
    """Largeur, hauteur et durée mesurées par ffprobe ; None si ffprobe manque."""
    if not shutil.which("ffprobe"):
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                          "-show_entries", "format=duration", "-of", "json", chemin], capture_output=True, text=True)
    d = json.loads(out.stdout or "{}")
    s = (d.get("streams") or [{}])[0]
    duree = d.get("format", {}).get("duration")
    return s.get("width"), s.get("height"), round(float(duree), 2) if duree and duree != "N/A" else None


def lire_notes(dossier):
    p = os.path.join(dossier, NOTES)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def ecrire_note(dossier, note):
    notes = [n for n in lire_notes(dossier) if n["fichier"] != note["fichier"]] + [note]
    with open(os.path.join(dossier, NOTES), "w", encoding="utf-8") as o:
        json.dump(notes, o, ensure_ascii=False, indent=2)


def analyser_ref(ref):
    parts = ref.split(":")
    if len(parts) != 3 or parts[0] not in ("pexels", "pixabay", "openverse") or parts[1] not in ("photo", "video"):
        raise ValueError(f"référence illisible : {ref} (forme : pexels:video:123, pixabay:photo:45, openverse:photo:<id>)")
    return parts


def chercher(q, typ="photo", banques=("pexels", "pixabay", "openverse"), vertical=False, n=5, apercus=None):
    trouve = []
    for b in banques:
        try:
            fs = [f for f in requete(b, typ, q=q, n=max(n * 2, 3), vertical=vertical) if garder(f, vertical)][:n]
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as e:
            print(f"{b} : recherche impossible ({getattr(e, 'code', '') or type(e).__name__})", file=sys.stderr)
            continue
        for f in fs:
            d = f" {f['duree']} s" if f["duree"] else ""
            c = " · crédit exigé" if f["credit"] else ""
            print(f"{f['ref']}  {f['largeur']}x{f['hauteur']}{d}  {f['auteur']}  {f['licence']}{c}  {f['page']}")
            if apercus and f["apercu"]:
                os.makedirs(apercus, exist_ok=True)
                try:
                    telecharger(f["apercu"], os.path.join(apercus, f["ref"].replace(":", "-") + ".jpg"))
                except (urllib.error.URLError, TimeoutError):
                    pass
        trouve += fs
    print(f"{len(trouve)} résultat(s) ; aperçus dans {apercus}/" if apercus else f"{len(trouve)} résultat(s)")
    return trouve


def prendre(ref, dossier):
    banque, typ, ident = analyser_ref(ref)
    fs = requete(banque, typ, ident=ident)
    if not fs:
        raise SystemExit(f"{ref} : introuvable, ou banque sans clé")
    f = fs[0]
    if not garder(f):
        raise SystemExit(f"{ref} refusé : {'marqué généré par IA' if f['ia'] else 'licence non permise : ' + f['licence']}")
    os.makedirs(dossier, exist_ok=True)
    ext = os.path.splitext(urllib.parse.urlparse(f["fichier_url"]).path)[1].lower()
    ext = ext if ext in MEDIAS else (".mp4" if typ == "video" else ".jpg")
    nom = ref.replace(":", "-") + ext
    telecharger(f["fichier_url"], os.path.join(dossier, nom))
    m = mesurer(os.path.join(dossier, nom))
    note = {"fichier": nom, "ref": ref, "banque": f["banque"], "type": typ, "page": f["page"], "auteur": f["auteur"],
            "auteur_url": f["auteur_url"], "licence": f["licence"], "licence_url": f["licence_url"],
            "credit_exige": bool(f["credit"]), "credit": f["credit"], "source": f["source"],
            "largeur": m[0] if m else f["largeur"], "hauteur": m[1] if m else f["hauteur"],
            "duree": ((m[2] if m else None) or f["duree"]) if typ == "video" else None, "telecharge_le": datetime.date.today().isoformat()}
    ecrire_note(dossier, note)
    print(f"{nom} : {note['largeur']}x{note['hauteur']}, {f['licence']}, noté dans {NOTES}")
    if f["credit"]:
        print(f"crédit à mettre dans la légende : {f['credit']}")
    return note


def noter(fichier, banque, page, auteur, licence=None, licence_url=None):
    b = banque.lower()
    if b in LICENCES and not licence:
        licence, licence_url = LICENCES[b]
    if not (page and auteur and licence and licence_url):
        raise SystemExit("noter : il faut --page, --auteur, et --licence avec --licence-url pour une banque inconnue")
    if not os.path.exists(fichier):
        raise SystemExit(f"noter : {fichier} n'existe pas")
    m = mesurer(fichier)
    typ = "video" if fichier.lower().endswith((".mp4", ".mov", ".webm", ".m4v")) else "photo"
    note = {"fichier": os.path.basename(fichier), "ref": None, "banque": banque, "type": typ, "page": page, "auteur": auteur, "auteur_url": None,
            "licence": licence, "licence_url": licence_url, "credit_exige": False, "credit": None, "source": "à la main",
            "largeur": m[0] if m else None, "hauteur": m[1] if m else None, "duree": m[2] if m and typ == "video" else None,
            "telecharge_le": datetime.date.today().isoformat()}
    ecrire_note(os.path.dirname(os.path.abspath(fichier)), note)
    print(f"{note['fichier']} : {licence}, noté dans {NOTES}")
    return note


def controler(dossier):
    notes = {n["fichier"]: n for n in lire_notes(dossier)}
    fichiers = sorted(x for x in os.listdir(dossier) if x.lower().endswith(MEDIAS))
    pb = [f"{x} : absent de {NOTES}" for x in fichiers if x not in notes]
    pb += [f"{x} : sans {k}" for x, n in notes.items() for k in ("page", "licence", "licence_url") if not n.get(k)]
    pb += [f"{x} : noté, mais le fichier manque" for x in notes if x not in fichiers]
    for p in pb:
        print(p)
    credits = [n["credit"] for n in notes.values() if n.get("credit_exige") and n.get("credit")]
    if credits:
        print("Crédits à mettre dans la légende :")
        for c in credits:
            print(f"  {c}")
    print(f"BANQUE_KO {len(pb)}" if pb else f"BANQUE_OK {len(fichiers)}")
    return not pb


def autotest():
    ok = 0
    pv = {"id": 1, "url": "https://www.pexels.com/video/1/", "duration": 6, "image": "https://a/1.jpg",
          "user": {"name": "A", "url": "https://www.pexels.com/@a"},
          "video_files": [{"width": w, "height": h, "link": f"https://v/{w}.mp4"} for w, h in
                          ((360, 640), (720, 1280), (1080, 1920), (2160, 3840))]}
    f = pexels_video(pv)
    assert (f["largeur"], f["hauteur"], f["fichier_url"]) == (1080, 1920, "https://v/1080.mp4"); ok += 1
    xv = {"id": 2, "pageURL": "https://pixabay.com/videos/id-2/", "duration": 9, "user": "b", "userURL": "https://u/b",
          "videos": {q: {"url": f"https://p/{q}.mp4", "width": w, "height": h, "thumbnail": f"https://p/{q}.jpg"}
                     for q, w, h in (("large", 3840, 2160), ("medium", 2560, 1440), ("small", 1920, 1080), ("tiny", 1280, 720))}}
    f = pixabay_video(xv)
    assert f["fichier_url"] == "https://p/small.mp4" and garder(f) and not garder(f, vertical=True); ok += 2
    xp = {"id": 3, "pageURL": "https://pixabay.com/photos/3/", "user": "c", "user_id": 9, "imageWidth": 4000,
          "imageHeight": 6000, "previewURL": "https://p/3.jpg", "largeImageURL": "https://p/3_1280.jpg", "isAiGenerated": True}
    assert not garder(pixabay_photo(xp)) and garder(pixabay_photo({**xp, "isAiGenerated": False}), vertical=True); ok += 2
    ov = {"id": "u", "foreign_landing_url": "https://www.flickr.com/p/1", "url": "https://f/1.jpg", "creator": "D",
          "license": "by", "license_version": "2.0", "license_url": "https://creativecommons.org/licenses/by/2.0/",
          "attribution": '"t" by D is licensed under CC BY 2.0.', "width": 1024, "height": 768, "source": "flickr"}
    f = openverse(ov)
    assert garder(f) and f["credit"] and f["licence"] == "CC BY 2.0"; ok += 1
    assert not garder(openverse({**ov, "license": "by-sa"})) and not garder(openverse({**ov, "license": "by-nc"})); ok += 1
    assert openverse({**ov, "license": "cc0", "license_version": "1.0"})["credit"] is None; ok += 1
    assert analyser_ref("pexels:video:27451031") == ["pexels", "video", "27451031"]; ok += 1
    for mauvaise in ("unsplash:photo:1", "pexels:audio:1", "pexels:1"):
        try:
            analyser_ref(mauvaise)
            raise AssertionError(mauvaise)
        except ValueError:
            pass
    ok += 1
    d = tempfile.mkdtemp()
    try:
        for x in ("a.jpg", "b.mp4"):
            open(os.path.join(d, x), "wb").write(b"\0")
        os.environ["PEXELS_API_KEY"] = "cle-temoin-a-ne-pas-ecrire"
        noter(os.path.join(d, "a.jpg"), "unsplash", "https://unsplash.com/photos/x", "E")
        assert not controler(d); ok += 1                                  # témoin : b.mp4 n'est pas noté
        noter(os.path.join(d, "b.mp4"), "pexels", "https://www.pexels.com/video/2/", "F")
        assert controler(d); ok += 1
        assert "cle-temoin" not in open(os.path.join(d, NOTES), encoding="utf-8").read(); ok += 1
        os.remove(os.path.join(d, "a.jpg"))
        assert not controler(d); ok += 1                                  # noté, mais le fichier manque
    finally:
        shutil.rmtree(d)
        os.environ.pop("PEXELS_API_KEY", None)
    print(f"autotest banque : {ok} contrôles passés")


def main(a):
    if a == ["--autotest"]:
        return autotest()
    if len(a) < 2 or a[0] not in ("chercher", "prendre", "noter", "controler"):
        raise SystemExit(__doc__)
    def opt(nom, defaut=None):
        return a[a.index(nom) + 1] if nom in a else defaut
    if a[0] == "chercher":
        chercher(a[1], opt("--type", "photo"), tuple(opt("--banques", "pexels,pixabay,openverse").split(",")),
                 "--vertical" in a, int(opt("-n", 5)), opt("--apercus"))
    elif a[0] == "prendre":
        if not opt("-o"):
            raise SystemExit("prendre : -o <dossier> manque")
        prendre(a[1], opt("-o"))
    elif a[0] == "noter":
        noter(a[1], opt("--banque", ""), opt("--page"), opt("--auteur"), opt("--licence"), opt("--licence-url"))
    else:
        sys.exit(0 if controler(a[1]) else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
