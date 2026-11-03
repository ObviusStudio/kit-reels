"""Avant de publier le dépôt : ni secret, ni chemin de la machine, ni fichier lourd. Dernière ligne : PROPRE_OK ou SALE n.

Usage : python3 outils/propre.py <dossier du dépôt>   ;   python3 outils/propre.py --autotest
"""
import os, re, sys

MOTIFS = {
    "clé ElevenLabs": re.compile(r"\bsk_[0-9a-f]{40,}\b"),
    "clé d'API": re.compile(r"\b(sk-ant-[\w-]{20,}|sk-[A-Za-z0-9]{32,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16})\b"),
    "clé recopiée": re.compile(r"(?i)(api[_-]?key|xi-api-key|token)\s*[=:]\s*['\"][A-Za-z0-9_\-]{20,}['\"]"),
    "chemin de la machine": re.compile(r"/Users/[A-Za-z0-9._-]+|/private/tmp/|/home/[a-z0-9._-]+/|[A-Z]:\\\\Users\\\\"),
}
LOURD = 5 * 1024 * 1024


def scanner(racine):
    defauts = []
    for d, dossiers, fichiers in os.walk(racine):
        dossiers[:] = [x for x in dossiers if x not in (".git", "node_modules", "__pycache__")]
        for f in fichiers:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, racine)
            if os.path.getsize(p) > LOURD:
                defauts.append(f"{rel} : fichier de plus de 5 Mo")
                continue
            if rel == os.path.join("outils", "propre.py"):
                continue                      # ce fichier contient les motifs eux-mêmes
            try:
                texte = open(p, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            for nom, motif in MOTIFS.items():
                for m in motif.finditer(texte):
                    ligne = texte.count("\n", 0, m.start()) + 1
                    defauts.append(f"{rel}:{ligne} : {nom}")
    return defauts


def autotest():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "ok.md"), "w").write("export ELEVENLABS_API_KEY=…\n")
        assert scanner(d) == []
        open(os.path.join(d, "ko.md"), "w").write("voir /Users/quelquun/projet et sk_" + "a" * 48 + "\n")
        assert len(scanner(d)) == 2, scanner(d)
    print("autotest propre : 2 contrôles passés")


if __name__ == "__main__":
    if sys.argv[1:] == ["--autotest"]:
        autotest()
        sys.exit()
    d = scanner(sys.argv[1])
    for x in d:
        print("À RETIRER ", x)
    print("PROPRE_OK" if not d else f"SALE {len(d)}")
    sys.exit(1 if d else 0)
