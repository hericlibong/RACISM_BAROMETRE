# Baromètre des faits racistes médiatisés

Projet de baromètre éditorial consacré aux faits liés au racisme, à l'antisémitisme, à la xénophobie et au néonazisme qui circulent dans l'actualité en France.

**État au 14 octobre 2026 : construction de l'application.** Le cadrage, le pilote méthodologique et la comparaison des collecteurs sont terminés. Google News RSS est retenu comme collecteur principal de départ ; le développement du baromètre commence dans le paquet `barometre/` à la racine.

## Première commande

La commande suivante prépare une collecte et affiche les requêtes sans effectuer d'appel réseau :

```powershell
.\.venv\Scripts\python.exe -m barometre collect --from 2026-10-01 --to 2026-10-14 --dry-run
```

Sans `--dry-run`, la collecte gratuite Google News RSS est enregistrée par défaut dans `data/raw/`. Relancer la même fenêtre met à jour le même fichier sans multiplier les articles déjà présents.

Le code de l'application se trouve dans `barometre/`. Le dossier `prototype/` conserve les essais historiques et n'est plus le lieu de développement du produit.

## Documentation

- [`docs/CADRAGE.md`](docs/CADRAGE.md) — vision, périmètre et limites ;
- [`docs/METHODOLOGIE.md`](docs/METHODOLOGIE.md) — méthode évolutive de détection, examen et classification ;
- [`docs/CORPUS-PILOTE.md`](docs/CORPUS-PILOTE.md) — protocole de recherche pilote réelle ;
- [`docs/MODELE-ET-WORKFLOW.md`](docs/MODELE-ET-WORKFLOW.md) — support de tri et de qualification minimale, sans schéma technique imposé ;
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — décisions acquises, hypothèses et questions à traiter au bon moment ;
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — avancement phase par phase.

## Matériau empirique existant

- `docs/SAMPLES_EVENTS.md` : premier relevé brut servant de benchmark informel ;
- `docs/FORGETED_SAMPLE.md` : cas supplémentaire sur la réactivation d'une ancienne séquence.

Ces fichiers ont servi à mettre la méthode et les collecteurs à l'épreuve. Ils restent un benchmark historique et ne constituent pas la base vivante de l'application.

## Principe directeur

**Les faits façonnent la méthode ; la méthode ne doit pas façonner artificiellement les faits que le baromètre est capable de voir.**

La suite active est décrite dans `docs/ROADMAP.md` : construire le moteur de collecte, transformer les articles en événements, puis réaliser l'application et sa visualisation.
