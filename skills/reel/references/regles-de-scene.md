# Règles de scène communes à toute vidéo

Dans cette fiche, « le kit » veut dire la charte de ta marque (`../modeles/charte.md`) : ses couleurs, ses polices, son ton et ce qu'elle s'interdit.

Les règles qui valent pour tout reel et tout montage, quel que soit le kit, qui peut les durcir, jamais les assouplir. Sans mention, une règle est une convention décidée ; les autres sont dites (mesuré sur des films de référence) ou (plateforme, à revérifier).

## 1. Le cadre 9:16

| Règle | Valeur |
|---|---|
| Format | 1080x1920, H.264, 30 i/s, 3 à 90 s, 300 Mo au plus (Reels Instagram, plateforme) (sources W16) ; 60 i/s pour le rendu premium (un mouvement rapide, une caméra 3D), à 20 Mbit/s (`hyperframes.md`, section 6) |
| Composition | pile verticale : une idée par écran, typo grande, centre de gravité au tiers haut du milieu ; le hook y tient, y=300 à 900 |
| Recadrage d'un 16:9 | interdit : on recompose la scène |
| Zones de sécurité | 150 px en haut, 150 px à droite (boutons), 420 px en bas : tout texte entre y=170 et y=1500, et entre x=80 et x=930 (en comparaison, Meta demande pour une publicité Reels qui porte une mention légale de laisser libre le bas de 40 %) (sources W31) |
| Zone des sous-titres | réglée par le kit ; par défaut y=1150 à 1350, jamais sur un visage ni sous y=1500 |
| Couverture | la première image sert de vignette, jamais vide ; la grille du profil rogne 240 px en haut et en bas (vignettes 3:4) : titre, logo et visage entre y=240 et y=1680 (plateforme) |
| Texte (corps à 1080 px) | titre et hook 90 px et plus ; appui 48 à 56 px ; sous-titres animés 70 à 110 px en gras avec contour (sources W29) ; microtexte 22 px et plus |

## 2. Le temps

