# Catalogue d'effets vidéo : chaque effet montre une information

Dans cette fiche, « le kit » veut dire la charte de ta marque (`../modeles/charte.md`) : ses couleurs, ses polices, son ton et ce qu'elle s'interdit.

Ce catalogue dit quel effet montre quelle information, comment le fabriquer et quel garde-fou le tient. Il sert à écrire la beat map d'un reel ou d'un montage : chaque événement nomme l'information qu'il montre et l'id de l'effet qui la montre. Les ids sont stables. « § N » désigne toujours la section N de `regles-de-scene.md`, y compris § 5, § 6 et § 7, qui ont un homonyme dans ce fichier ; les sections de ce fichier se citent par leur titre. Ta charte dit quels effets ta marque garde ou refuse (`../modeles/charte.md`, ligne « Effets ») : ce catalogue ne le dit jamais.

## 1. Comment s'en servir

### La marche à suivre

1. **Nommer l'information** que l'événement montre, dans la colonne « montre » de la beat map. Pas d'information, pas d'effet (§ 12).
2. **Aller à la famille** de cette information, dans le catalogue ci-dessous.
3. **Prendre un effet permis par le kit** (son fichier d'effets). Jamais un effet `à juger`, jamais un effet écarté. Sans kit : un effet `éprouvé` est permis, un effet `à l'essai` se signale à la validation.
4. **Écrire son id** dans la beat map et **tenir son garde-fou**. Si le garde-fou ne peut pas être tenu (pas de vraie capture, pas de source, pas de personne filmée), l'effet est retiré, jamais remplacé par un décor.
5. **Poser le son** de la famille (voir « Le son de chaque famille ») : un son par information, jamais par plan.

Le contrôle avant export vérifie que chaque effet de la beat map est un id de ce fichier, permis par le kit ; les effets à l'essai sont nommés dans le compte rendu de validation.

### Les statuts génériques

| Statut | Sens | Ce qu'on peut en faire |
|---|---|---|
| `éprouvé` | validé par un vote sur une pièce rendue, pour au moins une marque | s'en servir ; le vote vaut pour le mécanisme, le rendu doit passer § 13, le garde-fou de la ligne reste en vigueur |
| `à l'essai` | jamais voté sur une pièce rendue | s'en servir à l'essai, et le signaler à la validation |
| `à juger` | mécanisme gardé, rendu refusé ou jamais jugé | ne pas s'en servir avant un nouveau rendu, aux jetons du kit, puis jugé |
| `écarté` | interdit | jamais, sans accord écrit et daté |

Pour une marque, le statut du kit prévaut : un effet `éprouvé` ailleurs est à l'essai pour elle tant qu'elle ne l'a pas voté. Le kit range chaque effet (conservé, à l'essai, interdit), dit si une personne filmée est permise, et fixe l'intensité et ses interdits (exemples : toute secousse, un compteur qui défile).

### La colonne « Personne filmée »

- **oui** : une prise de la personne face caméra est nécessaire (ou, si le kit le permet, un rendu d'avatar de cette personne, avec l'étiquette « IA » à l'écran). Le montage en dépend : sans cette prise, l'effet n'a pas de matière. Un kit sans visage (mascotte) ou sans vraie personne l'exclut : l'effet est retiré.
- **non** : l'effet marche sur un objet, une capture, un document, une illustration ou une voix seule ; une personne peut y figurer, elle n'est pas requise.

## 2. Le catalogue, par information montrée

Les familles suivent la grammaire du § 12, plus l'appel à l'action et la continuité du film. Fabrication : les chiffres 1 à 3 sont les rangs de « L'ordre de fabrication » ; un rang absent n'a pas de sens pour l'effet. Les noms entre apostrophes inverses sont des composants du registre HyperFrames ou des commandes `npx --yes hyperframes@0.8.167`. Un effet `à juger` se fabrique à la main : aucun composant du registre ne le fait.

### Une quantité, un chiffre

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `count-up` | un chiffre qui monte jusqu'à sa valeur, avec son unité ; variante : les chiffres montent un par un, comme un compteur kilométrique | à l'essai | non | 2 `count-up`, `number-wheel`, `mk-progress-stat` | valeur finale vraie, unité et source en microtexte (§ 7) ; jamais un compteur qui défile sans unité ni source (§ 12) |
| `stat-card` | un chiffre posé d'un bloc, avec son unité et sa source | éprouvé | non | 2 `number-pop-in`, `pull-back-reveal` | un chiffre par écran, compté ou mesuré, source visible (`regles-de-scene.md` § 7) ; un chiffre que la personne dit comme une consigne (« on coupe à 25 minutes ») est une consigne, pas une mesure : il s'affiche comme tel (« consigne : 25 min »), sans source externe ; jamais un gain promis sans preuve |
| `bar-grow` | des quantités comparées par des barres à la bonne échelle | à l'essai | non | 2 `animated-bar-chart`, `chart-story`, `data-chart` | même échelle pour toutes les barres, valeurs et source lisibles (§ 12) |
| `data-stack` | plusieurs mesures du même sujet, en cartes empilées qui arrivent chacune sur le mot qui la nomme | à l'essai | non | 2 `notification-stack`, `animated-bar-chart`, `data-chart` | une carte par mesure, barres à la même échelle d'une carte à l'autre, unité et source lisibles ; 3 cartes au plus à la fois (§ 5) |
| `orbit-collection` | l'ensemble des pièces réelles de la marque, réunies autour ou derrière le sujet (ses reels en orbite autour de la personne) | à l'essai | non | 1 les vraies pièces et une prise du sujet ; 2 `three-orbiting-cards`, `stagger-cascade`, `npx --yes hyperframes@0.8.167 remove-background` | de vraies pièces seulement (reels publiés, écrans réels), jamais des cartes de décor ; sans personne, le sujet est un objet, un logo ou une interface |
| `hud-data` | une donnée réelle lue à sa source, en microtexte mono : compteur qui atteint sa valeur, étape réelle « 2/5 », source | à l'essai | non | 1 la donnée réelle capturée (journal, compteur, chiffre de l'outil) ; 2 `telemetry-hud` (lignes étiquette et valeur, sans les coins du composant) | seulement une donnée vraie, montrable à sa source ; mono de 22 px au moins, sans coins de cadre ni timecode (§ 9) ; sans donnée vraie, c'est `fake-hud` (écartés) ; le kit doit avoir une police mono |
| `visual-metaphor` | un tri : des éléments en désordre qui se rangent en trois groupes | à juger | non | 3 à la main | chaque groupe porte un nom et un nombre, jamais des volumes de décor (§ 9) |

