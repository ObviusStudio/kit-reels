# Ce que le kit utilise sans l'avoir écrit

| Composant | Licence | Comment il arrive chez toi |
|---|---|---|
| HyperFrames 0.8.167 (HeyGen), https://github.com/heygen-com/hyperframes | Apache-2.0 | lancé par `npx --yes hyperframes@0.8.167`, version fixée ; ses skills par `npx --yes hyperframes@0.8.167 skills`. Jamais recopié ici |
| three.js 0.181.2, https://github.com/mrdoob/three.js | MIT | chargé par la scène 3D depuis `https://cdn.jsdelivr.net/npm/three@0.181.2/+esm`, version fixée ; jamais recopié ici |
| GSAP 3.14.2, https://gsap.com | licence standard de GSAP (gratuite, usage commercial compris) | chargé par chaque composition depuis jsDelivr, comme le fait `hyperframes init` |
| ElevenLabs | service payant à l'usage, conditions d'ElevenLabs et d'Eleven Music (https://elevenlabs.io/music-terms) | appelé par `scripts/voix.py` et `scripts/son.py` avec ta clé ; la voix générée suit la licence de ton offre et celle de la voix choisie, la musique et les effets générés les conditions d'ElevenLabs et d'Eleven Music de ton offre |
| Pexels, Pixabay, Openverse | licence de chaque banque (Pexels, Content License de Pixabay ; CC0, domaine public ou CC BY par Openverse) | appelés par `scripts/banque.py` avec tes clés gratuites (`PEXELS_API_KEY`, `PIXABAY_API_KEY`) ; Openverse sans clé ; chaque fichier téléchargé garde sa licence dans `banque.json` ; aucune image ni vidéo tierce n'est fournie ici |
| ffmpeg | LGPL ou GPL selon ta version | installé par toi |
| yt-dlp, https://github.com/yt-dlp/yt-dlp | Unlicense | installé par toi, seulement pour refaire un reel à partir de son lien ; sinon, tu donnes le fichier |
| ScrapeCreators, https://scrapecreators.com | service payant au crédit, ses conditions d'utilisation | appelé avec ta clé, seulement pour refaire un reel à partir de son lien ; rien n'est inclus dans le kit |
| Python 3 | PSF | installé par toi ; les scripts n'utilisent que la bibliothèque standard |

`scripts/son.py` ne calcule ni musique ni bruitage : si tu les choisis, la musique se compose par ElevenLabs Music et les effets électro se génèrent par ElevenLabs ; sinon c'est ta piste, ou rien. Aucun fichier sonore tiers n'est fourni.
