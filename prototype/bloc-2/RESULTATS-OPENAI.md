# Smoke test — Solution A : OpenAI web search

> **Test exécuté le 23 août 2026.** Volet 1 complet (quatre angles, fenêtre du 20 juillet au 20 août 2026) et **première passe seulement** du volet 2. La seconde passe du volet 2 reste en attente.
>
> Ni Brave ni GDELT n'ont été testés.

## 1. Configuration — une seule, identique aux cinq appels

| Paramètre | Valeur |
|---|---|
| API | Responses API, SDK Python `openai` 3.3.1 |
| Modèle | **`gpt-5.6`** |
| Outil | `[{"type": "web_search"}]` |
| `include` | `["web_search_call.action.sources"]` |
| `max_tool_calls` | **8** |
| `max_output_tokens` | 8000 |
| Raisonnement | non paramétré — défaut du modèle |
| Clé | `OPENAI_API_KEY`, lue depuis `.env`, jamais affichée ni écrite |

Script : [`test_openai_websearch.py`](test_openai_websearch.py). Résultats bruts : [`resultats/`](resultats/).

## 2. Exécution

| Angle | Volet | Début (UTC) | Durée | Recherches `search` | Pages ouvertes | URL listées dans `sources` | Événements rendus |
|---|---|---|---|---|---|---|---|
| national | 1 | 18:05:12 | 67,5 s | 6 | 3 | 92 | 3 |
| episode | 1 | 18:06:42 | 117,2 s | 8 | 1 | 138 | 11 |
| lieu | 1 | 18:08:39 | 105,1 s | 8 | 1 | 126 | 7 |
| organisme | 1 | 18:10:24 | 70,9 s | 7 | 2 | 93 | 8 |
| **passe1** | **2** | **18:12:29** | 74,2 s | 7 | 2 | 106 | 2 |
| | | | **7 min 15 s** | **36** | **9** | **555** | **31** |

**5 appels API. Statut `completed` pour les cinq, aucune réponse tronquée.**

> ⚠️ **Le plafond a été saturé aux cinq appels** : 9 items de recherche à chaque fois, alors que `max_tool_calls` valait 8. L'écart d'une unité est constant et inexpliqué.
>
> **Correction du 23 août, après revue Codex.** Ce document affirmait auparavant que le modèle avait été « interrompu ». **Les données ne le démontrent pas** : les cinq réponses portent le statut `completed` et n'ont aucun `incomplete_details`. La saturation du plafond le rend suspect et a pu limiter le parcours, mais aucune troncature n'est établie.

## 3. Requêtes réellement formulées par le modèle

Aucune requête n'a été imposée : seul l'objectif l'était. Voici ce que le modèle a produit de lui-même.

