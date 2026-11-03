# L'écran : ce qu'on voit, où, et quand

## 1. Zones et tailles, format par format

Le même reel se décline en quatre formats. Le 9:16 reste le format par défaut ; les autres se demandent.

| Format | Taille | Pour | Tout texte entre | Sous-titres entre | Titre | Sous-titres |
|---|---|---|---|---|---|---|
| 9:16 | 1080 x 1920 | Reels, TikTok, Shorts | x = 80 et 930, y = 170 et 1500 (les boutons du réseau couvrent le bas et la droite) | y = 1150 et 1350 | 90 px et plus | 64 à 80 px |
| 4:5 | 1080 x 1350 | le fil d'Instagram, Facebook, LinkedIn sur téléphone | x = 108 et 972, y = 108 et 1242 (10 % de marge ; la vignette 3:4 du profil rogne 34 px de chaque côté, déjà dedans) | y = 1010 et 1180 | 90 px et plus | 64 à 76 px |
| 1:1 | 1080 x 1080 | le fil, un carrousel vidéo | x = 108 et 972, y = 108 et 972 | y = 800 et 950 | 80 px et plus | 60 à 72 px |
| 16:9 | 1920 x 1080 | YouTube, LinkedIn sur ordinateur, une présentation | x = 96 et 1824, y = 54 et 972 (5 % de marge, la bande basse laissée aux commandes du lecteur) | y = 830 et 960 | 100 px et plus | 64 à 80 px |

Sources des marges : la marge de 10 % des annonces du fil d'Instagram (pas de chiffre officiel pour une publication ordinaire) et la zone graphique de 5 % de la télévision (EBU R 095) pour le 16:9 ; la bande basse du 16:9 vient des commandes du lecteur et des sous-titres automatiques de YouTube, qui n'en donne pas la hauteur. Regarde le rendu dans l'appli avant de publier.

| Élément, tous formats | Règle |
|---|---|
| Titre et hook | 8 mots au plus à la fois, présent à 0,3 s |
| Texte d'appui | 48 à 56 px |
| Sous-titres | une ligne, 18 caractères au plus à 76 px, 3 mots de préférence, en gras avec un contour, jamais sur un visage |
| Source et date | 22 px et plus, sous l'élément qu'elles prouvent |
| Contraste | 4,5 pour 1 au moins entre le texte et son fond (3 pour 1 pour un titre de 90 px et plus) |
| Couleurs | celles de ta charte (`modeles/charte.md`) : une seule couleur d'accent par image |

**Décliner le même reel.** Écris la composition une fois, en 9:16, avec `html, body` en `100vw` et `100vh` (jamais une taille en pixels) et ses zones en variables CSS ; puis une règle par format sur la racine (`#root[data-format="4:5"] { --st-y: 1010px; ... }`). `python3 scripts/formats.py mon-reel 4:5 1:1 16:9` écrit `mon-reel-4x5/`, `mon-reel-1x1/` et `mon-reel-16x9/` : seul `index.html` change (taille de la racine, `data-format`, balise viewport), le reste est lié au projet. Rends chaque dossier, pose le son sur chacun, et vérifie chacun avec `verifier.py --format 4:5` (ou `1:1`, `16:9`). Une scène 3D prend son cadrage du format (`modeles/scene-3d.html`).

## 2. Le temps

- Une image nouvelle toutes les 2 s au plus ; aucune image figée plus d'une seconde, sauf la carte de fin.
- Les sous-titres se calent sur les temps des mots de `voix/align.json`, jamais sur une horloge.
- Un mot mis en grand à l'écran apparaît quand il est dit, puis disparaît ; il ne se répète pas dans les sous-titres.
- La coupe tombe sur le mot qui annonce l'image, environ 0,3 s avant lui.

## 3. Les vraies captures

| Source | Commande ou méthode |
|---|---|
| Un site | `npx --yes hyperframes@0.8.167 capture <url> -o capture --skip-vision` : captures de la page et images du site |
| Une appli | l'enregistrement d'écran du téléphone, fait par la personne, avec un profil fictif |
| Une page précise | une capture plein écran, datée dans le storyboard |

