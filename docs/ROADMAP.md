# Roadmap

Cette roadmap suit l'avancement réel du baromètre. Elle doit rester courte et être corrigée lorsque l'expérience invalide une étape prévue.

La boussole éditoriale du projet est résumée dans [`MOTIVATION.md`](MOTIVATION.md). Elle éclaire les choix futurs sans ajouter de tâches au pilote.

## Règles de suivi

- Une tâche est cochée seulement lorsqu'elle est réalisée et vérifiée.
- Une question future ne bloque pas le projet sauf si elle est explicitement nécessaire à l'étape suivante.
- Les faits découverts peuvent faire revenir sur le cadrage.
- Aucun choix technique n'est engagé avant une expérience réelle de recherche et de traitement.

## Phase 1 — Recadrage méthodologique

**État : terminée et validée par l'utilisateur le 21 août 2026.** Le cadrage initial du 20 août a été réouvert puis simplifié après lecture des samples et des recadrages utilisateur.

- [x] Lire le recadrage méthodologique et suspendre les phases suivantes.
- [x] Examiner les samples existants comme matériau brut non vérifié.
- [x] Simplifier `CORPUS-PILOTE.md` : supprimer quotas, composition artificielle et couverture obligatoire des cas limites.
- [x] Simplifier `METHODOLOGIE.md` : séparer détection et admission, rouvrir la temporalité, faire émerger la taxonomie.
- [x] Alléger `DECISIONS.md` : conserver les décisions structurantes et repousser les questions non urgentes.
- [x] Simplifier `MODELE-ET-WORKFLOW.md` : support souple et qualification minimale, sans schéma technique présumé.
- [x] Ajuster `CADRAGE.md`, le README et les instructions persistantes aux principes du recadrage.
- [x] Intégrer les dernières corrections : fenêtre pilote, benchmark, temporalité des épisodes et vocabulaire judiciaire prudent.
- [x] Figer la fenêtre pilote : **20 juillet–20 août 2026**.
- [x] Effectuer la revue finale de cohérence et obtenir la validation utilisateur.

**Sortie de phase :** une documentation légère qui autorise une vraie recherche exploratoire sans prédéterminer son corpus.

## Phase 2 — Recherche pilote réelle

**État : terminée le 22 août 2026**, après revue Codex et validation de l'utilisateur. Fenêtre : **20 juillet–20 août 2026**.

**Sortie de phase :** 27 candidats qualifiés — 22 admis, 3 incertains, 2 refusés — un relevé des catégories réellement apparues, un journal des frictions et un bilan de charge, ayant conduit à une révision minimale de la méthode.

- [x] Préparer un support simple pour consigner requêtes, candidats, documents et décisions.
- [x] Définir une procédure minimale de conservation des pages consultées pendant l'essai.
- [x] Effectuer une première passe de recherche Web documentée, nationale et locale.
- [x] Approfondir les recherches ciblées et les sources encore inaccessibles ou insuffisantes.
- [x] Conserver tous les candidats plausibles, y compris incomplets, ambigus ou finalement refusés.
- [x] Effectuer une première comparaison au benchmark informel : événements retrouvés, manqués et nouveaux candidats.
- [x] Analyser pourquoi les événements connus non retrouvés ont été manqués.
- [x] Commencer le rapprochement et distinguer provisoirement faits, épisodes et reprises.
- [x] Qualifier chaque candidat : admission, rattachement et classification minimale.
- [x] Relever les catégories apparues, sans liste fermée.
- [x] Tenir le journal des frictions et des cas limites réellement rencontrés.
- [x] Mesurer la charge jusqu'à une qualification minimale suffisante.
- [x] Réviser la méthode à partir de l'expérience et la soumettre à revue.

Le volume du corpus résulte de la fenêtre et de la recherche. Il n'est pas fixé par quota.

## Phase 3 — Prototype fonctionnel de collecte

