# Roadmap de réalisation du baromètre

Cette roadmap prend effet le **14 octobre 2026**. Elle repart du travail déjà accompli et organise la suite jusqu'à une application utilisable.

La roadmap précédente est conservée sans modification dans [`archives/ROADMAP-avant-reprise-2026-10-14.md`](archives/ROADMAP-avant-reprise-2026-10-14.md). Elle documente le cadrage, le pilote méthodologique et les essais de solutions réalisés entre le 20 et le 24 août 2026.

## Objectif du projet

Construire une application qui collecte régulièrement les faits, actes et paroles liés au racisme, à l'antisémitisme, à la xénophobie et au néonazisme rapportés dans les médias en France, puis :

1. identifie les événements derrière les articles ;
2. regroupe les articles qui parlent du même événement ;
3. classe les événements par date, lieu, nature, communauté ou dimension visée et contexte ;
4. produit un résumé ou commentaire court, fidèle aux sources ;
5. restitue leur évolution dans le temps jusqu'à l'élection présidentielle de 2027 ;
6. permet plus tard d'étudier leur circulation médiatique, les réactions et les réactivations.

Le baromètre porte sur les **faits médiatisés détectés par une méthode stable**. Il ne prétend pas mesurer tous les faits survenus ni démontrer à l'avance une hausse. Il doit pouvoir montrer une hausse, une stabilité ou une baisse du nombre d'événements documentés.

## Décisions acquises au point de reprise

- Les phases de cadrage et de pilote méthodologique sont terminées.
- Le corpus du 20 juillet au 20 août 2026 reste un banc d'essai historique ; il ne doit pas être réexaminé avant de construire l'application.
- Un article n'est pas une unité de comptage : plusieurs articles peuvent documenter un même événement.
- La collecte ne repose pas sur un tri éditorial lourd préalable. Elle conserve les résultats relevant du domaine, écarte le hors-sujet manifeste et regroupe les doublons.
- **Google News RSS est retenu comme collecteur principal de départ.** Sur le banc d'essai, il a retrouvé 20 des 22 faits admis après contrôle manuel, avec 439 articles, 387 titres distincts et 139 médias, sans coût ni compte.
- Les deux faits manqués par Google News RSS révèlent d'abord une limite du lexique de requêtes. Le jeu de requêtes sera donc ajusté progressivement à partir des manques observés.
- OpenAI Web Search, GDELT ou une autre source ne seront ajoutés à la collecte que si un angle mort concret et répété le justifie.
- La forme finale de la visualisation n'est pas décidée. La heatmap, la timeline et d'autres représentations seront comparées sur les données réelles de l'application.
- La circulation sociale, les réactions politiques et les mesures d'engagement sont des enrichissements ultérieurs ; elles ne bloquent pas la première application.

## Règles de conduite

- Une tâche est cochée seulement lorsqu'elle est réalisée et vérifiée.
- Construire le circuit complet avant d'ajouter des raffinements.
- Ne pas relancer une comparaison générale des collecteurs sans échec concret de Google News RSS.
- Ne pas transformer la collecte en enquête exhaustive ou en fact-checking.
- Ne rechercher une information complémentaire que si elle est nécessaire pour identifier, regrouper, classer ou formuler correctement un événement.
- Conserver les données brutes afin de pouvoir corriger le traitement sans relancer la collecte.
- Toute complexité nouvelle doit répondre à un besoin rencontré dans l'application.

## Acquis conservés

Les éléments suivants restent des références du projet :

- le cadrage éditorial dans `CADRAGE.md` ;
- la méthode et ses règles de prudence dans `METHODOLOGIE.md` ;
- les décisions acquises dans `DECISIONS.md` ;
- le journal du pilote dans `PILOTE-20JUIL-20AOUT-2026.md` ;
- le banc d'essai de 27 cas dans `prototype/banc-essai.csv` ;
- le format minimal d'un événement dans `prototype/FORMAT-MINIMAL.md` ;
- les scripts et sorties des essais OpenAI, GDELT et Google News RSS dans `prototype/bloc-2/`.

Ils servent de mémoire et de référence. Ils ne constituent plus une phase à recommencer.

Le dossier `prototype/` conserve désormais les essais, leurs scripts et leurs résultats historiques. **Le code de l'application n'y sera pas développé.** Il sera créé dans une structure de production à la racine du projet ; seuls les éléments utiles des prototypes y seront repris, sans déplacer ni renommer les preuves des essais passés.

## Phase 1 — Consolider le point de reprise

**État : en cours depuis le 14 octobre 2026.** Cette phase prépare un socle de développement propre sans rouvrir l'étude méthodologique.

