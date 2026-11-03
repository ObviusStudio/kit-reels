# Les douze styles vidéo et le choix par ce qu'on explique

Dans cette fiche, « le kit » veut dire la charte de ta marque (`../modeles/charte.md`) : ses couleurs, ses polices, son ton et ce qu'elle s'interdit.

Ce fichier sert à choisir le style d'un reel (rythme, typographie, mouvement, transitions, son) selon ce que la vidéo explique, puis à choisir ses effets.

Le look vient du kit de marque (ta charte, `../modeles/charte.md`), les effets de `effets.md`, et en cas de conflit `regles-de-scene.md` gagne. La ligne « Barre » de chaque style est un test : son unité et sa manière de mesurer sont à la section 4.

## 1. Ce qu'on explique, le style, les effets

| Ce qu'on explique | Style | Effets (un ou deux par information) |
|---|---|---|
| un outil et son résultat | `single-shot-ad` | `ui-result`, `proof-capture`, `word-swap` |
| un processus, une marche à suivre | `annotated-steps-tutorial`, `desk-screen-explainer` | `zoom-screen`, `spotlight-dim`, `checklist-sync` |
| une comparaison, un verdict | `specimen-freeze-lesson`, `split-screen-explainer` | `comparison-split`, `before-after-wipe`, `verdict-mark` |
| un chiffre | `beat-word-showreel` | `stat-card`, `count-up`, `bar-grow`, `chart-line` |
| une news | `presenter-over-broll`, `manifesto-page` | `split-source`, `proof-capture`, `lower-third` |
| un système, un concept | `dot-system-loop` | `dot-thread`, `cause-arrow`, `bar-grow` |
| une liste montrée sur une personne | `presenter-effects` | `chapter-pill`, `punch-in`, `freeze-label` |
| une annonce, un manifeste, une offre | `manifesto-page`, `product-world` | `type-wall`, `ui-tilt`, `depth-photo` |
| une histoire | `warm-light-story` | `lamp-bloom`, `caption-story`, `camera-reframe` |

Pour tous : carte de fin `end-card`, hook à l'image 0 et texte à 0,3 s au plus ; un film 16:9 se recompose en 9:16 ; une information nouvelle toutes les 1,5 à 2,5 s.

## 2. Les douze styles

### manifesto-page : des mots géants, puis la vraie page qui se redresse
- Référence : https://x.com/cleeeeeeeeement/status/2099798349226377546
- Beau : un mot géant puis la phrase 5 fois plus petite, chaque mot prend son poids, du maigre au gras, le logo devient l'en-tête de la vraie page.
- Rythme, typo : 5 plans de 1,1 s et un plan de 7 s pour la page ; mot de 250 px d'encre sur 80 à 100 % de la colonne.
- Mouvement, transitions : mise au point en 0,2 s ; la page se redresse en 1,6 s.
- Son : musique sans voix, un son par information.
- Effets : `type-wall`, `ui-tilt`, `zoom-screen`, `proof-capture`.
- Jamais : une image 0 noire ; une page inventée ; une offre dans un manifeste.
- Prompt : manifesto kinetic typography, one giant word then the sentence at one fifth the size, words gaining weight from light to bold, real page tilts then straightens
- Barre : l'OCR lit un mot à l'image 0 ; accent sous 12 % ; titre de la page redressée de 90 px ; aucune suite presque immobile de plus de 0,8 s.

### beat-word-showreel : un mot par temps, une matière par scène
- Référence : https://x.com/leonabboud/status/2103576084499358051
- Beau : un mot par demi-temps, un aplat par mot, trois voix typographiques (grasse, serif italique, mono), un morph de graisse.
- Rythme, typo : un mot par plan à 0,42 s, événements sur la grille ; mot plein cadre de 200 px d'encre.
- Mouvement, transitions : ligne tracée en 0,05 s, aplat en 0,13 s, point qui avale le cadre en 0,15 s .
- Son : 128 à 140 BPM si un mot tombe par temps.
- Effets : `beat-words`, `weight-morph`, `depth-object-pbr`, `data-stack`, `loop-back`.
- Jamais : un compteur sans source ; coin de cadre, faux timecode, particule.
- Prompt : beat-synced kinetic typography, one word per half beat, flat color field per word, heavy grotesk caps, weight morph
- Barre : un mot par temps (0,43 à 0,47 s), écart à la grille de 15 % de la période au plus ; transitions de 0,05 à 0,25 s.