### Une comparaison

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `comparison-split` | deux états côte à côte, à la même échelle, le meilleur qui s'allume | éprouvé | non | 2 `split-tilt-cards`, `focus-swap` | même échelle et même cadrage des deux côtés (§ 12) ; une affirmation à vérifier se montre avec sa réfutation dans la même scène |
| `clone-dialogue` | deux positions ou deux avis de la même personne dans le même cadre : des copies d'elle apparaissent à côté, sur ses mots | à l'essai | oui | 1 deux prises au trépied, cadre identique, puis le plan vide ; 2 `npx --yes hyperframes@0.8.167 remove-background` | chaque copie dit une information différente (objection et réponse, avant et après), jamais un gag ; un effet filmé par pièce au plus |
| `knockout-tiles` | des options nommées tombent en tuiles, puis sont écartées une à une jusqu'à celle qui reste | à l'essai | non | 1 une prise du sujet, ou un fond de marque ; 2 `npx --yes hyperframes@0.8.167 remove-background`, `stagger-cascade` | une tuile par option réellement comparée, avec son logo ou son icône (§ 13) ; une option sort quand la voix dit pourquoi ; 3 tuiles à la fois au plus (§ 5) |

### Une évolution

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `chart-line` | une valeur qui change dans le temps : la courbe se trace dans le sens du temps | à l'essai | non | 2 `mk-line-graph`, `chart-story` | axes, unités et source lisibles ; tracé calé sur la voix, jamais d'un bloc (§ 12) ; la montée vive tombe sur le mot dit |

### Une suite d'étapes

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `checklist-sync` | les étapes se cochent dans l'ordre, au moment où elles sont dites | à l'essai | non | 2 `mk-specs-list`, `success-check`, et `marker-checklist-card` pour un style marqueur | une coche par étape réellement faite ou dite, ou, pour des éléments extraits (tâches relevées, points listés), par élément réellement montré à l'image à cet instant ; jamais décorative ; repère « 2/5 » (§ 12) |
| `chapter-pill` | où l'on en est dans le film : la pastille de chapitre | à l'essai | non | 2 `tabs-slide-indicator` | utile au-delà de 20 s (§ 11) ; un repère d'étape (« n/total », ou trois repères nommés au format court), jamais un compteur qui défile |
| `screen-speedup` | un processus réel et long, compressé à l'écran, son facteur et sa durée réelle lisibles | à l'essai | non | 1 l'enregistrement d'écran réel, accéléré au montage à facteur constant ; 2 `cursor-zoom-follow` pour revenir à la zone qui compte ; 3 l'étiquette du facteur et de la durée, aux jetons du kit (aucun composant de vitesse connu) | facteur et durée vrais, à l'écran pendant tout l'accéléré ; facteur constant, jamais une courbe de vitesse ; retour à la vitesse réelle quand le résultat ou l'erreur arrive ; jamais un échec coupé |
| `step-teleport` | une suite d'étapes jouée par le sujet qui apparaît à chaque position | à l'essai | oui | 1 une prise au trépied : un pas, une pause, puis le plan vide | une position égale une étape nommée ; pause de 5 à 10 s à chaque pose au tournage ; un effet filmé par pièce au plus |
| `type-number` | un grand numéro qui guide une suite de pièces distinctes | à juger | non | 3 à la main | le numéro compte de vraies étapes, jamais un numéro décoratif |
| `timeline-progress` | trois étapes sur un rail vertical qui avance | à juger | non | 3 à la main | ni chiffre ni score inventé ; texte d'interface lisible sur téléphone (§ 13) |
| `living-index` | la liste entière et la place de l'élément qui joue : tous les noms lisibles dès l'image 0, celui qui joue s'allume, une pastille n/N le double | à l'essai | non | 1 les noms réels ; 2 `tabs-slide-indicator` pour la pastille ; 3 l'allumage du nom actif, à la main | pour une liste numérotée seulement ; noms lisibles à la vignette de 350 px de large, 17 au plus, au delà on groupe ; un seul nom allumé, celui que la voix dit, pastille n/N exacte ; un accent unique |
| `tag-build` | une liste dite qui se construit autour de la personne ou de l'objet : chaque élément en pastille posée sur son mot, l'élément dit allumé, les précédents atténués à 40 % | à l'essai | non | 2 `stagger-cascade` ; 3 la place des pastilles, à la main | chaque pastille arrive sur son mot (0,15 s avant au plus) ; posées sur une zone calme et sombre de l'image (vêtement, fond), jamais sur le visage ni les mains ; sept pastilles au plus ; icônes d'une seule famille ; 24 px d'encre au moins et 4,5:1 de contraste (sources C12) |

### Une cause, une relation

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `cause-arrow` | la cause qui mène à l'effet : une flèche de l'un à l'autre | à l'essai | non | 2 `tracing-beam`, et `hw-arrow` pour une flèche manuscrite | relie deux éléments réels de l'écran, de la cause vers l'effet (§ 12) ; jamais des liens qui clignotent ; la flèche manuscrite est un choix du kit |
| `ui-prompt` | la commande donnée à l'outil, avec le résultat qu'elle produit | éprouvé | non | 1 enregistrement d'écran de l'outil réellement utilisé ; 2 `typed-prompt`, `claude-exchange`, `agent-cursor` | de vrais blocs : capture de l'outil utilisé, datée ; reconstruction seulement si la capture est impossible, alors fidèle au pixel (§ 13) |
| `background-orbit` | des éléments reliés à un noyau commun | à juger | non | 3 à la main | chaque pictogramme nomme une vraie pièce du système, jamais un fond décoratif (§ 9) |
| `background-paper` | trois pièces posées sur papier et reliées entre elles | à juger | non | 3 à la main | la matière papier (collage déchiré, carte à ombre décalée) est celle du kit, jamais celle d'un autre |

