"""Smoke test de la solution A — OpenAI web search (Responses API).

Applique le protocole du §10 de SELECTION.md : quatre angles sur la fenêtre
du 20 juillet au 20 août 2026 (volet 1), puis une passe sur les dernières
24 heures (volet 2, première passe seulement).

Ne teste ni Brave ni GDELT. Ne vérifie que son propre prérequis :
OPENAI_API_KEY. La clé n'est ni affichée, ni journalisée, ni écrite dans un
fichier de résultats.

Usage :
    python prototype/bloc-2/test_openai_websearch.py national
    python prototype/bloc-2/test_openai_websearch.py national episode lieu organisme
    python prototype/bloc-2/test_openai_websearch.py passe1
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

RACINE = Path(__file__).resolve().parents[2]
DOSSIER_RESULTATS = Path(__file__).resolve().parent / "resultats"

# Configuration unique du test — toute modification doit être consignée au rapport.
MODELE = "gpt-5.6"
OUTILS = [{"type": "web_search"}]
INCLUDE = ["web_search_call.action.sources"]
MAX_TOOL_CALLS = 8  # plafond explicite de recherches Web par appel
MAX_OUTPUT_TOKENS = 8000

FENETRE = "du 20 juillet 2026 au 20 août 2026 inclus"

CONSIGNE_SORTIE = (
    "Réponds uniquement par un objet JSON, sans texte autour, de la forme "
    '{"evenements": [{"date_fait": "AAAA-MM-JJ ou approximation", '
    '"lieu": "commune et département", "resume": "une phrase factuelle", '
    '"nature": "propos public | insulte | agression | menace | dégradation | '
    'discrimination | harcèlement | autre", "cible": "groupe visé tel que rapporté", '
    '"urls": ["..."], "medias": ["..."]}]}. '
    "N'inclus que des faits que tu as réellement trouvés dans les résultats de "
    "recherche, chacun avec au moins une URL. N'invente aucune URL. "
    "Si tu ne trouves rien, renvoie une liste vide."
)

OBJECTIFS = {
    # Volet 1 — fenêtre du benchmark, quatre angles du protocole.
    "national": (
        f"Recherche sur le Web les actes et propos à caractère raciste, antisémite ou "
        f"xénophobe survenus en France et rapportés par la presse {FENETRE}. "
        f"Couvre la presse nationale. " + CONSIGNE_SORTIE
    ),
    "episode": (
        f"Recherche sur le Web les suites judiciaires et institutionnelles intervenues "
        f"en France {FENETRE} dans des affaires à caractère raciste, antisémite ou "
        f"xénophobe : plaintes déposées, enquêtes ouvertes, mises en examen, procès, "
        f"audiences correctionnelles, condamnations, réactions de préfets ou de maires. "
        f"Le fait d'origine peut être antérieur à cette période : c'est l'épisode "
        f"judiciaire ou institutionnel qui doit s'y situer. " + CONSIGNE_SORTIE
    ),
    "lieu": (
        f"Recherche sur le Web, dans la presse quotidienne régionale et les titres "
        f"locaux français, les actes et propos à caractère raciste, antisémite ou "
        f"xénophobe rapportés {FENETRE}. Vise explicitement les communes rurales, les "
        f"villes moyennes et les faits divers locaux qui n'ont pas été repris par la "
        f"presse nationale. Varie les régions. " + CONSIGNE_SORTIE
    ),
    "organisme": (
        f"Recherche sur le Web les actes racistes, antisémites ou xénophobes survenus "
        f"en France {FENETRE} et signalés par des organismes : SOS Racisme, LICRA, "
        f"MRAP, LDH, CRIF, DILCRAH, CNCDH, préfectures, parquets, mairies. "
        f"Appuie-toi sur leurs communiqués, campagnes, testings et publications. "
        + CONSIGNE_SORTIE
    ),
    # Volet 2 — première passe seulement, fenêtre glissante de 24 h.
    "passe1": (
        "Recherche sur le Web les actes et propos à caractère raciste, antisémite ou "
        "xénophobe survenus en France ou rapportés par la presse française au cours "
        "des dernières 24 heures, c'est-à-dire entre le DEBUT_24H et maintenant, "
        "MAINTENANT. N'inclus aucun fait rapporté avant cette fenêtre de 24 heures. "
        + CONSIGNE_SORTIE
    ),
}

VOLET = {
    "national": 1,
    "episode": 1,
    "lieu": 1,
    "organisme": 1,
    "passe1": 2,
}


def maintenant() -> datetime:
    return datetime.now(timezone.utc)


def objectif(angle: str) -> str:
    """Les accolades du JSON de consigne interdisent str.format : substitution littérale."""
    texte = OBJECTIFS[angle]
    if "MAINTENANT" in texte:
        ajd = maintenant()
        texte = texte.replace(
            "DEBUT_24H", (ajd - timedelta(hours=24)).strftime("%d/%m/%Y %H:%M UTC")
        ).replace("MAINTENANT", ajd.strftime("%d/%m/%Y %H:%M UTC"))
    return texte


def extraire_json(texte: str) -> dict | None:
    """Récupère l'objet JSON de la réponse du modèle, sans être strict sur l'emballage."""
    bloc = re.search(r"\{.*\}", texte, re.DOTALL)
    if not bloc:
        return None
    try:
        return json.loads(bloc.group(0))
    except json.JSONDecodeError:
        return None


def depouiller(brut: dict) -> dict:
    """Extrait du dump de la réponse ce que le protocole demande de conserver."""
    recherches, textes, citations = [], [], []

    for item in brut.get("output", []):
        if item.get("type") == "web_search_call":
            action = item.get("action") or {}
            recherches.append(
                {
                    "query": action.get("query"),
                    "type_action": action.get("type"),
                    "statut": item.get("status"),
                    "sources": [s.get("url") for s in (action.get("sources") or [])],
                }
            )
        elif item.get("type") == "message":
            for contenu in item.get("content", []):
                if contenu.get("type") == "output_text":
                    textes.append(contenu.get("text", ""))
                    for note in contenu.get("annotations", []) or []:
                        if note.get("type") == "url_citation":
                            citations.append(
                                {"url": note.get("url"), "titre": note.get("title")}
                            )

    texte = "\n".join(textes)
    charge = extraire_json(texte)
    return {
        "recherches_web": recherches,
        "nombre_recherches_web": len(recherches),
        "nombre_sources_consultees": sum(len(r["sources"]) for r in recherches),
        "citations": citations,
        "texte": texte,
        "evenements": (charge or {}).get("evenements"),
        "json_exploitable": charge is not None,
        "usage": brut.get("usage"),
        "response_id": brut.get("id"),
        "statut": brut.get("status"),
        "incomplete_details": brut.get("incomplete_details"),
    }


def lancer(client: OpenAI, angle: str) -> dict:
    consigne = objectif(angle)
    debut = maintenant()
    print(f"[{debut.isoformat()}] angle « {angle} » — appel en cours…", flush=True)

    reponse = client.responses.create(
        model=MODELE,
        input=consigne,
        tools=OUTILS,
        include=INCLUDE,
        max_tool_calls=MAX_TOOL_CALLS,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )
    fin = maintenant()

    brut = reponse.model_dump(mode="json")
    appel = {
        "angle": angle,
        "volet": VOLET[angle],
        "objectif_envoye": consigne,
        "horodatage_debut_utc": debut.isoformat(),
        "horodatage_fin_utc": fin.isoformat(),
        "duree_s": round((fin - debut).total_seconds(), 1),
        **depouiller(brut),
        "reponse_brute": brut,
    }
    print(
        f"    → {appel['nombre_recherches_web']} recherche(s) Web, "
        f"{appel['nombre_sources_consultees']} source(s), "
        f"{len(appel['citations'])} citation(s), "
        f"{appel['duree_s']} s, JSON exploitable : {appel['json_exploitable']}",
        flush=True,
    )
    return appel


def main() -> int:
    angles = sys.argv[1:] or list(OBJECTIFS)
    inconnus = [a for a in angles if a not in OBJECTIFS]
    if inconnus:
        print(f"Angle(s) inconnu(s) : {', '.join(inconnus)}")
        print(f"Angles disponibles : {', '.join(OBJECTIFS)}")
        return 2

    load_dotenv(RACINE / ".env")
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        print("OPENAI_API_KEY : absente. Voir prototype/bloc-2/ENVIRONNEMENT.md.")
        return 1

    client = OpenAI()
    appels, erreur = [], None
    for angle in angles:
        try:
            appels.append(lancer(client, angle))
        except Exception as exc:  # arrêt au premier échec : aucun essai payant répété
            erreur = {"angle": angle, "type": type(exc).__name__, "message": str(exc)}
            print(f"    ✗ échec ({erreur['type']}) : {erreur['message']}", flush=True)
            break

    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    horodatage = maintenant().strftime("%Y%m%dT%H%M%SZ")
    fichier = DOSSIER_RESULTATS / f"openai-{'-'.join(angles)}-{horodatage}.json"
    fichier.write_text(
        json.dumps(
            {
                "solution": "openai-web-search",
                "modele": MODELE,
                "parametres": {
                    "tools": OUTILS,
                    "include": INCLUDE,
                    "max_tool_calls": MAX_TOOL_CALLS,
                    "max_output_tokens": MAX_OUTPUT_TOKENS,
                },
                "angles_demandes": angles,
                "appels": appels,
                "erreur": erreur,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nRésultats bruts : {fichier.relative_to(RACINE)}")

    total_recherches = sum(a["nombre_recherches_web"] for a in appels)
    entree = sum((a["usage"] or {}).get("input_tokens", 0) for a in appels)
    sortie = sum((a["usage"] or {}).get("output_tokens", 0) for a in appels)
    print(
        f"Total : {len(appels)} appel(s) API, {total_recherches} recherche(s) Web, "
        f"{entree} jetons d'entrée, {sortie} jetons de sortie."
    )
    return 1 if erreur else 0


if __name__ == "__main__":
    sys.exit(main())