### single-shot-ad : un seul plan, de la promesse à la preuve
- Référence : https://x.com/samuel_yostt/status/2105746669035733275
- Beau : un plan unique où chaque scène sort de la précédente, texte au-dessus et preuve dessous, jamais deux idées.
- Rythme, typo : 15 s sans coupe, 13 événements, carte de fin de 1,5 s ; grotesque demi-grasse de 90 px, 2 lignes de 13 à 18 caractères.
- Mouvement, transitions : ease-out long, entrées de 0,3 à 0,5 s ; chaque raccord naît d'un élément à l'écran.
- Son : un son par information ; whoosh seulement si l'élément apporte l'information.
- Effets : `ui-result`, `proof-capture`, `word-swap`, `ui-tilt`, `checklist-sync`.
- Jamais : un mot qui change plus de 3 fois ; une fausse capture.
- Prompt : single continuous shot, no hard cuts, text on top and visual proof below, real phone frame, column brakes onto the chosen card
- Barre : une coupe par 5 s au plus ; texte y 300-900, preuve y 900-1500 ; preuve = capture réelle datée ; l'image 0 porte la phrase.

### dot-system-loop : un point, tout un système, en boucle
- Référence : https://x.com/ultimaxbt/status/2108935657334702300
- Beau : un seul objet conducteur traverse sept scènes, une physique mesurable (rebonds, écrasement, ressort), inversion forme et fond à chaque coupe, boucle parfaite.
- Rythme, typo : 17 plans, coupes au pas du temps (0,46 s à 130 BPM) ; grotesque très grasse, 2 mots lisibles.
- Mouvement, transitions : deux rebonds qui perdent un quart de hauteur, ressort stable en 0,3 s ; toutes les transitions naissent du point.
- Son : 130 BPM, coupes sur la grille.
- Effets : `dot-thread`, `chart-line`, `bar-grow`, `cause-arrow`, `checklist-sync`.
- Jamais : un second objet conducteur ; un rebond hors de la plage du kit.
- Prompt : one dot as the continuous thread, flat 2D shapes, three colors, figure and ground swap on every cut, squash and stretch, perfect loop
- Barre : objet conducteur sur 90 % des images (toutes les images à 30 i/s) ; coupes sur la grille à 5 % d'un temps près (écart maximal sur tous les raccords) ; écart moyen entre la dernière image et l'image 0 sous 2 sur 255. Mesures : section 4.

### presenter-effects : les effets démontrés sur la prise réelle
- Références : https://www.instagram.com/reel/DeXE2T0z7QW/ et https://www.instagram.com/reel/DeGSnoWzZTi/
- Beau : la prise réelle reste le héros, un repère de chapitre constant, un effet = une démonstration au mot près.
- Rythme, typo : plans de 4,7 s, événements de 0,7 s ; sous-titres sur une seule ligne, 3 mots de préférence (`regles-de-scene.md` § 5), mot clé 1,5 à 2 fois plus grand en accent ; pastille fixe en y 170-400.
- Mouvement, transitions : orbite, poussée, projecteur, liste cochée sur la prise, entrées de 150 à 220 ms.
- Son : master à -14 LUFS, la voix réglée pour l'atteindre (`regles-de-scene.md`, § 6), un clic par information.
- Effets : `chapter-pill`, `orbit-collection`, `punch-in`, `spotlight-dim`, `freeze-label`, `caption-keyword`.
- Jamais : deux mots d'appel différents ; une carte sur le visage ; un effet sans le mot qui le nomme.
- Prompt : real talking-head footage as the hero, each effect lands on the spoken word, constant chapter pill, keyword larger in accent
- Barre : sous-titres y 1150-1350 hors visage ; chaque effet à moins de 0,2 s de son mot ; personne visible sur 30 % de la hauteur.

### annotated-steps-tutorial : le résultat, puis une capture annotée par étape
- Référence : https://www.instagram.com/reel/Ddv031yRAU8/
- Beau : résultat chiffré et entouré dès l'image 0, vraie capture dans un vrai téléphone, cercle tracé à la main par capture, le fond qui change dit « nouvelle étape ».
- Rythme, typo : un événement toutes les 0,87 s, aucune image fixe de plus de 0,8 s ; légende de 2 lignes de 70 px ou plus.
- Mouvement, transitions : cercle tracé en 0,37 s à vitesse constante ; coupes franches, fond change à chaque étape.
- Son : voix sur fond continu, un son discret par trait tracé.
- Effets : `zoom-screen`, `spotlight-dim`, `freeze-label`, `checklist-sync`, `proof-capture`, `ui-tilt`.
- Jamais : un contour fin pour désigner ; une capture inventée ; un fond hors palette.
- Prompt : result first with real annotated numbers at frame zero, one step per shot, real capture in a phone frame, hand-drawn circle
- Barre : image 0 = résultat chiffré, réel, annoté ; téléphone de 50 à 75 % de la hauteur ; 4 couleurs par seconde au plus.

