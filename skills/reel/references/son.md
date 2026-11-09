# Le son : choisi pour ton film, posé sous ta voix

`scripts/son.py` pose le son de ton reel : celui que tu choisis pour ce film (une musique composée pour lui, des effets électro calés sur ses animations, ta piste, ou rien que ta voix), placé sous ta voix et mesuré, le master à -14 LUFS. Jamais un son calculé.

```bash
python3 scripts/son.py --video renders/reel.mp4 --voix voix/voix.wav --align voix/align.json -o final.mp4 \
  --compose | --musique ta-piste.mp3 | --sans-musique   [--effets effets.json] [--carte 29.4] [--style "..."] [--bpm 110]
```

Le film se rend muet ; `son.py` pose ta voix et le son choisi sans réencoder la vidéo. Il écrit aussi chaque couche telle que mixée, `final-musique.wav` et `final-effets.wav`. Dernière ligne : `SON_OK`.

## 1. Le choix, à chaque projet

Il n'y a pas de son par défaut : Claude te pose la question avec la voix, en te recommandant un choix, et ta réponse va dans le storyboard. Sans choix, `son.py` te le rappelle et s'arrête.

| Choix | Ce que `son.py` fait |
|---|---|
| Une musique composée pour ton film (`--compose`) | ElevenLabs Music (`music_v1`) la compose sur un plan à sections, à la durée de ton film (section 2), instrumentale, au style `--style` (le tien, en anglais ; sinon une chill house douce) et au tempo `--bpm` |
| Des effets électro calés sur les animations (`--effets effets.json`) | ElevenLabs génère la palette (section 3) et pose un effet sur chaque animation listée ; avec `--sans-musique` (un film sans musique) ou avec une musique |
| Ta piste (`--musique ta-piste.mp3`) | une piste libre de droits pour un usage commercial, dont tu gardes la licence ; calée et réglée comme la musique composée |
| Rien que ta voix (`--sans-musique`, sans `--effets`) | ta voix seule ; utile si une musique s'ajoute à la publication, dans l'appli |

Ce qui est généré se range dans le dossier où tu lances la commande, `musique/` et `effets/`, avec sa demande : la même demande n'est jamais repayée. **Sans clé** `ELEVENLABS_API_KEY`, ce qui n'est pas déjà généré ne l'est pas : `son.py` te le dit, te donne les trois choix (ta clé, que tu crées et ajoutes toi-même ; `--musique` ; `--sans-musique`) et s'arrête sans `SON_OK`. Claude te pose la question ; il n'écrit jamais ta clé. Plus aucune musique ni aucun bruitage ne se calculent sur ta machine depuis le 09/11/2026 : ils sonnaient mal.

Le coût, mesuré le 09/11/2026 sur une offre Pro : 363 crédits pour 20 s de musique, 348 pour 23 s ; 60 crédits pour cinq prises d'effets.

