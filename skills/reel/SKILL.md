---
name: reel
description: À charger pour faire un reel, un TikTok ou un short fini, d'un site, d'une appli, d'une idée ou de ta vidéo face caméra, jusqu'au MP4 vérifié. Script écrit pour être dit, voix ElevenLabs v3, vraies captures, scène 3D, son à -14 LUFS ; en 9:16, 4:5, 1:1 ou 16:9, à 30 ou 60 images par seconde. Douze styles, un catalogue d'effets, seize contrôles et un relecteur à part avant de montrer le film.
---

# reel

Ce skill fait un reel fini : le format et l'objectif choisis d'abord, la structure qui va avec, un script écrit pour être dit, une voix qui sonne humaine, de vraies captures, la musique, puis un MP4 vérifié par des mesures, en 9:16 (1080 x 1920) par défaut. Il est né d'un test : un skill gratuit montait des reels avec la voix robot de l'ordinateur, sans musique deux fois sur trois. Chaque règle ci-dessous corrige un défaut vu.

## Ce qu'il te faut

| Pour | Il faut | Vérifier |
|---|---|---|
| le montage | Node 22 ou plus, ffmpeg, python3, et les skills HyperFrames | `node --version`, `ffmpeg -version`, `npx --yes hyperframes@0.8.167 skills check` |
| la voix | une clé ElevenLabs dans `ELEVENLABS_API_KEY` ; sans clé, la personne s'enregistre (`references/voix.md`, section 6) | `python3 scripts/voix.py --voix-dispo` |
| la vérification | la transcription de HyperFrames ; Parakeet, plus juste, une fois : `npx --yes hyperframes@0.8.167 models install parakeet` | `python3 scripts/verifier.py --autotest` |

Les scripts sont dans le dossier de ce skill (`scripts/`) ; lance-les par leur chemin complet.

## Ce qu'il sait faire en plus (0.2)

Chacune de ces quatre choses a été rendue et mesurée le 02/11/2026 avant d'être écrite ici.

- **Le même reel en quatre formats** : 9:16 (1080 x 1920) pour les Reels et TikTok, 4:5 (1080 x 1350) et 1:1 (1080 x 1080) pour le fil, 16:9 (1920 x 1080) pour YouTube ou LinkedIn sur ordinateur. Tu écris la composition une fois, `scripts/formats.py` en fait une copie par format, chaque format a ses zones de texte et ses tailles (`references/ecran.md`, section 1).
- **Un rendu premium à 60 images par seconde**, à débit plus haut (20 Mbit/s), à côté du 30 par défaut : pour une caméra 3D ou un mouvement rapide (`references/hyperframes.md`, section 6).
- **Ta vidéo face caméra, montée** : tu déposes ta prise, le kit coupe les blancs et le raté sur l'énergie de ta voix, cale les sous-titres sur ta voix montée et pose les effets sur ta prise (`scripts/prise.py`, `references/face-camera.md`).
- **Une vraie scène 3D** : des objets en volume, une lumière, une caméra qui bouge, rendus image par image par three.js 0.181.2 dans HyperFrames, sans modèle vidéo IA (`modeles/scene-3d.html`, `references/ecran.md`, section 5).

## La méthode (0.3)

- **Douze styles**, choisis selon ce que la vidéo explique, chacun avec sa barre mesurable (`references/styles.md`).
- **Un catalogue d'effets** : chaque effet montre une information, avec sa fabrication et son garde-fou ; le storyboard les nomme par leur id (`references/effets.md`), et ils suivent les règles communes à toute vidéo (`references/regles-de-scene.md`).
- **Seize contrôles et un relecteur à part** avant de montrer le film : `verifier.py` lance ceux qu'une commande tranche, dont la note de mouvement de chaque seconde ; les autres se lisent sur la planche ; puis un Claude neuf, qui n'a pas fabriqué la vidéo, la relit (`references/controles.md`).
- **Des règles mesurées** : des études, des sources datées et plus de 2 000 vidéos relevées et mesurées (`references/sources.md`).

