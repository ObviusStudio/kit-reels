# Refaire un reel qui a marché, pour une entreprise

La personne donne un reel (un lien ou un fichier) et une phrase sur son entreprise, ou son site. Elle n'a pas besoin d'avoir une idée : c'est le travail de ce mode. Claude décortique le reel, propose cinq angles pour cette entreprise, attend son choix, écrit sa version sur la même structure, puis fabrique le film.

## 1. Ce qu'il faut

| Pour | Il faut |
|---|---|
| le reel | un lien Instagram ou TikTok, avec une clé ScrapeCreators dans `SCRAPECREATORS_API_KEY` (la vidéo et ses chiffres : vues, j'aime, commentaires, compte, date) ; sans clé, ou pour YouTube Shorts, `yt-dlp` ; sinon, un enregistrement d'écran du téléphone, déposé en fichier |
| l'entreprise | une phrase (« je tiens une boulangerie à Vanves ») ou son site |

Sans reel : demande-le. Sans entreprise : demande une phrase. Aucune autre question avant les angles : l'objectif par défaut est de faire venir des clients, écris-le dans ta réponse. Avec une seule phrase, propose quand même les angles et termine par : « Si tu as un site, donne-le-moi : les angles seront plus précis. »

## 2. Décortiquer

```bash
python3 scripts/decortiquer.py <lien ou fichier> -o reference/ --langue en
```

`--langue` est la langue du reel. Si elle n'est pas la bonne, tu le vois sur les planches : relance. Le script rend `reference/DECORTIQUE.md`, les planches d'images, les mots, les coupes et les silences. Il mesure le son, il ne l'écoute pas : ce que tu ne peux pas trancher, dis-le. Regarde toutes les planches avant d'écrire. Un passage trop rapide ou un texte trop petit : relance dans un autre dossier avec `--ips 6`. La transcription se trompe sur les noms et les chiffres : recoupe-la avec l'écran. Le nombre de coupes est un plancher : une rafale de plans ou un décor qui change dans le plan lui échappent. C'est sur les planches que le rythme se lit.

Puis ajoute à la fin de `DECORTIQUE.md` deux sections, sous ces titres exacts :

`## Plan par plan` : un tableau, une ligne par plan ou par changement de rôle. Quand le texte change toutes les demi-secondes, regroupe par rôle.

| t (s) | On entend | On lit | On voit | Son rôle |
|---|---|---|---|---|
| 0 à 2,6 | l'affirmation qui contredit ce qu'on croit | le même texte, deux lignes en haut | un personnage sur une pile qui monte | hook |

`## Le moule` : ce qui reste quand on retire le sujet, en six lignes, puis le test du moule.

1. La mécanique du hook, avec des trous : « Le [X] le plus [Y] n'est pas [la réponse attendue]. » ou « Tu décides de [geste banal] après [effort]. »
2. L'ordre des rôles : hook, promesse, classement, réponse, retournement, question.
3. Le rythme : durée, coupes par minute, où ça accélère.
4. Le texte et les sous-titres : où, combien de mots, ce qui est écrit et pas dit.
5. Le son : voix, musique, silence, bruitages.
6. Pourquoi on reste jusqu'au bout, et pourquoi on l'envoie à quelqu'un.

**Le test du moule.** Dis-le, et demande un autre reel, si le moule ne survit pas au retrait de ce qui l'a porté : une célébrité, une actualité, un son à la mode, le visage de son auteur, un hasard. Le moule survit si ce qui l'a porté peut être remplacé par quelque chose qui appartient à l'entreprise ; s'il faut une autre célébrité ou une autre marque connue, il ne survit pas. Quand il tient de justesse, dis-le, et propose quand même les angles. N'identifie jamais quelqu'un d'après son visage : ce qui n'est écrit ni dit nulle part, tu ne le sais pas. Dis aussi ce qui ne se reprend pas dans un moule qui tient : un public qui n'est pas celui de l'entreprise, un chiffre que l'entreprise n'a pas, une promesse que l'original ne tient pas dans le film (ta version, elle, dit tout).

## 3. Ce qu'on garde, ce qu'on refait

| On garde | On refait |
|---|---|
| la mécanique du hook | tous les mots : jamais 7 mots de suite de l'original, ce qu'il écrit à l'écran compris |
| l'ordre des rôles, la place du retournement | toutes les images : jamais son clip, ni ses plans, ni ses personnages |
| la durée à 20 % près (un reel long peut raccourcir si la personne le veut, en retirant un rôle répété), le rythme | la voix, la musique si elle est sous droits (elle s'ajoute dans l'application, à la publication) |
| l'emplacement des textes, dans le format choisi pour le film | son nom, sa marque, sa charte (la charte est celle de la personne) |

Le contrôle : ajoute à `reference/transcription.txt` ce que l'original écrit à l'écran, puis `python3 scripts/decortiquer.py --sept-mots reference/transcription.txt script.md`, jusqu'à `SEPT_MOTS_OK`. Il ne voit pas une traduction : la phrase d'origine traduite mot à mot est aussi une reprise, relis-toi.

Pourquoi : depuis 2024, Instagram remplace les reposts par l'original dans ses recommandations (https://www.engadget.com/instagrams-algorithm-overhaul-will-reward-original-content-and-penalize-aggregators-130018977.html, lu le 07/11/2026). En droit français, une idée n'est pas protégée, sa forme originale peut l'être, un format très précis aussi, et l'imitation peut relever de la concurrence déloyale (https://www.journaldunet.com/management/juridique/1029753-les-formats-televises-une-protection-delicate, lu le 07/11/2026) : ce n'est pas un conseil juridique, et un doute se pose à un juriste. Le film doit tenir sans que personne ne connaisse l'original.

Ne promets jamais les vues de l'original. Le format donne une structure qui a déjà marché ailleurs, pas un résultat. Un fichier ne donne ni les vues ni l'auteur, et un compteur visible à l'écran peut être celui d'une autre vidéo : ce que tu ne peux pas vérifier, dis-le.

## 4. Les angles

Lis d'abord le site, ou relis la phrase ; si le site ne répond pas, dis-le et continue avec la phrase. Écris les faits sur l'entreprise avec l'endroit où tu les as lus. Puis propose cinq angles, chacun d'une famille différente : cinq façons de faire entrer l'entreprise dans le moule, pas cinq versions de la même idée. Une famille sans matière sort.

| Famille | La question qu'elle pose |
|---|---|
| L'idée reçue | Que croient à tort les clients sur ce métier ? |
| L'erreur | Quelle erreur font-ils avant de venir ? |
| Le moment vécu | Quelle scène du quotidien tous les clients reconnaissent-ils ? |
| Les coulisses | Que fait l'entreprise que personne ne voit ? |
| Le chiffre | Quel chiffre de ce métier surprend ? (cherche-le, lis sa source, donne son lien) |
| Le résultat | Que voit-on de différent avant et après ? |

Écris les cinq dans `angles.md`, et donne-les aussi dans ta réponse, le recommandé en premier, quelle que soit sa famille, sous cette forme :

```markdown
### Angle 1 · <sa famille> (recommandé)
- **Hook :** la première phrase, dans le moule
- **La vidéo :** ce qu'elle raconte, en une phrase simple
- **Ce qu'on montre :** ce qui existe déjà ou ce qui est à filmer, plan par plan en une ligne
- **Le fait qu'il faut :** le fait, et « lu sur <source> » ou « à confirmer par toi »
- **Note du hook :** n sur 16
```

Règles :
- Le hook tient en 12 mots pour sa première phrase, écrite ou dite, 15 en tout, un nombre compte pour un mot ; à l'écran, 8 mots au plus à la fois. Un moule plus long se coupe.
- À ce stade, un hook par angle, noté a priori sur la grille de `references/hooks.md`, l'image 0 et le ton jugés sur ce qui est prévu. Sous 12 sur 16, retravaille le hook ou sors l'angle. Les dix candidats et le test de l'inconnu viennent après le choix.
- Un hook de sketch se note sur ce qu'il fait ressentir : le bénéfice vaut 1 si on s'y reconnaît.
- Un fait à trou est permis ici (« [X] heures ») : la note dit « une fois [X] confirmé ». Un fait que personne n'a confirmé porte « à confirmer par toi » et n'entre pas dans le script tant qu'il ne l'est pas.
- Une scène jouée peut inventer ce qui est de la fiction (un client, l'heure d'une scène), jamais un fait sur l'entreprise ou son marché.
- Une ligne dit pourquoi le premier est recommandé.
- Un angle tient si son fait existe ou se confirme d'un oui, et si quelqu'un qui ne connaît pas l'entreprise le comprend. Moins de trois angles qui tiennent : dis-le, ce reel ne va pas à cette entreprise, demande-en un autre.

Dans ta réponse : le reel en cinq lignes, le moule, ce qui ne se reprend pas, les angles. Le plan par plan reste dans le fichier.

**Puis arrête-toi et demande : « Lequel tu prends ? »** Pas de script avant son choix. La personne peut prendre un angle, en combiner deux ou en demander d'autres. Sans personne pour répondre (essai, tâche programmée), prends le recommandé et écris-le en tête du compte rendu.

## 5. Écrire sa version

1. Pose en un message les questions de l'ordre de marche encore ouvertes (style des images, mot à commenter, voix, charte), avec ta réponse recommandée, et fais confirmer les faits de l'angle.
2. Écris un tableau à deux colonnes, rôle par rôle : « L'original fait » et « Ta version dit ». Chaque rôle a sa ligne ; un rôle qui saute a sa raison.
3. Écris les dix candidats et garde trois hooks dans le moule, puis le script (`references/hooks.md`, `references/voix.md`). La durée reste à 20 % de l'original.
4. Passe `--sept-mots`. Chaque fait sur l'entreprise a sa source ; un fait public a son lien.

## 6. Fabriquer

Reprends à partir du storyboard, dans l'ordre de marche du skill. Chaque ligne du storyboard nomme le rôle de l'original qu'elle reprend.

- Un angle à filmer : donne la liste des plans à tourner au téléphone, la personne les filme, puis le montage d'une prise du skill s'applique.
- Un moule sans voix reste sans voix : le hook est écrit, la fin garde sa boucle sans carte de fin qui la casse, le mot à commenter va dans la légende.

Avant de montrer le film, pose côte à côte la planche de l'original et celle du film : mêmes rôles, à peu près aux mêmes moments, et aucune image reprise.
