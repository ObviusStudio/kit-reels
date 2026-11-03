# kit-reels

Un reel fini avec Claude Code, et une voix qui sonne humaine. Gratuit, licence MIT.

Tu donnes ton site, ton idée ou ta vidéo face caméra. Claude choisit avec toi le format et l'objectif, écrit un script fait pour être dit, fabrique la voix scène par scène (ou monte ta prise), monte de vraies captures ou une scène 3D, ajoute la musique, puis vérifie le fichier avant de te le rendre.

## Nouveau dans la 0.2

Quatre choses de plus, chacune rendue et mesurée le 02/11/2026 avant d'être écrite ici :

| | Ce que ça fait | Mesuré sur l'essai |
|---|---|---|
| **Quatre formats** | le même reel en 9:16 (1080 x 1920), 4:5 (1080 x 1350), 1:1 (1080 x 1080) et 16:9 (1920 x 1080), chacun avec ses zones de texte et ses tailles | les quatre rendus passent la vérification de leur format |
| **60 images par seconde** | un rendu premium, plus fluide, à 20 Mbit/s, à côté du 30 par défaut | 19,0 Mbit/s contre 7,6 ; 24 Mo contre 9,8 pour 10 s ; un rendu 1,7 fois plus long |
| **Ta vidéo face caméra** | tu déposes ta prise : le kit coupe les blancs et le raté sur l'énergie de ta voix, cale les sous-titres sur ta voix montée et pose les effets sur ta prise (cadrage alterné, titre du hook, mots clés, punch-in) | le raté retiré, 0 blanc de 0,20 s dans la voix montée, sous-titres à 0,14 s au plus du mot dit |
| **Une vraie scène 3D** | des objets en volume, une lumière, une caméra qui avance et tourne, rendus image par image par three.js 0.181.2, sans modèle vidéo IA | un rayon de supermarché, 623 produits, rendu dans les quatre formats et à 60 images par seconde |

La prise face caméra de l'essai est fabriquée (`outils/prise-essai.py` : une silhouette et une voix ElevenLabs) : personne n'a été filmé, et le cadrage sur un vrai visage reste à regarder sur ta prise.

## Nouveau dans la 0.3 : la méthode

| | Ce que ça fait | D'où ça vient |
|---|---|---|
| **Douze styles** | le style se choisit selon ce que la vidéo explique ; chaque style a sa barre mesurable (`references/styles.md`) | des films et des reels de référence, étudiés image par image (`references/sources.md`) |
| **Un catalogue d'effets** | chaque effet montre une information, avec sa fabrication et son garde-fou ; le storyboard les nomme par leur id (`references/effets.md`) | les mêmes relevés, et les règles communes de `references/regles-de-scene.md` |
| **Seize contrôles et un relecteur à part** | avant de te montrer le film, `verifier.py` lance ceux qu'une commande tranche, puis un Claude neuf, qui ne l'a pas fabriqué, le relit (`references/controles.md`) | les contrôles de la méthode, chacun avec sa commande |
| **Une note de mouvement** | chaque seconde du film est notée ; une seconde molle se reprend avant de te montrer le film (`scripts/porte_b.py`) | la seconde la plus calme de trois films de référence (relevé C10) |
| **Des règles mesurées** | des études, des sources datées et des relevés (`references/sources.md`) | plus de 2 000 vidéos relevées et mesurées (relevés C9 et C11) |

## Nouveau dans la 0.4 : les images

