"""Test de la solution C — GDELT DOC 2.0.

Troisième famille de la présélection, jamais testée : index d'actualités
gratuit, sans clé, sans compte, sans limite de débit documentée, et seul des
trois finalistes à disposer d'un filtre de dates natif.

Même banc d'essai que les tests OpenAI : fenêtre du 20 juillet au 20 août 2026,
corpus pilote non transmis, aucune admission ni classification prononcée.

Usage :
    python prototype/bloc-2/test_gdelt.py --sonde   # une seule requête, contrôle
    python prototype/bloc-2/test_gdelt.py           # la série complète
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

RACINE = Path(__file__).resolve().parents[2]
DOSSIER_RESULTATS = Path(__file__).resolve().parent / "resultats"

ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
DEBUT = "20260720000000"
FIN = "20260820235959"
MAXRECORDS = 250  # plafond documenté de l'API en mode ArticleList
PAUSE_S = 6.0     # GDELT demande une requête toutes les 5 secondes au maximum

# Requêtes thématiques en français. Volontairement lexicales et simples :
# GDELT est un index plein texte, pas un agent. Aucun lieu du corpus pilote
# n'est nommé, aucun identifiant C01-C27 n'est utilisé.
REQUETES = [
    '"acte raciste"',
    '"agression raciste"',
    '"injures racistes"',
    '"propos racistes"',
    '"insultes racistes"',
    '"tags racistes"',
    '"acte antisémite"',
    '"propos antisémites"',
    '"tags antisémites"',
    '"croix gammée"',
    '"discrimination raciale"',
    '"provocation à la haine raciale"',
]

FILTRES = "sourcelang:french sourcecountry:FR"


def maintenant() -> datetime:
    return datetime.now(timezone.utc)


def interroger(client: httpx.Client, requete: str) -> dict:
    """Une requête GDELT. Renvoie le résultat brut et les métadonnées d'appel."""
    parametres = {
        "query": f"{requete} {FILTRES}",
        "mode": "ArticleList",
        "format": "json",
        "maxrecords": MAXRECORDS,
        "startdatetime": DEBUT,
        "enddatetime": FIN,
        "sort": "datedesc",
    }
    debut = maintenant()
    reponse = client.get(ENDPOINT, params=parametres, timeout=60.0)
    fin = maintenant()

    trace = {
        "requete": requete,
        "url_appelee": str(reponse.url),
        "horodatage_utc": debut.isoformat(),
        "duree_s": round((fin - debut).total_seconds(), 2),
        "statut_http": reponse.status_code,
    }

    if reponse.status_code != 200:
        trace["erreur"] = f"HTTP {reponse.status_code}"
        trace["extrait_reponse"] = reponse.text[:300]
        trace["articles"] = []
        return trace

    try:
        charge = reponse.json()
    except ValueError:
        # GDELT renvoie parfois du texte brut en cas de requête mal formée
        trace["erreur"] = "réponse non JSON"
        trace["extrait_reponse"] = reponse.text[:300]
        trace["articles"] = []
        return trace

    articles = charge.get("articles") or []
    trace["articles"] = articles
    trace["nombre_articles"] = len(articles)
    trace["sature"] = len(articles) >= MAXRECORDS
    return trace


def main() -> int:
    sonde = "--sonde" in sys.argv
    requetes = REQUETES[:1] if sonde else REQUETES

    print(f"GDELT DOC 2.0 — fenêtre {DEBUT} → {FIN}")
    print(f"{len(requetes)} requête(s), maxrecords={MAXRECORDS}, filtres : {FILTRES}")
    print("Aucune clé, aucun compte, aucune dépense.\n")

    traces = []
    # GDELT refuse systématiquement les User-Agent non navigateur (HTTP 429).
    entetes = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
    }
    with httpx.Client(headers=entetes) as client:
        for i, requete in enumerate(requetes):
            try:
                trace = interroger(client, requete)
            except Exception as exc:
                trace = {
                    "requete": requete,
                    "erreur": f"{type(exc).__name__}: {exc}",
                    "articles": [],
                }
            traces.append(trace)
            nb = len(trace.get("articles") or [])
            drapeau = " [SATURÉ]" if trace.get("sature") else ""
            souci = f"  ⚠️ {trace['erreur']}" if trace.get("erreur") else ""
            print(f"  {requete:38s} → {nb:4d} article(s){drapeau}{souci}")
            if i < len(requetes) - 1:
                time.sleep(PAUSE_S)

    # Agrégation : on conserve chaque article, sans déduplication éditoriale.
    tous = []
    vus = set()
    for trace in traces:
        for article in trace.get("articles") or []:
            url = article.get("url", "")
            tous.append({**article, "requete_origine": trace["requete"]})
            vus.add(url)

    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    marque = maintenant().strftime("%Y%m%dT%H%M%SZ")
    suffixe = "sonde" if sonde else "serie"
    fichier = DOSSIER_RESULTATS / f"gdelt-{suffixe}-{marque}.json"
    fichier.write_text(
        json.dumps(
            {
                "solution": "gdelt-doc-2.0",
                "endpoint": ENDPOINT,
                "fenetre": {"debut": DEBUT, "fin": FIN},
                "filtres": FILTRES,
                "maxrecords": MAXRECORDS,
                "requetes": requetes,
                "traces": traces,
                "articles": tous,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\n{len(tous)} article(s) au total, {len(vus)} URL distinctes.")
    print(f"Résultats : {fichier.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