### Une transformation

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `before-after-wipe` | l'avant puis l'après à la même place, un volet les sépare | à l'essai | non | 1 deux prises réelles au même cadre ; 2 `before-after-wipe` | avant et après réels, jamais un avant fabriqué ; même cadre, même échelle |
| `fade-70` | l'avant et l'après superposés dans le même cadre | à l'essai | non | 1 deux prises au trépied, ou deux illustrations au même cadre ; 3 le plan du dessus à 70 % d'opacité | cadre identique ; 70 % d'opacité ; l'après arrive en fondu de 0,4 s |
| `strike-replace` | l'ancienne valeur barrée, la bonne qui la remplace | à l'essai | non | 2 `strikethrough-replace`, `line-swap` | les deux valeurs restent lisibles ensemble le temps d'être lues (1/3 s par mot, § 2) ; quand le titre et l'étude divergent, chacun garde sa source |
| `action-match-cut` | le même geste ou la même forme relie deux états | à l'essai | non | 1 deux prises raccordées sur le geste ou la forme | le raccord naît du plan, sans cercle ni repère ajouté ; il relie deux états du même contenu (avant puis après, cause puis effet) |
| `word-swap` | une phrase dont le dernier mot est remplacé par un autre : ce qui change, le reste est fixe | à l'essai | non | 2 `kinetic-type-swap`, `text-state-swap` (sortie par une coupe nette ou un fondu court, jamais un flou, § 13) | 3 valeurs au plus, tenues 0,8 s chacune, la dernière 1,3 s au moins (§ 2) ; chaque valeur est une vraie variante du propos, jamais un gag ; lisible son coupé ; un chiffre ou un prix qui change : `strike-replace` ; jamais sur une citation |
| `mask-wipe` | le produit puis son usage, relayés par cinq lamelles qui tournent | à juger | non | 3 à la main | un volet qui ne relie pas deux états du contenu est un décor (§ 9) |
| `transition-match` | un repère circulaire qui passe du plan produit au plan d'usage | à juger | non | 3 à la main | le repère est un cercle ajouté sur l'image : le vrai raccord est `action-match-cut` |
| `vertigo` | l'espace se déforme autour d'un sujet qui garde sa taille (zoom compensé), au moment du tournant | à l'essai | oui | 1 une prise de la personne au trépied, fond avec de la profondeur ; 2 `yt-camera-move` ; 3 la compensation d'échelle, à la main | une fois par pièce, au tournant, jamais un tic ; zoom géométrique (§ 4) ; sujet net, aucun flou ajouté ; aucune secousse |