## Les règles qui ne bougent pas

1. **Rien d'inventé.** Chaque fait vient de la source lue (le site, l'appli, la personne). Un chiffre que tu ne peux pas vérifier ne va ni à la voix ni à l'écran.
2. **Ce qu'on dit, on le montre.** Chaque phrase qui parle du produit a sa vraie capture, au moment où elle est dite. Jamais une fausse interface recréée.
3. **Jamais la voix intégrée de l'ordinateur** (`say`, synthèse du système) : elle rate les noms et le mot à commenter. Voix ElevenLabs v3 par scène (`scripts/voix.py`), ou la personne qui s'enregistre. Jamais un clone de voix sans qu'on te le demande.
4. **La durée se tient en coupant du texte, jamais en accélérant la voix.**
5. **Ne fouille pas l'ordinateur** : ni clé, ni fichier hors du dossier du projet. Une clé ElevenLabs dans l'environnement vaut accord pour la voix du reel : annonce le nombre de caractères avant de lancer.
6. **Un seul mot à commenter**, identique à la voix, à l'écran et dans la légende. Dis que la réponse automatique est à brancher avant de publier : sans elle, personne ne reçoit rien.
7. **Rien n'est publié.** Tu livres le MP4, la légende et le message privé ; la publication reste à la personne.

## L'ordre de marche

1. **Format et objectif** (`references/structures.md`). Pose 4 questions au plus, chacune avec ta réponse recommandée : le format, l'objectif, le mot à commenter, la voix. Si personne ne répond (mode non interactif), prends tes recommandations et écris-le en tête du compte rendu. Le format d'image est 9:16 ; 4:5, 1:1 ou 16:9 seulement si la personne les demande, en plus ou à la place. La cadence est 30 ; 60 si elle demande un rendu premium.
2. **La source.** Lis le site ou l'appli. Relève chaque fait avec l'endroit où tu l'as lu. Les vraies captures : `npx --yes hyperframes@0.8.167 capture <url> -o capture --skip-vision`, ou les enregistrements d'écran de la personne. Si elle donne sa vidéo face caméra, c'est elle la source et la voix : `references/face-camera.md`.
3. **Le hook** (`references/hooks.md`) : 10 candidats, notés sur 16, 12 au moins pour le garder.
4. **Le script, écrit pour être dit** (`references/voix.md`, sections 1 et 2). La durée se calcule : environ 150 mots par minute.
5. **Le storyboard** (`modeles/storyboard.md`) : choisis d'abord le style (`references/styles.md`) ; puis une ligne par phrase, avec la voix, ce qu'on voit, l'effet nommé par son id (`references/effets.md` : un effet montre une information, sinon il sort) et le son. Puis 4 images fixes (`references/hyperframes.md`, section 5). Montre-les et attends le go. Sans personne pour répondre : continue, et écris « storyboard non validé » en tête du compte rendu.
6. **La voix** : `scenes.json` (modèle `modeles/scenes.json`), puis `python3 scripts/voix.py scenes.json -o voix/`. `VOIX_A_RACCOURCIR` : raccourcis la phrase signalée et relance, le cache ne refacture pas les autres scènes. Avec une prise face caméra : `python3 scripts/prise.py couper prise.mp4`, garde les bons passages (`--garder`), puis `python3 scripts/prise.py monter prise.mp4 coupes.json -o voix/` jusqu'à `PRISE_OK`. Dans les deux cas : `voix/voix.wav`, `voix/align.json` et `voix/sous-titres.json`.
7. **Le montage HyperFrames** (`references/hyperframes.md`, `references/ecran.md`). La durée du film = la voix plus la carte de fin. Les sous-titres sont ceux de `voix/sous-titres.json`, recopiés dans la balise `<script type="application/json" id="sous-titres">` de la composition. Une scène 3D part de `modeles/scene-3d.html`. Pour d'autres formats : `python3 scripts/formats.py mon-reel 4:5 1:1 16:9`, puis un rendu par dossier. Rendu : `-f 30` par défaut, `-f 60 --video-bitrate 20M` pour le premium.
8. **Le son** : `python3 scripts/son.py --video renders/reel.mp4 --voix voix/voix.wav --align voix/align.json -o final.mp4` (`references/son.md`).
9. **La vérification** : `python3 scripts/verifier.py final.mp4 --align voix/align.json --mot <mot> --mots "<noms et chiffres dits>" --sous-titres index.html --voix voix/voix.wav --projet .` jusqu'à `VERIF_OK`, avec `--format 4:5` (ou `1:1`, `16:9`) et `--ips 60` quand ils ont été choisis, et `--absents "<mots du raté>"` pour une prise face caméra. Chaque format se vérifie. La note de mouvement signale chaque seconde molle : reprends-la (mouvement plus large, scène plus courte), sauf une respiration, une chute ou la carte de fin écrite dans le storyboard. Puis regarde la planche d'images (`references/verifier.md`) : une mesure ne voit pas un texte coupé. Ensuite, les contrôles de `references/controles.md` que la mesure ne tranche pas, et **un relecteur à part** : un Claude neuf, qui n'a pas fabriqué la vidéo, reçoit le storyboard, la planche et le rapport, avec le prompt de `references/controles.md` (section 3). Vérifie chacune de ses trouvailles avant de l'appliquer. Deux tours de reprise au plus : au-delà, livre le film avec la liste de ce qui reste à reprendre.
10. **Livrer** : le MP4, la légende (la valeur en première ligne, un bloc par idée, le mot à commenter seul en tête de son bloc, les hashtags à la fin), le message privé prêt à envoyer, et ce qui n'a pas été vérifié.

