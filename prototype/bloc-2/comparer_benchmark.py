"""Comparaison hors ligne d'un résultat de test avec le banc d'essai des 27 candidats.

Distingue trois niveaux, conformément à la revue Codex du 23 août 2026 :

  1. RENCONTRÉ  — une source correspondante figure dans les traces brutes
                  (`web_search_call.action.sources`) ;
  2. RESTITUÉ   — le candidat apparaît dans la sortie finale du modèle ;
  3. admis      — décision éditoriale, hors de portée de ce script.

Aucun appel réseau. Usage :
    python prototype/bloc-2/comparer_benchmark.py resultats/<fichier>.json [...]
"""

from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
BANC = RACINE / "prototype" / "banc-essai.csv"

# Motifs distinctifs par candidat : lieu, nom propre ou domaine caractéristique.
# Un motif « et » se note par un tuple ; une alternative, par plusieurs entrées.
MOTIFS: dict[str, list] = {
    "C01": ["marboz"],
    "C02": ["nanterre-cible", "naccache", ("nanterre", "rabbin"), ("nanterre", "antisemit")],
    "C03": ["machecoul"],
    "C04": ["la-fleche", "fleche-dans-la-sarthe", ("fleche", "sarthe"), ("fleche", "neonazi")],
    "C05": ["trelissac", ("louise-michel", "tags")],
    "C06": [("caen", "raciste"), ("caen", "agression"), ("caen", "crachat")],
    "C07": [("gendarme", "guyane"), ("gendarmerie", "guyane")],
    "C08": ["komokoli", ("rennes", "injures-racistes"), ("rennes", "elue")],
    "C09": ["pouye", ("talence", "raciste"), ("senatoriales", "raciste")],
    "C10": ["migennes"],
    "C11": [("avignon", "touristes"), ("avignon", "supermarche"), ("avignon", "menaces")],
    "C12": ["deux-alpes", "deux-alpes-isere"],
    "C13": ["espaly", "puy-en-velay"],
    "C14": ["plobannalec", "penmarc", "lesconil"],
    "C15": [("randonneur", "racis"), ("montagne", "racis"), ("montagne", "blancs")],
    "C16": ["chatonnay"],
    "C17": ["crepol", "perotto"],
    "C18": ["puremedias", "ozap", ("bfmtv", "micro"), ("bfmtv", "usurpation"), ("bfmtv", "faux-journaliste")],
    "C19": ["belle-ile", "saint-nazaire"],
    "C20": ["agde"],
    "C21": ["testing", "sos-racisme"],
    "C22": ["sarcelles"],
    "C23": ["thionville"],
    "C24": [("avignon", "condamn"), ("avignon", "prison"), ("avignon", "correctionnel"), ("avignon", "six-mois")],
    "C25": [("grenoble", "concert"), ("grenoble", "entrave"), ("grenoble", "militants")],
    "C26": ["aurignac"],
    "C27": ["bois-d-arcy", "boisdarcy", ("bois", "arcy")],
}


def normaliser(texte: str) -> str:
    """Minuscules, sans accents, ponctuation réduite à des tirets."""
    texte = unicodedata.normalize("NFD", texte or "")
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", texte)


def teste(motifs: list, unites: list[str]) -> bool:
    """Un motif composé doit être satisfait par une SEULE unité (une URL, une ligne).

    Tester sur la concaténation produirait des faux positifs : « grenoble » dans une
    URL et « concert » dans une autre ne signalent aucune source correspondante.
    """
    for unite in unites:
        for motif in motifs:
            if isinstance(motif, tuple):
                if all(m in unite for m in motif):
                    return True
            elif motif in unite:
                return True
    return False


def charger_banc() -> dict[str, dict]:
    with BANC.open(encoding="utf-8-sig", newline="") as f:
        return {l["id"]: l for l in csv.DictReader(f)}


def charger_index(fichiers: list[Path]) -> tuple[list[str], dict]:
    """Format des index d'actualités (Google News RSS, GDELT) : une liste plate
    d'articles. Il n'y a pas de couche de synthèse, donc un seul niveau de
    mesure : l'article a été rapporté, ou non."""
    unites = []
    compteurs = {"requetes": 0, "articles": 0, "medias": 0, "satures": 0}
    medias = set()

    for fichier in fichiers:
        donnees = json.loads(fichier.read_text(encoding="utf-8"))
        compteurs["requetes"] += len(donnees.get("requetes") or [])
        for trace in donnees.get("traces") or []:
            if len(trace.get("articles") or []) >= 100 or trace.get("sature"):
                compteurs["satures"] += 1
        for article in donnees.get("articles") or []:
            compteurs["articles"] += 1
            media = article.get("media") or article.get("domain") or ""
            medias.add(media)
            unites.append(" ".join(str(v) for v in (
                article.get("titre") or article.get("title") or "",
                media,
                article.get("media_url") or article.get("url") or "",
            )))
    compteurs["medias"] = len(medias)
    return unites, compteurs