| Règle | Valeur |
|---|---|
| Image 0 | jamais noire, jamais un logo, jamais statique (au moins un zoom de 1,0 à 1,05 sur 0,3 à 0,5 s vers le hook) : elle porte déjà le hook ; un même dispositif de hook s'use en 3 à 4 semaines (hypothèse de praticien) (sources C8) |
| Hook | le spectateur décide en 1,3 s environ (hypothèse de praticien) : hook lisible son coupé avant 1,3 s, sur deux dispositifs superposés (texte plus image ou mouvement) ; un hook visuel retient 2,4 fois mieux à 3 s (hypothèse de praticien, non remesurée) (sources C8) |
| Repère de marque | un repère du kit visible avant 2 s (accent, objet conducteur, visage habituel ; mesuré : seules 61 % des 620 publicités de créateurs (sources W23), parmi 1 217 publicités TikTok payantes (sources W24), ont un repère de marque avant 2 s), jamais un logo plein écran en ouverture |
| Milieu | entre 3 et 20 s, ouvrir une deuxième question ou changer de rythme avant de payer la première ; le paiement final vaut la promesse, chiffre à l'appui |
| Densité | un changement visuel tous les 1,5 à 2,5 s (mesuré sur 4 films) (sources C1), chacun montrant une information nouvelle ou précisée (§ 12) ; un praticien donne 1,5 à 3 s (sources W28) ; sans rien à montrer, le film raccourcit au lieu de se remplir d'effets ; des scènes de longueurs différentes, car un rythme parfaitement régulier lasse |
| Coupes (plans filmés) | 10 à 25 par minute, une toutes les 2,4 à 6 s (repère indicatif, corrélation : les vidéos à 10 à 25 coupes font 1,53 fois les vues habituelles du compte, sur 234 vidéos de comptes de commerces, de marques et de créateurs, TikTok surtout, 1,16 sur les Reels) (sources W22) ; sur 50 TikTok face caméra, médiane d'environ 20 coupes par minute, et un rythme plus élevé baisse le visionnage soutenu (sources W27) ; entre deux coupes, la densité se porte par des événements dans le plan (poussée vers un détail, entrée d'un élément) ; l'écart sans événement ne dépasse pas l'intervalle du kit (§ 11) |
| Calage musical | typo cinétique : un mot par temps, 0,42 à 0,47 s, soit 128 à 144 BPM (mesuré sur 2 films) (sources C1) |
| Temps de lecture | environ 1/3 s par mot ; un mot-clé final jamais moins de 1,3 s ; une carte d'étape jamais moins de 0,8 s (seuils à calibrer) (sources W95, W34, W82) |
| Une seule horloge | une timeline unique (les temps de la beat map) lue par le rendu, les sous-titres et le son ; la durée se déduit de la voix ou de la musique |
| Pause | aucune image sans mouvement plus de 0,8 s (sauf la chute d'un gag : 0,5 s de silence) ; le mouvement va vers l'information qui compte, jamais au hasard |
| Relance | un tournant à mi-film (deuxième question, révélation) : un changement d'échelle, de thème ou de lumière n'est permis que s'il dit ce tournant (§ 12) |
| Fin | carte de fin d'au moins 1,5 s, ou boucle parfaite (dernière image = première) |

## 3. La couleur et la typo

- **Un seul accent par film**, celui du kit : il marque l'objet conducteur et le mot clé de chaque scène, rien d'autre.
- **Deux familles de police au plus**, plus une mono pour le microtexte (grasse contre serif italique, ou grasse contre mono).
- **Contraste du texte sur son fond : 4,5:1 au minimum (AA), mesuré.** Seule exception : 3:1 pour un titre de 90 px et plus (le WCAG 1.4.3 l'admet dès 24 px). Sous-titres, appui et microtexte restent à 4,5:1 : ils se lisent en mouvement.

## 4. Le mouvement

- **Le contenu commande le mouvement** (§ 12) : direction, échelle, vitesse et ordre disent quelque chose (ce qui monte augmente, ce qui grandit compte). Un mouvement qui ne dit rien est retiré.
- Tout mouvement est calculé depuis le temps (HyperFrames, Remotion) : rendu identique à chaque export, sans transition CSS ni minuterie.
- **Un archétype de mouvement par kit** : Playful 0,15 à 0,3 s avec 10 à 20 % de dépassement ; Premium 0,35 à 0,6 s sans dépassement ; Corporate 0,2 à 0,4 s avec 0 à 3 % ; Energetic 0,1 à 0,25 s avec 15 à 30 %. Par défaut, ressort sans rebond (bézier 0.16, 1, 0.3, 1).
- Entrée en ease-out, sortie en ease-in (65 à 75 % de l'entrée), jamais de linéaire sur un déplacement ; caméra en ease-in-out. Zoom : échelle interpolée de façon géométrique, sinon il paraît ralentir en grandissant.
- Un seul héros en mouvement, 2 ou 3 éléments actifs au plus. Le fond ne bouge (20 à 30 % de la vitesse du héros) que s'il donne une information de profondeur.
- Chaque transition naît d'un élément déjà à l'écran (ligne qui ouvre, point qui grandit, forme qui se transforme, coupe sur l'action) ; jamais de transition « de logiciel » (cube, page qui tourne).
- Une famille de mouvements par film ; le spectaculaire se garde pour un seul moment, en général la preuve ou la révélation.

## 5. Le texte à l'écran et les sous-titres

- Le film se comprend son coupé : le texte à l'écran porte le message seul (70 à 85 % des vues, hypothèse de praticien) (sources C8). Le hook est un titre, pas un sous-titre : sa propre zone, sa propre taille.
- **Sous-titres** : 3 mots à la fois de préférence, un mot clé en accent par phrase, synchronisés à moins de 0,2 s. Quand les règles se contredisent, l'ordre est : 1. la coupe et la ligne (un groupe ne passe jamais sur une coupe ni sur deux lignes) ; 2. 0,8 s minimum par groupe ; 3. l'expression entière, qu'on ne sépare pas ; 4. les 3 mots. Un groupe de 4 mots est donc permis quand 3 mots dureraient moins de 0,8 s : au-delà de 150 mots par minute, 2 mots durent moins de 0,8 s (groupes de 3) ; au-delà de 225, 3 mots aussi (groupes de 4).
- Débit de lecture : environ 14 caractères par seconde pour une voix lente de narration, 17 à 20 pour 175 à 200 mots par minute ; le kit fixe le style, avec une seule police pour les deux passes.
- Un texte à lire apparaît d'un bloc, jamais en machine à écrire lente ; lettre par lettre seulement pour un mot qui devient un autre et pour les mots isolés de la typo cinétique.
- **Jamais de texte seul sans visuel animé** (graphique, icône, logo, interface : § 13). Jamais de tiret cadratin ni demi-cadratin. Jamais plus de 3 lignes de texte à la fois (hors carrousel).
- **Le décompte de « 8 mots et 3 lignes à la fois »** : compte tout texte écrit pour être lu (titre, texte d'appui, étiquette d'un ou deux mots, mot isolé). Ne comptent ni la source en microtexte (c'est une preuve, § 7), ni le repère de progression (« 1/3 », « 2/5 »). Un repère ajouté sur une scène déjà à 3 lignes ou à 8 mots reste donc permis ; une étiquette, non.

## 6. Le son

- Une musique au tempo net, choisie avant le montage ; les événements visuels sont calés sur ses temps. Un bruitage se pose sur une information qui arrive à l'image, jamais sur une coupe qui n'apporte rien (§ 12).
- **Niveaux, une seule cible** : le master à -14 LUFS intégré et -1 dBTP au plus, sans écrêtage (sources W14) ; c'est lui qu'on mesure (`ebur128`) et qui juge. La voix se règle pour l'atteindre : seule, elle mesure environ -14,3 LUFS, car la musique 12 dB dessous ajoute environ 0,3 LU. La musique joue à -18 LUFS quand elle est seule (ouverture, fin) et descend à 12 dB sous la voix quand la voix parle (ducking).
- **Une musique fournie** se ramène à -18 LUFS seule avant d'être posée : `ffmpeg -i musique.wav -af loudnorm=I=-18:TP=-2:LRA=11 -ar 48000 musique-18.wav` (sans `-ar`, `loudnorm` sort en 192 kHz). Relire le résultat : `ffmpeg -nostats -i musique-18.wav -af ebur128=peak=true -f null -`, ligne `I:` (cible -18,0 LUFS).
- **« Le son le plus fort du film »** s'entend en loudness à court terme (fenêtre glissante de 3 s, colonne `S` d'`ebur128`), pas en crête d'échantillon. Le maximum de `S` sur tout le film se lit avec la commande ci-dessous ; la fenêtre de 3 s qui finit à l'instant rendu doit recouvrir le gros payoff (§ 11) : `ffmpeg -nostats -i film.mp4 -vn -af ebur128 -f null - 2>&1 | awk '/ S: *-?[0-9]/ { match($0, /t: *[0-9.]+/); t = substr($0, RSTART + 2, RLENGTH - 2) + 0; match($0, /S: *-?[0-9.]+/); s = substr($0, RSTART + 2, RLENGTH - 2) + 0; if (n++ == 0 || s > m) { m = s; mt = t } } END { print "crête S", m, "LUFS, fenêtre qui finit à", mt, "s" }'`.
- Un son tendance démarre dans la première demi-seconde et s'ajoute au moment de publier, jamais incrusté dans le fichier (sources W46) : livrer une version sans musique. La musique d'Instagram est réservée à un usage non commercial : exclue sur toute pièce qui mène à une offre (mot-clé d'appel, lien, produit) (sources W49). Repli : Meta Sound Collection (sources W47) ; sur TikTok, la Commercial Music Library (sources W48). Source et licence de chaque piste : dans la fiche de la pièce.

## 7. La preuve

- Une preuve par pièce : chiffre sourcé, capture réelle, démonstration filmée, avant/après ou verdict argumenté.
- Une capture d'écran se filme comme un objet (inclinaison, poussée de caméra, curseur qui clique), jamais posée à plat sans mouvement.
- Un chiffre affiché porte sa source en microtexte ou dans la légende.

## 8. La carte de fin

1,5 à 2 s. Elle porte la signature du kit, une phrase, et le mot-clé d'appel en accent s'il y en a un. L'objet conducteur revient (le point, le curseur, le tampon). La signature sonore du kit joue, si elle existe.

## 9. Les signes de slop, refusés partout

Une vidéo faite par une IA se trahit par les mêmes tics (sources W42, W33), chacun motif de refus.

- Dégradé violet par défaut, glow ou particules décoratifs.
- Un effet qui ne montre aucune information du contenu (§ 12) : secousse, flash, glitch, whoosh sur une coupe vide, transition ajoutée « pour le rythme ».
- Fausse interface, faux tableau de bord, faux chiffre : on montre la vraie, ou un schéma assumé comme schéma.
- Texte animé qui ne désigne rien ; plus de 8 mots ou de 3 lignes à l'écran à la fois (décompte au § 5).
- Tics de cadre : étiquettes de coin, faux timecodes, « SYSTEM ONLINE », cadres de visée sans raison (sources W33).
- Une seule vitesse de mouvement du début à la fin, zoom sans motif.
- Sous-titres qui sautent mot par mot, un zoom à chaque phrase.
- Une fonction décrite par une phrase au lieu d'être montrée en action.
- Première image vide, fin abrupte sans carte ni boucle.

## 10. La vérification avant export

1. Rendre une image par temps de la beat map, les regarder toutes, vérifier sur elles les zones de sécurité (calque de marges).
2. Écouter le film en entier avec le son, puis sans.
3. Lire la colonne « montre » de la beat map, puis compter les récompenses (§ 11) : la première avant 3 s, jamais plus de 5 s sans récompense, un seul gros payoff dont le début tombe entre 60 et 80 % de la durée.
4. Puis seulement l'export complet, et le contrôle de qualité par un relecteur séparé.

## 11. La récompense : la dopamine de la clarté

**Le principe.** La dopamine signale l'écart entre ce qu'on attendait et ce qui arrive, et comprendre en fait partie (le « aha »). Ces études (sources E14, E15, E16) portent sur un insight trouvé par la personne, pas sur une vidéo : y voir un gain de clarté est une hypothèse maison. Ce qui est soutenu : le cerveau a besoin du temps de prédire, donc la question, un court temps, puis la réponse. Jamais un effet constant : un pic permanent habitue et devient le slop du § 9.

| Règle | Valeur |
|---|---|
| Promesse | le hook ouvre la boucle principale, payée au gros payoff (`hooks.md`) |
| Micro-récompense (R) | une information qui devient claire et termine quelque chose : coche, chiffre qui atteint sa valeur, pièce qui s'emboîte, avant/après, mot clé qui tombe quand il est dit, avec son son. Un mouvement qui ne clarifie rien n'en est pas une |
| Cadence | la première R avant 3 s ; ensuite une R là où une information devient claire, écart maximal = intervalle du kit, jamais plus de 5 s ; jamais une R posée pour tenir l'intervalle (§ 12) |
| Surprise | une R sur trois au moins arrive 20 % plus tôt que la médiane des intervalles, ou est plus grande que la précédente |
| Boucles | une question posée, fermée en 5 s au plus ; la suivante s'ouvre avant que la précédente se ferme (la fermeture en 5 s et l'enchaînement sont une convention maison ; corrélation, directionnel : une boucle ouverte dans le hook va avec 1,46 fois les vues habituelles du compte, porté par TikTok, 1,03 sur les Reels) (sources W22) |
| Respiration | 0,5 à 1 s plus calme juste avant le gros payoff : moins de mouvement, son qui se retire, jamais immobile |
| Gros payoff | un seul ; pour un reel de valeur ou d'enquête (explainer, liste, enquête), son début, l'instant où le résultat promis devient lisible, tombe entre 60 et 80 % de la durée ; pour une news, une publicité ou un film cinématique, aucun seuil : la révélation peut tomber avant 3 s (sources C9) (convention maison, inférence de 55 à 85 % mesurés sur 13 shorts YouTube par un vendeur d'outil) (sources W26) (ce qui le suit dans sa scène, comme la dernière coche, peut passer 80 %) : le résultat, le verdict ou la transformation promis, rendu évident ; l'accent à sa plus grande surface, le son le plus fort du film (crête de loudness à court terme mesurée par `ebur128`, § 6). Une pièce muette n'a pas de son : son payoff se marque par la plus grande surface d'accent de la pièce et le plus gros changement d'image (écart le plus grand entre deux images consécutives), et la carte de validation le dit |
| Son et couleur | chaque R a son son, posé à l'instant de son événement dans la timeline unique ; l'accent arrive avec l'information qui compte et ne décore jamais |
| Progression | au-delà de 20 s, un repère de progression visible (étape 2/5, jauge, compteur) à 25, 50 et 75 % de la durée |

Les instants des R se relèvent sur le rendu, chacun avec l'information rendue claire sur l'image extraite. Valeurs à recalibrer à 7 jours.

**Le kit fixe l'intensité et ses interdits.** L'intervalle entre deux récompenses va de 1,5 à 2,5 s (intensité maximale) à 4 à 5 s (intensité douce). Le kit dit ce que sa marque n'emploie jamais : un effet qui dramatise un risque de santé, une stimulation dans un produit du coucher, une tactique visible (compte à rebours, fausse rareté) devant un public averti.

## 12. Le contenu commande l'effet

Chaque effet, visuel ou animation montre une information du contenu (chiffre, comparaison, étape, cause, preuve, verdict, moment d'histoire). Ce qui ne montre rien est un décor, et un décor se retire. Pourquoi : une animation aide quand sa forme épouse la structure de ce qu'elle explique (sources E13) ; les détails hors sujet font baisser la compréhension (sources E17, E18) ; souligner l'essentiel aide à retenir (méta-analyse de 103 études : g = 0,53 en rétention) (sources E12).

| Le contenu dit | L'animation qui le montre | À éviter |
|---|---|---|
| une quantité, un chiffre | le chiffre qui atteint sa valeur, une barre à la bonne échelle, la source en microtexte | un compteur qui défile sans unité ni source |
| une comparaison | les deux côte à côte, à la même échelle, le meilleur s'allume | deux échelles différentes |
| une évolution | une courbe qui se trace dans le sens du temps, au rythme de la voix | une courbe d'un bloc |
| une suite d'étapes | les étapes qui se cochent dans l'ordre, repère « 2/5 » | toutes les étapes à la fois |
| une cause, une relation | une flèche de la cause à l'effet, deux pièces qui s'emboîtent | des liens qui clignotent |
| une transformation | l'après qui remplace l'avant à la même place (morph, volet, coupe raccord) | un fondu au noir entre deux scènes |
| un détail qui compte | une poussée vers le détail, le reste qui s'atténue | un zoom sans motif |
| une preuve | la vraie capture qui entre, le passage surligné, la source | une fausse interface |
| une hiérarchie | la taille et l'ordre d'entrée suivent l'importance | tout à la même taille, en même temps |
| un verdict | une marque qui tombe (tampon, jauge, mot final), une fois, après les preuves | un verdict avant les preuves |
| un moment d'histoire | le moment lui-même : la lampe s'allume quand la nuit tombe | une transition sans lien avec le récit |
| un espace, un système | une vue isométrique ou 3D, seulement quand l'espace porte l'information | de la 3D pour décorer |

- **Le test de la colonne « montre »** : chaque événement de la beat map nomme l'information qu'il montre ; case vide, événement retiré.
- **La clarté passe avant le rythme** : sans information nouvelle pour le prochain temps, la scène raccourcit, jamais un effet pour tenir la cadence.
- **L'ordre d'apparition suit l'ordre de compréhension** : la question avant la réponse, la cause avant l'effet, les preuves avant le verdict. Le hook cache la réponse, jamais la question : l'image 0 montre ce qui est en jeu.
- **Dispensés, car ils servent la lisibilité** : le punch-in qui masque une coupe en prise de personne parlante, le repère de marque avant 2 s, la carte de fin ou la boucle. Rien d'autre.
- **Le style habille l'information, il ne la remplace pas** : couleurs, polices et mouvement du kit s'appliquent à ce que la grammaire a choisi.

Les effets de chaque information : `effets.md`.

## 13. Les exigences de rendu

Ces neuf exigences visent le rendu, pas le mécanisme, et valent pour toute pièce ; un kit peut les durcir (pas d'emoji dans un appel à l'action, par exemple). Contrôle : sur l'image extraite.

| Exigence | Règle |
|---|---|
| Jamais un texte seul | chaque texte arrive avec un visuel animé qui montre la même information : graphique, logo, icône, capture, emoji si le kit le permet (sauf les sous-titres de la voix sur une prise de vue) |
| Une interface de niveau professionnel | toute interface montrée (même reconstruite) suit les règles d'UX : une seule action dominante, un retour visible après chaque action, la position « n sur total » dans un parcours à étapes, une fin confirmée, un texte lisible sur téléphone |
| Un vrai mockup d'iPhone | un cadre d'iPhone reconnaissable (bords, boutons latéraux, îlot ou encoche), jamais un rectangle arrondi ; l'écran porte la vraie capture |
| Les vrais blocs des outils | un prompt ou un outil se montre par une capture réelle et datée de l'outil utilisé ; reconstruction seulement si la capture est impossible, alors fidèle au pixel |
| La source à l'écran seulement pour les news | la source posée à côté du commentaire (`split-source`) n'est employée que dans une pièce d'actualité ; ailleurs, la source se lit en microtexte (§ 7) |
| Des illustrations riches | des icônes, des graphiques animés et, si le kit le permet, des emojis ; jamais une scène réduite à un aplat et un titre |
| Jamais un contour fin pour désigner | désigner par un projecteur qui assombrit le reste, un zoom ou une étiquette ; jamais un cadre fin ni des coins |
| Aucun flou posé par nous | ce qui ne doit pas se voir se remplace (une donnée de démonstration, un aplat plein, la surface voisine) ou sort du cadre, jamais flouté ; le mot qui compte se désigne par son poids, son échelle ou un projecteur qui assombrit le reste, jamais par un flou qui se résout ; aucun verre dépoli dans nos calques ; une vraie capture d'interface garde son rendu d'origine |
| Jamais une boîte plate sur l'image | sur une prise de vue ou un plan généré, un texte ou une interface se pose dans la scène (derrière la personne détourée, sur l'écran en perspective, avec son ombre), jamais une boîte sombre plate ni un carton noir à la place d'une image ; chaque information arrive sur une image du film, la carte de fin mise à part |

## 14. Le waou : une barre écrite, regardée par un autre

Sans barre écrite, « waou » reste un goût. Une pièce a du waou quand elle réunit trois conditions (point de départ, à affiner) :

1. au moins un effet éprouvé (statut de `effets.md`, ou conservé par le kit), posé sur une information réelle de la pièce. Les sous-titres (`caption-keyword`, `caption-payoff`, `caption-story`) ne comptent pas : ils sont dans toute pièce ;
2. au moins une transition motivée par le contenu : elle relie deux états de la même chose (§ 4 et § 12), jamais un spectacle posé entre deux plans ;
3. un payoff visuel unique, montré avant la fin : le gros payoff du § 11, dont le début tombe entre 60 et 80 % de la pièce.

**Le contrôle, en deux temps.** Mesuré : la session relève sur la beat map et les images extraites l'id de l'effet éprouvé, l'événement de la transition (il nomme les deux états qu'elle relie) et l'instant du payoff ; une condition manque, la pièce repart. Jugé : un évaluateur séparé, qui n'a pas fabriqué la pièce, puis la personne qui valide, répondent sur trois images extraites à « un motion designer expert aurait-il signé cette pièce ? ». Le fabricant ne choisit pas seul ces images : la première image, l'image du payoff (l'instant relevé au mesuré) et une image tirée au hasard parmi les images extraites, par l'évaluateur ou par un tirage de la session. Un non motivé est un refus. Si le refus demande ce qu'une règle écrite interdit (zone de sécurité, texte d'appui de 48 à 56 px, source exigée à l'écran), la règle écrite gagne : la pièce ne bouge pas contre elle, le refus est noté tel quel dans la carte de validation avec la règle qui le contredit, et la pièce va à la décision humaine de la personne qui valide. Le mesuré empêche que le waou manque, il ne le prouve pas : le rapport dit « jugé à l'œil ». Chaque kit porte, dans ses recettes, une ligne Waou : ce qui rend une pièce de sa marque « waou », en une ou deux phrases mesurables ou regardables, avec les effets conservés ou éprouvés de sa marque.
