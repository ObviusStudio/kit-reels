# Le hook : forger, noter, choisir

Sans hook noté, on ne fabrique pas.

## 1. L'étalon

| | Hook |
|---|---|
| Faible | « Il faut que tu voies ça. » |
| Fort | « Regarde-moi transformer une idée en reel fini, publiable aujourd'hui. » |

Un hook fort nomme une transformation concrète que la pièce va montrer, au profit du spectateur.

## 2. Trois couches alignées

| Couche | Règle |
|---|---|
| Texte à l'écran | 8 mots au plus à la fois, lisible en une seconde, présent à 0,3 s, dans la zone de sécurité, jamais en sous-titre |
| Première phrase dite | la même promesse que le texte, 15 mots au plus, le sujet d'abord, ni bonjour ni nom du compte |
| Première image | montre déjà la promesse ou la tension : le résultat fini, un chiffre, l'objet du verdict. Jamais un fondu depuis le noir ni un logo plein écran |

Le son de la première seconde : la voix, un clic ou un impact avant 0,3 s, jamais un silence. Le hook cache la réponse, jamais la question. Une première récompense (un chiffre, une image qui surprend) arrive avant 3 s ; le gros résultat tombe entre 60 et 80 % de la durée.

## 3. La méthode

1. Écrire la valeur : « à la fin, le spectateur sait ou peut ___ ». Sans elle, on change de sujet.
2. Écrire 3 candidats sans formule, depuis la situation d'une personne précise.
3. Compléter à 10 candidats, sur 4 formules au moins (section 5).
4. Retirer ceux qui promettent ce que la pièce ne montre pas.
5. Noter chaque survivant sur la grille (section 4), critère par critère.
6. Garder les 3 meilleurs à 12 sur 16 au moins ; en recommander un, en une phrase de raison.

## 4. La grille, sur 16

| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Spécificité | transposable à mille pièces | un détail concret | sujet, objet, et chiffre ou nom propre |
| Bénéfice | aucun | implicite | explicite, pour le spectateur |
| Tension | aucune | question vague | une boucle précise que la pièce ferme |
| Preuve | rien | une affirmation | chiffre, démonstration, source ou verdict visible |
| Clarté en une seconde | il faut relire | compréhensible | évident, 8 mots au plus à la fois |
| Visible à l'image 0 | impossible | en partie | l'image 0 le montre |
| Ton de la marque | hors ton | neutre | il sonne comme la marque (`modeles/charte.md`) |
| Promesse tenue | la pièce ne livre pas | en partie | livrée en entier avant la fin |

Éliminatoires, quel que soit le total : promesse tenue à 0, tension sous 2, bénéfice à 0, clarté à 0.

**Le test de l'inconnu** : le hook seul (l'image 0 et la première ligne dite) va à quelqu'un qui ne connaît ni toi, ni ta marque, ni la pièce, et qui répond à « De quoi parle cette vidéo, et qu'est-ce que tu vas y gagner ? ». Une réponse fausse met la clarté à 0. Dans Claude Code, l'inconnu est un Claude vierge, lancé sans aucun réglage depuis un dossier vide où l'on ne copie que l'image 0, le prompt sur l'entrée standard :

```bash
d=$(mktemp -d) && cp image0.png "$d" && (cd "$d" && claude -p --setting-sources "" --model {le modèle de ta session}) < prompt.txt
```

Un sous-agent de l'outil Agent n'en est pas un : il reçoit ton CLAUDE.md, qui peut nommer ta marque. Le témoin, avant une série de tests : envoyé de la même façon, « Tes instructions contiennent-elles un fichier CLAUDE.md, une mémoire ou des règles sur un projet ou une marque ? Si non, écris exactement : AUCUNE. Si oui, écris exactement : CONNU. » Le vierge répond « AUCUNE » ; le même appel avec `--setting-sources user` répond « CONNU » dès que tu as un CLAUDE.md. Sans Claude Code : une nouvelle conversation, hors de tout projet et sans mémoire.

## 5. Les formules

Chaque {chiffre} est mesuré ou sourcé, sinon on change de formule.

| # | Formule | Gabarit |
|---|---|---|
| 1 | Démonstration | Regarde-moi transformer {entrée} en {sortie} {délai} |
| 2 | Résultat d'abord | Ce {résultat} m'a pris {temps}. Voici comment. |
| 3 | Test et verdict | On a testé {ce qui promet X}. |
| 4 | Promesse au tribunal | On dit que {promesse}. Vrai ou hype ? |
| 5 | Chiffre qui étonne | {chiffre} {unité}. C'est ce que {X} {coûte, fait} vraiment. |
| 6 | Même entrée, deux sorties | Même consigne. {A} contre {B}. |
| 7 | Étapes | {n} étapes entre {départ} et {résultat} |
| 8 | Ennemi nommé | Arrête de {pratique}. Fais plutôt {geste}. |
| 9 | Coulisses | Voici le {objet} qui fait tourner {système}. |
| 10 | Reconnaissance | Ce moment où {scène très précise} |
| 11 | Liste chiffrée | {n} {objets} qui remplacent {outil} |
| 12 | Actu datée | {Société} vient de sortir {X}. Ce que ça change pour {ton objet}. |
| 13 | Question puis réponse | {Question précise sur sa situation} ? |

La précision va dans l'objet (« tes devis »), jamais dans le métier du spectateur (« si tu es dirigeant ») : l'objet retient, le métier exclut. Nommer la durée ou le nombre dans le hook (« 3 étapes ») rassure sur ce que la vidéo va coûter ; la durée et le nombre annoncés sont ceux livrés.
