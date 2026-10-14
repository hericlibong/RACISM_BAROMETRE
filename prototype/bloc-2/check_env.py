"""Vérifie que les clés API du banc d'essai sont présentes localement.

Ce script ne fait aucun appel réseau et n'affiche jamais la valeur d'une clé,
ni son préfixe, ni sa longueur, ni une version masquée : seulement
« configurée » ou « absente ».

Codes de sortie : 0 = tout est configuré · 1 = au moins une clé manque
· 2 = le fichier .env est introuvable.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

RACINE = Path(__file__).resolve().parents[2]
FICHIER_ENV = RACINE / ".env"

VARIABLES = ("OPENAI_API_KEY", "BRAVE_SEARCH_API_KEY")


def main() -> int:
    if not FICHIER_ENV.exists():
        print(f"Fichier .env introuvable : {FICHIER_ENV}")
        print("Copier .env.example vers .env, puis y inscrire les clés.")
        return 2

    load_dotenv(FICHIER_ENV)

    manquantes = []
    for nom in VARIABLES:
        if os.environ.get(nom, "").strip():
            print(f"{nom} : configurée")
        else:
            print(f"{nom} : absente")
            manquantes.append(nom)

    print()
    if manquantes:
        print(f"Clés manquantes : {', '.join(manquantes)}")
        print("Aucun appel réseau n'a été effectué.")
        return 1

    print("Les deux clés sont configurées. Aucun appel réseau n'a été effectué.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
