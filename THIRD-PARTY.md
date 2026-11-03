# Ce que le kit utilise sans l'avoir écrit

| Composant | Licence | Comment il arrive chez toi |
|---|---|---|
| HyperFrames 0.8.167 (HeyGen), https://github.com/heygen-com/hyperframes | Apache-2.0 | lancé par `npx --yes hyperframes@0.8.167`, version fixée ; ses skills par `npx --yes hyperframes@0.8.167 skills`. Jamais recopié ici |
| three.js 0.181.2, https://github.com/mrdoob/three.js | MIT | chargé par la scène 3D depuis `https://cdn.jsdelivr.net/npm/three@0.181.2/+esm`, version fixée ; jamais recopié ici |
| GSAP 3.14.2, https://gsap.com | licence standard de GSAP (gratuite, usage commercial compris) | chargé par chaque composition depuis jsDelivr, comme le fait `hyperframes init` |
| ElevenLabs | service payant à l'usage, conditions d'ElevenLabs | appelé par `scripts/voix.py` avec ta clé ; la voix générée suit la licence de ton offre et celle de la voix choisie |
| ffmpeg | LGPL ou GPL selon ta version | installé par toi |
| Python 3 | PSF | installé par toi ; les scripts n'utilisent que la bibliothèque standard |

La musique et les bruitages de `scripts/son.py` sont calculés sur ta machine : aucun fichier sonore tiers n'est fourni.
