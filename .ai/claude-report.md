# Rapport Claude — Bloc 2, première partie : présélection des solutions de collecte (v4)

**Date :** 23 août 2026
**Statut : ajustements de la revue Codex v3 appliqués. Aucun smoke test exécuté.**

## 1. Les quatre ajustements demandés

| # | Demande Codex | Vérification | Correction |
|---|---|---|---|
| 1 | Le smoke test contenait encore quatre solutions malgré l'annonce « une par famille » | Fondé — contradiction interne | **Trois finalistes : OpenAI web search · Brave Search · GDELT.** Anthropic, Tavily et Google News RSS deviennent des solutions de secours, non testées au premier tour |
| 2 | Les accès API ne sont pas établis ; « aucun compte nouveau » supposait une clé Anthropic non vérifiée | Fondé. Le fait que Claude Code fonctionne ne démontre pas la disposition d'une clé API facturable | Motif supprimé. **Deux points de décision explicites** ajoutés au §9, et la ligne « Authentification » du tableau comparatif passe de ✅ à ❓ pour la famille A |
| 3a | GDELT documente un plafond de 250 résultats en `ArticleList` | **Confirmé sur la documentation officielle** : `MAXRECORDS`, 75 par défaut, 250 au maximum. J'avais écrit « non documenté » | Corrigé au §5 et dans le tableau |
| 3b | Le tarif OpenAI doit venir de la page officielle ; les 25 $ concernent l'ancien outil preview avec modèles non raisonnants | **Confirmé sur la page tarifaire officielle** : outil actuel **10 $/1 000 appels**, tokens au tarif du modèle. Ma formulation « 10 $ sur modèles de raisonnement, 25 $ sur les autres » était fausse | Corrigé et sourcé sur la page tarifaire officielle |

## 2. Les trois finalistes

| Famille | Finaliste | Motif | Reléguée en secours |
|---|---|---|---|
| **A — Agentique** | **OpenAI web search** | L'option la plus proche de l'expérience initiale du projet, et **la seule de sa famille à exposer la liste complète des URL consultées** (`sources`) — donc la seule à fournir une matière à déduplication comparable aux autres familles. Même tarif | Anthropic `web_search` |
| **B — API filtrable** | **Brave Search** | 5 $/1 000 contre un palier à 30 $/mois pour Tavily au même volume ; seule à cumuler endpoint news, `country`, `search_lang` et plage de dates personnalisée | Tavily |
| **C — Index gratuit** | **GDELT** | Documentation officielle, URL primaires, aucune authentification. Google News RSS n'a aucune documentation officielle ni engagement de service | Google News RSS |

J'ai suivi la recommandation de Codex sur les trois. Le seul point où je l'aurais formulé autrement : Google News RSS reste l'option la plus prometteuse sur la couverture locale française, et c'est écrit — elle passe après, elle n'est pas enterrée.

## 3. Deux questions qui vous reviennent avant tout test

**Quels accès API possédez-vous réellement ?** Deux finalistes sur trois en dépendent :

- **OpenAI** — une clé API, distincte d'un abonnement ChatGPT ? La recherche avancée qui a produit les samples passait par l'interface, pas nécessairement par l'API.
- **Anthropic** — une clé utilisable pour l'outil `web_search` facturé ? Que Claude Code fonctionne ne le démontre pas.

**Le compte Brave.** La famille B est intestable sans compte ni clé, ce que la consigne du Bloc 2 interdit. **Je ne créerai aucun compte à votre place.** Vous créez le compte et fournissez la clé (5 $ de crédits mensuels — le test serait gratuit), ou on reporte B après A et C, ou on l'écarte.

**Conséquence** : selon vos réponses, le smoke test portera sur trois familles, deux, ou la seule famille C — la seule à ne rien exiger.

## 4. Fichiers

| Fichier | Nature |
|---|---|
| `prototype/bloc-2/SELECTION.md` | Unique livrable — **v4**, 11 sections |
| `.ai/claude-report.md` | Ce rapport |

Format minimal, banc d'essai et corpus pilote non modifiés. `.ai/codex-review.md` non modifié.

## 5. Confirmations

- **Aucun smoke test, aucun benchmark, aucun appel expérimental à une API de collecte.** Les capacités décrites viennent de documentation lue.
- **Aucun compte créé, aucun abonnement souscrit, aucune dépense engagée.**
- Aucun développement, aucune installation, aucun choix définitif de solution.
- Le Bloc 3 n'est pas commencé.
- **Roadmap inchangée** : 25 cochées / 21 ouvertes — aucune tâche du Bloc 2 cochée.
- **Git** : deux commits, aucun nouveau ; rien en staging ; aucun tag ; configuration inchangée.

## 6. Revue Codex de la v4 et suite décidée

**Verdict Codex : validée.** Les quatre ajustements sont constatés présents, le choix des trois finalistes est jugé cohérent, et aucun test, script, compte ni appel API n'a été réalisé.

Un point utile ajouté par la revue : **une clé Anthropic n'est plus nécessaire** au premier smoke test, puisque cette solution est passée en secours. Il ne reste donc que **deux** questions d'accès — clé OpenAI facturable, et décision sur le compte Brave — au lieu de trois.

Codex conclut par : « La roadmap doit rester inchangée et aucun commit ne doit être créé pour l'instant. »

**Décision de l'utilisateur : ne rien committer.** La position de Codex est suivie à la lettre.

- Aucun commit, aucun staging, aucun tag, aucune modification de configuration Git.
- Roadmap inchangée : **25 cochées / 21 ouvertes**, aucune case du Bloc 2 cochée.
- `prototype/bloc-2/` reste en non suivi dans git.
- Le smoke test n'est pas lancé et attend les réponses sur les accès.

---

**La v4 est validée sur le fond, non committée.** Le smoke test attend vos réponses sur les deux accès.
