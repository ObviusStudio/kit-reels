# Ta prise face caméra : couper, sous-titrer, habiller

Tu te filmes, tu déposes ta vidéo, le kit la monte : il coupe les blancs et le raté sur l'énergie de ta voix, cale les sous-titres sur ta voix montée et pose les effets sur ta prise. La méthode vient du montage des vidéos face caméra de taubiwan.ai, ramenée à une prise et au reste du kit : la voix montée sort au même format que la voix ElevenLabs (`voix/voix.wav`, `align.json`, `sous-titres.json`), donc `son.py` et `verifier.py` la traitent pareil.

## 1. Filmer

- Une prise d'une traite, comme si tu racontais à un ami. Tu rates une phrase ? Marque un temps et reprends-la : le kit retire le raté, jamais une phrase que tu veux garder.
- Téléphone vertical, 1080 x 1920 ou 4K, 30 ou 60 images par seconde, la lumière en face.
- Une vidéo d'iPhone en HEVC se copie d'abord en H.264 : `ffmpeg -i prise.mov -c:v libx264 -crf 18 -c:a aac prise.mp4`.
- Rien de privé à l'image : un écran, un courrier, une adresse se cachent avant de filmer, jamais floutés après.

## 2. Couper sur l'énergie de ta voix

```bash
python3 scripts/prise.py couper prise.mp4
```

Le script lit l'énergie de ta voix par trames de 10 ms, sur la prise nettoyée comme le sera ta voix montée, et rend la liste des passages parlés, chacun avec ce que tu y dis :

```
  1     0.63 à    2.54 s  (1.91 s)  gardé  « Alors euh, je recommence. »
  2     3.70 à    6.07 s  (2.37 s)  gardé  « Voici le montage de ma prise fait par Claude. »
```

Relis la liste, puis garde les bons passages : `python3 scripts/prise.py couper prise.mp4 --garder 2,3,4,5,6`. Le résultat va dans `coupes.json`, une plage par passage, avec sa raison.

| Se coupe | Ne se coupe jamais |
|---|---|
| un blanc de 0,20 s ou plus | une phrase que tu n'as pas dit de retirer |
| une bribe : moins de 0,15 s, aucun mot (souffle, bruit de bouche) | un mot en son milieu |
| un raté, un faux départ : le passage entier, à ta demande | une négation ou une condition (« pas », « sauf », « si ») |

Pourquoi l'énergie, et pas les dates de la transcription : elles avalent les silences, un mot s'étire sur la pause qui le suit. Pourquoi la prise nettoyée : sur la prise brute, le bruit de la pièce remplit les pauses (essayé : une virgule de 0,23 s, invisible sur la brute, restait un trou dans la voix montée).

## 3. La voix montée et ses sous-titres

```bash
python3 scripts/prise.py monter prise.mp4 coupes.json -o voix/
```

| Sortie | Contenu |
|---|---|
| `voix/voix.wav` | ta voix des passages gardés, mise bout à bout, nettoyée (débruitage, coupe-bas, compression, présence) à -14 LUFS |
| `voix/align.json` | les temps de chaque mot, sur le temps du montage, relus par la transcription de ta voix montée |
| `voix/sous-titres.json` | les groupes d'une ligne (18 caractères au plus, 3 mots de préférence, 0,8 s pour lire), jamais à cheval sur une coupe, jamais fini sur un petit mot (« ton », « se ») |
| `voix/plages.html` | une balise `<video>` muette par plage, à coller telle quelle dans la composition |

Puis le contrôle des blancs : aucun trou de 0,20 s ou plus dans ta voix montée. Son témoin, ta prise brute, doit en avoir, sinon la mesure ne prouve rien. Dernière ligne : `PRISE_OK`.

Un sous-titre qui tomberait dans un blanc se pose sur le retour de ta voix, lu sur l'énergie : après une pause, les moteurs de transcription datent le mot jusqu'à 0,3 s trop tôt.

