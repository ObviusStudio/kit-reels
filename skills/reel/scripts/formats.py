"""Le même reel en 4:5, 1:1 ou 16:9, à côté du 9:16 : une copie du projet HyperFrames par format.

Usage :
  python3 formats.py mon-reel 4:5 1:1 16:9     écrit mon-reel-4x5/, mon-reel-1x1/, mon-reel-16x9/ à côté de mon-reel/
  python3 formats.py --autotest

Dans chaque copie, seul index.html change : la taille de la racine (data-width, data-height), son data-format, et la
balise viewport. Les autres fichiers sont des liens vers ceux du projet : une capture ou une voix changée là se voit
ici. La mise en page propre à chaque format s'écrit dans la composition, par des règles [data-format="4:5"] (zones et
tailles : references/ecran.md, section 1). La page doit prendre sa taille de la fenêtre (html, body en 100vw et
100vh), jamais en pixels écrits : sinon la copie garderait la taille du 9:16, et le script refuse.
"""
import os, re, shutil, sys, tempfile

FORMATS = {"9:16": (1080, 1920), "4:5": (1080, 1350), "1:1": (1080, 1080), "16:9": (1920, 1080)}
NON_LIES = {"index.html", "renders", "snapshots", ".hyperframes", "node_modules"}


def redimensionner(html, fmt):
    """index.html à la taille du format : racine, data-format et viewport ; le reste ne bouge pas."""
    l, h = FORMATS[fmt]
    corps = re.search(r"html\s*,\s*body\s*\{[^}]*\}", html)
    if corps and re.search(r"(?:width|height)\s*:\s*\d+px", corps.group(0)):
        raise ValueError("html, body ont une taille en pixels : écris width: 100vw; height: 100vh")
    m = re.search(r"<[^>]*\sdata-composition-id=[^>]*>", html)
    if not m:
        raise ValueError("pas de racine data-composition-id")
    racine = m.group(0)
    for k, v in (("data-width", l), ("data-height", h), ("data-format", fmt)):
        racine = re.sub(rf'\s{k}="[^"]*"', "", racine)
        racine = racine[:-1].rstrip() + f' {k}="{v}">'
    html = html[:m.start()] + racine + html[m.end():]
    html = re.sub(r'(<meta name="viewport" content=")[^"]*"', rf'\g<1>width={l}, height={h}"', html)
    return re.sub(r'(<html[^>]*?)\sdata-resolution="[^"]*"', r"\1", html)      # le préréglage d'init ne vaut plus


def decliner(projet, fmt):
    projet = os.path.abspath(projet.rstrip("/"))
    cible = f"{projet}-{fmt.replace(':', 'x')}"
    html = redimensionner(open(os.path.join(projet, "index.html"), encoding="utf-8").read(), fmt)
    if os.path.exists(cible):
        shutil.rmtree(cible)
    os.makedirs(cible)
    open(os.path.join(cible, "index.html"), "w", encoding="utf-8").write(html)
    for x in os.listdir(projet):
        if x not in NON_LIES:
            os.symlink(os.path.join(projet, x), os.path.join(cible, x))
    l, h = FORMATS[fmt]
    print(f"{os.path.basename(cible)}/ : {l} x {h}, index.html réécrit, {len(os.listdir(cible)) - 1} lien(s)")
    return cible


def autotest():
    page = ('<!doctype html><html lang="fr" data-resolution="portrait"><head><meta name="viewport" content="width=1080, height=1920" />'
            '<style>html, body { width: 100vw; height: 100vh; }</style></head><body>'
            '<div id="root" data-composition-id="main" data-start="0" data-duration="10" data-width="1080" data-height="1920">'
            '</div></body></html>')
    p = redimensionner(page, "16:9")
    assert 'data-width="1920"' in p and 'data-height="1080"' in p and 'data-format="16:9"' in p, p
    assert 'content="width=1920, height=1080"' in p and "data-resolution" not in p and p.count("data-width") == 1, p
    assert redimensionner(p, "4:5").count('data-format="4:5"') == 1                 # une copie se redimensionne encore
    try:
        redimensionner(page.replace("100vw", "1080px"), "1:1")
        raise AssertionError("une page en pixels écrits est acceptée")
    except ValueError:
        pass
    with tempfile.TemporaryDirectory() as d:
        proj = os.path.join(d, "reel")
        os.makedirs(os.path.join(proj, "voix"))
        open(os.path.join(proj, "index.html"), "w").write(page)
        open(os.path.join(proj, "voix", "voix.wav"), "w").write("x")
        c = decliner(proj, "1:1")
        assert os.path.islink(os.path.join(c, "voix")) and open(os.path.join(c, "voix", "voix.wav")).read() == "x"
        assert 'data-height="1080"' in open(os.path.join(c, "index.html")).read()
    print("autotest formats : 6 contrôles passés")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--autotest"]:
        autotest()
        sys.exit()
    if len(a) < 2 or any(f not in FORMATS for f in a[1:]):
        sys.exit(__doc__)
    for f in a[1:]:
        decliner(a[0], f)