### Un détail qui compte

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `zoom-screen` | le détail d'une interface qui compte, agrandi puis remis dans son contexte | éprouvé | non | 1 enregistrement d'écran réel ; 2 `cursor-zoom-follow`, `ui-focus-zoom` | détail lisible sur téléphone ; zoom géométrique (§ 4) ; cible à 200 à 300 %, tenue 0,8 s, retour au plan large à l'étape suivante |
| `camera-reframe` | le cadre glisse vers le sujet qui compte | éprouvé | non | 1 un plan filmé avec de la marge ; 2 `yt-camera-move` | un seul mouvement par plan, ease-in-out (§ 4) ; vers l'information, jamais au hasard (§ 2) |
| `punch-in` | le mot ou le détail qui porte l'information, agrandi sur la même prise | à l'essai | non | 1 la prise elle-même ; 2 `yt-camera-move` | 110 à 125 % sur le mot qui porte l'information ; sert surtout à masquer une coupe en prise de personne parlante (dispensé du § 12) ; sur un objet ou une capture, même règle |
| `spotlight-dim` | tout s'assombrit sauf la phrase ou la zone qui compte (variante : la lumière coupe sur une phrase puis revient) | éprouvé | non | 2 `yt-feather-highlight` ; 3 un voile noir animé sur la phrase | le projecteur tombe sur un vrai texte ou une vraie zone de la capture, jamais sur du vide ; remplace le contour fin (§ 13) ; la phrase reste lisible, jamais un fondu au noir entre deux scènes (§ 12) |
| `freeze-label` | l'image figée qui nomme ce qu'elle montre (étiquettes sur l'image figée, ou autocollant annoté à la main) | éprouvé | non | 1 la prise ou la capture figée ; 2 `freeze-frame-dressing`, et `hw-box-label` pour une annotation manuscrite | l'étiquette porte un fait lisible (nom, valeur, source) ; sans la couche flash du composant (§ 9) ; sans personne, on fige une capture ou un objet ; annotation manuscrite, papier et ruban : matière du kit |
| `sticky-text` | le nom ou le titre de la personne, collé à elle et qui la suit | à l'essai | oui | 1 une prise de la personne qui bouge ; 2 `lt-bold-block` ; 3 le suivi du mouvement, à la main (aucun composant de suivi) | l'étiquette porte un fait lisible (nom, titre, valeur), jamais un slogan ; elle désigne sans contour fin (§ 13) |
| `pointer-callout` | les éléments d'un sujet, d'un objet ou d'une capture, nommés par des cartes reliées par un trait | à l'essai | non | 1 une capture réelle, ou une prise de l'objet ; 2 `browser-device-stage`, `grid-card-assemble` ; 3 le trait de liaison et le suivi, à la main | 3 cartes au plus (§ 5), chacune nomme un élément réel ; la carte désigne et le trait la relie, il ne cadre rien (§ 13) ; un style tracé à la main désigne par `marker-circle` et `freeze-label` |
| `marker-circle` | la preuve entourée d'un cercle tracé à la main | éprouvé | non | 2 `marker-highlight`, `hw-callout-circle` | trait épais (6 à 9 px), jamais un contour fin (§ 13) ; entoure ce que la voix dit à cet instant |
| `focus-ring` | le champ ou le bouton visé, cadré par des coins | à juger | non | 3 à la main | les coins fins sont un contour fin (§ 13) : désigner par `spotlight-dim`, un zoom ou une étiquette |
| `selection-box` | le mot du verdict sélectionné comme dans un logiciel de design : une pastille pleine aux couleurs du kit, entourée d'un cadre en pointillés à quatre poignées | à l'essai | non | 3 à la main : la pastille, puis le cadre 0,1 à 0,2 s après | un ou deux mots par pièce, le verdict ou le mot à retenir, jamais un mot qui n'est pas dit ; texte de la pastille à 4,5:1 de contraste au moins ; le cadre reste fin et ne clignote pas (sources C12) |

### Une preuve

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `proof-capture` | la vraie source qui entre dans l'image, le passage utile surligné | à l'essai | non | 1 enregistrement d'écran réel ou capture datée ; 2 `browser-device-stage`, `cursor-zoom-follow`, `inline-highlight`, `x-post` pour un vrai post | capture réelle et datée, filmée comme un objet (§ 7) ; source lisible, données privées masquées ; une capture d'étude n'est jamais retouchée ; le kit dit quelles sources montrer (jamais le post d'un tiers) |
| `app-pull-back` | l'outil qui a produit la pièce : le film recule dans la fenêtre de l'application et on le voit se monter | à l'essai | non | 1 un enregistrement d'écran réel de l'outil de montage, daté ; 2 `pull-back-reveal` (recul de caméra sur la fenêtre de l'outil), `browser-device-stage` | la vraie capture de l'outil utilisé (§ 13), jamais une fausse interface (§ 9) ; un seul recul par film (§ 4) |
| `ui-floating` | l'interface réelle dans son contexte, avec du relief | éprouvé | non | 1 capture réelle ; 2 `browser-device-stage` | interface de niveau professionnel (§ 13) ; jamais une fausse interface (§ 9) |
| `ui-floating-v2` | une capture réelle de l'outil qui alterne avec le prompt et le produit | éprouvé | non | 1 capture réelle de l'outil ; 3 l'alternance capture, prompt, produit, à la main | mêmes exigences que `ui-floating` ; capture réelle datée |
| `ui-world` | l'outil réel qui remplit le cadre, et celui qui l'explique devant lui | à l'essai | oui | 1 un enregistrement d'écran réel et une prise de la personne ; 2 `browser-device-stage`, `npx --yes hyperframes@0.8.167 remove-background` | capture réelle et datée, lisible sur téléphone derrière la personne (§ 13) ; sans personne, voir `ui-floating` et `proof-capture` |
| `ui-result` | le résultat tel que l'utilisateur le verra, dans un téléphone qui arrive à côté et joue un écran | éprouvé | non | 2 `vfx-iphone-device`, `device-frame-stage` | un vrai mockup d'iPhone, jamais un rectangle arrondi (§ 13) ; l'écran montre la vraie capture ; jamais de donnée personnelle réelle : profil fictif |
| `ui-result-v2` | le contenu produit (histoire, résultat) tel qu'il apparaît dans l'application | éprouvé | non | 1 capture réelle de l'application ; 3 cadre iPhone authentique et scène, à la main | cadre iPhone authentique ; profil fictif ; vient après la vue pleine scène, jamais à sa place |
| `split-source` | la source et le commentaire en même temps : la preuve au-dessus de la parole | éprouvé | non | 1 capture réelle de la source ; 3 les deux zones, à la main | réservé aux pièces d'actualité (§ 13) ; ailleurs, la source se lit en microtexte (§ 7) ; celui qui commente : la personne, une mascotte ou aucun visage selon le kit |
| `headline-wall` | ce que plusieurs sources disent du même sujet : un mur de titres (variante : derrière la personne) | à l'essai | non | 1 captures réelles des titres ; 2 `stagger-lattice` | vrais titres, datés, source lisible ; pages publiques, jamais le post d'un tiers |
| `ui-tilt` | la capture filmée comme un objet : l'interface arrive en perspective et se redresse pendant la poussée | à l'essai | non | 1 la capture réelle ; 2 `tilt-card`, `browser-device-stage` | inclinaison de 25 degrés qui finit à plat, texte lisible sur téléphone avant la fin du redressement (§ 7) ; jamais une fausse interface (§ 9) ; la capture n'est pas retouchée |
| `broll-cutaway` | l'objet, l'écran ou le geste dont la voix parle, en plan de coupe à l'instant où elle le nomme | à l'essai | non | 1 un plan filmé ou une capture réelle ; 3 la coupe sur le mot, posée au montage (aucun composant de plan de coupe) | montre la chose nommée, jamais une image d'ambiance (§ 12) ; entre sur son mot, tient 1,2 s au moins pour une capture ; jamais un média de tiers sans droit clair ; jamais un visage identifiable pour illustrer un verdict négatif ; un kit sans visage tourne mains, dos ou décor |
| `pip-presenter` | celui qui explique, en vignette sur l'écran réel ; ou le résultat réel en vignette sous le menton de la personne, à 1,2 s dans le hook | à l'essai | oui | 1 une prise de la personne et un enregistrement d'écran réel ; 2 `browser-device-stage` ; 3 la vignette arrondie, masque à la main (aucun composant d'incrustation) | vignette dans x=80 à 930 et y=170 à 1500, hors de la zone des boutons, jamais sur la zone d'action de la capture ni sur les sous-titres ; sous le menton (vers y=1100), jamais sur le visage ; sur un avatar, l'étiquette « IA » à l'écran |
| `lower-third` | qui parle, quel outil, quelle source : le nom posé près de ce qu'il désigne | à l'essai | non | 2 `lt-kicker-name`, `lt-side-rule`, `lt-clean-bar`, `lt-soft-pill`, aux jetons du kit | un nom par apparition, qui porte un fait lisible : la personne, l'outil ou la source datée (§ 7) ; zone « pied », y=1370 à 1500, jamais sur les sous-titres ; ni `lt-neon-border` (brille), ni `news-ticker` (défile) ; ligne de source sous l'élément sourcé, 22 px au moins |
| `redact-blur` | la preuve sans ses données privées : la zone masquée se voit masquée, le reste reste lisible | à l'essai | non | 1 d'abord ne rien capturer de privé (fenêtre propre, données de démonstration) ; 3 sinon un aplat plein posé au montage, jamais un flou (§ 13) | clés, jetons, e-mails, noms de clients, prénoms, chemins personnels : masqués avant l'export, jamais cachés par un calque qu'on peut ôter ; le masque suit l'élément et couvre toute la durée où la donnée est visible ; un aplat plein, opaque, qu'aucun caractère ne traverse |
| `transition-page` | la page d'annonce puis sa source : une feuille qui se tourne | à juger | non | 3 à la main | une page qui tourne est une transition de logiciel (§ 4), sauf si la page est un vrai document du contenu |
| `showcase-card` | les démonstrations successives de la chose présentée, jouées dans une carte arrondie posée sur la poitrine de la personne pendant que la prise principale ne bouge pas | à l'essai | oui | 1 une prise fixe de la personne, ou un rendu de son avatar ; 2 `browser-device-stage`, `grid-card-assemble` pour la carte (à confirmer dans le registre) ; 3 la carte arrondie sur la poitrine, à la main | la prise principale ne bouge jamais, le visage reste libre ; chaque démonstration est une vraie capture, datée (§ 13) ; pour une liste d'outils ou de réglages seulement |

