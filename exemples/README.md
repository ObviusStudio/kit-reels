# Les exemples : le même reel, avant et après le kit

Trois projets réels, la même commande (`reel pour <site>`), un Claude neuf à chaque fois. V1 : le skill gratuit `reel-builder` (dépôt Ootto-AI/claude-content-skills), le 01/11/2026. V2 : ce kit, version 0.1.0, le 02/11/2026. Une image toutes les 2 secondes de chaque reel.

| Projet | V1 | V2 |
|---|---|---|
| StoryForKid (histoires du soir illustrées) | `1-v1.jpg` : voix de l'ordinateur, « Commente DRAGON » entendu « Commande dragon » | `1-v2.jpg` : démo de l'appli dans un téléphone 3D, voix ElevenLabs à 147 mots/min, « dragon » entendu juste, musique, -14,2 LUFS |
| Evidnce (chercher un logement à plusieurs) | `2-v1.jpg` : voix de l'ordinateur, « Commente ÉQUIPE » entendu « Comment t'équipes », pas de musique | `2-v2.jpg` : vraies captures du site dans un téléphone, 151 mots/min, « équipe » entendu juste, musique, -14,1 LUFS |
| Obvius Studio (l'IA intégrée aux PME) | `3-v1.jpg` : voix de l'ordinateur, pas de musique | `3-v2.jpg` : explication en motion sur les vraies captures, chiffres sourcés à l'écran, 160 mots/min, « audit » entendu juste, musique, -14,0 LUFS ; le nom « Obvius » sort mal prononcé |

Mesures : ffmpeg (format, volume, silences) et Whisper large-v3 (la voix relue). Infos sur les projets : 37 en V1, 36 en V2, aucune inventée, chacune retrouvée sur le site du projet.
