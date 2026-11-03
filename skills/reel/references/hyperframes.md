# HyperFrames : installer, créer, contrôler, rendre

HyperFrames transforme une composition HTML animée par GSAP en MP4 (licence Apache 2.0, par HeyGen). Les commandes ci-dessous ont été lancées sur la version 0.8.167, fixée à chaque `npx` : une mise à jour du moteur ne change jamais un rendu sans qu'on l'ait décidé.

## 1. Ce qu'il faut avant

```bash
node --version          # 22 ou plus
ffmpeg -version | head -1
npx --yes hyperframes@0.8.167 doctor
```

`doctor` affiche des ✗ pour Docker, Docker running, TTS (Kokoro) et BGM (MusicGen), puis « Some checks failed », et sort avec le code 0 : ces quatre lignes sont facultatives ici (la voix vient d'ElevenLabs, la musique de `son.py`). Le reste doit être ✓. Une connexion est nécessaire au premier rendu (GSAP et les polices sont téléchargés puis gardés en cache).

## 2. Les skills de HyperFrames

Ils apprennent à Claude le contrat de composition, les effets et la ligne de commande. Une fois par machine :

```bash
npx --yes hyperframes@0.8.167 skills
npx --yes hyperframes@0.8.167 skills check
```

Cette commande écrit dans le dossier des skills de chaque agent installé : c'est son rôle, on la lance en le sachant.

## 3. Créer le projet, puis écrire `BRIEF.md` en premier

```bash
HYPERFRAMES_SKIP_SKILLS=1 DO_NOT_TRACK=1 npx --yes hyperframes@0.8.167 init mon-reel --resolution portrait --non-interactive
cd mon-reel
```

**Toujours `HYPERFRAMES_SKIP_SKILLS=1` devant `init`** : sans elle, `init` clone le dépôt de HyperFrames et réinstalle ses skills dans les dossiers de configuration de chaque agent de la machine, hors du projet. L'option `--skip-skills` est ignorée en 0.8.167 ; seule la variable l'empêche. `DO_NOT_TRACK=1` coupe la télémétrie anonyme.

`init` refuse un dossier non vide : `BRIEF.md` s'écrit après, dans le dossier créé, avant toute autre action. Trouvant ce fichier, HyperFrames ne pose aucune question.

| Champ de `BRIEF.md` | Valeur pour un reel |
|---|---|
| `workflow` | `faceless-explainer` (voix et motion), `product-launch-video` (une URL à montrer), `talking-head-recut` (face caméra), sinon `general-video` |
| `flow` | `automation` |
| `storyboard` | `yes` |
| `message` | la phrase unique du reel (la promesse, pas le hook) |
| `destination`, `aspect`, `language`, `length` | `reels`, `1080x1920` (ou `1080x1350`, `1080x1080`, `1920x1080`), `fr`, la durée de la voix plus la carte de fin |
| Corps | l'intention, les fichiers (captures, `voix/voix.wav`, `voix/align.json`), le storyboard ligne par ligne, la charte (couleurs, polices), les zones de sécurité |

## 4. Le contrat de la composition

| Règle | Raison |
|---|---|
| La racine porte `data-composition-id`, `data-width`, `data-height`, `data-duration` | le moteur y lit la durée et le format |
| Une seule timeline GSAP en pause, rangée dans `window.__timelines["<id>"]` | le moteur la fait avancer image par image |
| Une scène = un élément `class="clip"` avec `data-start`, `data-duration`, `data-track-index` | il l'affiche et la masque aux bons temps |
| Jamais d'animation de `autoAlpha` ni de `visibility` sur un `.clip` | le moteur gère sa visibilité : animer les éléments intérieurs |
| Aucun `Math.random` sans graine, ni `Date.now`, ni transition CSS | le rendu doit être identique à chaque passage |
| Les mouvements par `transform`, jamais par `width`, `height`, `top`, `left` | sinon, saccades et avertissements |
| La timeline se construit au chargement, d'un bloc | une timeline construite plus tard manque au rendu |
| Une police de la liste de HyperFrames (Inter), ou un `<link>` Google Fonts, ou un `@font-face` avec son fichier | `lint` refuse une famille sans fichier |
| `html, body` en `100vw` et `100vh`, les zones en variables CSS réglées par `[data-format]` | la même composition se décline en quatre formats (`scripts/formats.py`, `references/ecran.md`, section 1) |
| Une scène 3D : three.js 0.181.2 et son contrat (`references/ecran.md`, section 5) | elle se dessine depuis le temps de HyperFrames, jamais depuis l'horloge |

La voix finale ne va pas dans la composition : on rend la vidéo muette, et `son.py` pose la voix, la musique et les bruitages. Les temps des scènes et des sous-titres viennent de `voix/align.json`.

## 5. Quatre images fixes avant le rendu

```bash
npx --yes hyperframes@0.8.167 snapshot --at 0,8.5,24,41 --no-end --describe false -o snapshots
```

Les temps : le hook, une preuve, le moment fort, la carte de fin. `--describe false` garde les images sur la machine (sinon une analyse par un service externe se lance quand une clé existe). Regarde les images : le hook lisible à l'image 0, le texte dans la zone, une seule couleur d'accent.

## 6. Contrôler, puis rendre

```bash
npx --yes hyperframes@0.8.167 lint
npx --yes hyperframes@0.8.167 check
npx --yes hyperframes@0.8.167 render -o renders/reel.mp4 -f 30 -q delivery --format mp4 --strict
```

Seuil : 0 erreur, 0 débordement, contraste valide.

**Le rendu premium, 60 images par seconde**, à côté du 30 par défaut :

```bash
npx --yes hyperframes@0.8.167 render -o renders/reel-60.mp4 -f 60 -q delivery --video-bitrate 20M --format mp4 --strict
```

| Sur le reel d'essai de 10 s (scène 3D, 9:16) | 30 i/s, `-q delivery` | 60 i/s, `--video-bitrate 20M` |
|---|---|---|
| Débit vidéo | 7,6 Mbit/s | 19,0 Mbit/s |
| Fichier, son compris | 9,8 Mo | 24,0 Mo |
| Temps de rendu sur un Mac | 14,8 s | 25,8 s |

Le 60 sert quand ça bouge vite (une caméra 3D, un défilement, un geste) : le mouvement reste fluide et la plateforme reçoit une source plus riche à recompresser. Sinon, 30. `son.py` pose le son sans réencoder la vidéo, la cadence et le débit restent ; `verifier.py --ips 60` vérifie la cadence choisie.

Chaque format se rend dans son propre dossier : `python3 scripts/formats.py mon-reel 4:5 1:1 16:9`, puis la même commande `render` dans `mon-reel-4x5/`, `mon-reel-1x1/` et `mon-reel-16x9/`.

Le rendu se lance au premier plan ou en tâche suivie par l'outil, jamais avec `&` dans un shell qui se ferme : il mourrait avec lui. On lit le code de sortie avant de passer au son.

## 7. Erreurs payées

| Erreur | Parade |
|---|---|
| Animer le `.clip` lui-même en opacité | animer un `div` intérieur |
| Un `fromTo` posé tard sur un objet visible avant | `immediateRender: false`, sinon l'objet est caché dès l'image 0 |
| Un `transform` en CSS animé aussi par GSAP | laisser GSAP le posséder (`gsap.set` au chargement) |
| Un petit objet animé sur une image immobile | un mouvement large et lent (poussée, dérive), puis la mesure des images figées |
| Le dossier de travail `.hyperframes/` laissé dans un dépôt | l'ignorer : il contient des chemins de la machine |

## 8. Jamais sans l'accord de la personne

`publish` (envoie le projet sur un service externe), `cloud`, `lambda`, `cloudrun` (rendus payants sur un compte tiers), `auth` (connexion à un compte). Un reel se rend en local.
