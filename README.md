# Baromètre des faits racistes médiatisés

Projet de baromètre éditorial consacré aux faits liés au racisme, à l'antisémitisme, à la xénophobie et au néonazisme qui circulent dans l'actualité en France.

**État du projet.** L’application minimale est disponible en local. La relecture humaine précède la publication. Google News RSS est le collecteur principal. La [phase 5](docs/ROADMAP.md#phase-5--concevoir-la-visualisation-du-baromètre) porte sur la visualisation et la direction artistique.

Les collectes brutes, la base SQLite et les exports de relecture sont conservés dans le dossier de travail local. Pour initialiser une base dans un nouveau clone, suivre les sections « Lancer une collecte » et « Préparer les événements ».

## Ouvrir l’application locale

Pour créer l’environnement Python dans un nouveau clone, depuis la racine du projet, exécuter `py -3.12 -m venv .venv`. Avec la base de travail locale en place, lancer l’application.

```powershell
.\.venv\Scripts\python.exe -m barometre serve
```

Ouvrir [le baromètre local](http://127.0.0.1:8765/) dans le navigateur. La chronologie affiche le corpus de travail, les filtres et les compteurs par jour, semaine et mois. Le détail d’un fait donne accès à ses sources. Les dates trop imprécises restent visibles dans le total de la sélection et sont indiquées à part des compteurs par période.

- **Relecture** permet d’ajouter un fait avec sa source, de corriger une fiche ou de déplacer un article. Après enregistrement des corrections, la personne qui relit peut valider la version enregistrée pour publication ou classer le dossier hors publication.
- **Aperçu public** montre uniquement les dossiers admis et validés par une personne. Les admissions du corpus existant sont conservées dans la chronologie de travail. Leur validation pour publication se fait fiche par fiche. Une modification du contenu de la fiche ou de ses rattachements remet le dossier en relecture.

### Relire une fiche

1. Dans **Relire ou corriger**, cliquer sur **Lire les articles** et ouvrir un titre. Par exemple, plusieurs articles relatent les mêmes inscriptions près de la mosquée de Lodève. Ils restent ensemble dans la fiche. Comparer leur contenu au résumé et à la date du fait décrits par la fiche.
2. Si une information est à modifier, ouvrir **Corriger la fiche**, puis enregistrer. La date d’une suite concerne un épisode ultérieur, par exemple une décision du parquet. Les notes internes sont réservées à l’espace de travail. Si un article manque, **Ajouter un article à ce fait** permet de chercher dans la base ou de coller le lien direct. Si un article parle d’un autre fait, ouvrir **Corriger le classement de cet article** puis **Choisir une autre fiche**. La date, le lieu et le résumé permettent de reconnaître la fiche où déplacer cet article.
3. Cliquer sur **Voir la fiche côté lecteur** pour vérifier le dernier rendu enregistré. La décision de publication est en bas de la page de relecture. La validation requiert au moins un article qui relate le fait, avec un lien.

L’application est accessible sur cette machine. Pour l’arrêter, utiliser `Ctrl+C` dans le terminal. L’option `--database` permet de lancer l’application sur une copie de travail.

## Lancer une collecte

La commande suivante prépare une collecte et affiche les requêtes sans effectuer d'appel réseau :

```powershell
.\.venv\Scripts\python.exe -m barometre collect --from 2026-10-01 --to 2026-10-14 --dry-run
```

Sans `--dry-run`, la collecte gratuite Google News RSS est enregistrée par défaut dans `data/raw/`. Relancer la même fenêtre met à jour le même fichier sans multiplier les articles déjà présents.

## Préparer les événements

La phase 3 utilise une base SQLite locale sans modifier le fichier brut :

```powershell
.\.venv\Scripts\python.exe -m barometre prepare --input data/raw/gnews-2026-10-10-2026-10-14.json
.\.venv\Scripts\python.exe -m barometre status
```

Cette préparation importe les articles, repère les doublons exacts, propose certains rôles et rapprochements à partir des titres. Les propositions restent distinctes des décisions éditoriales : **aucun regroupement proposé n'est automatiquement compté comme événement**. Les commandes `classify`, `event create`, `event link` et `event unlink` permettent de valider ou corriger progressivement le travail sans altérer la collecte d'origine.

Les événements effectivement qualifiés peuvent être exportés dans un JSON lisible :

```powershell
.\.venv\Scripts\python.exe -m barometre export --output data/processed/events-2026-10-10-2026-10-14.json
```

L'export contient aussi `candidates_to_review`, la file des articles encore à vérifier, y compris ceux qui n'ont été trouvés que par une seule source. Seuls les événements portant `counted_in_barometer: true` alimentent le comptage ; les dossiers de contexte et les candidats à vérifier restent visibles sans gonfler la courbe.

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
