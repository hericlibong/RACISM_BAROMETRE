"""Point d'entrée en ligne de commande du baromètre."""

from __future__ import annotations

import argparse
import sys
from contextlib import closing
from pathlib import Path

from .collect import collect_google_news, default_output_path, prepare_collection
from .storage import (
    ARTICLE_ROLES,
    EVENT_ARTICLE_ROLES,
    attach_article,
    connect,
    create_event,
    database_summary,
    detach_article,
    export_events,
    import_collection,
    set_article_role,
    update_event,
)


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

    prepare = subparsers.add_parser(
        "prepare", help="importer une collecte et préparer le passage aux événements"
    )
    prepare.add_argument("--input", type=Path, required=True, help="collecte JSON brute")
    prepare.add_argument(
        "--database", type=Path, default=Path("data/barometre.sqlite"), help="base SQLite"
    )

    status = subparsers.add_parser("status", help="afficher l'état de la base de travail")
    status.add_argument(
        "--database", type=Path, default=Path("data/barometre.sqlite"), help="base SQLite"
    )

    classify = subparsers.add_parser("classify", help="valider le rôle d'un article")
    classify.add_argument("--database", type=Path, default=Path("data/barometre.sqlite"))
    classify.add_argument("--article", type=int, required=True)
    classify.add_argument("--role", choices=ARTICLE_ROLES, required=True)
    classify.add_argument("--note")

    event = subparsers.add_parser("event", help="créer ou corriger un événement")
    event_subparsers = event.add_subparsers(dest="event_command", required=True)
    event_create = event_subparsers.add_parser("create", help="créer un événement brouillon")
    event_create.add_argument("--database", type=Path, default=Path("data/barometre.sqlite"))
    event_create.add_argument("--summary", required=True)
    event_create.add_argument("--article", type=int, action="append", default=[])

    event_link = event_subparsers.add_parser("link", help="rattacher un article")
    event_link.add_argument("--database", type=Path, default=Path("data/barometre.sqlite"))
    event_link.add_argument("--event", required=True)
    event_link.add_argument("--article", type=int, required=True)
    event_link.add_argument("--role", choices=EVENT_ARTICLE_ROLES, required=True)

    event_unlink = event_subparsers.add_parser("unlink", help="retirer un rattachement")
    event_unlink.add_argument("--database", type=Path, default=Path("data/barometre.sqlite"))
    event_unlink.add_argument("--event", required=True)
    event_unlink.add_argument("--article", type=int, required=True)

    event_update = event_subparsers.add_parser("update", help="compléter un événement")
    event_update.add_argument("--database", type=Path, default=Path("data/barometre.sqlite"))
    event_update.add_argument("--event", required=True)
    event_update.add_argument("--date-start")
    event_update.add_argument("--date-end")
    event_update.add_argument("--date-precision")
    event_update.add_argument("--episode-date-start")
    event_update.add_argument("--episode-date-end")
    event_update.add_argument("--episode-date-precision")
    event_update.add_argument("--location")
    event_update.add_argument("--summary")
    event_update.add_argument("--nature")
    event_update.add_argument("--target-dimension")
    event_update.add_argument("--context")
    event_update.add_argument("--status", choices=("brouillon", "admis", "refuse", "incertain"))
    event_update.add_argument("--notes")

    export = subparsers.add_parser("export", help="exporter les événements qualifiés en JSON")
    export.add_argument("--database", type=Path, default=Path("data/barometre.sqlite"))
    export.add_argument("--output", type=Path, required=True)
    serve = subparsers.add_parser("serve", help="ouvrir le baromètre dans un navigateur local")
    serve.add_argument("--database", type=Path, default=Path("data/barometre.sqlite"))
    serve.add_argument("--port", type=int, default=8765)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "serve":
        from .webapp import serve

        try:
            serve(args.database, args.port)
        except (OSError, ValueError, OverflowError) as exc:
            print(f"Impossible de lancer le baromètre : {exc}", file=sys.stderr)
            return 1
        return 0

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
            f"dont {result['new_article_count']} nouveau(x), "
            f"{result['media_count']} média(s), {result['query_count']} requête(s)."
        )
        if result["saturated_query_count"]:
            print(f"Attention : {result['saturated_query_count']} requête(s) ont atteint 100 résultats.")
        print(f"Résultat : {output}")
        return 0

    if args.command == "prepare":
        try:
            with closing(connect(args.database)) as connection:
                result = import_collection(connection, args.input)
        except (OSError, ValueError) as exc:
            print(f"Échec de la préparation : {exc}", file=sys.stderr)
            return 1
        print(
            f"{result['article_count']} article(s) importé(s), "
            f"dont {result['new_article_count']} nouveau(x) ; "
            f"{result['exact_duplicate_count']} doublon(s) exact(s), "
            f"{result['suggested_role_count']} rôle(s) proposé(s), "
            f"{result['grouping_proposal_count']} regroupement(s) proposé(s)."
        )
        print(f"Base : {args.database}")
        return 0

    if args.command == "status":
        with closing(connect(args.database)) as connection:
            for name, value in database_summary(connection).items():
                print(f"{name}: {value}")
        return 0

    if args.command == "classify":
        try:
            with closing(connect(args.database)) as connection:
                set_article_role(connection, args.article, args.role, args.note)
        except ValueError as exc:
            print(f"Erreur : {exc}", file=sys.stderr)
            return 2
        print(f"Article {args.article} classé comme {args.role}.")
        return 0

    if args.command == "event":
        try:
            with closing(connect(args.database)) as connection:
                if args.event_command == "create":
                    public_id = create_event(connection, args.summary, args.article)
                    print(f"Événement {public_id} créé.")
                elif args.event_command == "link":
                    attach_article(connection, args.event, args.article, args.role)
                    print(f"Article {args.article} rattaché à {args.event} comme {args.role}.")
                elif args.event_command == "unlink":
                    detach_article(connection, args.event, args.article)
                    print(f"Article {args.article} détaché de {args.event}.")
                elif args.event_command == "update":
                    update_event(
                        connection,
                        args.event,
                        date_start=args.date_start,
                        date_end=args.date_end,
                        date_precision=args.date_precision,
                        episode_date_start=args.episode_date_start,
                        episode_date_end=args.episode_date_end,
                        episode_date_precision=args.episode_date_precision,
                        location=args.location,
                        summary=args.summary,
                        nature=args.nature,
                        target_dimension=args.target_dimension,
                        context=args.context,
                        editorial_status=args.status,
                        notes=args.notes,
                    )
                    print(f"Événement {args.event} mis à jour.")
        except ValueError as exc:
            print(f"Erreur : {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "export":
        with closing(connect(args.database)) as connection:
            result = export_events(connection, args.output)
        print(f"{len(result['events'])} événement(s) exporté(s) dans {args.output}.")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
