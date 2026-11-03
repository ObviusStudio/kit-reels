# Les contrôles : seize mesures sur le rendu, puis un relecteur séparé

Avant de te montrer un film, on le mesure, puis un agent qui ne l'a pas fabriqué le relit. `scripts/verifier.py` lance les contrôles qu'une commande peut trancher, dont ceux de `scripts/porte_b.py` (image 0, note de mouvement de chaque seconde, déterminisme, tirets longs, et une alerte quand du contenu entre dans les bandes hors zone, à relire sur la planche) ; la colonne « Commande ou méthode » dit comment chacun se lance, et `verifier.md` dit lesquels sont automatiques. Le reste se lit sur la planche d'images, et c'est le relecteur qui le juge. Le mot « vérifié » ne s'écrit que devant une commande lancée et une sortie lue.

## 1. Les seize contrôles, mesurés sur le rendu

Toutes les mesures se lancent sur le MP4 réel. Variable utilisée ci-dessous : `F=renders/reel.mp4`.

| # | Contrôle | Seuil | Commande ou méthode |
|---|---|---|---|
| 1 | Durée, résolution, cadence, codec | durée à 0,5 s près de la beat map, 1080x1920, 30 i/s, H.264 | `ffprobe` (bloc 1) |
| 2 | Image 0 | ni noire ni logo, elle porte le hook | luminance moyenne au-dessus de 16 (un noir pur donne 16) et image lue (bloc 2) |
| 3 | Une image par temps de la beat map | chaque information annoncée est visible | extraction d'images et planche (bloc 2) |
| 4 | Zones de sécurité | aucun texte hors de x 80-930, y 170-1500 | bandes recadrées (bloc 3) |
| 5 | Contraste des textes | 4,5 à 1 ; 3 à 1 seulement pour un titre de 90 px au moins | `check` (passe de contraste), plus le calcul des paires du kit (bloc 8) |
| 6 | Immobilité et mouvement | aucune image figée pendant 0,8 s ou plus (hors chute d'un gag) ; la note de rythme de chaque seconde complète, un pondéré (03/11/2026, sources C12) : moitié mouvement (écart moyen entre images successives, gris 96x96, 30 i/s, sur 255, divisé par 0,6 et plafonné à 1), moitié arrivées d'information (un mot, un objet, une étiquette qui apparaît ; deux par seconde valent 1) ; aucune seconde sous 0,5 (sources C10), sauf une respiration, une chute ou la carte de fin écrites dans la beat map ; une seconde faible se reprend avant de montrer le film (mouvement plus large, scène plus courte) ; sur une prise face caméra (`verifier.py --face-camera`), la note se lit pour mémoire : son seuil vient de films de motion sans voix, et le cadrage alterné et le punch-in se regardent sur la planche | `freezedetect` (bloc 3) et la note de chaque seconde de `scripts/porte_b.py`, lancée par `verifier.py` ; son témoin, une seconde figée, doit sortir faible |
| 7 | Déterminisme | aucun hasard sans graine, aucune horloge | `grep` (bloc 3) |
| 8 | Sous-titres | à moins de 0,2 s de la voix, 0 mot d'écart avec le script verrouillé | transcription du son final avec horodatage des mots, comparée aux temps de la composition |
| 9 | Son | mixage final à -14 LUFS, plus ou moins 1 ; crête vraie à -1 dBTP au plus | `ebur128` (bloc 4) |
| 10 | Carte de fin | au moins 1,5 s à l'écran | `timeline --json` (bloc 5) |
| 11 | Effets et colonne « Montre » | chaque effet nommé, chaque ligne a son information | porte A, relue sur le rendu |
| 12 | Récompenses mesurées sur le rendu | première avant 3 s, écart de 5 s au plus, début du payoff à 60-80 % (les cinq formats du kit sont des pièces de valeur ou d'enquête : le seuil vaut pour tous ; une news, une publicité ou un film cinématique n'en ont pas, sources C9) | temps lus sur la planche, comparés à la colonne R de la beat map ; le payoff se date à la première image où le résultat promis est lisible, pas à sa dernière coche |
| 13 | Boucle (seulement si annoncée) | similarité entre première et dernière image de 0,95 au moins | `ssim` (bloc 6) |
| 14 | Contrôles du moteur | `lint` et `check` sans erreur | `hyperframes.md` |
| 15 | Typographie du texte | aucun tiret cadratin, demi-cadratin ni signe moins typographique | `grep` (bloc 7) |
| 16 | Barre du waou | un effet qui montre l'information, une transition née d'un élément à l'écran, un seul payoff, début à 60-80 % (les cinq formats du kit sont des pièces de valeur ou d'enquête : le seuil vaut pour tous ; une news, une publicité ou un film cinématique n'en ont pas, sources C9) | relecteur séparé, section 2 |

Bloc 1, format :

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,nb_frames:format=duration,size -of default=nw=1 $F
```

Bloc 2, image 0, une image par temps de la beat map, planche (2 images par seconde, 6 colonnes, autant de lignes que la durée l'exige). La liste de temps de la boucle `for` est celle de la beat map (ici 0 ; 1,7 ; 3,3 ; 5 ; 6,1 et 7,6 s) : le hook, une image par scène, le moment fort, la carte de fin.

```bash
ffmpeg -hide_banner -i $F -vf "select=eq(n\,0),signalstats,metadata=print:key=lavfi.signalstats.YAVG" -an -f null - 2>&1 | grep -o "YAVG=[0-9.]*" | head -1
for t in 0 1.7 3.3 5 6.1 7.6; do ffmpeg -hide_banner -loglevel error -y -ss $t -i $F -frames:v 1 image-$t.png; done
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F); R=$(awk -v d="$D" 'BEGIN{print int((d*2+5)/6)}')
ffmpeg -hide_banner -loglevel error -y -i $F -vf "fps=2,scale=270:-1,tile=6x$R" -frames:v 1 planche.png
```

`R` est le nombre de lignes : 6 colonnes sur `R` lignes tiennent toutes les images à 2 par seconde (8,3 s : 3 lignes, 1620x1440 ; 30 s : 10 lignes). Une grille fixe de 6x5 s'arrête à 15 s.

Lire les images extraites avec les yeux : la mesure dit qu'une image n'est pas noire, pas qu'elle montre le hook.

Bloc 3, zones de sécurité, immobilité, déterminisme. Les quatre bandes sont le haut (170 px), le bas (420 px sous y 1500), la gauche (79 px) et la droite (149 px au-delà de x 930). On mesure d'abord le fond (carré de 100 px en haut à gauche de l'image 0), puis, pour chaque bande, la luminance minimale et la maximale.

```bash
ffmpeg -hide_banner -i $F -vf "select=eq(n\,0),crop=100:100:0:0,signalstats,metadata=print:key=lavfi.signalstats.YAVG" -an -f null - 2>&1 | grep -o "YAVG=[0-9.]*" | head -1
for band in "1080:170:0:0" "1080:420:0:1500" "79:1920:0:0" "149:1920:931:0"; do for k in YMIN YMAX; do printf "bande $band $k="; ffmpeg -hide_banner -i $F -vf "crop=$band,signalstats,metadata=print:key=lavfi.signalstats.$k" -an -f null - 2>&1 | grep -o "$k=[0-9]*" | sed "s/$k=//" | sort -n | { if [ $k = YMIN ]; then head -1; else tail -1; fi; }; done; done
ffmpeg -hide_banner -i $F -vf "freezedetect=n=-60dB:d=0.8" -an -f null - 2>&1 | grep freeze_
grep -rnE "Math\.random|Date\.now|performance\.now" --include='*.html' .
```

Seuils d'une bande, selon le fond mesuré (valeurs en niveaux de luminance, 16 à 235) :

| Fond | Contenu hors zone | Seuil |
|---|---|---|
| Sombre | texte ou objet clair : la maximale dépasse 200 | maximale d'une bande au plus égale au fond plus 50 (relevé sur un film à fond sombre de luminance 30 : bandes à 30, 30, 32 et 40) |
| Clair | texte ou objet sombre : la minimale tombe sous 100 | minimale d'une bande au moins égale au fond moins 20 ; maximale au plus égale au fond plus 8 (une surface blanche donne 238) |

Exemple rendu (fond clair de luminance 228) : bandes 228 à 228 en haut et en bas, 228 à 229 à gauche, 225 à 232 à droite, soit au plus 3 niveaux sous le fond et 4 au-dessus : le halo d'encodage au bord des cartes, pas un contenu. Dans les deux cas, un parasite d'encodage reste à quelques niveaux du fond. Sur un fond clair, on lit la minimale, parce qu'un contenu foncé sur un fond clair est ce que l'on cherche ; une surface blanche hors zone ne se repère que par la maximale. `freezedetect` ne liste rien quand tout bouge : un petit objet qui bouge (un point, un arc fin) ne l'empêche pas de signaler un arrêt, il faut un mouvement large et lent ; chaque arrêt listé est soit supprimé par un mouvement lent, soit justifié par la beat map (la chute d'un gag). Contrôle positif relevé sur un reel de référence : la scène de comparaison grossie de 10 % sur une copie du projet a fait tomber les minimales de gauche et de droite à 27 et 30 et monter la maximale à 238, donc la mesure échoue quand elle le doit.

Bloc 4, son (pour une pièce avec piste audio) ; lire `I` (LUFS intégrés) et `Peak` (crête vraie) :

```bash
ffmpeg -hide_banner -nostats -i $F -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
ffmpeg -hide_banner -i voix-musique.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 mixage.wav
```

La seconde commande corrige le niveau d'un mixage ; relancer la première après correction. Cible du mixage, une seule : le master à -14 LUFS et -1 dBTP au plus (`regles-de-scene.md`, § 6). La voix se règle pour l'atteindre (seule, environ -14,3 LUFS) ; la musique joue à -18 LUFS quand elle est seule et descend à 12 dB sous la voix quand celle-ci parle. Un rendu sans piste audio (`ffprobe` ne liste aucun flux audio) saute ce bloc et le dit.

Bloc 5, carte de fin : lire la durée du dernier clip de scène (une ligne `s4` qui commence à 6,45 s et dure 1,85 s donne une carte de 1,85 s).

```bash
npx --yes hyperframes@0.8.167 timeline --json | python3 -c "import json,sys; r=json.load(sys.stdin)['timeline']['tracks'][0]['rows']; print([(x['id'],x['start'],x['duration']) for x in r])"
```

Bloc 6, boucle : comparer la première et la dernière image de la piste vidéo (la fin du fichier peut dépasser la fin de la vidéo si l'audio est plus long) ; le contrôle est réussi si `All` vaut 0,95 ou plus.

```bash
D=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 $F); T=$(echo "$D - 0.1" | bc)
ffmpeg -hide_banner -loglevel error -y -i $F -frames:v 1 premiere.png
ffmpeg -hide_banner -loglevel error -y -ss $T -i $F -frames:v 1 derniere.png
ffmpeg -hide_banner -i premiere.png -i derniere.png -lavfi ssim -f null - 2>&1 | grep -o "All:[0-9.]*"
```

Une pièce qui n'annonce pas de boucle et finit sur une carte donne autour de 0,92 : c'est attendu. Les blocs 5 et 8 lancent `python3`, le bloc 6 lance `bc`.

Bloc 7, tirets (le motif est écrit en octets pour ne pas contenir les caractères interdits) :

```bash
grep -nE $'\xe2\x80\x94|\xe2\x80\x93|\xe2\x88\x92' BRIEF.md index.html
```

Aucune ligne affichée, code de sortie 1 : propre. Si un texte réel contient un tiret cadratin, la ligne s'affiche et `grep` sort avec le code 0 : le contrôle sait donc échouer.

Bloc 8, contraste des paires du kit. `check` applique le seuil des grands textes (3 à 1) dès 24 px, ou dès 19 px en gras (lu dans le code de la version 0.8.167), et ne rend que des compteurs : un texte d'appui de 48 px à 3,2 à 1 passe `check` et viole la règle du skill (4,5 à 1 sous 90 px). On calcule donc le ratio de chaque paire texte sur fond de ta charte, depuis ses hex, et on exige 4,5 au moins.

```bash
python3 -c "import sys;L=lambda h:sum(w*(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4) for w,c in zip((.2126,.7152,.0722),[int(h.lstrip('#')[i:i+2],16)/255 for i in (0,2,4)]));a,b=sorted((L(sys.argv[1]),L(sys.argv[2])),reverse=True);print(round((a+.05)/(b+.05),2))" '#545B66' '#F6F7F9'
```

Une paire sous 4,5 se corrige dans ta charte (`../modeles/charte.md`), pas dans la pièce.

Une détection de coupures de plans (`select='gt(scene,0.3)'`) ne trouve rien sur un film motion à fonds plats : elle sert aux films tournés ou générés ; pour un film motion, on s'appuie sur la beat map, `freezedetect` et une image par temps.

Chaque source de chiffre est relue : une pièce où un chiffre affiché diffère de celui de la source échoue, même si tout le reste passe.

## 2. Le relecteur séparé

Pour un lot, ou une pièce à enjeu, un agent qui n'a pas fabriqué la pièce la relit avec l'œil de quelqu'un qui cherche l'erreur. Son prompt est en section 3. Il reçoit la beat map, les images extraites et le rapport de mesures, sans l'avis du fabricant.

| Règle | Raison |
|---|---|
| Il cherche : chiffres faux, hooks faibles, doublons, odeur de vente, registre, oral, texte hors zone | ce sont les défauts que l'auteur ne voit plus |
| Il pose la question du waou : un motion designer expert signerait-il cette pièce ? | une pièce correcte et plate se voit à la relecture, pas à la mesure |
| Chaque trouvaille est vérifiée avant d'être appliquée | un relecteur se trompe aussi : appliquer sans vérifier remplace un défaut par un autre |
| Une correction part avec l'ancienne version archivée | on peut revenir en arrière |
| Un refus est motivé dans le compte rendu | sinon le même point revient au tour suivant |
| Il ne corrige pas lui-même et ne publie rien | une relecture qui écrit n'est plus une relecture |

Le compte rendu de la porte liste trois colonnes : corrigé, refusé avec la raison, remesuré (chiffre relu à l'instant, depuis la source). Le mot « vérifié » ne s'écrit que devant une commande lancée et une sortie lue.


## 3. Le prompt du relecteur

À lancer dans un agent qui n'a pas fabriqué la pièce (un Claude neuf, sans ton avis), avec la beat map, les images extraites et le rapport de mesures.

```text
Tu es le relecteur d'un reel que tu n'as pas fabriqué. Tu as : la beat map, les images extraites à chaque temps, le rapport de mesures (durée, résolution, zones, contraste, niveaux).
Cherche, dans cet ordre, et cite à chaque fois la ligne de la beat map et le temps :
1. Chiffres : tout chiffre dit ou affiché sans source, ou différent de celui de la source.
2. Hook : promesse floue, plus de 8 mots, illisible son coupé, illisible à l'image 0.
3. Informations : tout événement qui ne montre aucune information (à retirer) ; toute animation répétée sur deux événements consécutifs.
4. Texte : hors zone de sécurité, chevauchements, texte seul sans visuel animé, plus de 3 lignes ou de 8 mots à la fois, comptés comme `regles-de-scene.md` § 5 le dit : la source en microtexte et le repère « 1/3 » ne comptent pas, une étiquette compte.
5. Preuve : interface inventée, capture non datée, claim sans sa source à l'écran.
6. Récompenses : première après 3 s, intervalle de plus de 5 s, début du payoff hors 60-80 % (l'instant où le résultat promis devient lisible, pas sa dernière coche).
7. Marque : couleur, police ou mot hors de la charte ; mot interdit ; registre ; tirets longs.
8. Waou : « un motion designer expert aurait-il signé cette pièce ? » sur trois images, oui ou non motivé.
Réponds par une liste de défauts classés (bloquant, à corriger, à noter), chacun avec le temps, la ligne et la correction proposée. N'écris aucune correction dans les fichiers et ne publie rien. Si tu ne trouves rien, dis ce que tu as vérifié.
```