### presenter-over-broll : la personne au tiers bas, le monde derrière
- Références : https://www.instagram.com/reel/DeHyLDDz5Sq/, https://www.instagram.com/reel/DeUmc6YND2P/ et https://www.instagram.com/reel/Dd1VZiXNo8e/
- Beau : un B-roll chaud qui montre ce que la voix dit, deux plans seulement (la personne nette devant, le monde derrière), voix immédiate.
- Rythme, typo : une coupe sèche toutes les 1,6 à 2,5 s, aucun B-roll au-delà de 3 s ; titre en 2 ou 3 plaques de capitales de 90 px (y 580-840), sous-titres de 1 à 4 mots.
- Mouvement, transitions : aucune transition animée, micro push-in de 100 à 106 % sur une photo tenue ; fin par retour à l'image d'ouverture.
- Son : voix nue, sans musique, premier mot avant 0,1 s.
- Effets : `split-illustration`, `broll-cutaway`, `lower-third`, `headline-wall`, `pip-presenter`, `loop-back`.
- Jamais : une rafale sous 0,4 s sur un texte ; la personne qui cache l'objet ; un B-roll de banque hors sujet.
- Prompt : presenter cut out in the lower third over full-frame editorial B-roll, dry hard cuts every two seconds, still photo alternates with motion
- Barre : personne sur 35 à 50 % de la hauteur ; 2 plans sur 3 montrent la chose nommée ; sous-titres jamais sous y 1500.

### split-screen-explainer : l'illustration en haut, la parole en bas
- Référence : https://www.instagram.com/reel/DdFVPyjCB1J/ (regardé)
- Beau : split horizontal : en haut l'interface ou un graphique, en bas une personne, sous-titre sur plaque sombre posée sur la couture.
- Rythme, typo : premier changement avant 1,5 s, puis toutes les 1,5 à 2,5 s ; sous-titres de 84 px vers y 1350, mot clé sur plaque d'accent.
- Mouvement, transitions : l'illustration bouge, la moitié basse reste lisible ; la couture reste fixe (y 1100-1200).
- Son : bruitages posés sur une information, jamais de riser.
- Effets : `split-illustration`, `split-source`, `caption-payoff`, `proof-capture`, `strike-replace`.
- Jamais : un claim repris sans vérification ni sans sa réfutation sur le même écran.
- Prompt : horizontal split screen, real interface or clean graphic on top, warm interior below, small caps caption on a dark plate on the seam
- Barre : couture entre y 1100 et 1200 ; la moitié haute change toutes les 1,5 à 2,5 s ; chaque claim a sa source lisible.

### specimen-freeze-lesson : l'exemple joue, gèle, revient en carte, puis la leçon
- Références : https://www.instagram.com/reel/DdN-rujgYld/, https://www.instagram.com/reel/Dd3HtgHArRG/, https://www.instagram.com/reel/DeGlk7KIPpk/ et https://www.instagram.com/reel/DeAL3vPADSS/
- Beau : l'effet vécu puis nommé, le gel qui assombrit tout sauf une carte nette, un impact grave au gel puis la voix.
- Rythme, typo : l'exemple joue 2 à 4 s, texte du hook dès 0,3 s ; titre en trois graisses (mot lourd de 90 px, ligne fine de 48 px).
- Mouvement, transitions : la carte entre en fondu et monte sur 0,63 s, arrêt net ; coupe sèche sur l'image figée ; leçon de 3 mots tenue 0,8 à 1 s.
- Son : impact grave au gel (énergie sous 200 Hz), voix 0,1 à 0,6 s après.
- Effets : `freeze-label`, `spotlight-dim`, `proof-capture`, `comparison-split`, `redact-blur`.
- Jamais : un clip ou un chiffre de tiers ; une ouverture sans texte au-delà de 0,3 s ; le verdict à l'image 0.
- Prompt : specimen plays full screen, hard cut to a freeze frame, background dims to a third, one sharp centered card rises, low boom
- Barre : au gel, fond entre 0,20 et 0,45 de la luminance de l'exemple ; carte de 38 à 42 % de la largeur, seule surface nette.