## Les fiches

| Fichier | Contenu |
|---|---|
| `references/structures.md` | les cinq formats, les cinq objectifs, la structure de chaque format, le choix par défaut |
| `references/hooks.md` | le hook : trois couches, la grille sur 16, les formules |
| `references/voix.md` | écrire pour être dit, la durée, les scènes, ElevenLabs, sans clé, pourquoi ces réglages |
| `references/ecran.md` | zones et tailles des quatre formats, sous-titres, vraies captures, cadre de téléphone, scène 3D, carte de fin |
| `references/face-camera.md` | ta prise face caméra : filmer, couper sur l'énergie, voix montée, sous-titres, effets, vérifier |
| `references/son.md` | musique, bruitages, niveaux, droits |
| `references/hyperframes.md` | installer, créer le projet, images fixes, contrôler, rendre en 30 ou 60 images par seconde, erreurs payées |
| `references/verifier.md` | ce que mesure `verifier.py`, la planche d'images, ce qui reste à l'œil |
| `references/styles.md` | les douze styles, le choix selon ce que la vidéo explique, comment juger un style |
| `references/effets.md` | le catalogue d'effets : l'information que chacun montre, sa fabrication, son garde-fou |
| `references/regles-de-scene.md` | les règles communes à toute vidéo : cadre, temps, couleur, mouvement, texte, son, preuve, waou |
| `references/controles.md` | les seize contrôles du rendu, le relecteur à part et son prompt |
| `references/sources.md` | d'où viennent les règles : études, sources datées, relevés de plus de 2 000 vidéos |
| `modeles/` | `scenes.json`, `storyboard.md`, `charte.md` (ta marque : couleurs, polices, ton), `scene-3d.html` (la scène 3D éprouvée, à adapter) |
| `scripts/` | `voix.py` (voix et sous-titres), `prise.py` (ta prise face caméra), `formats.py` (4:5, 1:1, 16:9), `son.py`, `verifier.py`, `porte_b.py` (image 0, zones, note de mouvement, déterminisme, tirets) |
