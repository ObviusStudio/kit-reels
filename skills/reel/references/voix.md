# La voix : écrite pour être dite, fabriquée scène par scène

La voix fait ou défait un reel. Dans notre test, la voix intégrée de l'ordinateur ratait les noms et le mot à commenter ; le correctif ElevenLabs, poussé à la vitesse maximale pour tenir la durée, sonnait pressé. Voici ce qui marche.

## 1. Écrire pour être dit

| Règle | Exemple |
|---|---|
| Une idée par phrase, 15 mots au plus | « Tu décris ton projet en une phrase. » |
| Des questions qui relancent | « Résultat ? », « Et le prix ? » |
| Des enchaînements parlés | « Et », « Mais », « Donc » en tête de phrase |
| Les chiffres en chiffres | « plus de 1 500 sites » |
| Un nom difficile s'écrit comme il se dit | une marque « Evidnce » s'écrit « Évidence » pour la voix, et garde son orthographe à l'écran |
| Le mot à commenter en minuscules entre guillemets | « Commente « équipe » » |
| Ni sigle épelé, ni parenthèse, ni liste à virgules de plus de 3 éléments | « l'IA » plutôt que « AI » |

Relis le texte à voix haute : chaque phrase où tu reprends ton souffle au milieu est trop longue.

**Le nom de la marque** : après la voix, `verifier.py --mots "<nom>"` doit l'entendre. S'il est entendu autrement (dans notre test, « Obvius » transcrit « Obvious »), réécris-le comme il se dit dans `scenes.json` (« Obvi-us ») et refais cette seule scène : le cache ne refacture pas les autres.

## 2. La durée se calcule

Environ 150 mots par minute, soit 2,5 mots par seconde. Un reel de 40 s porte environ 100 mots dits.

Trop long ? On coupe du texte. Jamais une vitesse poussée : au-dessus de 200 mots par minute, la voix sonne pressée, même avec une bonne voix.

## 3. Les scènes

Une scène = 2 à 4 phrases dites d'un souffle, en général une ligne du storyboard. La voix est fabriquée scène par scène : chaque scène a son ton, et une scène ratée se refait seule.

```json
{"voix": "NBjtCdChq5Ph56VnCM8Z", "ton": "excited",
 "scenes": [
  {"id": "s01", "texte": "Chercher un appart à plusieurs, c'est ça."},
  {"id": "s02", "texte": "Qui a vu quoi ? Qui a aimé quoi ? Plus personne ne suit."}
 ]}
```

`ton` est une balise d'ElevenLabs v3 posée en tête de chaque scène : `excited` donne une voix vivante ; `""` la retire.

## 4. ElevenLabs

- **La clé** : dans la variable `ELEVENLABS_API_KEY` (`export ELEVENLABS_API_KEY=…` dans ton terminal, ou dans le fichier de configuration de ton shell). Elle n'est jamais affichée ni écrite dans un fichier du projet.
- **Le coût** : un caractère du texte = un crédit. Un reel de 40 s fait environ 700 caractères, plus les reprises. L'offre gratuite donne 10 000 crédits par mois, pour un usage non commercial d'après les guides tiers ; pour une marque, vérifie la licence de ton offre sur la page des prix d'ElevenLabs.
- **La voix** : Théo (`NBjtCdChq5Ph56VnCM8Z`), une voix française de la bibliothèque, par défaut. `python3 scripts/voix.py --voix-dispo` liste celles de ton compte. Une voix de la bibliothèque peut demander une offre payante : si Théo est refusé, prends-en une de la liste. Un clone de voix ne s'emploie que si la personne le demande.
- **Les réglages** : modèle `eleven_v3`, stabilité 0,5, similarité 0,8. Le modèle v3 ne connaît pas de réglage de vitesse : le rythme passe par la ponctuation.

## 5. Lancer, et lire le rapport

```bash
python3 scripts/voix.py scenes.json -o voix/
```

Pour chaque scène, le débit mesuré. Au-dessus de 200 mots par minute, le script refait la scène une fois avec des pauses écrites (« … » entre les phrases) et garde la prise la plus posée. Si elle reste trop rapide : `À RACCOURCIR`, et la dernière ligne dit `VOIX_A_RACCOURCIR`. Raccourcis la phrase, ou coupe la scène en deux (« Commente « équipe ». » puis « Je t'envoie le lien. »), et relance : les scènes déjà faites viennent du cache, sans être refacturées.

Sorties : `voix/voix.wav` (nettoyée : débruitage, coupe-bas, compression, présence, -14 LUFS), `voix/align.json` (les temps de chaque mot), `voix/rapport.json`.

## 6. Sans clé : s'enregistrer

1. Lis tout le texte d'une traite, avec ton téléphone, comme si tu le racontais à un ami. Jamais phrase par phrase : le ton se casse.
2. `python3 scripts/voix.py --enregistrement prise.m4a -o voix/` nettoie la prise, la met à -14 LUFS et la transcrit pour obtenir les temps des mots (`align.json`).
3. Les blancs et les ratés se coupent sur l'énergie de ta voix, comme une prise face caméra : `python3 scripts/prise.py couper prise.m4a`, garde les bons passages (`--garder`), puis `python3 scripts/prise.py monter prise.m4a coupes.json -o voix/` (essayé sur un son seul : `PRISE_OK`). La voix montée remplace alors celle de l'étape 2 (`references/face-camera.md`).

## 7. Pourquoi ces réglages

| Essai | Ce qu'on a entendu |
|---|---|
| Voix de l'ordinateur, vers 200 mots par minute | robot ; « Commente ÉQUIPE » transcrit « Comment t'équipes », « Pilot » transcrit « Kilo » |
| ElevenLabs multilingual v2, vitesse 1,2 pour tenir 41 s | les mots justes, mais pressé |
| ElevenLabs v3, Théo, ton « excited », scène par scène, sans toucher la vitesse | 157 mots par minute en moyenne, mots clés justes ; deux scènes courtes restaient vers 225 à 235 mots par minute : d'où la reprise automatique et la règle « on raccourcit » |