| | Ce que ça fait | D'où ça vient |
|---|---|---|
| **Onze styles d'illustration** | vraies captures, interface flottante, 3D, formes à plat, données vivantes, collage à la Vox, isométrique, typographie en mouvement, banque teintée, dessin tracé, image générée étiquetée ; chacun avec sa fabrication dans HyperFrames, ses effets et son garde-fou (`references/illustrations.md`) | les effets du catalogue et les règles de scène |
| **La question du style, avec une recommandation** | Claude lit ta charte, te recommande le style qui va à ce que la vidéo explique et à ta charte, te donne deux autres choix, et peut te montrer l'image du hook dans les trois | ce que la vidéo explique (`references/styles.md`, § 1) et ta charte |
| **Images et vidéos libres de droit** | `scripts/banque.py` cherche sur Pexels, Pixabay et Openverse, télécharge la bonne taille et note la licence de chaque fichier ; `controler` refuse un fichier sans licence notée et donne les crédits à mettre dans la légende | licences relues le 03/11/2026 |

## Pourquoi ce kit

Le 01/11/2026, j'ai testé un skill gratuit qui promettait de monter des reels, de la voix à la musique (`reel-builder`, dépôt `Ootto-AI/claude-content-skills`), sur trois de mes projets : StoryForKid, Evidnce et Obvius Studio. Même commande, un Claude neuf à chaque fois.

| | Le skill testé (01/11) | kit-reels (02/11) |
|---|---|---|
| La vidéo dès la première demande | 1 projet sur 3 | 3 projets sur 3 |
| La voix | la voix de l'ordinateur, robot | ElevenLabs v3, 147 à 160 mots par minute |
| Le mot à commenter, relu par Whisper | raté 2 fois sur 3 (« Commande dragon ») | juste 3 fois sur 3 |
| La musique | 1 reel sur 3 | 3 reels sur 3, sans trou de silence |
| Le volume | -13,9 à -14,1 LUFS | -14,0 à -14,2 LUFS |
| Les infos sur les projets | 37, aucune inventée | 36, aucune inventée |
| Le temps | 13 à 18 minutes, deux demandes pour 2 projets sur 3 | 12 à 18 minutes, une demande |

Mesuré avec Whisper large-v3 et ffmpeg ; les reels des deux tests et leurs mesures sont dans `exemples/`. Ce qui reste : un nom de marque peut sortir mal prononcé (« Obvius » entendu « Obvious ») ; `verifier.py` le signale, et tu le réécris comme il se dit.

## Ce qu'il fait de plus

| | Un skill de script | kit-reels |
|---|---|---|
| Point de départ | un sujet | le format et l'objectif, puis la structure qui va avec |
| Voix | rien : la voix de l'ordinateur, ou toi | ElevenLabs v3 scène par scène, débit mesuré, reprise si elle va trop vite, mots clés relus |
| Musique et son | rien | une musique sous la voix qui se baisse quand on parle, un bruitage par information, master à -14 LUFS |
| Images | des interfaces recréées | tes vraies captures, en perspective ou dans un vrai modèle de téléphone ; onze styles d'illustration proposés selon le sujet et ta charte ; des images et vidéos libres de droit, licence notée |
| Style et effets | au hasard du prompt | douze styles et un catalogue d'effets, chacun lié à une information |
| Vérification | à l'œil | un script mesure le MP4 : format, cadence, durée, volume, musique, images figées, débit, mots entendus, sous-titres calés sur la voix, image 0, note de mouvement de chaque seconde ; puis seize contrôles et un relecteur à part |
| Fin | « Commente MOT », rien derrière | le message privé prêt, et le rappel de brancher la réponse automatique |

## Comment t'en servir

### 1. L'installer