### desk-screen-explainer : un plan fixe, un écran réel devant, un repère qui avance
- Référence : https://www.instagram.com/reel/DdAFS1PRxQO/
- Beau : la preuve avant la méthode, trois plans de profondeur (écran net, visage, décor assombri), un repère de progression constant.
- Rythme, typo : un plan fixe poitrine, l'écran change toutes les 1,5 à 3 s au mot, un seul punch-in ; titre de 90 px sorti à 2 s.
- Mouvement, transitions : la caméra ne bouge pas, l'écran porte le mouvement ; une seule coupe franche.
- Son : voix compressée, fond musical bas, premier mot à 0,08 s.
- Effets : `ui-world`, `pip-presenter`, `checklist-sync`, `hud-data`, `chapter-pill`, `screen-speedup`.
- Jamais : un anneau de compte à rebours ; un écran fixe plus de 3 s sans nouvelle information.
- Prompt : static chest-up framing at a desk, real screen sharp in front, dim room behind, out of the light, screen changes on the spoken word, step counter
- Barre : écran de 25 à 35 % de la hauteur ; chaque slide affiche « n/total » en 48 px ; le repère avance toutes les 5 s au plus.

### product-world : un univers produit à plusieurs profondeurs, un panneau net
- Référence : https://www.instagram.com/reel/Dd_HxWYh0Ot/ (regardé)
- Beau : un chiffre géant ouvre, puis des sections de page nettes flottent devant une photo plein cadre : la profondeur fait le soin.
- Rythme, typo : un changement toutes les 1,5 à 2,5 s, aucune image fixe au-delà de 0,8 s ; ouverture en capitales condensées de 92 px, titres de 96 px.
- Mouvement, transitions : la caméra glisse entre les plans, le panneau reste net, bézier (0.16, 1, 0.3, 1) ; avant et après superposés à 70 % (`fade-70`).
- Son : 110 à 140 BPM, un clic par micro-récompense, carte de fin silencieuse.
- Effets : `ui-floating`, `depth-photo`, `depth-object-pbr`, `camera-reframe`, `fade-70`.
- Jamais : flou (`regles-de-scene.md`, § 13) ; halo, lueur si le kit les interdit (on assombrit les plans lointains) ; microtexte en coin.
- Prompt : layered product world, one sharp central panel, near and far planes darkened not blurred, slow camera glide between planes
- Barre : le panneau central est la seule surface au contraste plein ; trois plans de profondeur au moins.

### warm-light-story : la lueur chaude qui devient l'histoire (maison, sans référence)
- Référence : aucune ; style construit, à valider sur une pièce rendue
- Beau : un seul objet (la lueur d'une lampe ou d'un écran) ouvre, devient le monde de l'histoire, puis ferme sur l'objet signature ; la lenteur est la beauté.
- Rythme, typo : une coupe toutes les 3 à 5 s, aucune sous 2,4 s, un mouvement par plan ; serif de titre de 96 px, un seul mot en italique.
- Mouvement, transitions : entrées de 0,4 à 0,6 s, aucun dépassement ; fondu enchaîné de 0,4 s, la lueur gonfle et avale la pièce (`lamp-bloom`) ; pas de fondu au noir.
- Son : berceuse acoustique, piano doux, sans percussion, jamais whoosh ni impact.
- Effets : `lamp-bloom`, `camera-reframe`, `caption-story`, `split-illustration-v2`, `depth-photo`.
- Jamais : un visage ou une voix d'enfant ; punch-in, glitch, flash, speed ramp ; le logo à l'image 0.
- Prompt : warm bedside lamp glow as the only through-line, slow push-in, the glow swallows the real room to become the story world, no overshoot
- Barre : la lueur sur 80 % des images ; accent sous 12 % ; carte de fin de 2 s sans fondu au noir.

## 3. Juger un style sur une pièce

Extraire nos images aux mêmes temps que la référence (`ffmpeg -ss <t> -i film.mp4 -frames:v 1 <t>.jpg`), monter une planche côte à côte, lire la barre critère par critère, puis demander « aussi beau que la référence ? ». Un non nomme le levier manquant (la ligne « Beau ») et la pièce repart de là.

## 4. Mesurer la barre d'un style

Chaque seuil de la ligne « Barre » a une unité, une règle (moyenne ou maximum) et des images sur lesquelles il se lit. Sans cela, deux relecteurs mesurent deux choses. Les images viennent du MP4 rendu (`F=renders/reel.mp4`), jamais de la composition.

