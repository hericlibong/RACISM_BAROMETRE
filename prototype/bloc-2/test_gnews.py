"""Test de la solution C2 — Google News RSS.

Édition française native, aucune clé, aucun compte, aucune dépense. Filtres de
dates `after:` / `before:` à la journée.

Même banc d'essai que les tests précédents : fenêtre du 20 juillet au 20 août
2026, corpus pilote non transmis, aucune admission ni classification prononcée.

Réserve connue, inscrite dans la présélection : les liens sont des URL de
redirection Google. Le média est identifiable via la balise <source>, mais
l'URL d'origine de l'article ne l'est pas sans une résolution supplémentaire,
qui n'est PAS faite ici — un appel HTTP par article serait disproportionné à ce
stade.

Usage :
    python prototype/bloc-2/test_gnews.py --sonde
    python prototype/bloc-2/test_gnews.py
"""

from __future__ import annotations

import json
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import httpx

RACINE = Path(__file__).resolve().parents[2]
DOSSIER_RESULTATS = Path(__file__).resolve().parent / "resultats"

ENDPOINT = "https://news.google.com/rss/search"
EDITION = {"hl": "fr", "gl": "FR", "ceid": "FR:fr"}
# `before:` est exclusif : on vise le 21 pour inclure le 20 août.
FENETRE = "after:2026-07-20 before:2026-08-21"
PAUSE_S = 2.0

# Mêmes requêtes lexicales que le test GDELT, pour que les deux soient comparables.
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

ENTETES = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
}


def maintenant() -> datetime:
    return datetime.now(timezone.utc)


def interroger(client: httpx.Client, requete: str) -> dict:
    parametres = {"q": f"{requete} {FENETRE}", **EDITION}
    debut = maintenant()
    reponse = client.get(ENDPOINT, params=parametres, timeout=60.0)
    fin = maintenant()

    trace = {
        "requete": requete,
        "url_appelee": str(reponse.url),
        "horodatage_utc": debut.isoformat(),
        "duree_s": round((fin - debut).total_seconds(), 2),
        "statut_http": reponse.status_code,
        "articles": [],
    }

    if reponse.status_code != 200:
        trace["erreur"] = f"HTTP {reponse.status_code}"
        trace["extrait_reponse"] = reponse.text[:300]
        return trace

    try:
        racine = ET.fromstring(reponse.content)
    except ET.ParseError as exc:
        trace["erreur"] = f"XML illisible : {exc}"
        trace["extrait_reponse"] = reponse.text[:300]
        return trace

    for item in racine.iterfind(".//item"):
        source = item.find("source")
        trace["articles"].append(
            {
                "titre": (item.findtext("title") or "").strip(),
                "lien_google": (item.findtext("link") or "").strip(),
                "date_publication": (item.findtext("pubDate") or "").strip(),
                "media": (source.text or "").strip() if source is not None else None,
                "media_url": source.get("url") if source is not None else None,
            }
        )
    trace["nombre_articles"] = len(trace["articles"])
    return trace


def main() -> int:
    sonde = "--sonde" in sys.argv
    requetes = REQUETES[:1] if sonde else REQUETES

    print(f"Google News RSS — édition {EDITION['ceid']} — {FENETRE}")
    print(f"{len(requetes)} requête(s). Aucune clé, aucun compte, aucune dépense.\n")

    traces = []
    with httpx.Client(headers=ENTETES, follow_redirects=True) as client:
        for i, requete in enumerate(requetes):
            try:
                trace = interroger(client, requete)
            except Exception as exc:
                trace = {"requete": requete, "articles": [],
                         "erreur": f"{type(exc).__name__}: {exc}"}
            traces.append(trace)
            souci = f"  ⚠️ {trace['erreur']}" if trace.get("erreur") else ""
            print(f"  {requete:38s} → {len(trace['articles']):4d} article(s){souci}")
            if i < len(requetes) - 1:
                time.sleep(PAUSE_S)

    tous, medias = [], {}
    for trace in traces:
        for article in trace["articles"]:
            tous.append({**article, "requete_origine": trace["requete"]})
            cle = article.get("media") or "inconnu"
            medias[cle] = medias.get(cle, 0) + 1

    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    marque = maintenant().strftime("%Y%m%dT%H%M%SZ")
    fichier = DOSSIER_RESULTATS / f"gnews-{'sonde' if sonde else 'serie'}-{marque}.json"
    fichier.write_text(
        json.dumps(
            {
                "solution": "google-news-rss",
                "endpoint": ENDPOINT,
                "edition": EDITION,
                "fenetre": FENETRE,
                "requetes": requetes,
                "traces": traces,
                "articles": tous,
                "medias": dict(sorted(medias.items(), key=lambda x: -x[1])),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    titres_uniques = {a["titre"] for a in tous}
    print(f"\n{len(tous)} article(s), {len(titres_uniques)} titre(s) distinct(s), "
          f"{len(medias)} média(s).")
    print(f"Résultats : {fichier.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