### Une hiérarchie, la parole

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `caption-keyword` | le mot qui porte l'information, en accent dans le sous-titre | éprouvé | non | 2 `caption-pill-karaoke`, `caption-editorial-emphasis`, `caption-highlight` | un mot clé par phrase (§ 5) ; style, police et corps du kit |
| `caption-payoff` | le résultat qui quitte la ligne basse et devient un bloc central | éprouvé | non | 2 `kinetic-center-build` | jamais un texte sans visuel animé (graphique, emoji, icône ou logo) : le bloc arrive avec un visuel qui montre la même information (§ 13) |
| `split-illustration` | la parole et l'image qui l'illustre, en même temps (la personne passe en bas, tout l'écran montre ce dont elle parle) | éprouvé | non | 2 `grid-card-assemble`, `icon-morph-beat` | icônes, emojis (si le kit les permet) et animations graphiques (§ 13) ; en bas, la personne, une mascotte ou aucun visage selon le kit ; une source à l'écran n'entre pas ici : `split-source`, news seulement |
| `type-wall` | le mot qui porte l'information, géant derrière le sujet et remplacé à chaque mot clé dit | à l'essai | non | 1 une prise du sujet (personne, objet ou capture) ; 2 `npx --yes hyperframes@0.8.167 remove-background`, `kinetic-center-build` | un mot clé par phrase, celui du sous-titre (§ 5), jamais un mur de décor ; devant, un visuel qui montre la même information (§ 13) ; 8 mots à l'écran au plus (§ 9) |
| `beat-words` | les mots clés de l'énoncé, un par temps de la musique, chacun plein écran sur son fond, dans l'ordre où on les comprend | à l'essai | non | 1 pour chaque fond, la capture ou la prise qui montre le même mot ; 2 `caption-kinetic-slam` ; 3 le calage sur la grille (140 BPM : 0,43 s par mot) | 4 mots d'affilée au plus, puis un autre mouvement ; un mot par temps de 0,42 à 0,47 s (§ 2), donc une pièce portée par la musique (avec une voix, la voix fixe l'horloge) ; chaque fond montre la même information que son mot (§ 5) ; sans secousse (`slam-shake`, écartés) ; 8 mots à l'écran au plus (§ 9) |
| `weight-morph` | le mot qui porte l'information prend du poids : sa graisse monte lettre par lettre jusqu'au gras | à l'essai | non | 2 `variable-axis-type`, `variable-font-flex` pour un mot seul | police variable seulement (axe de graisse dans la police du kit) ; la graisse monte vers l'importance, jamais en va-et-vient (§ 12) ; de Medium à Bold ; un mot par phrase, celui du sous-titre (§ 5) ; lettre par lettre permis ici seulement |
| `type-headline` | un titre qui se décline en trois cadres proportionnés (9:16, 1:1, 4:5) | à juger | non | 3 à la main | le titre est lui-même l'information (un message, trois cadres), jamais décoratif |
| `forced-perspective` | l'objet qui compte, géant devant le sujet : la taille dit l'importance | à l'essai | oui | 1 trois plans au trépied : l'objet très près, le sujet très loin, le plan vide | l'objet géant est le sujet du propos, jamais un gag ; un effet filmé par pièce au plus |
| `paper-cut` | l'élément qui compte (mot, chiffre, objet détouré) découpé dans du papier déchiré posé sur le fond | à l'essai | non | 1 le sujet réel (objet, capture ou prise) ; 2 `npx --yes hyperframes@0.8.167 remove-background`, `freeze-frame-dressing` (papier et ruban) ; 3 le bord déchiré, à la main | désigne un élément réel de la pièce (nom, valeur, source lisible), jamais un décor (§ 12) ; bord épais, jamais un contour fin (§ 13) ; le collage est la matière d'un kit |
| `cover-story` | la personne posée en une de magazine : le titre du sujet en lettres de couverture derrière sa tête | à l'essai | oui | 1 une prise de la personne qui bouge peu ; 2 `npx --yes hyperframes@0.8.167 remove-background`, `kinetic-center-build` ; 3 le titre et sa mise en page, à la main | le titre est l'information de la pièce, jamais un décor ; 8 mots à l'écran au plus (§ 9) ; voisin de `type-wall` (mots qui défilent) et de `headline-wall` (vrais titres) : celui-ci pose un seul titre fixe |
| `glass-type` | le mot qui porte l'information, en lettres 3D de verre posées dans l'espace de la scène | à l'essai | non | 2 chercher d'abord dans le registre (`npx --yes hyperframes@0.8.167 catalog --query "glass"`) ; 3 lettres de verre à la main, avec Remotion si la 3D est au cœur du plan | un seul mot clé par plan, celui du sous-titre (§ 5) ; verre sans halo ni lueur (§ 9), jamais un fond de verre ; lisible sur téléphone, 90 px et plus |
| `kicker-keyword` | la phrase en trois étages : son début en petit surtitre de capitales espacées, le mot qui porte l'information en géant, la suite en petit dessous, mot par mot ; le mot géant prend l'une de deux voix : l'italique (une serif si le kit en a une) pour l'élan, un métier, une aspiration ; les capitales grasses ou condensées pour une catégorie, un verdict | à l'essai | non | 2 `kinetic-center-build`, `caption-editorial-emphasis` ; 3 le surtitre et la suite, à la main | un mot géant par phrase, celui que dit la voix, posé de 0,15 s avant à 0,1 s après lui ; le surtitre reprend les mots dits, jamais un titre inventé ; deux voix par pièce au plus, dans les polices du kit (sans serif au kit : son italique) ; l'accent seulement sur le mot du sujet ; le mot géant sort des sous-titres (sources C12) |
| `editorial-card` | la chose concrète que nomme la phrase, sur une carte éditoriale plein cadre : un objet seul, le nom dit en grand, la phrase qui s'écrit mot par mot, qui parle et où en pied, le nom de la personne et le chapitre en petites capitales verticales sur les bords | à l'essai | non | 1 l'objet, au style d'illustration `objet-studio` ; 3 la carte, à la main | seulement quand la phrase nomme une chose concrète ; 2 à 6 s, la voix continue dessous ; un objet, un nom et une source par carte ; les marques de page (code-barres, filets) ne portent aucun faux texte lisible ; si le kit veut la personne à l'image tout le film, la carte ne la remplace pas : l'objet passe dans sa main ou derrière elle (sources C12) |
| `word-icon` | le mot géant et une petite icône de ce qu'il nomme, à l'accent, juste au-dessus (une toque sur « étudiant », un tracteur sur « agriculteur ») | à l'essai | non | 1 une icône d'une bibliothèque libre, au trait du kit (Lucide, Phosphor) ; 3 à la main | une icône par mot géant, qui dit la chose, jamais un décor ; une seule famille d'icônes dans la pièce ; elle arrive avec son mot ; pas d'emoji si le kit les refuse (sources C12) |

### Un verdict

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `verdict-mark` | le verdict qui tombe, une seule fois, après les preuves | éprouvé | non | 2 `hw-callout-circle` pour la note entourée ; 3 le tampon, aux jetons du kit | une seule fois, après les preuves (§ 12) ; aucune secousse (§ 9) ; pour une pièce qui juge (enquête, test) |
| `gauge-fill` | la note qui se remplit jusqu'à sa valeur | éprouvé | non | 2 `conic-progress-ring`, `mk-usage-arc` | pour une pièce qui note : jauge vide dès le premier beat d'épreuve, remplie au gros payoff, retirée sur la carte de fin |

### Un moment d'histoire

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `caption-story` | la phrase de l'histoire, lisible sur la scène entière | éprouvé | non | 2 `caption-pill-karaoke` | pilule opaque, 3 mots à la fois de préférence, 4 si 3 durent moins de 0,8 s (ordre des règles : `regles-de-scene.md` § 5) ; jamais pendant que le texte du hook est visible ; en surimpression, jamais incrustée dans l'image générée |
| `split-illustration-v2` | trois plans de l'histoire et la scène pleine hauteur | éprouvé | non | 3 à la main | de vrais plans distincts ; l'histoire reste en plein écran avec sous-titres |
| `lamp-bloom` | la lueur de la lampe qui gonfle et fait entrer dans l'histoire | à l'essai | non | 2 `iris-reveal` | la lueur est un objet de la scène (lampe de chevet, écran de téléphone), jamais décorative ; sans flash ; sert le passage du réel à l'histoire |
| `depth-camera-travel` | la caméra traverse trois plans illustrés de l'histoire | à juger | non | 3 à la main | un seul mouvement par plan, plein écran avec sous-titres |

### Un espace, un système

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `depth-photo` | l'espace d'une scène : une photo qui prend du relief | éprouvé | non | 1 une photo réelle ; 2 `yt-camera-move` ; 3 la photo découpée en plans (sujet, décor) à des vitesses différentes, à la main | mouvement lent vers l'information (§ 2) ; la profondeur dit quelque chose : sujet devant, décor derrière, fond à 20 à 30 % de la vitesse du sujet (§ 4) ; jamais un visage d'enfant photoréaliste |
| `depth-object-pbr` | un objet réel en volume, dont la matière et l'ombre changent avec l'angle | éprouvé | non | 1 le vrai objet, filmé ou scanné ; 3 un objet 3D à matière physique, éclairé et orienté par le temps, à la main (adaptateur Three.js de HyperFrames) | seulement quand l'espace porte l'information (§ 12) ; jamais sur le logo ; droits du modèle 3D notés |
| `mask-spotlight` | la lumière qui révèle le volume et la matière d'un objet | à juger | non | 3 à la main | le rendu porte des visuels, icônes et polices (§ 13), jamais un objet seul dans la lumière |
| `vector-network` | un parcours en isométrie : idée, création, validation reliées par un signal | à juger | non | 3 à la main | isométrie seulement quand l'espace porte l'information (§ 12) |
| `vector-diagram` | trois vues reliées sur une diagonale isométrique | à juger | non | 3 à la main | les trois vues sont de vraies captures |
| `depth-interface-z` | une interface réelle qui arrive en perspective, le champ saisi se rapproche | à juger | non | 3 à la main | la capture reste lisible malgré la perspective |

### Une continuité, le fil du film

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `dot-thread` | le même objet d'une scène à l'autre : il ouvre le film, relie les scènes et revient sur la carte de fin, porteur de l'accent | éprouvé | non | 1 l'objet réel de la marque dans la scène (curseur sur l'interface, cercle autour de la phrase, lampe de chambre) ; 2 `offset-path-traveler` (trajet d'un élément à l'autre, rotation à la tangente, sans rebond ni écrasement) ; 3 sa courbe de ressort est la même fonction que le chiffre ou la courbe qu'il guide ; s'il rebondit et s'écrase : trajets en paraboles, écrasement au contact sur 0,1 s, en fonction pure du temps (aucun composant ne le fait) | un objet conducteur par film : sur l'image 0, dans chaque scène, sur la carte de fin ; celui du kit, jamais celui d'un autre ; part d'un élément déjà à l'écran et rejoint le suivant (§ 4), jamais un point qui flotte ; un seul accent par film (§ 3) ; dispensé du test « montre » comme repère de marque avant 2 s (§ 12) |
| `loop-back` | la fin ramène à l'image d'ouverture : retour accéléré de 0,5 s au plus après la carte de fin, ou dernière image égale à la première | à l'essai | non | 1 la première image, reprise comme dernière ; 3 le retour accéléré vers l'image 0, à la main (aucun composant) | avec un mot-clé d'appel : carte de fin tenue 1,5 s au moins, puis retour de 0,5 s au plus ; sans mot-clé : boucle parfaite (§ 2, § 12) ; jamais une carte de fin coupée |
| `tint-flash` | le passage d'un format à l'autre (le visage et une carte) : une lumière à la teinte du kit traverse l'image en 0,2 s, puis la coupe | à l'essai | non | 3 à la main : un dégradé radial à la teinte du kit, en `mix-blend-mode: screen`, de 0 à 60 % puis à 0 en six images | deux fois par pièce au plus, sur les deux changements de format les plus forts ; coupes franches partout ailleurs ; jamais de flou ; la teinte vient du kit, jamais une couleur d'emprunt (sources C12) |

### Un appel à l'action

| Id | Montre | Statut | Personne filmée | Fabrication | Garde-fou |
|---|---|---|---|---|---|
| `comment-cta` | le mot à commenter pour recevoir la ressource : un commentaire se tape et se publie, la réponse avec le lien arrive | à l'essai | non | 2 `cta-close`, `yt-comment-card` | seulement avec un flux de réponse et une ressource réels ; le même mot à l'écran, dans la voix et dans la légende (un reel de référence en donnait deux : à ne pas imiter) ; la technique, jamais une promesse non tenue ; un kit peut interdire de dire le mot à la voix |
| `end-card` | la carte de fin : la signature, une phrase, l'invitation, l'objet conducteur qui revient | éprouvé | non | 2 `cta-close`, `cta-lockup`, `logo-brand-close` (mot-symbole d'un bloc, sans arrivée lettre par lettre : § 5) | 1,5 à 2 s, signature sonore s'il y en a une (§ 8) ; dispensée du test « montre » (§ 12) ; le kit fixe fond, logo, phrase, mot-clé en accent, son (silence ou carillon), emoji éventuel ; jamais coupée |

## 3. Les effets écartés

Un effet écarté ne revient que sur un accord écrit et daté. Un rejet qui visait le rendu seul ne les écarte pas : ces mécanismes sont au catalogue en `à juger`.

| Id | Pourquoi |
|---|---|
| `building-jump`, `ceiling-spider`, `levitating-object` | un saut par-dessus un bâtiment, une araignée au plafond, un objet coupé en lévitation : spectacle sans information (§ 12) |
| `clone-fire-dissolve` | dédoublement en fondu avec feu au sol : ne montre rien du contenu ; seule la technique du clone est gardée, dans `clone-dialogue` |
| `garment-match-cut` | le match cut d'un vêtement : spectacle sans information ; le vrai raccord reste permis : `action-match-cut` |
| `named-only-effects` | cinq effets connus par leur seul nom (flash, portail, toile d'araignée, étalée de couleur, nuages) : aucune recette, du spectacle |
| `constant-push-in` | zoom lent continu sur chaque plan : un zoom sans motif (§ 2, Pause) |
| `whip-pan-every-cut` | panoramique filé à chaque coupe : une transition sur chaque coupe n'apporte rien ; permis seulement s'il guide le regard |
| `whoosh-every-card` | whoosh sur chaque panoramique et chaque carte : un bruitage se pose sur une information qui arrive, jamais sur une coupe vide (§ 6, § 9) |
| `glitch` | secousse, flash, glitch : du slop (§ 9) ; en santé ils dramatisent ; composant du registre : `caption-glitch-rgb` |
| `particles-glow` | glow et particules décoratifs : du slop ; composant : `caption-particle-burst` |
| `neon-captions` | un glow décoratif sur le texte ; composants : `caption-neon-glow`, `caption-neon-accent` |
| `slam-shake` | la secousse d'écran à l'impact d'un mot : du slop (§ 9), aussi retirée du tampon d'un verdict |
| `fake-hud` | un habillage HUD sans donnée vraie : coins, faux timecode, « SYSTEM ONLINE » (§ 9) ; avec une donnée vraie : `hud-data` |
| `fake-interface` | un faux tableau de bord, une fausse interface, un faux chiffre : on montre la vraie, ou un schéma assumé (§ 9) |
| `software-transition` | cube, page qui tourne, étoile (§ 4) |
| `frame-break` | la vidéo se réduit en carte et la personne en sort : spectacle sans contenu (§ 12), et exige une personne filmée |
| `zoom-through-cut` | la caméra plonge à travers la personne vers le plan suivant : ne relie aucun état du contenu (§ 4, § 12), exige une personne filmée ; le vrai raccord : `action-match-cut` |
| `timeline-burn` | le feu qui prend à la timeline sur un mot : ne montre rien du contenu ; voir plutôt `timeline-progress` (à juger) et `app-pull-back` |
| `doodle-boil` | un contour blanc dessiné à la main qui tremble autour de la personne : un contour fin pour désigner (§ 13) |
| `blur-focus` | le mot ou la carte qui passe du flou au net : un flou posé par nous (§ 13), écarté le 31/10/2026 ; le mot qui compte se désigne par `weight-morph`, une poussée vers lui ou `spotlight-dim` |
| `gif-finder` | un GIF de banque tierce : licence non garantie, republier un média de tiers est interdit |

## 4. L'ordre de fabrication

| Rang | Source | Pourquoi |
|---|---|---|
| 1 | la vraie chose, filmée ou capturée | une preuve vaut mieux que sa reconstruction (§ 7, § 9) ; exigée pour les prompts, les outils et l'iPhone |
| 2 | un composant du registre HyperFrames, restylé aux jetons du kit | rendu calculé depuis le temps, identique à chaque export (§ 4) ; on le cherche avec `npx --yes hyperframes@0.8.167 catalog --query "<geste en anglais>"` |
| 3 | du code à la main | en dernier, quand rien de ce qui précède ne convient |

- Le premier rang possible l'emporte : ce qui peut être filmé ou capturé ne se refabrique pas en composant.
- Aucun média de tiers n'est republié : les films de référence se regardent pour leur direction, jamais pour leur média.
- Un composant se restyle aux jetons du kit avant usage : le style habille l'information, il ne la remplace pas (§ 12). Un nom absent du registre au moment de l'usage se cherche à nouveau avec `npx --yes hyperframes@0.8.167 catalog --query`.

## 5. Le son de chaque famille

Un son par information qui arrive à l'image, jamais par plan (§ 6, § 9, § 12). Niveaux : une seule cible, le master à -14 LUFS intégré et -1 dBTP au plus, la voix réglée pour l'atteindre, la musique 12 dB sous la voix (`regles-de-scene.md` § 6). Bruitage courant : sous la voix et la musique, à mesurer sur le premier rendu. Le gros payoff porte le son le plus fort du film (crête de loudness à court terme, `regles-de-scene.md` § 6), une fois ; pour une pièce muette, il se marque autrement (`regles-de-scene.md` § 11) ; les 0,5 à 1 s qui le précèdent retirent le son. Aucun son sur une coupe sans information ni pendant la respiration. Le kit peut retirer d'autres sons (produit du coucher : ni whoosh, ni impact, ni notification ; carte de fin silencieuse). Bibliothèque : bruitages libres de droits ou jeu généré à la main, jamais un son de glitch.

| Famille | Son | Jamais |
|---|---|---|
| Une quantité, un chiffre | un seul son quand le chiffre atteint sa valeur (un tick sec) ; un son de réussite si ce chiffre est le gros payoff ; `hud-data` : le même tick, une fois | un son pendant le défilement ; un son sans événement à l'image (§ 11) |
| Une comparaison | pop à l'arrivée de chaque côté ; un clic doux quand le meilleur s'allume | un whoosh qui ne fait arriver aucune information |
| Une évolution | à mesurer sur le premier rendu : un seul son, quand la courbe atteint sa valeur finale | un riser qui monte avec la courbe (une tension qui dramatise) |
| Une suite d'étapes | ding à chaque coche ; un clic à chaque étape faite ; `screen-speedup` : aucun son sur l'accéléré, le son du résultat au retour à la vitesse réelle ; `chapter-pill` : aucun | un ding sur une étape que la voix n'a pas dite |
| Une cause, une relation | scribble quand la flèche manuscrite se trace ; sinon à mesurer | un scribble sans trait tracé à l'image |
| Une transformation | whoosh seulement si le plan qui arrive montre une information nouvelle ; un clic sur l'état résultat ; `word-swap` : un pop léger à chaque permutation ; `fade-70` : aucun | un whoosh sur un fondu ou une coupe vide |
| Un détail qui compte | shutter quand la capture se fige ; si le gel doit peser (carte de leçon figée), un coup grave et court (un shutter a presque aucune énergie sous 200 Hz, mesuré) ; silence tenu pendant la poussée vers un chiffre, la musique se retire | pour un kit sans stimulation, tout son de zoom (zoom-punch, impact, whoosh) |
| Une preuve | shutter sur la capture qui entre ; un whoosh d'interface ; `ui-tilt` et `broll-cutaway` : le son de la capture qui entre ; `pip-presenter`, `lower-third`, `redact-blur` : aucun | un bruitage d'alerte sur une preuve de santé |
| Une hiérarchie, la parole | un seul son sur le mot clé qui tombe quand il est dit, ou sur le bloc central qui arrive ; `beat-words` : le temps de la musique porte les mots ; `weight-morph` : une seule note qui monte avec la graisse | un son par groupe de sous-titres ou par mot de typo cinétique |
| Un verdict | stamp sur le tampon, le plus fort du film ; un son de réussite, réservé au gros payoff, dont le début tombe entre 60 et 80 % de la durée | un riser avant le verdict ; un bruitage d'alerte |
| Un moment d'histoire | page qui tourne, shimmer doux, carillon ou boîte à musique pour la révélation ; berceuse sans percussion ; ambiance de chambre -35 dB, scène finale -28 dB (ordre de grandeur, au kit de régler) | whoosh, impact, notification |
| Un espace, un système | à mesurer : aucun son propre à la 3D ni à l'isométrie ; un seul son, quand le mouvement fait arriver l'information | un whoosh à chaque mouvement de caméra |
| Une continuité | aucun son propre ; un clic doux seulement quand l'objet change d'état ou atterrit sur l'élément qu'il désigne ; au retour de `loop-back` : rien | un son à chaque déplacement du point ; un whoosh sur le trajet |
| Un appel à l'action | signature sonore du kit sur la carte de fin, 1 à 2 s, si elle existe ; carte silencieuse ou carillon doux de 1 à 1,5 s selon le kit | un son tendance incrusté dans le fichier ; la musique d'Instagram sur une pièce qui mène à une offre (§ 6) |

## 6. La typographie

Ta charte fixe les polices et les corps de ta marque (`../modeles/charte.md`). Un texte s'écrit dans une police de ta charte, jamais dans celle d'une autre marque. Repères génériques, à 1080 px de large (deux familles au plus par film, plus la mono du microtexte, § 3) :

| Rôle | Corps | Règle |
|---|---|---|
| Titre et hook | 90 à 96 px et plus ; chiffre géant 150 à 280 px | police grasse du kit ; un seul mot clé en italique par titre si le kit a un serif ; contraste 3:1 permis dès 90 px |
| Texte d'appui | 48 à 56 px ; 32 px au moins en carrousel | police de texte du kit, contraste 4,5:1 |
| Sous-titres | 70 à 84 px, jusqu'à 110 px | 3 mots de préférence, 4 si 3 durent moins de 0,8 s, mot actif en accent, une seule police pour les deux passes (§ 5) |
| Micro, étiquettes, annotations | 22 à 28 px | mono ou grasse ; annotation manuscrite (62 px environ, inclinée de -4 à -7 degrés) seulement si le kit la prévoit |

## 7. Un exemple : un reel de référence, effet par effet

Un reel public de référence (compte tenfoldmarc, 46 s) se décompose en neuf informations, chacune montrée par un effet de ce catalogue : la forme d'une beat map (un instant, une information, un id).

| Instant | Ce qui est montré | Id |
|---|---|---|
| 0 à 5,77 s | un mur de titres de presse sur le sujet | `headline-wall` |
| 5,77 à 9,2 s | ses propres reels en orbite autour de sa tête | `orbit-collection` |
| 9,2 à 15,23 s | un zoom numérique sur le plan | `punch-in` |
| 15,23 à 19,63 s | tout s'assombrit sauf une phrase | `spotlight-dim` |
| 19,63 à 29,37 s | une liste cochée au rythme de la voix | `checklist-sync` |
| 29,37 à 33,37 s | une image figée et étiquetée | `freeze-label` |
| 33,37 à 38,30 s | le film brut contre le résultat monté | `before-after-wipe` |
| 38,30 à 46,37 s | un appel à commenter un mot | `comment-cta` |
| tout le film | une pastille de chapitre | `chapter-pill` |

Coupes détectées par ffmpeg (seuil 0,22) : 5,77 ; 15,23 ; 19,63 ; 29,37 ; 30,77 ; 30,80 ; 31,87 ; 33,37 ; 38,30 s. Le passage de l'orbite au zoom (9,2 s) n'a pas de coupe : repère pris à la voix. Une seule couleur d'accent et la pastille de chapitre font la cohérence du film.
