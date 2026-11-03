# Les styles d'illustration : la nature des images, proposée selon le contenu et la charte

Ce fichier sert à choisir comment on illustre un reel (vraies captures, objet seul en studio, collage d'archives à la Vox, isométrique, 3D, formes à plat, données…), à poser la question à la personne avec une recommandation tirée de ce que la vidéo explique et de sa charte, puis à trouver des images et des vidéos libres de droit avec leur licence notée.

Trois choix, trois fichiers : le style vidéo donne le rythme et la mise en page (`styles.md`) ; le style d'illustration donne la nature des images (ce fichier) ; la charte donne les couleurs, les polices et les interdits (`../modeles/charte.md`). En cas de conflit, `regles-de-scene.md` gagne.

## 1. Les règles

| # | Règle | Raison |
|---|---|---|
| 1 | **Ce qui se capture se capture.** Un outil, un site, un résultat, un document se montrent par leur vraie capture (`capture-reelle`), quel que soit le style choisi ; le style d'illustration habille tout le reste | une illustration ne prouve rien |
| 2 | **Un style dominant par reel**, un deuxième au plus quand une ligne l'exige ; la capture ne compte pas | trois styles font un patchwork |
| 3 | **Le contenu propose, la charte départage, la personne choisit** (sections 3 et 4). Un interdit de la charte retire le style de la liste | c'est sa marque et son public |
| 4 | **Chaque style se dessine aux variables de la charte** (`--fond`, `--texte`, `--accent`, `--police`), jamais aux couleurs d'un exemple ; l'accent marque une seule chose à la fois | le même reel doit pouvoir changer de marque |
| 5 | **Chaque image a sa source** : capture (adresse et date), banque (`banque.json`, section 5), image générée (son prompt gardé et la mention « Image générée par IA » à l'écran) | ce qu'on ne peut pas sourcer ne passe pas |
| 6 | **Aucun flou**, ni pour décorer ni pour cacher : on recadre ou on change d'image | un flou se lit comme un raté |
| 7 | **Le statut commande l'usage**, comme pour les effets (`effets.md`, § 1) : un style `à l'essai` s'emploie et se signale à la validation | on sait ce qui a déjà tenu sur un vrai rendu |

## 2. Les douze styles

Le statut d'un style suit ses effets et ce qui a déjà été rendu : `éprouvé` quand son effet principal l'est dans `effets.md` ; sinon `à l'essai`.

| Style (id) | À quoi ça ressemble | Fabrication dans HyperFrames | Effets (`effets.md`) | Garde-fou | Statut |
|---|---|---|---|---|---|
| `capture-reelle` | la vraie page, le vrai écran, le vrai document, cadrés sur le détail qui compte | `npx --yes hyperframes@0.8.167 capture <url>`, cadre de téléphone, zoom sur le détail (`ecran.md`) | `ui-result`, `zoom-screen`, `spotlight-dim`, `marker-circle`, `split-source` | datée ; jamais refaite ni retouchée | éprouvé |
| `ui-flottante` | l'interface découpée en cartes qui flottent à des profondeurs différentes, en perspective, avec une ombre portée nette | la vraie capture recadrée en cartes (`object-position`), posées en couches (`perspective`, `translateZ`), ombre décalée sans flou | `ui-floating`, `ui-floating-v2`, `ui-prompt`, `ui-tilt` | chaque carte est un morceau de la vraie capture, jamais une interface inventée | éprouvé |
| `scene-3d` | des objets en volume, une lumière, une caméra qui tourne autour de ce qui change | `../modeles/scene-3d.html` (three.js 0.181.2), objets simples teintés par la charte, caméra par la timeline | `depth-object-pbr`, `camera-reframe`, `depth-photo` | la 3D montre un état qui change, jamais un décor ; 60 i/s si la caméra va vite | éprouvé |
| `objet-studio` | un seul objet réel par nom concret, en lumière de studio, posé ou en lévitation avec son ombre de contact, sur une carte d'une teinte de la charte : le nom dit, montré par la chose | une photo de banque détourée (`scripts/banque.py`, puis `npx --yes hyperframes@0.8.167 remove-background`) ou un modèle 3D libre (Poly Haven, CC0) rendu dans `../modeles/scene-3d.html` ; ombre de contact en `radial-gradient` ; entrée par l'échelle (0,92 à 1), le fondu et l'ombre qui naît | `editorial-card`, `word-icon`, `depth-photo` | un objet réel, photographié ou modélisé, jamais généré par IA (sinon `scene-generee-etiquetee`, avec sa mention) ; un objet et un nom par carte ; aucun logo ni modèle du commerce identifiable ; jamais en flou | à l'essai |
| `formes-flat` | des formes pleines et des icônes d'une seule famille qui entrent, se transforment et s'assemblent, à plat | SVG et CSS, formes aux couleurs de la charte, entrées élastiques (`back.out`), une icône qui devient la suivante | `split-illustration`, `checklist-sync`, `comparison-split`, `knockout-tiles` | une famille d'icônes (même trait) ; un objet focal par plan | éprouvé |
| `donnees-vivantes` | le chiffre en grand, les barres qui poussent, la courbe qui se trace, la carte qui se colore, la source en pied | SVG : barres depuis zéro, courbe en `stroke-dashoffset`, chiffre qui compte ; fond de carte libre (Natural Earth, domaine public) | `stat-card`, `count-up`, `bar-grow`, `chart-line`, `data-stack` | échelle depuis zéro ; source et date à l'écran ; une donnée clé par plan | éprouvé |
| `collage-vox` | le collage d'un explainer à la Vox : archives et photos détourées sur papier, trame d'imprimerie, mot surligné sur le vrai document, cercle et flèche tracés à la main, cadres qui glissent | photos de banque ou d'archives (section 5) détourées (`npx --yes hyperframes@0.8.167 remove-background`) ; papier en CSS (bruit SVG `feTurbulence` à faible opacité) ; trame en `radial-gradient` ; surligneur = bande `--accent` en `scaleX` de 0 à 1 sous le mot, en `mix-blend-mode: multiply` ; trait à la main en SVG `stroke-dashoffset` ; ombres dures | `paper-cut`, `marker-circle`, `split-source`, `headline-wall`, `pointer-callout` | une archive est vraie, datée et sourcée à l'écran, jamais générée ; le surligneur tombe sur le mot quand il est dit ; on ne détourne pas le sens d'une photo de personne réelle | à l'essai |
| `iso-systeme` | des blocs en vue isométrique, des étages, des flux de points qui circulent d'une pièce à l'autre | un plan en CSS 3D (`rotateX(60deg) rotateZ(-45deg)`) ou en SVG sur grille isométrique ; trois faces par bloc en `color-mix()` de `--fond` (dessus clair, côtés sombres) ; le flux en `--accent` | `dot-thread`, `cause-arrow` (les effets isométriques du catalogue sont `à juger` : les refaire aux couleurs de la charte et les juger avant) | seulement quand l'espace porte l'information (`regles-de-scene.md`, § 12) ; cinq blocs au plus ; étiquettes de face, hors du plan | à l'essai |
| `typo-cinetique` | des mots géants qui prennent du poids, s'empilent, se barrent, se remplacent | la police de la charte (graisse variable si elle en a : `font-variation-settings`), masques qui révèlent | `type-wall`, `weight-morph`, `word-swap`, `strike-replace`, `caption-keyword` | un mot en grand apparaît quand il est dit et sort des sous-titres | à l'essai |
| `banque-teintee` | de vraies photos et vidéos d'une situation vécue, passées dans deux tons de la charte, cadrées serré, grain fin | `scripts/banque.py` (section 5) ; duotone par filtre SVG (`feColorMatrix`) entre deux tons de la charte, de la photo comme de la vidéo | `broll-cutaway`, `depth-photo`, `camera-reframe`, `caption-story` | jamais une preuve ; dans le sujet dit, au mot près ; aucun logo ; aucune personne identifiable sous un jour négatif ni en caution de ton produit ; l'accent ne teinte pas la photo | à l'essai |
| `dessin-trace` | un dessin au trait qui se trace sous les yeux, comme au tableau : feutre sur fond clair ou craie sur fond sombre | SVG en traits (`stroke-dasharray`, `stroke-dashoffset`), trait irrégulier par un léger `feDisplacementMap` (pas de flou) | `cause-arrow`, `dot-thread`, `before-after-wipe` | un dessin, une idée ; lisible en vignette ; jamais d'écriture manuscrite illisible | à l'essai |
| `scene-generee-etiquetee` | une image ou un plan symbolique généré par IA, un seul sujet, avec la mention « Image générée par IA » à l'écran | le générateur choisi par la personne ; le plan étalonné dans les tons de la charte ; mention en HTML net, 24 px d'encre au moins, dans les zones de texte (`ecran.md`) | `split-illustration-v2`, `caption-story`, `depth-photo` | jamais une preuve, jamais une personne réelle ; ni texte, ni chiffre, ni logo dessinés par le modèle ; prompt gardé ; l'étiquette IA de la plateforme se coche à la publication ; la charte peut l'interdire | à l'essai |

## 3. La recommandation : le contenu propose, la charte départage

**Étape 1, le contenu.** La ligne de ce que la vidéo explique (mêmes lignes que `styles.md`, § 1) donne trois candidats, dans l'ordre.

| Ce qu'on explique | Recommandé | Puis |
|---|---|---|
| un outil et son résultat | `capture-reelle` | `ui-flottante`, `scene-3d` (un objet physique) |
| un processus, une marche à suivre | `capture-reelle` | `dessin-trace`, `iso-systeme` (plusieurs acteurs) |
| une comparaison, un verdict | `donnees-vivantes` | `formes-flat`, `collage-vox` (deux sources face à face) |
| un chiffre, une étude | `donnees-vivantes` | `collage-vox` (l'étude surlignée), `typo-cinetique` |
| une news, un décryptage, une histoire vraie | `collage-vox` | `capture-reelle` (la source), `banque-teintee` |
| un système, une architecture, un flux | `iso-systeme` | `scene-3d`, `dessin-trace` |
| un concept, une idée abstraite | `formes-flat` | `dessin-trace`, `scene-generee-etiquetee` |
| un produit, un objet, une construction | `scene-3d` | `objet-studio`, `ui-flottante` |
| une annonce, un manifeste, une opinion | `typo-cinetique` | `scene-3d`, `collage-vox` |
| une histoire, une émotion, une situation vécue | `banque-teintee` | `dessin-trace`, `scene-generee-etiquetee` |
| une liste de conseils | `formes-flat` | `typo-cinetique`, `banque-teintee` |
| un conseil ou un avis qui nomme des choses concrètes (des métiers, des objets, des lieux) | `objet-studio` | `formes-flat`, `banque-teintee` |

**Étape 2, la charte.** Relève le fond, l'accent, la police et le ton (`charte.md`, ou la page d'accueil de la personne), puis remonte d'un rang chaque candidat que la charte appelle et descends d'un rang celui qu'elle écarte. Un fond est sombre quand sa luminance relative (celle du contraste WCAG) est sous 0,18.

| La charte | Appelle | Écarte |
|---|---|---|
| fond sombre, accent vif, police géométrique (tech, logiciel, IA) | `scene-3d`, `iso-systeme`, `ui-flottante`, `donnees-vivantes` | `dessin-trace` en feutre sur blanc ; le `collage-vox` y passe en papier sombre |
| fond clair, crème ou papier, police à empattements (média, éditorial, conseil) | `collage-vox`, `objet-studio`, `donnees-vivantes`, `typo-cinetique` | `scene-3d` brillante |
| couleurs franches, ton grand public ou ludique | `formes-flat`, `dessin-trace` | les archives sombres |
| une personne ou un commerce, ton chaleureux (coach, artisan, restaurant) | `banque-teintee`, `capture-reelle`, `dessin-trace` | `iso-systeme` |
| luxe, premium, une seule couleur | `objet-studio`, `scene-3d` (un objet seul), `banque-teintee` en duotone | `formes-flat` chargées |

**Étape 3, les interdits.** Retire tout style que la charte interdit (pas de photo de personne, pas d'image générée, pas d'emoji…) ou que la source ne peut pas nourrir (un `collage-vox` sans archive ni document vrai, une `capture-reelle` sans écran à capturer). Le premier qui reste est la recommandation ; les deux suivants sont les autres choix.

## 4. La question à poser

Elle part dans le message des questions de l'étape 1 du skill (`../SKILL.md`), en mots simples, l'id entre parenthèses :

```text
Le style des images. Je te recommande un collage à la Vox (collage-vox) : des archives et le vrai rapport,
le mot clé surligné quand il est dit. C'est une news avec un document à montrer, et ta charte papier s'y prête.
Autres choix : des données vivantes (les chiffres du rapport qui se construisent) ; les vraies captures seules.
Tu veux les voir ? Je te fais l'image du hook dans les trois styles.
```

- La raison tient en une ligne : ce que la vidéo explique, puis ce que la charte appelle.
- Si la personne veut voir, rends l'image du hook dans chacun des trois styles (une composition par style, une image fixe chacune : `hyperframes.md`, section 5) et montre-les côte à côte : on choisit sur une image, pas sur un mot.
- Sans réponse (mode non interactif), prends la recommandation et écris-la en tête du compte rendu.
- Si le style recommandé prend des images de banque (`banque-teintee`, `collage-vox`) et qu'une clé manque, dis-le dans la même question : la clé gratuite qu'il faudra, et ce qu'on fait sans elle (Openverse seul, ou un autre style) (section 5).
- Le storyboard l'écrit en tête, « Style d'illustration : <id> (+ <id> pour la ligne qui l'exige) », et chaque ligne nomme sa source.

## 5. Les images et les vidéos libres de droit

**L'ordre.** D'abord la vraie capture ou les images de la personne ; puis une banque libre de droit ; une image générée en dernier, étiquetée. Une image de banque n'est jamais la preuve de ce que dit la voix : elle montre une situation, pas un fait.

| Banque | Images | Vidéos | Clé | Licence, relue le 03/11/2026 | Crédit |
|---|---|---|---|---|---|
| Pexels | originales | oui, souvent verticales, jusqu'en 4K | `PEXELS_API_KEY`, gratuite : https://www.pexels.com/api/ | https://www.pexels.com/license/ : usage commercial et modification permis ; interdit de vendre une copie non modifiée, de redistribuer sur une autre banque, de laisser croire qu'une personne ou une marque de l'image soutient ton produit, de montrer une personne identifiable sous un jour offensant, d'en faire une marque | non exigé |
| Pixabay | 1 280 px de haut au plus par l'API : pour un élément, pas pour un plein écran | oui, surtout horizontales, jusqu'en 4K | `PIXABAY_API_KEY`, gratuite : https://pixabay.com/api/docs/ | https://pixabay.com/service/license-summary/ : usage commercial et modification permis ; interdit de diffuser le contenu seul, sans apport créatif ; interdit tout usage trompeur ; une marque reconnaissable sur l'image ne s'emploie pas pour vendre ; l'outil écarte ce que Pixabay marque généré par IA | non exigé |
| Openverse (Wikimedia Commons, Flickr, musées, archives) | oui : les archives du `collage-vox` | non | aucune | l'outil ne garde que CC0, domaine public et CC BY ; ni BY-SA, ni NC, ni ND ; Openverse ne garantit pas la licence : relis la page d'origine avant de garder l'image | exigé pour CC BY : la ligne que donne l'outil, dans la légende |
| Unsplash | à la main, sur le site | non | aucune | https://unsplash.com/license : pas de revente sans apport créatif réel, pas de compilation pour un service concurrent ; son API demande des images liées à leur adresse et un usage non automatisé, donc pas d'outil : la personne télécharge, puis `banque.py noter` | non exigé |

**L'outil** (`scripts/banque.py`, sans dépendance) :

```bash
python3 scripts/banque.py chercher "typewriter close up" --type video --vertical --apercus apercus/
python3 scripts/banque.py prendre pexels:video:27451031 -o medias/
python3 scripts/banque.py noter medias/photo.jpg --banque unsplash --page <adresse de la photo> --auteur "<nom affiché>"
python3 scripts/banque.py controler medias/
```

- Cherche en anglais, avec des mots concrets : l'objet, le geste, le lieu (« hands typing old keyboard », pas « productivité »). Regarde les aperçus avant de prendre : on choisit, on ne prend pas le premier.
- `prendre` télécharge la plus petite version qui couvre 1080 px, mesure le fichier, et note dans `medias/banque.json` la banque, la page, l'auteur, la licence, le crédit exigé et la date. `controler` rend `BANQUE_OK` quand chaque image ou vidéo du dossier y est notée : il passe avant la vérification du film, et donne les crédits à mettre dans la légende.
- **Les clés, Claude les demande.** Openverse marche sans clé. Pexels et Pixabay en demandent une, gratuite : si le film en a besoin et qu'elle manque (l'outil le dit), demande-la à la personne, avec le lien pour la créer (https://www.pexels.com/api/, https://pixabay.com/api/docs/) et la ligne à ajouter elle-même dans son terminal, ou dans `~/.zshrc` pour la garder : `export PEXELS_API_KEY=<sa clé>`. Ne la cherche jamais dans ses fichiers, ne l'écris dans aucun fichier et ne l'affiche pas. Si elle la colle dans la conversation, passe-la seulement à la commande (`PEXELS_API_KEY=<sa clé> python3 scripts/banque.py …`) et dis-lui qu'elle reste dans l'historique de la conversation. L'outil ne l'affiche ni ne l'écrit, pas même dans `banque.json`.

**Le traitement.** Une image de banque prend la charte : recadrage serré sur un seul sujet, duotone entre deux tons de la charte ou étalonnage vers son fond, grain fin ; jamais l'accent sur la photo (il reste à l'information). Une vidéo de banque dure de 1,2 à 3 s, entre sur le mot qu'elle illustre et se coupe avant de se répéter.

## 6. Les ressources libres, par style

| Style | Ressource | Licence |
|---|---|---|
| `formes-flat`, `ui-flottante`, `dessin-trace` | icônes Lucide (https://lucide.dev) ou Phosphor (https://phosphoricons.com) : une seule famille par reel, au trait de la charte | ISC ; MIT |
| `scene-3d`, `objet-studio` | Poly Haven (https://polyhaven.com) : éclairages HDRI, matières, modèles | CC0 |
| `donnees-vivantes` | Natural Earth (https://www.naturalearthdata.com) : fonds de carte | domaine public |
| `typo-cinetique` | la police de la charte ; à défaut, Google Fonts (https://fonts.google.com), avec la licence de la police (OFL le plus souvent) | selon la police |
| `collage-vox`, `banque-teintee`, `objet-studio` | les banques de la section 5, par `scripts/banque.py` | selon la banque |