Une capture n'est jamais retouchée ni recréée en code. Les données personnelles sont masquées avant l'enregistrement, jamais floutées après.

**La capture qui arrive en perspective** : elle entre inclinée d'environ 25 degrés, se redresse pendant une poussée lente et finit à plat, lisible avant la fin du mouvement.

**Le détail qui compte** : agrandi de 200 à 300 % sur la zone utile, tenu 0,8 s, puis retour au plan large.

## 4. Le cadre de téléphone

- Un vrai modèle de téléphone : le bloc `vfx-iphone-device` du catalogue de HyperFrames (`npx --yes hyperframes@0.8.167 add vfx-iphone-device`), qui affiche la capture en direct sur son écran. Jamais un rectangle arrondi dessiné.
- Le téléphone occupe 50 à 75 % de la hauteur de l'image quand il porte la preuve.
- L'écran montre la vraie capture ou l'enregistrement de l'appli, jamais une maquette.

## 5. La scène 3D

Une vraie scène en volume : des objets, une lumière, une caméra qui avance ou tourne, rendus image par image par three.js dans HyperFrames. Pas de modèle vidéo IA : tout est calculé, et le même rendu sort deux fois pareil.

| Règle | Pourquoi |
|---|---|
| three.js 0.181.2, chargé par `https://cdn.jsdelivr.net/npm/three@0.181.2/+esm`, version écrite en entier | une mise à jour de three.js ne change jamais un rendu sans qu'on l'ait décidé |
| La scène se dessine depuis le temps de HyperFrames : `window.addEventListener("hf-seek", e => renderAt(e.detail.time))` | l'image d'un instant ne dépend que de cet instant ; jamais `requestAnimationFrame`, jamais l'horloge |
| La caméra et chaque mouvement sont des fonctions du temps (`renderAt(t)`) | on peut rendre n'importe quelle image dans n'importe quel ordre |
| Le hasard a une graine fixe (les 623 produits du modèle) | la même scène à chaque rendu |
| La taille du rendu vient de la racine (`data-width`, `data-height`), l'angle de la caméra du format | la scène se décline en 4:5, 1:1 et 16:9 sans rien réécrire |
| `window.__hf.buildReady["scene-3d"]`, une promesse posée dans un script classique et tenue après la première image | le rendu attend que la scène soit dessinée |
| Le texte de la scène (une étiquette, une marque) ne passe jamais sous un texte de l'écran | sur la carte de fin du modèle, un fondu d'encre couvre le haut, la brique de lait descend dans la moitié basse |
| Le titre se pose sur du vide, jamais sur les objets | vu en 1:1 et en 16:9 : les rayons montent jusqu'en haut de l'image et le titre tombait sur les produits ; le modèle le resserre (deux lignes en 1:1, une ligne centrée en 16:9) sur un fondu d'encre qui part avec lui |
| La caméra reste dans le décor | essayé : un arc trop large entrait dans le rayon ; le modèle le borne à 1,1 m de l'axe |

Le modèle `modeles/scene-3d.html` est éprouvé : un rayon de supermarché en volume (deux rayonnages, 623 produits, un frigo à lait au fond), une caméra qui traverse l'allée puis tourne autour de la brique, le titre, les sous-titres et la carte de fin ; rendu en 9:16, 4:5, 1:1, 16:9 et à 60 images par seconde. Copie-le, remplace les objets, les temps et les sous-titres, garde le contrat ci-dessus. `npx --yes hyperframes@0.8.167 lint` doit rendre 0 erreur, puis regarde quatre images (`snapshot`) avant le rendu.

## 6. Ce qu'on évite

- Le flou, sous toutes ses formes : on recadre ou on remplace l'image.
- Les sous-titres qui sautent mot par mot, un zoom à chaque phrase, les emoji dans les titres.
- Une boîte plate posée sur l'image : un texte se pose dans la scène (derrière la personne, sur la capture en perspective).
- Un logo plein écran ou un fondu au noir à l'image 0.

## 7. La carte de fin

1,5 à 2 s. Le mot à commenter en capitales, ce qu'on reçoit en une ligne, le nom du compte. Elle peut tenir immobile : c'est la seule.
