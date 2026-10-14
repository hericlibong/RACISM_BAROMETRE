# Revue Codex — résultats OpenAI Luna et état réel des essais

**Date :** 24 août 2026  
**Verdict :** résultat non validable comme solution de collecte. Il ne faut pas lancer un nouvel essai Luna dans cette direction.

## Conclusion principale

Le troisième test a amélioré la traçabilité technique et réduit le coût, mais il n'a pas amélioré le résultat utile au projet. Il retrouve seulement **5 des 22 candidats admis** du benchmark, dans la matière Web comme dans la restitution finale.

Le premier test avait restitué **12/22** candidats admis et en avait rencontré au moins **16/22** dans sa matière brute. La couverture du troisième test est donc très nettement inférieure. Le problème n'est plus une perte pendant la synthèse : la recherche elle-même ne rencontre pas assez d'événements.

Le fichier de sortie confirme aussi une collecte étroite et répétitive : plusieurs entrées concernent les mêmes affaires de Grenoble, Crépol ou Agde, tandis que 17 candidats admis du benchmark restent absents.

## Ce qui a réellement changé

- `web_search_call.results` a fourni 181 résultats avec titres, extraits et URL : la matière brute est désormais vérifiable.
- Le test Luna 3 a utilisé 7 appels de recherche, 63 024 jetons d'entrée et 4 557 jetons de sortie, pour un coût estimé à 0,0881 dollar.
- Les cinq candidats admis rencontrés ont tous été restitués : il n'y a pas de perte supplémentaire lors de la synthèse.

Ces améliorations sont techniques. Elles ne compensent pas la faiblesse de la couverture et ne rendent pas cette solution acceptable pour la collecte du baromètre.

## Le rapport Claude n'est plus à jour

Le rapport décrit correctement le seul test `luna3`, mais il ne décrit pas l'état actuel du répertoire :

- le script porte maintenant le préfixe `luna4` ;
- ses plafonds ont été portés à **40 appels d'outil** et **16 000 jetons de sortie** ;
- deux nouvelles exécutions ont été tentées après le test rapporté ;
- elles ont toutes les deux échoué avec une erreur de limite de débit `429` ;
- elles n'ont produit aucun résultat de recherche exploitable.

Les fichiers d'incident montrent des requêtes d'environ 71 600 à 71 800 jetons face à une limite de 200 000 jetons par minute déjà partiellement consommée. L'affirmation du rapport selon laquelle il n'y a eu qu'une exécution et aucune relance n'est donc vraie que pour le test Luna 3, pas pour l'état complet des essais présents dans le dépôt.

## Décision recommandée

1. Ne pas relancer `luna4` et ne pas augmenter encore les plafonds.
2. Considérer la variante « un appel OpenAI Luna avec recherche Web large » comme **testée et insuffisante** pour ce benchmark.
3. Conserver les fichiers produits comme preuves du test, mais ne pas valider cette variante comme solution de collecte.
4. Mettre le rapport à jour pour intégrer les deux échecs Luna 4 avant toute clôture documentaire.
5. Passer ensuite à une autre solution simple du Bloc 2, sans ajouter une nouvelle couche de prompts ou de découpages à cette variante.

Le troisième essai n'était pas inutile : il permet de conclure que le manque de couverture vient de la découverte Web opérée dans cette configuration, et non d'un simple filtrage de la réponse finale. En revanche, continuer à ajuster ce même mécanisme n'est plus justifié par les résultats.
