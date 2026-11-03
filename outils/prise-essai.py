"""Fabrique une prise face caméra d'essai, pour éprouver le montage sans filmer personne.

Usage : python3 outils/prise-essai.py -o dossier/     (clé ElevenLabs dans ELEVENLABS_API_KEY, environ 230 caractères)

Écrit dossier/prise.mp4 (1080 x 1920, 30 i/s, 13 s environ) et dossier/verite.json : les vrais temps de chaque mot
dans la prise, tirés de l'alignement d'ElevenLabs, pour mesurer le calage des sous-titres sans passer par une
transcription. La prise commence par un raté (« Alors, euh… attends, je recommence. »), laisse 0,6 à 1,2 s de blanc
entre les phrases, et garde un léger bruit de pièce, comme un téléphone. L'image est une silhouette dessinée dont la
bouche s'ouvre sur chaque mot : c'est la voix qui compte ici, pas le visage. Rien de cette prise ne va dans le dépôt.
"""
import importlib.util, json, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("voix", os.path.join(ICI, "..", "skills", "reel", "scripts", "voix.py"))
voix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voix)

PHRASES = [("Alors, euh… attends, je recommence.", 1.1),
           ("Voici le montage de ma prise, fait par Claude.", 0.9),
           ("Il coupe chaque blanc, sur l'énergie de ma voix.", 1.2),
           ("Les sous-titres tombent pile sur ce que je dis.", 0.8),
           ("Et les effets se posent sur l'image.", 0.6)]
TETE, IPS = 0.6, 30


def fabriquer(sortie):
    cache = os.path.join(sortie, "cache")
    os.makedirs(cache, exist_ok=True)
    t, morceaux, mots, payes = TETE, [], [], 0
    for texte, blanc in PHRASES:
        mp3, ali, c = voix.prise(voix.THEO, texte, cache)
        payes += c
        mots += voix.mots_alignes(ali, t)
        d = voix.duree_fichier(mp3)
        morceaux.append((mp3, t))
        t += d + blanc
    duree = round(t, 3)
    # le son : chaque phrase à sa place, sur un bruit de pièce à -50 dB environ
    entrees = sum((["-i", m] for m, _ in morceaux), [])
    pose = "".join(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={int(a * 1000)}[p{i}];" for i, (_, a) in enumerate(morceaux))
    son = os.path.join(cache, "prise.wav")
    voix.ffmpeg(*entrees, "-f", "lavfi", "-i", f"anoisesrc=c=pink:a=0.004:d={duree}:r=48000",
                "-filter_complex", pose + "".join(f"[p{i}]" for i in range(len(morceaux)))
                + f"[{len(morceaux)}:a]amix=inputs={len(morceaux) + 1}:normalize=0:duration=longest,atrim=0:{duree}[o]",
                "-map", "[o]", "-ac", "1", son)
    # l'image : un fond qui dérive, une silhouette, une bouche ouverte pendant chaque mot, un clignement toutes les 3,5 s
    ouverte = "+".join(f"between(t,{m['start']:.3f},{m['end']:.3f})" for m in mots)
    graphe = (f"color=c=black:s=54x96:r={IPS}:d={duree},format=gbrp,"
              "geq=r='34+22*sin(T*0.7)+Y/2':g='40+18*sin(T*0.7+2)+Y/2.4':b='58+20*sin(T*0.7+4)+Y/2',scale=1080:1920:flags=bicubic,"
              "drawbox=x=300:y=1240:w=480:h=680:color=0x2f3a4f:t=fill,"            # le buste
              "drawbox=x=470:y=1090:w=140:h=170:color=0xd9a184:t=fill,"            # le cou
              "drawbox=x=380:y=600:w=320:h=520:color=0xe6b393:t=fill,"             # le visage
              "drawbox=x=370:y=560:w=340:h=110:color=0x2b1d16:t=fill,"             # les cheveux
              "drawbox=x=450:y=790:w=48:h=30:color=0x2a1b14:t=fill:enable='lt(mod(t,3.5),3.38)',"
              "drawbox=x=582:y=790:w=48:h=30:color=0x2a1b14:t=fill:enable='lt(mod(t,3.5),3.38)',"
              "drawbox=x=480:y=968:w=120:h=12:color=0x7a3a34:t=fill,"
              f"drawbox=x=486:y=950:w=108:h=52:color=0x5a1c24:t=fill:enable='{ouverte}'[v]")
    film = os.path.join(sortie, "prise.mp4")
    voix.ffmpeg("-i", son, "-filter_complex", graphe, "-map", "[v]", "-map", "0:a", "-t", str(duree),
                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(IPS),
                "-c:a", "aac", "-b:a", "192k", film)
    json.dump({"duree": duree, "phrases": [p for p, _ in PHRASES], "mots": mots},
              open(os.path.join(sortie, "verite.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{film} : {duree} s, {len(mots)} mots, {payes} caractères payés à ElevenLabs (le cache ne refacture rien)")
    print("PRISE_ESSAI_OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "-o" not in a:
        sys.exit(__doc__)
    fabriquer(a[a.index("-o") + 1])