- [x] Archiver sans modification la roadmap précédente.
- [x] Acter Google News RSS comme collecteur principal de départ.
- [x] Écrire la roadmap de réalisation allant de la collecte à l'application.
- [x] Mettre le README et les documents d'état en cohérence avec cette reprise, sans réécrire les archives du pilote.
- [x] Consolider dans Git les scripts et rapports historiques utiles actuellement non suivis, en les distinguant clairement du futur code de production ; conserver hors Git les sorties API brutes pouvant contenir des identifiants opaques.
- [x] Créer à la racine une structure minimale pour le véritable baromètre, séparée de `prototype/`, sans déplacer les archives ni engager une réorganisation générale inutile.
- [x] Définir à la racine la gestion des dépendances de l'application ; utiliser `prototype/bloc-2/requirements.txt` comme inventaire de départ, et non comme manifeste définitif du produit.
- [x] Recréer un environnement Python fonctionnel depuis cette configuration racine et supprimer l'ambiguïté avec le `Pipfile` vide.
- [x] Reprendre dans le code de production uniquement la logique utile du collecteur Google News RSS ; conserver le script expérimental intact comme référence.
- [x] Vérifier qu'une commande locale unique permet de lancer la collecte Google News RSS sans appel payant.

**Sortie de phase : atteinte le 14 octobre 2026.** Le dépôt possède une seule roadmap active, un environnement Python 3.12 fonctionnel, un socle applicatif séparé des prototypes et une commande de collecte vérifiée en mode sans réseau.

## Phase 2 — Construire le moteur de collecte

**État : non lancée.** L'objectif est un collecteur réutilisable, pas un nouveau smoke test.

- [ ] Implémenter dans le code de l'application un module de collecte configurable fondé sur les enseignements du script Google News RSS expérimental, sans faire dépendre le produit du dossier `prototype/`.
- [ ] Sortir les requêtes, la langue, le pays et la fenêtre temporelle du code afin de pouvoir les modifier sans réécrire le collecteur.
- [ ] Reprendre le lexique testé et ajouter les formulations correspondant aux manques déjà observés, notamment les campagnes ou communications stigmatisantes, les circonstances aggravantes et les séquences de réponses publiques.
- [ ] Collecter pour chaque article : titre, média, date de publication, lien Google, domaine du média, requête d'origine et horodatage de collecte.
- [ ] Conserver la réponse brute ou les données suffisantes pour rejouer le traitement sans rappeler Google News.
- [ ] Rendre la collecte idempotente : relancer une même fenêtre ne doit pas multiplier les mêmes articles.
- [ ] Détecter et consigner les requêtes qui atteignent le plafond de résultats.
- [ ] Définir une stratégie proportionnée pour les URL : conserver d'abord le lien Google et le domaine du média, puis résoudre l'URL d'origine seulement lorsque cela est utile et fiable.
- [ ] Exécuter la collecte sur une fenêtre récente et vérifier le fonctionnement technique, sans refaire une qualification exhaustive du benchmark historique.

**Sortie de phase :** une commande reproductible produit un ensemble d'articles datés, traçables et réutilisables pour une période donnée.

## Phase 3 — Passer des articles aux événements

**État : non lancée.** Cette phase transforme la collecte médiatique en matière exploitable par le baromètre.

- [ ] Définir le support de stockage le plus simple pour les articles, les événements et leurs relations ; SQLite est l'option de départ à confirmer lors de l'implémentation.
- [ ] Importer les articles collectés sans perte de leur provenance.
- [ ] Regrouper les doublons exacts et proposer le rattachement des articles parlant du même fait.
- [ ] Permettre la correction manuelle d'un regroupement sans modifier les données brutes.
- [ ] Produire pour chaque événement les informations minimales déjà établies : identifiant, date du fait, lieu, résumé, nature, cible ou dimension, contexte, sources et relation éventuelle.
- [ ] Distinguer la date de publication de la date du fait et conserver une précision variable lorsqu'une date exacte n'est pas connue.
- [ ] Générer un résumé ou commentaire court qui attribue clairement les accusations, contestations ou qualifications lorsqu'elles ne sont pas établies directement.
- [ ] Écarter uniquement le hors-sujet manifeste ; ne pas créer une procédure d'admission lourde en amont.
- [ ] Vérifier le traitement sur un ensemble réduit d'événements réels, puis corriger seulement les erreurs qui empêchent leur regroupement, leur classement ou leur lecture.

**Sortie de phase :** une base d'événements reliés à leurs articles sources, avec une classification et une formulation exploitables.

## Phase 4 — Construire l'application minimale

**État : non lancée.** La première version doit rendre le baromètre consultable avant de chercher sa forme graphique définitive.

- [ ] Choisir une pile technique légère adaptée à une application locale puis publiable.
- [ ] Créer une vue chronologique des événements.
- [ ] Créer une fiche d'événement avec résumé, classification, dates, lieu et articles sources.
- [ ] Ajouter des filtres par période, nature, communauté ou dimension visée, contexte et territoire.
- [ ] Afficher les nombres d'événements par jour, semaine et mois sans les confondre avec le nombre d'articles.
- [ ] Permettre la consultation et la correction des regroupements et classifications.
- [ ] Afficher clairement la méthode, le périmètre et la date de dernière collecte.
- [ ] Vérifier que l'application reste utilisable avec plusieurs articles rattachés au même événement.

