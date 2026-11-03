# Vérifier le reel fini

Un reel jamais regardé part cassé. On mesure le fichier, puis on le regarde.

## 1. Les mesures

```bash
python3 scripts/verifier.py final.mp4 --align voix/align.json --mot équipe --mots "Pilot,1 500,L'IA" \
  --sous-titres index.html --voix voix/voix.wav --projet . [--format 9:16] [--ips 30] [--carte 2]
```

| Ligne | Seuil |
|---|---|
| format | celui de `--format` : 9:16 (par défaut, 1080 x 1920), 4:5 (1080 x 1350), 1:1 (1080 x 1080), 16:9 (1920 x 1080) |
| vidéo | H.264, à la cadence de `--ips` (30, ou 60 pour le rendu premium) ; sans elle, 24 à 60 images par seconde ; le débit est affiché |
| durée | 8 à 90 s |
| volume | -15 à -13 LUFS (visé -14) |
| crête | -0,5 dBTP au plus (visé -1) |
| musique | aucun silence de 0,4 s ou plus sous -45 dB, sauf la dernière seconde |
| images figées | aucune de plus d'une seconde, sauf les 2 dernières secondes |
| débit | chaque scène sous 200 mots par minute (avec `--align`) |
| mots entendus | le mot à commenter et chaque nom ou chiffre de `--mots`, relus dans la voix |
| mots coupés | chaque mot de `--absents` (le raté d'une prise face caméra) ne s'entend plus |
| sous-titres | `--sous-titres` (la composition, ou `voix/sous-titres.json`) : 90 % des mots retrouvés dans la voix, chaque groupe à 0,2 s au plus du mot dit ; après un blanc, l'écart se lit sur l'énergie de la voix seule (`--voix`), au retour de la voix ; deux témoins, les mêmes sous-titres avancés et retardés de 0,3 s, doivent être refusés |
| image 0 | pas noire : la première image porte déjà le hook |
| zones | une alerte, jamais un refus : du contenu dans les bandes hors de la zone du texte de `--format` (`ecran.md`, section 1) ; à relire sur la planche, car seul le texte doit rester dans sa zone |
| mouvement | chaque seconde complète notée (écart moyen entre images successives, gris 96 x 96, 30 images par seconde, sur 255) ; une seconde sous 0,6 est molle et se reprend, sauf une respiration, une chute ou la carte de fin écrite dans le storyboard ; les secondes de `--carte` (2 par défaut) ne sont pas notées ; son témoin, une seconde figée, doit sortir molle |
| déterminisme | avec `--projet` : aucun `Math.random`, `Date.now` ni `performance.now` dans `index.html` et `compositions/` |
| tirets | avec `--projet` : aucun tiret cadratin, demi-cadratin ni signe moins typographique dans les textes de la composition |

Ces cinq lignes viennent de `scripts/porte_b.py`. Les seize contrôles de la méthode, ceux qu'une commande ne tranche pas et le relecteur à part sont dans `controles.md`.

Pour une prise face caméra, le débit est celui de la personne : il s'affiche pour mémoire (`INFO`), sans défaut.

Pourquoi l'énergie après un blanc : sur le reel d'essai, après une pause, la transcription datait « ton » à 6,64 s et l'alignement d'ElevenLabs à 6,86 s, quand la voix revient à 6,96 s. Aucune date de mot n'est crue après un blanc.

La voix est relue par `npx --yes hyperframes@0.8.167 transcribe` en français. Installe Parakeet une fois (`npx --yes hyperframes@0.8.167 models install parakeet`) : sans lui, la transcription passe par Whisper. Un nom anglais dit à la française (« Pilot » entendu « Pilote ») est accepté.

Dernière ligne : `VERIF_OK`, ou `VERIF_A_REVOIR` et le nombre de défauts.

## 2. La planche d'images

```bash
ffmpeg -v error -i final.mp4 -vf "fps=1/2,scale=270:-1,tile=6x4" -frames:v 1 planche.png
```

Une image toutes les 2 s. Regarde-la : un texte coupé, un texte hors zone, une capture illisible, une image vide ne se mesurent pas.

## 3. Ce qui reste à l'œil et à l'oreille

- Le hook se comprend-il en une seconde, son coupé ?
- La voix sonne-t-elle naturelle, sans précipitation ?
- Chaque phrase a-t-elle son image au bon moment ?
- La carte de fin dit-elle le bon mot, et la réponse automatique est-elle branchée ?
