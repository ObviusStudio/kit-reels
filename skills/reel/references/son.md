# Le son : musique, bruitages, niveaux

```bash
python3 scripts/son.py --video renders/reel.mp4 --voix voix/voix.wav --align voix/align.json -o final.mp4 \
  [--musique ta-piste.mp3] [--bpm 110] [--bruitages bruitages.json]
```

## 1. La musique

| Choix | Quand |
|---|---|
| Ta piste (`--musique`) | une piste libre de droits pour un usage commercial, dont tu gardes la licence |
| La musique calculée (par défaut) | des accords doux, une basse, un pied et un charleston au tempo `--bpm`, fabriqués sur ta machine : libres de droits, sans téléchargement |
| `--sans-musique` | seulement si une musique s'ajoute à la publication, dans l'appli |

Une musique d'Instagram est réservée à un usage non commercial : pas sur un reel qui mène à une offre, un lien ou un produit. Un titre du commerce ou un thème de film ne va jamais dans le fichier.

## 2. Les bruitages

Un son par information qui arrive à l'image (un chiffre, une capture, un mot en grand), jamais sur une coupe qui n'apporte rien. `bruitages.json` :

```json
[{"t": 3.2, "son": "pop"}, {"t": 8.1, "son": "souffle"}, {"t": 12.4, "son": "tic"}]
```

`pop` pour un chiffre ou un mot qui tombe, `souffle` pour une capture qui entre, `tic` pour un clic dans l'appli. Les temps viennent du storyboard et de `align.json`.

## 3. Les niveaux

| Élément | Niveau |
|---|---|
| La voix | réglée à -14 LUFS par `voix.py` |
| La musique seule (ouverture, fin) | -18 LUFS |
| La musique sous la voix | 8 dB plus bas, donc environ 12 dB sous la voix, avec des rampes de 0,15 s |
| Le master | -14 LUFS intégré, crête à -1 dBTP au plus |

`son.py` baisse la musique sur les temps des mots de `align.json`, mixe, ramène le tout à -14 LUFS en deux passes et pose le son sur la vidéo sans la réencoder.
