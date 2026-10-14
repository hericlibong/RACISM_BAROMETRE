"""Troisième test OpenAI — découverte large avec gpt-5.6-luna.

Préparé selon les instructions Codex du 24 août 2026. **Non exécuté.**

Ce que ce test mesure : la capacité d'une solution simple à retrouver, sur un
mois connu, les faits dont la présence Web est déjà établie. Il ne simule pas
la collecte quotidienne future.

Principes tenus :
  - un seul appel principal, une seule demande large, aucune boucle ni relance ;
  - au moins une recherche Web garantie (`tool_choice="required"`), faute de quoi
    la comparaison au benchmark n'aurait aucun sens ;
  - fenêtre impérative du 20 juillet au 20 août 2026 inclus ;
  - ni le benchmark ni les identifiants C01-C27 ne sont transmis au modèle ;
  - aucune passe thématique, régionale ou par type de source ;
  - ni admission, ni classification définitive, ni déduplication pendant la
    découverte ;
  - la réponse brute est écrite sur disque **avant** toute extraction locale.

Limite assumée : dans un appel Responses synchrone avec Web Search hébergé, les
résultats du moteur ne peuvent pas être interceptés avant la synthèse faite sur
les serveurs OpenAI. On peut seulement en demander l'inclusion et sauvegarder la
réponse telle quelle dès réception. Aucun second pipeline n'est construit pour
contourner cette limite.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

RACINE = Path(__file__).resolve().parents[2]
DOSSIER_RESULTATS = Path(__file__).resolve().parent / "resultats"
PREFIXE = "luna4"

# --- Paramètres de l'appel -------------------------------------------------
MODELE = "gpt-5.6-luna"
OUTILS = [{"type": "web_search"}]

# `action.sources` est garanti par la documentation stable ; `results` figure
# dans le schéma du SDK installé mais reste moins garanti. Son absence dans la
# réponse est traitée comme normale, jamais comme une erreur.
INCLUDE = ["web_search_call.action.sources", "web_search_call.results"]

# Run 4 : le run 3 s'était arrêté de lui-même à 7 recherches sur 15 autorisées.
# Le plafond n'était donc pas la contrainte : on le relève ET on demande
# explicitement un balayage complet de la fenêtre (voir CONSIGNE).
MAX_TOOL_CALLS = 40   # PLAFOND, et non un objectif à atteindre
MAX_OUTPUT_TOKENS = 16000  # inclut la sortie visible ET les jetons de raisonnement
MAX_RETRIES = 0       # aucune relance automatique du SDK

# Web Search est le seul outil fourni : « required » garantit au moins un appel
# Web, sans pour autant pousser le modèle vers le plafond de 15.
TOOL_CHOICE = "required"

# Effort de raisonnement : NON transmis, donc défaut de Luna (« medium »).

# SEUIL DE CONTRÔLE APRÈS EXÉCUTION — ce n'est pas un plafond : le coût ne peut
# être calculé qu'une fois la réponse reçue, donc ce seuil ne bloque aucune
# dépense, il ne fait qu'alerter a posteriori. Les seules limites réellement
# préalables sont MAX_TOOL_CALLS et MAX_OUTPUT_TOKENS.
# Tarifs officiels du 23 août 2026 (Luna : 0,20 $/M entrée, 0,02 $/M entrée en
# cache, 1,20 $/M sortie ; web_search : 10 $/1 000 requêtes facturées).
# Estimation attendue pour le run 4 ≈ 0,50 $ (40 recherches au plus).
SEUIL_ALERTE_COUT_USD = 1.00

CONSIGNE = (
    "Recherche largement sur le Web les contenus publiés ou médiatisés en France "
    "entre le 20 juillet et le 20 août 2026 inclus concernant des faits, affaires, "
    "actes, propos, agressions, dégradations, discriminations ou manifestations "
    "pouvant relever du racisme, de l'antisémitisme, de la xénophobie liée à "
    "l'origine ou du néonazisme.\n\n"
    "La période concerne l'actualité : un fait initial plus ancien peut être retenu "
    "s'il connaît pendant cette fenêtre une plainte, une procédure judiciaire, une "
    "condamnation, une nouvelle médiatisation, une réaction ou une réactivation "
    "significative.\n\n"
    "À ce stade, privilégie fortement la découverte et le rappel. Ne décide pas "
    "encore de l'admission au baromètre. Ne cherche pas à établir une classification "
    "définitive. Ne fusionne pas volontairement plusieurs résultats en un événement "
    "unique.\n\n"
    "Conserve largement les pistes plausibles disposant d'une source identifiable. "
    "Pour chacune, fournis seulement une description très courte, la date ou période "
    "si disponible, le lieu si disponible et les URL correspondantes.\n\n"
    "Procède à un balayage complet de la période. Ne te limite pas à quelques "
    "recherches : couvre successivement chaque semaine du 20 juillet au 20 août 2026, "
    "et poursuis tant que la fenêtre n'a pas été entièrement parcourue. Beaucoup de "
    "faits n'ont été rapportés que par un seul titre de presse et n'apparaissent pas "
    "dans les premiers résultats généralistes : va les chercher. Un relevé de "
    "plusieurs dizaines de pistes est attendu, plutôt qu'une sélection restreinte.\n\n"
    "L'objectif est de ne pas perdre de contenus pertinents pendant la synthèse."
)

# Seuls ces en-têtes de réponse sont conservés en cas d'erreur : ils décrivent le
# débit et l'identifiant de requête, et ne peuvent contenir aucun secret.
ENTETES_DEBIT = ("x-request-id", "retry-after", "x-ratelimit-limit-requests",
                 "x-ratelimit-limit-tokens", "x-ratelimit-remaining-requests",
                 "x-ratelimit-remaining-tokens", "x-ratelimit-reset-requests",
                 "x-ratelimit-reset-tokens")


def maintenant() -> datetime:
    return datetime.now(timezone.utc)


def horodatage(instant: datetime) -> str:
    return instant.strftime("%Y%m%dT%H%M%SZ")


def ecrire(fichier: Path, contenu) -> Path:
    fichier.parent.mkdir(exist_ok=True)
    texte = contenu if isinstance(contenu, str) else json.dumps(
        contenu, ensure_ascii=False, indent=2
    )
    fichier.write_text(texte, encoding="utf-8")
    return fichier


def consigner_incident(exc: Exception, debut: datetime) -> Path:
    """Enregistre type, message, identifiant de requête et informations de débit.

    Aucune clé ni en-tête d'autorisation n'est conservé : seuls les en-têtes de
    débit explicitement listés le sont.
    """
    reponse = getattr(exc, "response", None)
    entetes = {}
    if reponse is not None:
        bruts = getattr(reponse, "headers", None) or {}
        entetes = {c: bruts.get(c) for c in ENTETES_DEBIT if bruts.get(c) is not None}

    incident = {
        "test": f"{PREFIXE}-decouverte-large",
        "modele": MODELE,
        "horodatage_debut_utc": debut.isoformat(),
        "horodatage_erreur_utc": maintenant().isoformat(),
        "type": type(exc).__name__,
        "message": str(exc),
        "request_id": getattr(exc, "request_id", None),
        "status_code": getattr(exc, "status_code", None),
        "entetes_debit": entetes,
    }
    return ecrire(
        DOSSIER_RESULTATS / f"{PREFIXE}-incident-{horodatage(maintenant())}.json",
        incident,
    )


def depouiller(brut: dict) -> dict:
    """Extrait séparément requêtes, actions, sources et éventuels `results`.

    `action.sources` liste les URL que l'outil rapporte avoir consultées. Ce
    n'est PAS nécessairement la totalité des résultats renvoyés par le moteur :
    ce dépouillement ne doit jamais être présenté comme tel.
    """
    actions, textes, citations = [], [], []
    resultats_presents = False

    for item in brut.get("output", []):
        if item.get("type") == "web_search_call":
            action = item.get("action") or {}
            # Distinguer « clé absente » de « clé présente mais liste vide » :
            # une liste vide reste une réponse du champ, pas son absence.
            if "results" in item:
                resultats_presents = True
            resultats = item.get("results")
            queries = action.get("queries") or []
            actions.append(
                {
                    "id": item.get("id"),
                    "statut": item.get("status"),
                    "type_action": action.get("type"),
                    "query": action.get("query"),
                    "queries": queries,
                    # si l'API ne sert que le champ singulier, il compte pour une
                    "nombre_requetes": len(queries) if queries else (1 if action.get("query") else 0),
                    "sources": [s.get("url") for s in (action.get("sources") or [])],
                    "results": resultats,
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

    return {
        "actions_web": actions,
        "nombre_items_web": len(actions),
        "nombre_requetes_formulees": sum(a["nombre_requetes"] for a in actions),
        "nombre_sources_consultees": sum(len(a["sources"]) for a in actions),
        "nombre_results": sum(
            len(a["results"]) for a in actions if isinstance(a["results"], list)
        ),
        "champ_results_present": resultats_presents,
        "requetes_facturees": ((brut.get("tool_usage") or {}).get("web_search") or {}).get(
            "num_requests"
        ),
        "citations": citations,
        "texte": "\n".join(textes),
        "usage": brut.get("usage"),
        "response_id": brut.get("id"),
        "statut": brut.get("status"),
        "incomplete_details": brut.get("incomplete_details"),
    }


def cout_estime(usage: dict, requetes_facturees: int | None) -> dict:
    """Tarifs officiels Luna, contexte court, relevés le 23 août 2026."""
    details = usage.get("input_tokens_details") or {}
    cache = details.get("cached_tokens", 0)
    entree = usage.get("input_tokens", 0) - cache
    sortie = usage.get("output_tokens", 0)
    web = (requetes_facturees or 0) * 10.0 / 1000
    modele = entree * 0.20 / 1e6 + cache * 0.02 / 1e6 + sortie * 1.20 / 1e6
    return {
        "modele_usd": round(modele, 4),
        "web_usd": round(web, 4),
        "total_usd": round(modele + web, 4),
    }


def main() -> int:
    load_dotenv(RACINE / ".env")
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        print("OPENAI_API_KEY : absente. Voir prototype/bloc-2/ENVIRONNEMENT.md.")
        return 1

    debut = maintenant()
    print(f"[{debut.isoformat()}] {MODELE} — appel unique")
    print(f"  max_tool_calls={MAX_TOOL_CALLS} (plafond) | "
          f"max_output_tokens={MAX_OUTPUT_TOKENS} | max_retries={MAX_RETRIES}")
    print(f"  include={INCLUDE} | tool_choice={TOOL_CHOICE}")
    print(f"  seuil d'alerte de coût (contrôle APRÈS exécution, ne bloque rien) : "
          f"{SEUIL_ALERTE_COUT_USD:.2f} $", flush=True)

    client = OpenAI(max_retries=MAX_RETRIES)
    try:
        reponse = client.responses.create(
            model=MODELE,
            input=CONSIGNE,
            tools=OUTILS,
            tool_choice=TOOL_CHOICE,
            include=INCLUDE,
            max_tool_calls=MAX_TOOL_CALLS,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )
    except Exception as exc:  # aucune relance : on consigne et on s'arrête
        fichier = consigner_incident(exc, debut)
        print(f"✗ échec ({type(exc).__name__}) : {exc}")
        print(f"Incident consigné : {fichier.relative_to(RACINE)}")
        return 1

    fin = maintenant()
    marque = horodatage(fin)

    # (1) Trace brute écrite AVANT toute extraction ou comparaison locale.
    brut = reponse.model_dump(mode="json")
    fichier_brut = ecrire(DOSSIER_RESULTATS / f"{PREFIXE}-brut-{marque}.json", brut)
    print(f"\nTrace brute écrite : {fichier_brut.relative_to(RACINE)}")

    # (2) Extraction locale, seulement ensuite.
    depouille = depouiller(brut)
    cout = cout_estime(depouille["usage"] or {}, depouille["requetes_facturees"])

    fichier_json = ecrire(
        DOSSIER_RESULTATS / f"{PREFIXE}-detection-{marque}.json",
        {
            "solution": "openai-web-search",
            "test": f"{PREFIXE}-decouverte-large",
            "modele": MODELE,
            "parametres": {
                "tools": OUTILS,
                "tool_choice": TOOL_CHOICE,
                "include": INCLUDE,
                "max_tool_calls": MAX_TOOL_CALLS,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
                "max_retries": MAX_RETRIES,
                "reasoning_effort": "défaut du modèle (medium), non transmis",
                "seuil_alerte_cout_usd": SEUIL_ALERTE_COUT_USD,
                "note_seuil": "contrôle après exécution ; ne bloque aucune dépense",
            },
            "trace_brute": fichier_brut.name,
            "appels": [
                {
                    "angle": "decouverte-large",
                    "volet": 1,
                    "objectif_envoye": CONSIGNE,
                    "horodatage_debut_utc": debut.isoformat(),
                    "horodatage_fin_utc": fin.isoformat(),
                    "duree_s": round((fin - debut).total_seconds(), 1),
                    "cout_estime_usd": cout,
                    **depouille,
                    "reponse_brute": brut,
                }
            ],
            "erreur": None,
        },
    )

    # (3) Sortie du modèle conservée telle quelle, séparément.
    fichier_texte = ecrire(
        DOSSIER_RESULTATS / f"{PREFIXE}-detection-{marque}.md", depouille["texte"]
    )

    usage = depouille["usage"] or {}
    print(f"→ {depouille['nombre_items_web']} items web | "
          f"{depouille['nombre_requetes_formulees']} requêtes formulées | "
          f"{depouille['requetes_facturees']} facturées")
    print(f"→ {depouille['nombre_sources_consultees']} sources listées | "
          f"champ `results` présent : {depouille['champ_results_present']} "
          f"({depouille['nombre_results']} entrées)")
    print(f"→ jetons : {usage.get('input_tokens')} entrée / {usage.get('output_tokens')} sortie")
    print(f"→ statut : {depouille['statut']} | incomplete : {depouille['incomplete_details']}")
    print(f"→ coût estimé : {cout['total_usd']:.4f} $ "
          f"(modèle {cout['modele_usd']:.4f} + web {cout['web_usd']:.4f})")
    if cout["total_usd"] > SEUIL_ALERTE_COUT_USD:
        print("⚠️  SEUIL D'ALERTE DE COÛT DÉPASSÉ — la dépense a déjà eu lieu ; "
              "aucune relance ne doit être effectuée.")
    print(f"\nDépouillement : {fichier_json.relative_to(RACINE)}")
    print(f"Sortie modèle : {fichier_texte.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