**Les droits** suivent ton offre ElevenLabs (conditions d'Eleven Music mises à jour le 09/10/2026, lues le 09/11/2026 : https://elevenlabs.io/music-terms) : tout usage commercial en ligne est permis, sauf film, télévision, radio et jeux vidéo de studio ; l'offre gratuite demande de citer Eleven Music à la diffusion ; les offres gratuite à Pro sont réservées à un usage individuel, Scale aux structures de moins de 10 salariés. Une musique d'Instagram est réservée à un usage non commercial : pas sur un reel qui mène à une offre, un lien ou un produit. Un titre du commerce ou un thème de film ne va jamais dans le fichier.

## 2. La musique composée : le plan et le calage

| Section | Durée | Styles |
|---|---|---|
| Intro | 4 s | intro dépouillée, le pied qui entre |
| Groove, puis Variation | ton film jusqu'à 1 s après la carte de fin, moins l'intro (6 s au moins), en sections de 110 s au plus | le groove plein ; puis le même, plus lumineux, l'énergie qui monte doucement |
| Outro | le reste de la carte, plus 8 s | la phrase finale, les accords qui s'ouvrent, la fin résolue sur la tonique, le dernier accord qui résonne |

En secondes entières : ton film rendu de nouveau, à quelques images près, retrouve le même plan, donc la même musique. Écartés sur tout le morceau : voix, chant, chœurs, paroles, sifflement, mélodie chargée, drop agressif, distorsion.

Le calage se mesure sur la piste, composée ou la tienne, par trames de 50 ms : sa tête muette est sautée, et son dernier son plein (l'accord final, avant qu'il s'éteigne) tombe 0,5 s après le début de la carte de fin (`--carte`, par défaut la fin du dernier mot d'`align.json`) : le dernier accord sonne sur la carte. Elle entre en fondu de 0,15 s, sans clic. Une piste trop courte entre plus tard dans le film, et le script le dit ; une piste finie avant le film aussi.

## 3. Les effets électro

Sept effets, chacun généré par ElevenLabs (`/v1/sound-generation`) depuis son prompt, en une ou deux prises qui alternent. `effets.json` se lit dans le storyboard : un effet par animation, à son instant.

| Effet | Pour | Durée | Prises | Sous la crête de ta voix |
|---|---|---|---|---|
| `whoosh` | l'entrée d'un panneau, d'une scène | 0,9 s | 2 | 11 dB |
| `impact` | un mot géant, un chiffre qui tombe | 0,8 s | 2 | 8 dB |
| `blip` | une interface, une coche | 0,5 s | 2 | 12 dB |
| `glitch` | un compteur qui change | 0,6 s | 2 | 11 dB |
| `frappe` | une ligne qui s'écrit | 1 s | 1 | 14 dB |
| `montee` | la montée jusqu'à une révélation | 1,4 s | 1 | 9 dB |
| `stab` | la carte de fin | 1,5 s | 2 | 6 dB |

```json
[{"t": 0.0, "son": "whoosh"}, {"t": 0.13, "son": "impact"}, {"t": 8.1, "son": "stab"}]
```

Règles : deux effets à moins de 0,12 s, le plus important reste (`montee`, `stab`, `frappe`, `glitch`, `impact`, `whoosh`, `blip`, dans cet ordre) ; les prises d'un même effet alternent ; la tête muette de chaque prise est retirée, pour qu'il parte à son instant ; chaque effet se règle sous la crête de ta voix (tableau), et la piste entière reste 3 dB au moins dessous ; aucun effet dans les 0,2 dernières secondes.

Mesuré le 09/11/2026 sur un reel de 10 s : un `whoosh` à chaque scène, un `impact` sur chaque mot clé, un `stab` sur la carte de fin ; la piste des effets 3,9 dB sous la crête de la voix ; le film à -14,0 LUFS, crête -1,5 dBTP, VERIF_OK avec `--sans-musique`.

## 4. Les niveaux

| Élément | Niveau |
|---|---|
| Ta voix | réglée à -14 LUFS par `voix.py` ou `prise.py` |
| La musique sous ta voix | 11 dB sous ta voix, mesuré en LUFS sur la même fenêtre (du début du film à la carte) ; hors de 8 à 14 dB, le script s'arrête |
| La musique sur la carte de fin | 6 dB plus haut, montée en 0,3 s quand ta voix s'arrête ; fondu de 0,8 s à la fin |
| Les effets | sous la crête de ta voix, de 6 à 14 dB selon l'effet ; 3 dB au moins pour la piste entière |
| Le master | -14 LUFS intégré, crête à -1 dBTP au plus, mesurée sur le film encodé (le master vise -1,5 dBTP, car l'AAC ajoute de la crête, et se rabote si le film dépasse -1) |

Mesuré le 09/11/2026 sur un reel de 10 s (la voix jusqu'à 8,1 s) : la musique 11,0 dB sous la voix, la carte de fin à -20,4 LUFS, relevée de 4,5 dB ; le film à -14,0 LUFS, crête -1,5 dBTP, sans trou de silence (`verifier.py`). Sans musique, les silences entre tes phrases sont voulus : `verifier.py --sans-musique` les dit pour mémoire.

## 5. Jamais un son calculé

Ni musique ni bruitage ne se fabriquent sur ta machine. Un son hors de la palette est un vrai son (une banque libre de droits, licence notée, ou ton enregistrement), posé dans la composition sur une information qui arrive à l'image, jamais sur une coupe qui n'apporte rien (`effets.md`, section 5).

## 6. Si ta composition porte déjà la voix

`--piste` écrit seulement le son ajouté (la musique, les effets, ou les deux), calé et réglé sur ta voix, à poser à volume 1 sur sa propre piste ; le compte rendu donne la balise `<audio>` à copier :

```bash
python3 scripts/son.py --piste --duree 13.26 --carte 11.76 --voix voix.wav -o musique.wav --compose
python3 scripts/son.py --piste --duree 13.26 --voix voix.wav -o effets.wav --sans-musique --effets effets.json
```
