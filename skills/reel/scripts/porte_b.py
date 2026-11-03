"""Les contrôles de la porte B que verifier.py n'avait pas (references/controles.md) : image 0, zones de sécurité, note de
mouvement de chaque seconde, déterminisme de la composition, tirets longs. Chacun rend (ok, texte) ; verifier.py les écrit dans
son rapport.

Usage seul :
  python3 porte_b.py final.mp4 [--format 9:16] [--projet dossier-hyperframes] [--carte 2]   (--carte : secondes de la carte de fin, non notées)
  python3 porte_b.py --autotest
"""
import os, re, subprocess, sys, tempfile

# Bandes hors de la zone du texte (x, y, largeur, hauteur), format par format, d'après references/ecran.md § 1.
BANDES = {"9:16": {"haut": (0, 0, 1080, 170), "bas": (0, 1500, 1080, 420), "gauche": (0, 0, 79, 1920), "droite": (931, 0, 149, 1920)},
          "4:5": {"haut": (0, 0, 1080, 108), "bas": (0, 1242, 1080, 108), "gauche": (0, 0, 108, 1350), "droite": (972, 0, 108, 1350)},
          "1:1": {"haut": (0, 0, 1080, 108), "bas": (0, 972, 1080, 108), "gauche": (0, 0, 108, 1080), "droite": (972, 0, 108, 1080)},
          "16:9": {"haut": (0, 0, 1920, 54), "bas": (0, 972, 1920, 108), "gauche": (0, 0, 96, 1080), "droite": (1824, 0, 96, 1080)}}
CARTE = 2.0  # la carte de fin (1,5 à 2 s) tient presque immobile : ses secondes ne sont pas notées
SOMBRE, ECART_SOMBRE, ECART_CLAIR_BAS, ECART_CLAIR_HAUT = 128, 50, 20, 8
NOIR = 16  # luminance d'un noir pur en vidéo
COTE, MOU = 96, 0.6  # images en gris 96x96 à 30 i/s ; une seconde sous 0,6 de mouvement est faible (sources.md, C10)
# témoin du mouvement : les images 29 à 60 sont la même, la seconde de 1 à 2 s est figée, les autres bougent
GEL = "testsrc2=d=4:s=320x240:r=30,split[a][b];[a][b]freezeframes=first=30:last=60:replace=29"
INTERDITS_CODE = re.compile(r"Math\.random|Date\.now|performance\.now")
TIRETS = re.compile("[—–−]")  # tiret cadratin, demi-cadratin, signe moins typographique


def _sortie(*cmd):
    s = subprocess.run(list(cmd), capture_output=True, text=True)
    return s.stdout + s.stderr


def _luminance(film, filtre, cle, fonction):
    t = _sortie("ffmpeg", "-hide_banner", "-nostats", "-i", film, "-an", "-vf", f"{filtre},signalstats,metadata=print:key=lavfi.signalstats.{cle}", "-f", "null", "-")
    valeurs = [float(x) for x in re.findall(rf"{cle}=([\d.]+)", t)]
    return fonction(valeurs) if valeurs else None


def image_0(film):
    y = _luminance(film, r"select=eq(n\,0)", "YAVG", max)
    ok = y is not None and y > NOIR + 4
    return ok, f"image 0 : luminance {y if y is not None else 'illisible'} (un noir pur donne {NOIR}) : " + ("elle porte une image" if ok else "noire ou vide : le hook doit y être")