**État : non lancée.** Cette phase change de régime : après le cadrage et le pilote méthodologique, il faut maintenant tester concrètement comment retrouver et structurer les événements avec le moins de complexité possible.

> **Principe directeur :** le corpus du 20 juillet–20 août 2026 devient un banc d’essai. La solution technique doit démontrer qu’elle sait accomplir la tâche avant qu’une architecture plus large soit envisagée.

> **Garde-fou :** ne pas chercher la solution la plus complète. Chercher la solution minimale qui retrouve, déduplique et qualifie correctement les événements utiles. Toute complexité supplémentaire doit répondre à un besoin observé ou à un échec concret du test.

- [ ] Définir le **format minimal de sortie** attendu pour un événement à partir du corpus pilote : identifiant, date, lieu, résumé court, nature, cible/dimension, contexte, sources et relation éventuelle avec un autre événement.
- [ ] Transformer les 27 candidats du pilote en **banc d’essai fonctionnel**, sans les réexaminer : événements attendus, refus connus, cas incertains et exemples utiles de liaison ou de regroupement.
- [ ] Identifier un petit nombre de **solutions techniques simples** permettant de rechercher des événements sur une période donnée : recherche Web assistée par agent, API ou agrégateur de presse, combinaison légère de recherche et traitement automatique, ou autre option concrète justifiée.
- [ ] Tester les solutions retenues sur la **même fenêtre du 20 juillet au 20 août 2026**.
- [ ] Comparer les résultats sur des critères concrets : événements connus retrouvés, nouveaux candidats utiles, faux positifs, doublons, qualité des dates et catégories extraites, effort humain restant, coût et contraintes d’accès.
- [ ] Choisir la **solution la plus simple suffisamment efficace**. Ne pas retenir une architecture plus complexe si une solution légère accomplit correctement la tâche.
- [ ] Réaliser un premier passage de bout en bout avec la solution retenue : **période → recherche → candidats → déduplication → qualification minimale → sortie structurée**.

**Sortie de phase :** une méthode de collecte techniquement testée sur le corpus pilote, un format minimal d’événement et une solution retenue sur preuves plutôt que sur hypothèses.

Cette phase ne construit pas encore le site final, ne met pas en place de pipeline industriel et ne traite pas encore systématiquement les réseaux sociaux.

## Phase 4 — Structuration et première restitution

**État : non lancée.** Elle commence seulement lorsque la collecte fonctionnelle a été testée et qu’un format minimal d’événement a fait ses preuves.

- [ ] Choisir le support de données le plus simple compatible avec la solution retenue et les événements réellement produits.
- [ ] Stabiliser uniquement les catégories utiles pour comprendre, filtrer, regrouper et visualiser les événements, sans créer de taxonomie nouvelle.
- [ ] Importer le corpus pilote et un premier résultat de collecte dans ce support.
- [ ] Produire une première restitution temporelle simple : liste chronologique, timeline ou graphique léger.
- [ ] Vérifier ce que la restitution rend lisible et quelles données sont réellement manquantes avant d’ajouter de nouveaux champs.
- [ ] Si nécessaire, réaliser une première interface minimale permettant d’explorer les événements et leurs sources.

**Sortie de phase :** des événements structurés dans un support simple et une première représentation concrète du baromètre.

> **Garde-fou :** un événement correctement qualifié en Phase 2 n’est pas revérifié ici sauf si sa transformation en donnée ou en restitution révèle un problème concret.

## Phase 5 — Mise en fonctionnement récurrente

**État : non lancée.** Elle consiste à rendre reproductible la collecte retenue, sans transformer le projet en infrastructure lourde.

- [ ] Rejouer la collecte sur une nouvelle fenêtre réelle.
- [ ] Identifier les opérations qui nécessitent encore une intervention humaine.
- [ ] Automatiser uniquement les opérations répétitives dont le gain est démontré.
- [ ] Définir une cadence de collecte et de mise à jour soutenable.
- [ ] Maintenir une qualification humaine minimale uniquement là où elle reste nécessaire.