**Sortie de phase :** une application utilisable permet d'explorer les événements, leurs catégories et leurs sources dans le temps.

## Phase 5 — Concevoir la visualisation du baromètre

**État : non lancée.** Le design est décidé sur l'application et ses données réelles, pas à l'avance.

- [ ] Définir les questions que la visualisation doit permettre de lire immédiatement.
- [ ] Prototyper une timeline simple comme référence de lisibilité.
- [ ] Prototyper la heatmap ou heatmap-timeline envisagée initialement.
- [ ] Comparer les représentations sur les mêmes données : évolution temporelle, densité, catégories, filtres et accès aux faits.
- [ ] Retenir une représentation principale et, seulement si utile, une représentation complémentaire.
- [ ] Vérifier que les variations affichées décrivent les événements documentés et non une mesure exhaustive du racisme en France.
- [ ] Intégrer la visualisation retenue dans l'application.

**Sortie de phase :** le baromètre possède une représentation temporelle lisible, fidèle aux données et reliée aux événements sources.

## Phase 6 — Mettre la collecte en fonctionnement récurrent

**État : non lancée.** Cette phase transforme l'application en outil de suivi jusqu'à l'élection présidentielle de 2027.

- [ ] Définir une cadence de collecte soutenable.
- [ ] Collecter uniquement les nouvelles fenêtres et conserver l'historique des passages.
- [ ] Automatiser l'import, le rapprochement et la préparation de la classification.
- [ ] Prévoir une file simple pour les événements nécessitant une correction humaine.
- [ ] Journaliser les erreurs de collecte, les requêtes saturées et les changements du lexique.
- [ ] Contrôler périodiquement quelques résultats pour détecter une dérive de couverture, sans refaire une vérification exhaustive.
- [ ] Ajouter un collecteur complémentaire seulement si un manque récurrent est démontré et si ce complément apporte des événements que Google News RSS ne trouve pas.
- [ ] Préparer le déploiement, la sauvegarde des données et la reprise après incident.

**Sortie de phase :** l'application se met à jour régulièrement avec une intervention humaine limitée aux corrections utiles.

## Phase 7 — Enrichissements éditoriaux

**État : ultérieure.** Ces fonctions approfondissent le projet mais ne bloquent ni la collecte ni le baromètre initial.

- [ ] Mesurer la durée et le volume de la couverture médiatique d'un événement.
- [ ] Structurer les réactions politiques, institutionnelles et associatives.
- [ ] Identifier les réactivations d'anciens faits.
- [ ] Étudier les plateformes sociales et les métriques réellement accessibles.
- [ ] Identifier les observatoires, associations, médias ou sites spécialisés qui collectent déjà des faits comparables, ainsi que les applications qui les présentent ou les visualisent.
- [ ] Relever seulement ce qui peut enrichir concrètement le baromètre : sources originales, types d'événements couverts, catégories utiles, modes de visualisation et conditions d'accès aux données.
- [ ] Intégrer une source spécialisée uniquement si elle apporte une information ou une couverture absente de la collecte principale, sans remplacer ni compliquer inutilement Google News RSS.
- [ ] Ajouter des analyses périodiques courtes à partir des événements documentés.
- [ ] Examiner les signes de banalisation ou de tolérance sans fabriquer d'indice opaque.

## Définition de la première application terminée

La première application est considérée comme fonctionnelle lorsqu'elle peut :

1. collecter une période avec Google News RSS ;
2. conserver les articles et leur provenance ;
3. regrouper plusieurs articles sous un même événement ;
4. produire et corriger une classification et un résumé court ;
5. afficher une liste temporelle, des compteurs et des filtres ;
6. ouvrir les sources d'un événement ;
7. être relancée sur une nouvelle période sans créer de doublons.

La heatmap, les réseaux sociaux et l'analyse approfondie de la circulation ne conditionnent pas cette première version.

## Prochaine étape

Terminer la **Phase 1 — Consolider le point de reprise**, puis commencer immédiatement le moteur de collecte Google News RSS. Aucune nouvelle comparaison générale de solutions n'est requise avant cela.

## Historique

| Date | Évolution |
|---|---|
| 2026-08-20 au 2026-08-24 | Cadrage, pilote méthodologique, constitution du banc d'essai et essais OpenAI, GDELT et Google News RSS. Détail conservé dans la roadmap archivée et les journaux du projet. |
| 2026-10-14 | Reprise du projet : objectif recentré sur la construction de l'application ; Google News RSS retenu comme collecteur principal ; roadmap précédente archivée sans modification. |
| 2026-10-14 | Clarification du passage en production : `prototype/` devient une mémoire des essais, le baromètre reçoit son propre socle à la racine, et le repérage de sources spécialisées est ajouté aux enrichissements éditoriaux. |
| 2026-10-14 | Phase 1 de reprise terminée : documentation réalignée, environnement Python réparé, configuration racine créée et première commande du collecteur de production vérifiée sans réseau. |