def charger(fichiers: list[Path]) -> tuple[list[str], list[str], list[str], dict]:
    """Retourne (URL consultées, requêtes formulées, textes restitués, compteurs).

    Une URL consultée et une requête formulée sont deux choses différentes :
    seule la première atteste qu'une source a été rencontrée.
    """
    urls, requetes, textes = [], [], []
    compteurs = {"appels": 0, "items_web": 0, "requetes": 0, "num_requests": 0,
                 "entree": 0, "cache": 0, "sortie": 0, "raisonnement": 0}

    for fichier in fichiers:
        donnees = json.loads(fichier.read_text(encoding="utf-8"))
        for appel in donnees["appels"]:
            compteurs["appels"] += 1
            textes.append(appel.get("texte") or "")
            brut = appel["reponse_brute"]

            usage = brut.get("usage") or {}
            compteurs["entree"] += usage.get("input_tokens", 0)
            compteurs["sortie"] += usage.get("output_tokens", 0)
            compteurs["cache"] += (usage.get("input_tokens_details") or {}).get("cached_tokens", 0)
            compteurs["raisonnement"] += (usage.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
            web = (brut.get("tool_usage") or {}).get("web_search") or {}
            compteurs["num_requests"] += web.get("num_requests", 0)

            for item in brut.get("output", []):
                if item.get("type") != "web_search_call":
                    continue
                compteurs["items_web"] += 1
                action = item.get("action") or {}
                compteurs["requetes"] += len(action.get("queries") or [])
                urls.extend(s.get("url", "") for s in (action.get("sources") or []))
                requetes.extend(action.get("queries") or [])

    return urls, requetes, textes, compteurs


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    fichiers = [Path(a) if Path(a).is_absolute() else RACINE / "prototype" / "bloc-2" / a
                for a in sys.argv[1:]]
    manquants = [f for f in fichiers if not f.exists()]
    if manquants:
        print("Fichier(s) introuvable(s) :", ", ".join(str(f) for f in manquants))
        return 2

    banc = charger_banc()

    # Index d'actualités : format et mesure différents des réponses OpenAI.
    premier = json.loads(fichiers[0].read_text(encoding="utf-8"))
    if "appels" not in premier:
        unites, c = charger_index(fichiers)
        corpus = [normaliser(u) for u in unites]
        print(f"Fichiers analysés : {', '.join(f.name for f in fichiers)}")
        print(f"Solution : {premier.get('solution')} | {c['requetes']} requêtes | "
              f"{c['articles']} articles | {c['medias']} médias | "
              f"{c['satures']} requête(s) saturée(s)\n")
        print(f"{'ID':5s} {'référence':10s} {'trouvé':8s}  remarque")
        print("-" * 62)
        stats = {}
        for cid, ligne in banc.items():
            trouve = teste(MOTIFS.get(cid, []), corpus)
            stats[cid] = (ligne["attendu"], trouve)
            print(f"{cid:5s} {ligne['attendu']:10s} {'oui' if trouve else 'non':8s}  "
                  f"{ligne['remarque'][:34]}")
        print()
        for attendu, libelle in (("retrouve", "ADMIS attendus"), ("incertain", "INCERTAINS"),
                                 ("rejete", "REJETÉS")):
            cibles = [s for s in stats.values() if s[0] == attendu]
            suffixe = " (bruit : à ne PAS trouver)" if attendu == "rejete" else ""
            print(f"{libelle:16s} : trouvés {sum(1 for s in cibles if s[1])}/{len(cibles)}{suffixe}")
        return 0

    urls, requetes, textes, c = charger(fichiers)
    corpus_urls = [normaliser(u) for u in urls]
    corpus_requetes = [normaliser(r) for r in requetes]
    # une unité de restitution = une ligne, pour qu'un motif composé reste local
    corpus_texte = [normaliser(l) for t in textes for l in t.splitlines() if l.strip()]

    print(f"Fichiers analysés : {', '.join(f.name for f in fichiers)}")
    print(f"Appels API : {c['appels']} | items web_search_call : {c['items_web']} | "
          f"requêtes formulées : {c['requetes']} | requêtes facturées (num_requests) : {c['num_requests']}")
    print(f"Jetons — entrée {c['entree']} (dont cache {c['cache']}), "
          f"sortie {c['sortie']} (dont raisonnement {c['raisonnement']})")
    print(f"URL consultées : {len(urls)}\n")

    print(f"{'ID':5s} {'référence':10s} {'URL vue':8s} {'cherché':8s} {'restitué':9s}  remarque")
    print("-" * 86)
    stats = {}
    for cid, ligne in banc.items():
        motifs = MOTIFS.get(cid, [])
        vue = teste(motifs, corpus_urls)
        cherche = teste(motifs, corpus_requetes)
        restitue = teste(motifs, corpus_texte)
        stats[cid] = (ligne["attendu"], vue, cherche, restitue)
        print(f"{cid:5s} {ligne['attendu']:10s} {'oui' if vue else 'non':8s} "
              f"{'oui' if cherche else 'non':8s} {'oui' if restitue else 'non':9s}  {ligne['remarque'][:30]}")

    def bilan(attendu: str) -> tuple[int, int, int]:
        cibles = [s for s in stats.values() if s[0] == attendu]
        return len(cibles), sum(1 for s in cibles if s[1]), sum(1 for s in cibles if s[3])

    print()
    for attendu, libelle in (("retrouve", "ADMIS attendus"), ("incertain", "INCERTAINS"), ("rejete", "REJETÉS")):
        total, vus, rest = bilan(attendu)
        suffixe = " (ne comptent pas comme cibles manquées)" if attendu == "rejete" else ""
        print(f"{libelle:16s} : URL vue {vus}/{total} | restitués {rest}/{total}{suffixe}")

    perdus = [c_ for c_, s in stats.items() if s[0] != "rejete" and s[1] and not s[3]]
    print(f"\nPerdus entre la recherche et la synthèse : {', '.join(perdus) if perdus else 'aucun'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
