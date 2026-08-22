# Format minimal de sortie d'un événement

Contrat **logique**, indépendant du support. Il décrit ce qu'une solution de collecte devra produire pour un événement — pas comment le stocker. Le choix CSV, JSON, SQLite ou autre reste ouvert.

## Les neuf champs

| Champ | Obligatoire | Contenu | Pourquoi il est nécessaire |
|---|---|---|---|
| `id` | oui | Identifiant stable | Le corpus pilote a montré qu'un même dossier est repris, corrigé et arbitré plusieurs fois : sans identifiant, aucune correction n'est traçable |
| `date` | oui | Date du fait. Précision variable admise : jour, intervalle, mois, ou vide si indéterminée | Deux candidats n'ont aucune date exploitable et quatre n'ont qu'une date approximative. Forcer une date unique fabriquerait de la précision |
| `lieu` | oui | Commune et département, ou mention nationale / en ligne | Sert au rapprochement et à la recherche locale, angle mort identifié pendant le pilote |
| `resume` | oui | **Une phrase courte**, factuelle | La qualification minimale s'est révélée réalisable à ce niveau de détail |
| `nature` | oui | Une ou **plusieurs** valeurs | 39 mentions pour 27 candidats : les valeurs multiples sont la règle, pas l'exception |
| `cible_dimension` | oui | Une ou **plusieurs** valeurs ; peut valoir « non déterminée » | 28 mentions pour 27 candidats. Deux cas réels — C03 et C17 — n'ont pas de cible déterminable |
| `contexte` | oui | Une valeur | Une seule suffit : aucun candidat n'en a demandé deux |
| `sources` | oui | Références ou URL nécessaires | Sans analyse par source : le pilote a montré que le détail n'est pas requis pour qualifier |
| `relation` | **non** | Lien avec un autre événement ou avec des éléments antérieurs | Facultatif. Seuls quelques cas réels en ont eu besoin |

## Ce que `relation` doit pouvoir exprimer

Trois situations rencontrées, et rien de plus :

- **Un événement relié à des éléments antérieurs** sans fusion — C15 : des réponses publiques renvoyant à des propos plus anciens. Les deux ne se confondent pas et ne se comptent pas ensemble.
- **Un événement unique comportant plusieurs observations ou résultats** — C21 : une campagne dont les constats et les plaintes sont rattachés sans devenir plusieurs événements.
- **Un épisode dont le fait initial est antérieur** à la période observée — C13, C17, C22, C24.

La forme technique de ce lien n'est pas décidée ici.

## Ce que le contrat exclut

Volontairement absents, faute de besoin démontré par le corpus :

- schéma de base de données, modèle normalisé, métadonnées techniques ;
- champ prévu pour un besoin futur hypothétique ;
- score, niveau de gravité, indice ;
- niveau de confiance chiffré ;
- règle de qualification supplémentaire — celles de `docs/METHODOLOGIE.md` suffisent ;
- analyse détaillée par source.

Le statut éditorial — admis, refusé, incertain — **ne figure pas** dans ce contrat : il relève de la décision humaine, non de la sortie d'une solution de collecte.

## Exemple

Un candidat du corpus, rendu au format :

```
id              C21
date            2026-07-24/2026-07-26
lieu            Nice, Marseille, Montpellier
resume          Une campagne de testings dans des plages privées et des
                établissements de nuit donne lieu au dépôt de huit plaintes.
nature          discrimination
cible_dimension racisme anti-Noirs ; racisme anti-Arabes
contexte        espace public
sources         sos-racisme.org ; lecourrierdelatlas.com ; toulouse7.com
relation        événement unique ; observations, résultats et 8 plaintes rattachés
```
