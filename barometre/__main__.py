"""Point d'entrée en ligne de commande du baromètre."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .collect import collect_google_news, default_output_path, prepare_collection


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m barometre",
        description="Collecte les articles du baromètre depuis Google News RSS.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect = subparsers.add_parser("collect", help="collecter une période")
    collect.add_argument("--from", dest="start", required=True, help="début inclus, AAAA-MM-JJ")
    collect.add_argument("--to", dest="end", required=True, help="fin incluse, AAAA-MM-JJ")
    collect.add_argument("--output", type=Path, help="fichier JSON de sortie")
    collect.add_argument(
        "--queries",
        type=Path,
        help="fichier de requêtes, une par ligne ; utilise la configuration intégrée par défaut",
    )
    collect.add_argument(
        "--limit-queries",
        type=int,
        help="limiter le nombre de requêtes, utile pour un contrôle rapide",
    )
    collect.add_argument(
        "--dry-run",
        action="store_true",
        help="afficher les requêtes et URL sans appeler Google News",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "collect":
        try:
            plan = prepare_collection(
                start=args.start,
                end=args.end,
                queries_file=args.queries,
                limit_queries=args.limit_queries,
            )
        except (OSError, ValueError) as exc:
            print(f"Erreur : {exc}", file=sys.stderr)
            return 2

        if args.dry_run:
            print(f"Fenêtre : du {plan.start.isoformat()} au {plan.end.isoformat()} inclus")
            print(f"Requêtes : {len(plan.queries)}")
            for query, url in plan.urls:
                print(f"- {query}\n  {url}")
            print("\nDry-run : aucun appel réseau effectué.")
            return 0

        output = args.output or default_output_path(plan.start, plan.end)
        try:
            result = collect_google_news(plan, output)
        except (OSError, ValueError) as exc:
            print(f"Échec de la collecte : {exc}", file=sys.stderr)
            return 1

        print(
            f"{result['article_count']} article(s) uniques, "
            f"{result['media_count']} média(s), {result['query_count']} requête(s)."
        )
        print(f"Résultat : {output}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