## Phase 6 — Enrichissements éditoriaux

**État : non lancée.** Ces éléments donnent sa profondeur éditoriale au baromètre mais ne conditionnent pas le fonctionnement de base.

- [ ] Structurer la circulation médiatique et les réactivations d’un fait lorsque ces données sont accessibles.
- [ ] Intégrer les réactions politiques et institutionnelles utiles.
- [ ] Étudier les plateformes sociales et les métriques réellement accessibles : reprises, engagement, durée de circulation, réactivation.
- [ ] Examiner comment documenter, sans fabriquer d’indice artificiel, les signes éventuels de banalisation ou de tolérance croissante.
- [ ] Enrichir les visualisations et les filtres à partir des données réellement disponibles.

## Règle de régime à partir de la Phase 3

À partir de cette phase, le projet n’avance plus par ajout de documentation théorique.

Toute nouvelle règle, couche technique, vérification ou structure doit être justifiée par l’un des éléments suivants :

1. un besoin concret observé dans le corpus ;
2. un échec mesuré lors d’un test fonctionnel ;
3. une nécessité indispensable pour exploiter ou afficher les données.

À défaut, ne pas l’ajouter.

La question prioritaire devient :

> **Quelle est la manière la plus simple de retrouver, normaliser et restituer les événements d’une période donnée ?**

Le terme « baromètre » décrit le résultat produit dans la durée ; il ne doit plus provoquer de surarchitecture en amont.

## Historique

| Date | Évolution |
|---|---|
| 2026-08-20 | Cadrage documentaire initial. |
| 2026-08-21 | Recadrage : phase 1 réouverte, corpus réel prioritaire, suppression des quotas, du modèle technique anticipé et de la logique de produit minimum. |
| 2026-08-21 | Phase 1 validée par l'utilisateur ; ouverture de la recherche pilote réelle. |
| 2026-08-21 | Première passe Web consignée : benchmark comparé, nouveaux candidats conservés et premiers rapprochements éditoriaux amorcés. |
| 2026-08-21 | Approfondissement ciblé effectué et causes des manques analysées : benchmark requalifié comme collecte assistée par IA, bloc Finistère redaté, candidats C16–C22 précisés, Thionville examiné et classé hors fenêtre. |
| 2026-08-21 | Couverture du 20 au 24 juillet : cinq épisodes documentés, deux fausses pistes écartées, chiffres de contexte CNCDH sourcés. |
| 2026-08-21 | Correction après revue Codex : deux épisodes manqués ajoutés (C24 Avignon, C25 Grenoble), conclusion erronée sur la couverture intégrale retirée — le 22 juillet reste sans entrée et la période n'est pas close. |
| 2026-08-21 | Recadrage du traitement : remplacement du passage éditorial par une qualification minimale, proportionnée et assortie d'une règle d'arrêt. |
| 2026-08-21 | Qualification minimale des 25 candidats : 20 admis, 3 incertains, 2 refusés, 0 rattaché, sans recherche complémentaire. |
| 2026-08-21 | Relevé descriptif des catégories apparues sur les trois axes ; deux natures nouvelles et trois chevauchements signalés. |
| 2026-08-22 | Journal des frictions ouvert : huit entrées retenues après filtre restrictif ; formulations obsolètes sur C21 corrigées. |
| 2026-08-22 | Bilan de charge : effort concentré sur la recherche, l'accès aux sources et les corrections ; la qualification elle-même reste légère. |
| 2026-08-22 | Correction après revue Codex : ajout de C26 Aurignac et C27 Bois-d'Arcy, corroborés mais omis — corpus porté à 27 candidats, 22 admis, 3 incertains, 2 refusés, 0 rattaché. |
| 2026-08-22 | Révision minimale de la méthode validée par Codex puis par l'utilisateur : Phase 2 terminée. |
| 2026-08-22 | Réorientation fonctionnelle : le corpus pilote devient un banc d'essai pour comparer des solutions simples de collecte avant toute architecture plus large. |