## 4. Les effets sur ta prise

Copie ta prise dans le projet HyperFrames, colle `voix/plages.html` dans la racine, et les sous-titres dans `<script type="application/json" id="sous-titres">` (la balise que lit `verifier.py`). La prise joue muette ; `son.py` pose ta voix montée et le son que tu as choisi (`son.md`).

| Effet | Règle |
|---|---|
| Cadrage alterné | une plage sur deux à 108 % (`data-cadrage="108"`), l'origine à 45 % de la hauteur : chaque coupe se lit voulue |
| Ouverture | le premier plan se pose de 103 à 100 % : l'image 0 n'est jamais figée |
| Le hook en trois couches | ta première phrase, en grand, ligne par ligne au moment où tu la dis ; aucun sous-titre tant qu'elle est à l'écran |
| Le mot clé | une pastille d'accent quand il est dit ; un punch-in à 110-125 % sur le mot qui porte l'information, deux fois par reel au plus |
| La carte de fin | sur un fond d'encre, 1,5 à 2 s |

```js
gsap.set(".plan", { transformOrigin: "50% 45%" });
gsap.set('[data-cadrage="108"]', { scale: 1.08 });
tl.fromTo("#w1", { scale: 1.03 }, { scale: 1, duration: 2.37, ease: "power2.out" }, 0);
tl.fromTo("#w3", { scale: 1 }, { scale: 1.15, duration: 0.2, ease: "power2.out", immediateRender: false }, 3.76);
```

Sous-titres en blanc avec un contour d'encre, sous le menton (y = 1150 à 1350 en 9:16), jamais sur le visage.

## 5. Vérifier

```bash
python3 scripts/son.py --video renders/montage.mp4 --voix voix/voix.wav --align voix/align.json -o final.mp4 --compose
python3 scripts/verifier.py final.mp4 --align voix/align.json --mot montage --mots "Claude" \
  --absents "recommence" --sous-titres index.html --voix voix/voix.wav --face-camera
```

`--absents` : les mots du raté, qui ne doivent plus s'entendre. `--face-camera` : la note de mouvement s'affiche pour mémoire, sans défaut, car son seuil vient de films de motion sans voix ; une tête qui parle bouge moins, et le cadrage alterné et le punch-in se regardent sur la planche. Le débit est le tien : il s'affiche, sans défaut. Puis la planche d'images (`references/verifier.md`, section 2).

## 6. Ce que l'essai du 02/11/2026 a prouvé, et ce qu'il ne prouve pas

La prise d'essai vient de `outils/prise-essai.py` : une silhouette dessinée dont la bouche s'ouvre sur chaque mot, une voix ElevenLabs, un raté au début, des blancs de 0,6 à 1,2 s, un bruit de pièce. Personne n'a été filmé.

| Mesuré | Résultat |
|---|---|
| La prise | 16,5 s, 6 passages parlés trouvés sur l'énergie, le raté en premier |
| Le montage | 5 plages gardées, 8,96 s ; le raté (« recommence », « attends ») ne s'entend plus |
| Les blancs | 0 trou de 0,20 s dans la voix montée ; 4 dans la prise brute (le témoin) |
| Les sous-titres | 10 groupes ; mesurés sur ta voix seule, sans aucun moteur de transcription (le front des sifflantes, au-dessus de 4 kHz) : 0,14 s d'écart au plus sur 4 groupes ; le témoin retardé de 0,3 s est refusé |
| Le fichier | 1080 x 1920, 30 i/s, 10,8 s, -14,1 LUFS, `VERIF_OK` |

Ce que l'essai ne prouve pas : un vrai visage (le cadrage et le punch-in sur une vraie tête restent à regarder), un vrai micro de téléphone, une prise de plusieurs minutes.

## 7. Ce que ce kit ne fait pas

Le texte derrière toi (le détourage du film), les plans de coupe sur une capture pendant que tu parles, plusieurs prises à assembler, la timeline pour DaVinci.