> **Complété le 23 août.** Chaque `web_search_call` porte en réalité **jusqu'à quatre requêtes parallèles**, dans un champ `action.queries` que mon premier dépouillement ignorait au profit de `action.query`. Le modèle a donc formulé **115 requêtes au volet 1** et 142 au total, non 36. La liste ci-dessous n'en montre que la première de chaque groupe. Parmi les requêtes ainsi révélées figure un **balayage de la fenêtre par tranches de dates successives** (`"25 juillet 2026" OR "26 juillet 2026" OR …`, puis les tranches suivantes jusqu'au 20 août) : la couverture temporelle était plus méthodique que ce document ne le laissait croire.

**Angle national** — `site:lemonde.fr raciste OR antisémitisme OR xénophobe France "juillet 2026"` · `France acte raciste antisémite xénophobe "20 juillet 2026" OR "21 juillet 2026" OR "22 juillet 2026" OR "23 juillet 2026" OR "24 juillet 2026"` · `site:lemonde.fr/societe/article/2026/08 raciste France` · `"Cette violence atteint directement ma vie" Rennes injures racistes dégradations 14 août 2026` · `site:leparisien.fr "élue LFI à Rennes" "injures racistes"` · `Aminata Pouye agression raciste samedi août 2026 Bordeaux Talence`

**Angle episode** — `France racisme plainte enquête mise en examen condamnation préfet maire "juillet 2026"` · `"Publié le" "juillet 2026" raciste plainte France enquête` · `site:franceinfo.fr "août 2026" raciste plainte enquête` · `"La Flèche" tags néonazis enquête ouverte 3 août 2026` · `projet attaque synagogue Sarcelles six hommes présentés justice juillet 2026 PNAT` · `raciste condamné tribunal "20 juillet 2026" France` · `Aminata Pouye agression raciste plainte 9 août 2026 Talence` · `Tomer Eyal agressé parc loisirs Val-d'Oise 7 août 2026 plainte 11 août`

**Angle lieu** — `site:fr "raciste" "août 2026" commune` · `"Espaly-Saint-Marcel" "injures racistes" enfants 2026` · `site:ledauphine.com 2026/07 raciste Isère Joris Châtonnay` · `site:ouest-france.fr 2026/08 "raciste" "août 2026"` · `site:fr 2026/08 "antisémites" "commune" "août"` · `Trélissac fresque Louise Michel tags antisémites 7 août 2026 local` · `Yonne recrudescence inscriptions agressions racistes août 2026 associations habitants` · `site:lyonne.fr "Ça rappelle des heures très sombres de l'Histoire" tags racistes Migennes`

**Angle organisme** — `site:sos-racisme.org juillet 2026 racisme antisémitisme discrimination France` · `site:crif.org août 2026 antisémitisme agression menace dégradation France` · `France "20 juillet 2026" raciste antisémite xénophobe` · `Marboz féria chants racistes juillet 2026 date` · `site:mrap.fr/ "août 2026" raciste OR antisémite OR xénophobe` · `"LICRA" "août 2026" antisémitisme France` · `Aminata Pouye agression raciste 15 août 2026 mairie Talence communiqué`

**Passe 1 (24 h)** — `France raciste OR racisme OR antisémite OR antisémitisme OR xénophobe OR xénophobie 23 août 2026` · `"23 août 2026" "raciste" France agression OR insultes OR tags` · `site:mediapart.fr "drapeau" "Rhodésie" militaires 23 août 2026` · `"militaires" "drapeau suprémaciste blanc" Mediapart Nîmes` · `"Publié le 23 août 2026" "raciste"` · `site:mediapart.fr/journal/france/230826 Rhodésie militaires` · `AMFIS 2026 Châteauneuf-sur-Isère Domaine Ô Lac 20 23 août 2026`

**Trois observations sur ce comportement.**

1. **Le modèle compense l'absence de filtre de fraîcheur par des dates littérales** — `"20 juillet 2026" OR "21 juillet 2026" OR …`, `"Publié le 23 août 2026"`. C'est exactement le contournement en prose que la présélection anticipait, et il fonctionne partiellement.
2. **Il se rabat massivement sur `site:`** — `lemonde.fr`, `ouest-france.fr`, `ledauphine.com`, `lyonne.fr`, `sos-racisme.org`, `crif.org`, `mrap.fr`. La couverture dépend donc des titres que le modèle décide d'interroger.
3. **Il reformule à partir de ce qu'il vient de lire** : deux requêtes citent des extraits d'articles (`"Cette violence atteint directement ma vie"`, `"Ça rappelle des heures très sombres de l'Histoire"`) et une cible un nom propre découvert en cours de route (`Joris Châtonnay`). C'est la capacité propre à cette famille, et elle est visible.

Quatre requêtes ont renvoyé **0 source**, dont trois sur des noms propres précis (`Tomer Eyal…`, `Aminata Pouye… communiqué`, `AMFIS 2026…`).

## 4. Les cinq repères du protocole

| Repère | Ce qu'il éprouve | Résultat | Par quel angle |
|---|---|---|---|
| **C18** — micro d'une chaîne d'info, 30 juillet | Le rappel de base, cas national très visible | ❌ **Non retrouvé** | Aucun |
| **C26** — Aurignac, 1er-2 août | Presse locale seule | ❌ **Non retrouvé** | Aucun |
| **C24** — Avignon, audience du 21 juillet | L'angle mort documenté du pilote | ✅ **Retrouvé** | `episode` |
| **C21** — testings SOS Racisme | Source associative, composantes multiples | ⚠️ **Retrouvé mais éclaté** | `organisme` |
| **C14** — Finistère, refusé | Mesure du bruit | Non remonté — sans conséquence |

### C24 : le meilleur résultat du test

L'angle `episode` a retrouvé la condamnation d'Avignon **et l'a datée correctement** : `date_fait = 2026-05-27`, résumé mentionnant la condamnation du 21 juillet. La distinction entre le fait et son épisode judiciaire — que le pilote avait manquée sept fois — est ici **restituée spontanément**. Même comportement correct sur C17 (Crépol, daté 2023-11-18/19) et C22 (Sarcelles).

### C21 : retrouvé, mais découpé à l'inverse de la règle

L'angle `organisme` a trouvé les deux communiqués de SOS Racisme et **en a tiré six événements distincts** — La Grande-Motte, Montpellier, Marseille, Antibes, Nice (deux entrées). Le banc d'essai impose l'inverse : *« événement unique ; observations, résultats et huit plaintes rattachés — ne pas éclater »*.

Ce n'est **pas un défaut de rappel mais de granularité**. La matière est là, complète et bien sourcée ; c'est la décision de regroupement qui manque.

> **Correction du 23 août, après revue Codex.** Ce document présentait cet éclatement comme un défaut irréductible de la solution. C'est excessif : **la règle de l'événement unique n'était pas transmise dans le prompt**. Il s'agit donc aussi, et peut-être d'abord, d'un défaut de consigne. Ce que le test établit, c'est que la solution ne regroupe pas spontanément ; il n'établit pas qu'elle en serait incapable si on le lui demandait.

### C18 et C26 : diagnostic, pas élimination

Conformément au protocole, l'absence de C18 appelle un diagnostic avant tout jugement. Trois causes possibles, non départagées par ce test :

- **le plafond** — saturé aux cinq appels, le modèle a été coupé alors qu'il cherchait encore ; c'est la cause la plus plausible et elle m'est imputable, pas à la solution ;
- **l'angle** — C18 est un fait « en ligne », sans lieu ni suite judiciaire : il ne tombe idéalement dans aucun des quatre angles, et l'angle national n'a produit que 3 événements ;
- **l'indexation** — non vérifiée.

Pour C26 (Aurignac), l'angle `lieu` a bien travaillé la presse régionale et rapporté sept faits locaux, mais sur d'autres départements. Rien n'indique que la source soit inaccessible : le modèle n'a simplement pas interrogé la Haute-Garonne.

## 5. Ce que le test retrouve du corpus pilote

> **Mesure corrigée le 23 août, après revue Codex.** Ce document annonçait « 14 des 27 candidats ». **C'était une mesure mal construite** : elle additionnait admis et incertains, sur un dénominateur incluant les deux candidats rejetés — qu'une bonne collecte n'a justement pas vocation à produire. Elle est remplacée par trois mesures distinctes.

| Mesure | Résultat |
|---|---|
| **Rappel final — admis restitués** | **12 / 22** |
| Couverture des incertains | 2 / 3 |
| Rejetés remontés à tort | 0 / 2 — *ne comptent pas comme cibles manquées* |
| Rappel de la couche **recherche** — admis dont une source a été consultée | **16 / 22** |

**12 admis sur 22, c'est-à-dire 10 manqués, est insuffisant** pour une solution destinée à collecter les faits du baromètre.

### Trois niveaux à ne pas confondre

Le test mesure une chaîne, pas un seul geste :

1. **rencontré** — une source correspondante figure dans les traces `action.sources` ;
2. **restitué** — le candidat figure dans la sortie finale du modèle ;
3. **admis** — décision éditoriale, hors du champ de ce test.

**Quatre candidats ont été rencontrés puis perdus pendant la synthèse** : C13 (URL de la LDH sur Espaly-Saint-Marcel), C16 (quatre pages sur Châtonnay, dont *Le Dauphiné*), C18 (article Ozap sur la plainte pour usurpation d'identité) et C20 (article sur l'affiche d'Agde retirée). La recherche Web les avait trouvés ; c'est l'étape de sélection qui les a écartés.

Le tableau complet candidat par candidat est reproductible hors ligne :

```powershell
.\.venv\Scripts\python.exe prototype\bloc-2\comparer_benchmark.py resultats\openai-national-*.json resultats\openai-episode-lieu-organisme-*.json
```

| ID | Référence | URL consultée | Restitué |
|---|---|---|---|
| C01 C02 C04 C05 C06 C08 C09 C10 C11 C12 C21 C24 | admis | oui | **oui** |
| **C13 C16 C18 C20** | admis | **oui** | **non** — perdus à la synthèse |
| C03 C07 C15 C19 C26 C27 | admis | non | non — jamais rencontrés |
| C17 C22 | incertain | oui | oui |
| C25 | incertain | non | non |
| C14 C23 | rejeté | non | non — aucun bruit |

| Retrouvés | Angle(s) | Datation restituée |
|---|---|---|
| C01 Marboz | lieu, organisme | 25 juillet ✅ |
| C02 Nanterre | episode, lieu | 26 juillet ✅ |
| C04 La Flèche | episode, lieu | 2-3 août ⚠️ *(corpus : 3-4 août)* |
| C05 Trélissac | lieu, organisme | 6 août ✅ |
| C06 Caen | episode, lieu | 8 août ✅ |
| C08 Rennes | national | 7-8 août ✅ |
| C09 Talence | episode | 8-9 août ✅ |
| C10 Migennes | lieu | 5 août ⚠️ *(corpus : date indéterminable)* |
| C11 Avignon, touristes | national, episode | 11 août ✅ |
| C12 Les Deux-Alpes | national, episode | 14 août ✅ |
| C17 Crépol *(incertain)* | episode | nov. 2023 ✅ |
| C21 testings | organisme | 24-26 juillet ✅ mais éclaté |
| C22 Sarcelles *(incertain)* | episode | 11 juillet ✅ |
| C24 Avignon, audience | episode | 27 mai ✅ |

**Non restitués** : C03, C07, C13, C15, C16, C18, C19, C20, C26, C27 — dix candidats attendus, dont **quatre avaient pourtant une source dans les traces** (voir ci-dessus). Pour C13 et C16, le modèle avait même formulé la requête exacte — `"Espaly-Saint-Marcel" "injures racistes" enfants 2026` et `site:ledauphine.com 2026/07 raciste Isère Joris Châtonnay` — consulté les pages, puis ne les a pas retenues.

**Six seulement n'ont jamais été rencontrés** : C03, C07, C15, C19, C26, C27.

**Sur la datation**, deux écarts seulement, et de sens opposés : un décalage d'un jour sur C04, et surtout **C10, que le modèle date du 5 août là où le pilote avait conclu que la date était indéterminable**. La solution est plus assertive que le corpus sur les dates — c'est un risque, pas une qualité.

## 6. Nouveaux candidats — non admis

Trois faits absents du corpus pilote, dans la fenêtre :

| Fait | Date | Source | Réserve |
|---|---|---|---|
| Lyon — danseurs et musicien d'une compagnie visés par des insultes racistes et homophobes, puis des tirs de mortier | 1er août | `europesays.com` | **Source à vérifier** : agrégateur, pas un titre de presse |
| Strasbourg (Neudorf) — inscriptions associant « Juifs » à une étoile de David | 5 août | `pokaa.fr`, `strasbourg.eu` | Source municipale solide |
| Sarcelles — deux hommes condamnés pour des saluts nazis devant une synagogue | 11 août *(épisode judiciaire)* | `leparisien.fr` | Distinct de C22 |

Et deux hors fenêtre, issus de la passe 1 : les militaires du 2e REI posant avec un drapeau rhodésien (Nîmes), et des propos tenus aux universités d'été de LFI visant le CRIF — ce dernier **sourcé sur un seul média militant**, et de qualification incertaine.

**Aucun n'est admis ici.** Le test mesure une solution, il ne qualifie pas de candidats.

## 7. Faux positifs, doublons, qualité des sources

**Faux positifs : non mesurables en l'état.** C14 et C23 ne sont pas remontés, et aucun fait manifestement hors périmètre thématique n'a été produit.

> **Correction du 23 août, après revue Codex.** Ce document concluait « aucun faux positif ». **C'était prématuré** : les nouveaux candidats n'ont pas été qualifiés et plusieurs reposent sur des sources faibles ou discutables. Un faux positif ne se constate qu'après examen éditorial, qui n'a pas eu lieu. Ce que le test établit se limite à ceci : **les deux cas de bruit connus du banc d'essai ne sont pas remontés**.

**Doublons.** 31 événements rendus pour environ **22 faits distincts** au volet 1.

- **Inter-angles** : sept faits produits par deux angles. Trois sont détectables **mécaniquement par URL identique** (Nanterre, La Flèche, Avignon) ; les quatre autres partagent le fait sans partager l'URL — la déduplication mécanique par URL en attraperait donc **moins de la moitié**.
- **Intra-angle** : les six lignes de la campagne de testings, qui ne relèvent pas d'une déduplication mais d'un rattachement.

**Traçabilité des sources.** C'était le motif du choix d'OpenAI dans sa famille, et il tient : `include=["web_search_call.action.sources"]` a listé **555 URL consultées** sur les cinq appels. Contrôle effectué sur les 45 URL restituées par le modèle : **aucune ne porte sur un domaine jamais consulté**. Six URL exactes ne figurent pas dans la liste, toutes sur `sos-racisme.org`, un domaine bien consulté — vraisemblablement des pages ouvertes via `open_page`, dont les sources **ne sont pas remontées**. C'est une lacune : les 9 ouvertures de page du test sont invisibles dans `sources`.

⚠️ **Les citations structurées sont absentes** : `annotations` est vide sur les cinq appels, parce que le modèle répond en JSON. Les URL viennent donc du texte produit par le modèle, pas d'un champ garanti par l'API. Le contrôle ci-dessus montre que c'est fiable ici, mais c'est une garantie empirique, pas contractuelle.

## 8. Effort humain restant

Pour ces 31 lignes : fusionner les six lignes de testings en un événement, rapprocher les sept doublons inter-angles dont quatre échappent à l'URL, vérifier les sources faibles (`europesays.com`, `inforadar.fr`, un blog Mediapart, `le-dossier.fr`, `francemag.fr`), contrôler la date de C10 que le modèle affirme alors que le pilote la disait indéterminable, et décider de l'admission. **Le tri éditorial reste entier ; la recherche et la mise en forme, non.**

## 9. Coût

**L'API ne renvoie aucun montant**, mais elle renvoie le **décompte facturable** : `tool_usage.web_search.num_requests`.

| Mesure | Volet 1 (4 appels) | Passe 1 | Total |
|---|---|---|---|
| Appels API | 4 | 1 | **5** |
| Items `web_search_call` | 36 | 9 | 45 |
| Requêtes formulées (`action.queries`) | 115 | 27 | 142 |
| **Requêtes facturées (`num_requests`)** | 25 | 6 | **31** |
| Jetons d'entrée | 276 289 | 61 168 | **337 457** |
| dont en cache | 13 185 | 4 395 | 17 580 |
| Jetons de sortie | 14 828 | 2 722 | **17 550** |
| dont raisonnement | 9 503 | 2 542 | **12 045** |

`gpt-5.6` est l'alias de **GPT-5.6 Sol**, le modèle haut de gamme. Aux tarifs officiels relevés le 23 août 2026 — 4 $/M en entrée, 0,40 $/M en entrée mise en cache, 20 $/M en sortie, et 10 $/1 000 appels d'outil Web :

| Poste | Calcul | Montant |
|---|---|---|
| Entrée hors cache | 319 877 × 4 $/M | 1,280 $ |
| Entrée en cache | 17 580 × 0,40 $/M | 0,007 $ |
| Sortie | 17 550 × 20 $/M | 0,351 $ |
| Outil Web | 31 × 0,01 $ | 0,310 $ |
| | | **≈ 1,95 $** |

Le tableau de facturation OpenAI reste la source définitive du montant réellement débité.

**Extrapolation.** Une passe récente comme celle observée revient à **≈ 0,35 $** avec Sol, soit **≈ 165 $ pour 476 passes**. **La configuration testée n'est pas adaptée à une collecte récurrente.** Aux tarifs de GPT-5.6 Luna (0,20 $/M et 1,20 $/M), les mêmes jetons auraient coûté **≈ 0,085 $** au lieu de 1,64 $ — l'outil Web, dont le prix ne dépend pas du modèle, deviendrait alors la dépense principale.

**Ce que le test lève, en revanche, c'est l'inconnue principale** : le contenu Web rapporté coûte **environ 61 000 à 71 000 jetons d'entrée par appel**. Extrapolé aux ~476 passes du régime visé, à raison d'une passe comme celle observée : **≈ 29 millions de jetons d'entrée et ≈ 4 300 recherches**. C'est la donnée qui manquait le plus, et elle est désormais mesurée.

## 10. Limites et incidents

- **Plafond saturé aux cinq appels** : le test mesure autant mon `max_tool_calls=8` que la solution. Une reprise à plafond plus élevé changerait probablement le rappel.
- **Un incident de script**, sans appel API ni coût : la première tentative de passe 1 a échoué sur un `KeyError` — `str.format()` interprétait les accolades du JSON de consigne. Corrigé par substitution littérale, puis relancé. Zéro appel facturé sur l'exécution échouée.
- **`open_page` n'expose pas ses sources**, ce qui crée un angle mort de traçabilité.
- **Pas de citations structurées** dès lors que la réponse est demandée en JSON.
- **Aucun rang de résultat** n'est exposé par l'API : le protocole demandait de conserver le rang, ce n'est pas possible ici.
- Un seul essai par angle : **aucune mesure de la variabilité** entre deux exécutions identiques.

## 11. État du volet 2

**Première passe effectuée le 23 août 2026 à 18:12:29 UTC.** Elle a rendu 2 événements pour 7 recherches.

**La seconde passe est abandonnée à ce stade**, sur décision de la revue Codex du 23 août : elle mesurerait le recouvrement entre deux passes, alors que ce qui bloque l'évaluation est la faiblesse du rappel. Le recouvrement, la part de doublons mécaniquement identifiables et le respect réel de la contrainte de fraîcheur **restent donc non mesurés**, et ce n'est pas la priorité.
