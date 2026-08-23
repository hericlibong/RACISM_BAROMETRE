# Revue Codex — présélection v4 du Bloc 2

**Date :** 23 août 2026  
**Verdict : validée. Le smoke test reste en attente des accès nécessaires.**

Les quatre ajustements demandés sont présents dans le rapport et dans `prototype/bloc-2/SELECTION.md` :

- trois finalistes exactement, un par famille : OpenAI Web Search, Brave Search et GDELT ;
- Anthropic, Tavily et Google News RSS conservés comme solutions de secours, hors du premier smoke test ;
- disponibilité des clés API explicitement non supposée ;
- plafond GDELT corrigé à 75 résultats par défaut et 250 au maximum ;
- tarif OpenAI corrigé et relié à la documentation officielle ;
- aucun test, script, compte, abonnement ou appel API réalisé.

Le choix des trois finalistes est cohérent : OpenAI représente la recherche agentique la plus proche de l’expérience initiale, Brave l’API filtrable, et GDELT l’index gratuit sans authentification.

Deux décisions opérationnelles sont maintenant nécessaires avant le smoke test :

1. confirmer la disponibilité d’une clé API OpenAI facturable, distincte d’un abonnement ChatGPT ;
2. décider si l’utilisateur souhaite créer lui-même un compte Brave et fournir une clé de test.

Une clé Anthropic n’est pas nécessaire pour le premier smoke test puisque cette solution est désormais en secours.

Sans clé OpenAI ni Brave, seul GDELT pourra être testé, ce qui ne permettra pas une comparaison suffisante entre les trois familles. Après clarification des accès, un banc Python minimal pourra être préparé pour exécuter les mêmes objectifs, conserver les sorties brutes et mesurer les appels sans construire le pipeline final.

La roadmap doit rester inchangée et aucun commit ne doit être créé pour l’instant.