Il te faut [Claude Code](https://claude.com/claude-code), Node 22 ou plus, ffmpeg et python3.

Dans Claude Code :

```
/plugin marketplace add Taubiwan/kit-reels
/plugin install kit-reels@kit-reels
```

Puis, une seule fois, dans ton terminal, les skills du moteur de montage (HyperFrames, gratuit) et son modèle de transcription :

```bash
npx --yes hyperframes@0.8.167 skills
npx --yes hyperframes@0.8.167 models install parakeet
```

### 2. Ta voix

Avec ElevenLabs : crée une clé sur elevenlabs.io, puis dans ton terminal

```bash
export ELEVENLABS_API_KEY=ta-clé
```

(ajoute cette ligne au fichier de configuration de ton terminal pour la garder). La clé présente vaut accord pour la voix du reel : environ 700 caractères pour 40 secondes. La voix par défaut est Théo, une voix française de la bibliothèque ElevenLabs.

Sans ElevenLabs : tu t'enregistres avec ton téléphone, d'une traite, et le kit nettoie ta prise (`references/voix.md`, section 6).

### 3. Lancer

```
/reel reel pour ton-site.com
```

Ou plus précis :

```
/reel démo de mon appli ton-site.com, objectif : des commentaires, mot « essai »
/reel monte ma vidéo prise.mp4, en 9:16 et en 4:5
/reel une scène 3D sur le lait au fond du magasin, en 60 images par seconde
```

Claude te pose cinq questions au plus (format, objectif, style des images, mot à commenter, voix), avec sa réponse recommandée. Puis il te montre le storyboard et quatre images avant de fabriquer. À la fin, tu as `final.mp4`, la légende et le message privé à envoyer. Rien n'est publié à ta place.

Si un autre skill s'appelle aussi `reel` chez toi : `/kit-reels:reel`.

## Les formats et les objectifs

| Format | Quand |
|---|---|
| Démo d'appli en cadre de téléphone | une appli ou un site où l'on fait quelque chose |
| Face caméra et preuves | tu te filmes, un avis, un retour d'expérience : le kit monte ta prise |
| Explication en motion | un mécanisme à faire comprendre, sans visage |
| Test d'outil (vrai ou hype) | une promesse vue en ligne, à vérifier |
| Avant / après | un résultat visible |

Objectifs : vues et partages, abonnés, commentaires (puis message privé), enregistrements, clics ou installations. Chacun change l'ordre et la fin du reel : `skills/reel/references/structures.md`.

## Ce que ça coûte

- Claude Code : ton abonnement.
- ElevenLabs : environ 700 caractères pour un reel de 40 secondes, plus les reprises. L'offre gratuite donne 10 000 crédits par mois ; pour une marque, vérifie la licence commerciale de ton offre.
- HyperFrames, three.js, la musique et les bruitages : gratuits, calculés sur ta machine.
- Ta prise face caméra : rien à payer, la transcription tourne sur ta machine.

## Les fichiers

```
skills/reel/
  SKILL.md                 l'ordre de marche et les règles
  references/              structures, hooks, voix, écran, son, HyperFrames, vérification,
                           styles, effets, styles d'illustration et banques, règles de scène, contrôles, sources
  scripts/voix.py          la voix ElevenLabs v3 scène par scène (ou ta prise nettoyée), et ses sous-titres
  scripts/prise.py         ta vidéo face caméra : coupes sur l'énergie de ta voix, voix montée, contrôle des blancs
  scripts/formats.py       le même reel en 4:5, 1:1 et 16:9
  scripts/son.py           musique, bruitages, master à -14 LUFS
  scripts/verifier.py      les mesures du MP4 fini
  scripts/banque.py        images et vidéos libres de droit (Pexels, Pixabay, Openverse), licence notée
  scripts/porte_b.py       image 0, zones, note de mouvement, déterminisme, tirets (lancé par verifier.py)
  modeles/                 scenes.json, storyboard.md, charte.md, scene-3d.html (la scène 3D éprouvée)
exemples/                  les reels du test, V1 et V2
outils/                    propre.py (rien de privé avant publication), prise-essai.py (une prise face caméra d'essai)
```

Chaque script a son autotest : `python3 skills/reel/scripts/voix.py --autotest` (de même pour `prise.py`, `formats.py`, `son.py`, `verifier.py`, `banque.py` et `porte_b.py`).

## Licence

MIT, voir `LICENSE`. Ce que le kit utilise sans l'avoir écrit : `THIRD-PARTY.md`.

Fait par taubiwan.ai.