| Forme du seuil | Unité | Moyenne ou maximum | Sur quelles images | Comment |
|---|---|---|---|---|
| « écart dernière image et image 0 sous N sur 255 » | niveaux de luminance sur 255 | moyenne sur tous les pixels de la valeur absolue de la différence | l'image 0 et la dernière image (durée moins 0,1 s) | commande A ci-dessous |
| « X sur N % des images » (objet conducteur, lueur) | % des images du film | un compte : images qui contiennent l'objet, divisées par toutes les images | toutes les images à 30 i/s, pas un échantillon | commande B : l'objet est présent quand 3 pixels au moins ont la couleur de l'accent |
| « accent sous N % » | % de la surface de l'image | moyenne sur toutes les images (le maximum se relève aussi et se dit) | toutes les images | commande B : part des pixels à la couleur de l'accent |
| « coupes sur la grille à N % près » | % de la période d'un temps (60 divisé par le BPM) | maximum : le pire raccord décide | le début de chaque scène de la beat map | commande C : écart entre le début de la scène et le multiple de la période le plus proche |
| « un mot par temps (de A à B s) », « transitions de A à B s » | secondes | chaque occurrence doit tenir dans la plage ; ni moyenne ni médiane | chaque mot, chaque transition de la beat map | durées lues dans la composition (`data-duration`, positions de la timeline), vérifiées sur une image avant et une après |
| « aucune suite presque immobile de plus de 0,8 s » | secondes | maximum : aucune ne dépasse | tout le film | `freezedetect=n=-60dB:d=0.8` (`controles.md`, bloc 3) : liste vide |
| « Y de la hauteur », « Y de la largeur » (téléphone, personne, carte) | % de 1920 px ou de 1080 px | chaque image extraite où l'élément figure doit tenir dans l'intervalle | une image par temps de la beat map où l'élément est présent | boîte englobante lue sur l'image |
| « y de a à b », « couture entre y a et b » | pixels du cadre 1080x1920 | chaque image extraite | une image par temps de la beat map | position lue sur l'image |
| « chaque effet à moins de 0,2 s de son mot » | secondes | maximum sur tous les effets | chaque effet de la beat map | temps de l'effet moins temps du mot (colonne « Temps » de la beat map, mots lus dans la transcription) |
| « OCR lit un mot », « 2 plans sur 3 montrent la chose nommée », « 4 couleurs par seconde au plus » | oui ou non, ou un compte | jugé : il n'y a pas de commande, la relecture le dit | l'image 0, ou une image par plan | le relecteur séparé note PASSE ou ÉCHOUE avec l'image à l'appui |

```bash
F=renders/reel.mp4
# A. écart entre la dernière image et l'image 0 (moyenne de |a-b| sur 255)
T=$(echo "$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 $F) - 0.1" | bc)
ffmpeg -hide_banner -loglevel error -y -i $F -frames:v 1 premiere.png
ffmpeg -hide_banner -loglevel error -y -ss $T -i $F -frames:v 1 derniere.png
ffmpeg -hide_banner -i premiere.png -i derniere.png -filter_complex "[0][1]blend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG" -f null - 2>&1 | grep -o "YAVG=[0-9.]*" | head -1
# B. objet conducteur et surface d'accent, sur toutes les images (remplacer 11 122 95 par l'accent du kit en décimal)
ffmpeg -hide_banner -loglevel error -i $F -vf scale=108:192 -f rawvideo -pix_fmt rgb24 - | python3 -I -c "
import sys
d=sys.stdin.buffer.read(); W,H=108,192; n=len(d)//(W*H*3); a=(11,122,95); part=[]
for i in range(n):
    f=d[i*W*H*3:(i+1)*W*H*3]
    part.append(sum(all(abs(f[p+k]-a[k])<40 for k in range(3)) for p in range(0,len(f),3))/(W*H))
print('images',n,'| avec accent',round(100*sum(x>=3/(W*H) for x in part)/n,1),'% | surface moyenne',round(100*sum(part)/n,2),'% | maximale',round(100*max(part),2),'%')
"
# C. coupes sur la grille : écart maximal, en % de la période (BPM du kit : 130)
python3 -I - <<'FIN'
import re
B = 60 / 130
s = open('index.html', encoding='utf-8').read()
e = [abs(t - round(t / B) * B) / B * 100 for t in map(float, re.findall(r'class="clip" data-start="([0-9.]+)"', s))]
print('écart max', round(max(e), 1), '% de la période')
FIN
```

Essayé sur `examples/reel-court/` (130 BPM, accent `#0B7A5F`) : A donne `YAVG=9.69` (pas une boucle : le film finit sur une carte) ; B donne 249 images, accent présent sur 100 % d'elles, surface moyenne 0,14 %, maximale 0,44 % ; C donne 2,5 % de la période, donc sous 5 %. Contrôles positifs : pour C, le début de la scène 3 décalé d'un tiers de temps (4,15 à 4,3038 s) dans une copie fait lire 32,5 % ; pour B, un accent d'une autre couleur (200, 30, 30) fait lire 0 %.