def zones(film, format_="9:16"):
    """Alerte, jamais un refus : une bande voit tout contenu, et seule la place du texte est une règle (une image peut déborder)."""
    fond = _luminance(film, r"select=eq(n\,0),crop=100:100:0:0", "YAVG", max)
    fautes = []
    for nom, (x, y, w, h) in BANDES[format_].items():
        bas = _luminance(film, f"crop={w}:{h}:{x}:{y}", "YMIN", min)
        haut = _luminance(film, f"crop={w}:{h}:{x}:{y}", "YMAX", max)
        if fond < SOMBRE and haut > fond + ECART_SOMBRE:
            fautes.append(f"{nom} (max {haut:.0f} pour un fond à {fond:.0f})")
        if fond >= SOMBRE and (bas < fond - ECART_CLAIR_BAS or haut > fond + ECART_CLAIR_HAUT):
            fautes.append(f"{nom} (de {bas:.0f} à {haut:.0f} pour un fond à {fond:.0f})")
    return True, (f"zones de sécurité ({format_}) : bandes vides" if not fautes else
                  f"zones de sécurité ({format_}) : contenu dans les bandes {', '.join(fautes)} ; à relire sur la planche : seul le texte doit rester dans sa zone")


def notes(film):
    """Note de mouvement de chaque seconde complète : écart moyen entre images successives, en gris 96x96 à 30 i/s, sur 255."""
    # shortcut: secondes fixes (0-1 s, 1-2 s...) et fin incomplète ignorée ; un arrêt court à cheval sur deux secondes compte
    # à moitié dans chacune : freezedetect (verifier.py) reste le juge des arrêts ; passer à des fenêtres glissantes si ça gêne
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", film, "-an", "-vf", f"fps=30,scale={COTE}:{COTE},format=gray", "-f", "rawvideo", "-"],
                       capture_output=True)
    n = COTE * COTE
    im = [r.stdout[i:i + n] for i in range(0, len(r.stdout) - n + 1, n)]
    d = [sum(abs(a - b) for a, b in zip(x, y)) / n for x, y in zip(im, im[1:])]
    # la seconde k reçoit les écarts qui mènent à ses images 30k à 30k+29
    return [sum(t) / len(t) for t in (d[max(0, 30 * k - 1):30 * k + 29] for k in range(len(im) // 30))]


def mouvement(film, carte=CARTE):
    with tempfile.TemporaryDirectory() as d:
        t = os.path.join(d, "gel.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", GEL, t], check=True)
        temoin = [k for k, x in enumerate(notes(t)) if x < MOU]
    if temoin != [1]:  # sans témoin qui échoue, la mesure ne prouverait rien
        return False, f"note de mouvement : le témoin (une seconde figée) n'est pas vu ({temoin}), la mesure ne prouve rien"
    n = notes(film)
    notees = n[:max(1, len(n) - int(carte))]  # sans les secondes de la carte de fin
    faibles = [(k, x) for k, x in enumerate(notees) if x < MOU]
    if not n:
        return False, "note de mouvement : film de moins d'une seconde"
    return not faibles, (f"note de mouvement : {len(notees)} secondes notées (carte de fin à part), toutes à {MOU} ou plus (la plus calme : {min(notees):.2f})" if not faibles else
                         f"secondes faibles (sous {MOU}) : " + ", ".join(f"{k}-{k + 1} s ({x:.2f})" for k, x in faibles[:8]) +
                         " ; à reprendre, sauf une respiration, une chute ou la carte de fin écrite dans le storyboard")


def _textes(projet, extensions):
    """La composition seule : index.html et compositions/, jamais les captures de sites, les bibliothèques ni les rendus."""
    chemins = [os.path.join(projet, "index.html")]
    for d, _, fichiers in os.walk(os.path.join(projet, "compositions")):
        chemins += [os.path.join(d, f) for f in fichiers]
    for p in sorted(chemins):
        if p.endswith(extensions) and os.path.isfile(p):
            yield os.path.relpath(p, projet), open(p, encoding="utf-8", errors="ignore").read()


def determinisme(projet):
    fautes = [f"{p}:{t.count(chr(10), 0, m.start()) + 1} ({m.group(0)})" for p, t in _textes(projet, (".html", ".js")) for m in INTERDITS_CODE.finditer(t)]
    return not fautes, "composition déterministe : aucun hasard sans graine, aucune horloge" if not fautes else "hasard ou horloge dans la composition : " + ", ".join(fautes[:5])


def tirets(projet):
    fautes = [f"{p}:{t.count(chr(10), 0, m.start()) + 1}" for p, t in _textes(projet, (".html",)) for m in TIRETS.finditer(t)]
    return not fautes, "aucun tiret long dans les textes" if not fautes else "tiret long (cadratin, demi-cadratin ou signe moins typographique) : " + ", ".join(fautes[:5])


def controles(film, format_="9:16", projet=None, carte=CARTE):
    r = [image_0(film), zones(film, format_), mouvement(film, carte)]
    if projet:
        r += [determinisme(projet), tirets(projet)]
    return r


def autotest():
    with tempfile.TemporaryDirectory() as d:
        ff = lambda *a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
        noir, propre, deborde = (os.path.join(d, f) for f in ("noir.mp4", "propre.mp4", "deborde.mp4"))
        ff("-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=1:r=30", "-pix_fmt", "yuv420p", noir)
        ff("-f", "lavfi", "-i", "color=c=0x0A0F16:s=1080x1920:d=1:r=30", "-vf", "drawbox=x=200:y=600:w=600:h=300:color=white:t=fill", "-pix_fmt", "yuv420p", propre)
        ff("-f", "lavfi", "-i", "color=c=0x0A0F16:s=1080x1920:d=1:r=30", "-vf", "drawbox=x=200:y=60:w=600:h=80:color=white:t=fill", "-pix_fmt", "yuv420p", deborde)
        assert not image_0(noir)[0] and image_0(propre)[0]
        bouge, gel = os.path.join(d, "bouge.mp4"), os.path.join(d, "gel.mp4")
        ff("-f", "lavfi", "-i", "testsrc2=d=3:s=320x240:r=30", bouge)
        ff("-f", "lavfi", "-i", GEL, gel)
        assert mouvement(bouge, carte=0)[0], mouvement(bouge, carte=0)
        assert not mouvement(gel, carte=0)[0] and "1-2 s" in mouvement(gel, carte=0)[1], mouvement(gel, carte=0)
        assert not mouvement(gel, carte=1)[0]  # la seconde figée n'est pas dans la carte de fin : toujours faible
        ff("-f", "lavfi", "-i", "testsrc2=d=3:s=320x240:r=30,split[a][b];[a][b]freezeframes=first=60:last=89:replace=59", os.path.join(d, "fin.mp4"))
        assert mouvement(os.path.join(d, "fin.mp4"), carte=1)[0]  # une carte de fin immobile ne compte pas
        assert "bandes vides" in zones(propre)[1], zones(propre)
        assert zones(deborde)[0] and "haut" in zones(deborde)[1], zones(deborde)  # une alerte, jamais un refus
        projet = os.path.join(d, "projet"); os.mkdir(projet)
        open(os.path.join(projet, "index.html"), "w").write("<script>gsap.to('.a', {x: 10});</script><p>Une phrase simple.</p>")
        assert determinisme(projet)[0] and tirets(projet)[0]
        open(os.path.join(projet, "index.html"), "a").write("<script>const r = Math.random();</script><p>un tiret — long</p>")
        assert not determinisme(projet)[0] and not tirets(projet)[0]
        os.makedirs(os.path.join(projet, "capture")); open(os.path.join(projet, "capture", "site.html"), "w").write("un site \u2014 capturé")
        open(os.path.join(projet, "index.html"), "w").write("<p>Une phrase simple.</p>")
        assert tirets(projet)[0]  # une capture de site n'est pas un texte de la vidéo
    print("autotest porte B : 14 contrôles passés")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--autotest"]:
        autotest()
        sys.exit()
    if not a or a[0].startswith("-"):
        sys.exit(__doc__)
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    defauts = 0
    for ok, texte in controles(a[0], opt("--format") or "9:16", opt("--projet"), float(opt("--carte") or CARTE)):
        print(("OK        " if ok else "À REVOIR  ") + texte)
        defauts += not ok
    print("PORTE_B_OK" if not defauts else f"PORTE_B_A_REVOIR {defauts}")
    sys.exit(1 if defauts else 0)
