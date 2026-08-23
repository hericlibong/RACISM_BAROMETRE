# Bloc 2, première partie — Identification et présélection des solutions de collecte

> **État : présélection, version 4.** Aucun test exécuté, aucun compte créé, aucun abonnement souscrit, aucune dépense engagée, aucun appel expérimental à une API.
>
> **Trois finalistes, un par famille : OpenAI web search · Brave Search · GDELT.** Deux d'entre eux dépendent d'un accès API à établir — voir les points de décision du §9.

## 1. Le régime visé

Une **collecte automatisée deux fois par jour, matin et soir**, qui met à jour une base sans intervention à chaque passe.

**La fenêtre de chaque passe est glissante, de l'ordre de 24 à 48 heures — délibérément plus large que l'intervalle entre deux passes.** Ce recouvrement n'est pas un défaut à minimiser : c'est une **protection contre l'indexation tardive**. Un fait publié à 23 h et indexé à 3 h du matin serait perdu par une fenêtre strictement calée sur « depuis la passe précédente ». La déduplication est donc **attendue de tout montage**, quelle que soit la solution retenue.

**Volume réel.** Du 23 août 2026 au premier tour du 18 avril 2027 : 238 jours, soit **environ 476 passes** (442 au 1er avril, 500 au 30 avril). *La version 2 de ce document avançait 1 200 passes — chiffre faux, et toutes les extrapolations qui en découlaient ont été recalculées.*

La fenêtre du **20 juillet au 20 août 2026** n'est pas ce régime : c'est un **instrument de mesure**, 27 candidats déjà qualifiés permettant de constater ce qu'une solution retrouve, manque ou ajoute.

## 2. Ce que le régime impose comme critères

| Critère | Question posée à la solution |
|---|---|
| **Fraîcheur paramétrable** | Puis-je demander « les dernières 24 heures » autrement qu'en le formulant en prose ? |
| **Matière à déduplication** | Que me donne la solution pour reconnaître ce que j'ai déjà : URL stable, date de publication, nom du média ? |
| **Rejeu d'une période passée** | Puis-je rejouer la fenêtre de juillet-août pour le benchmark ? *(secondaire — mesure, pas exploitation)* |
| **Couverture de la presse locale** | Faiblesse établie du pilote. C'est l'inconnue que le test doit lever |
| **Coût par passe** | Extrapolé sur ~476 passes |

Sur la déduplication, deux problèmes distincts, dont un seul concerne les solutions examinées :

- **Doublon de document** — même URL, même dépêche reprise, même article revu à la passe suivante. Mécanique. C'est ici que la matière fournie par la solution compte.
- **Doublon d'événement** — plainte, enquête, comparution ne sont pas trois faits mais trois **épisodes** d'un même dossier. Les traiter comme des faits neufs gonflerait le baromètre, c'est-à-dire fausserait la mesure même que le projet produit. Ce cas n'appelle pas un rejet mais un **rattachement** (champ `relation` de [`../FORMAT-MINIMAL.md`](../FORMAT-MINIMAL.md)). **Il ne relève d'aucune solution de collecte** et ne départage donc rien.

> 🔎 **Hypothèse de montage, non acquise.** Les descriptions ci-dessous supposent qu'un agent de traitement commun suit la découverte. C'est le montage le plus probable, pas une contrainte : une solution pourrait rendre une partie du traitement inutile, ou en exiger un différent. À trancher après le test, pas avant.

## 3. Correction d'une attribution erronée

La version 1 affirmait que la recherche Web agentique « a produit le corpus pilote ». **Faux deux fois.** Les **samples du benchmark** viennent d'une recherche avancée menée par l'utilisateur avec un assistant OpenAI — le journal du pilote le documentait déjà (jetons `citeturnXXsearchYY`, paramètres `utm_source=chatgpt.com`, §3). Les **candidats C01–C27** ont été trouvés avec l'outil de recherche de la session Claude Code, cousin mais pas identique à l'outil serveur de l'API.

**Aucune solution examinée ici n'a rien produit dans ce projet.** Ce que le pilote apprend sur la recherche agentique vaut comme hypothèse transférable, pas comme résultat acquis.

## 4. Trois familles, six solutions

| Famille | Mode de découverte | Solutions retenues à l'examen |
|---|---|---|
| **A — Recherche Web agentique** | Le modèle formule ses propres requêtes, lit les résultats et relance | Anthropic `web_search` · OpenAI web search |
| **B — API de recherche filtrable + agent** | Un moteur commercial renvoie des résultats structurés et filtrables | Brave Search API · Tavily |
| **C — Index d'actualités gratuit interrogeable** | Requête sur un index de presse déjà constitué, sans compte | GDELT DOC 2.0 · Google News RSS |

Deux voies sont écartées au §8 : le scraping direct, et les flux RSS des titres eux-mêmes comme découverte principale.

## 5. Les solutions

### A1 — Anthropic `web_search` *(`_20260209` ou `_20260318`)*

- ✅ Paramètres : `max_uses`, `allowed_domains` / `blocked_domains`, `user_location`, `allowed_callers`. **Aucun filtre de date ni de fraîcheur.**
- ✅ **Tarif publié : 10 $ pour 1 000 recherches**, plus les jetons du contenu rapporté, comptés en entrée. *(La v2 laissait ce tarif « non vérifié » ; il figure dans la documentation officielle.)*
- ✅ Chaque résultat porte `url`, `title` et **`page_age`** — date de dernière mise à jour de la page. Ce n'est pas un filtre, mais **c'est une information temporelle exploitable en aval**. La v2 présentait A comme dépourvue de toute prise temporelle : c'était trop tranché.
- ✅ `web_search_20260318` accepte `response_inclusion: "excluded"`, qui retire les blocs de résultats bruts de la réponse et réduit le coût en jetons de sortie — pertinent pour un enchaînement récurrent.
- ✅ Disponible sur l'API Claude, Claude Platform on AWS et Microsoft Foundry ; sur Google Cloud, variante de base seulement ; **absente d'Amazon Bedrock**.
- 🔎 Sans paramètre de fraîcheur, la fenêtre de 24 h ne peut être demandée qu'en prose, et le filtrage retombe sur `page_age` après coup. **Ampleur réelle de la gêne : à mesurer, pas à décréter.**

### A2 — OpenAI web search

- ✅ Agentique avec les modèles de raisonnement : le modèle enchaîne ses recherches dans son raisonnement et décide s'il continue.
- ✅ Paramètres : `user_location`, `search_context_size`, filtrage de domaines (jusqu'à 100), `external_web_access`, `return_token_budget`. **Aucun filtre de date ni de fraîcheur non plus.**
- ✅ **Un champ `sources` renvoie la liste complète des URL consultées**, en plus des citations. C'est exactement la matière à déduplication qui manque le plus à cette famille — **avantage fonctionnel net sur A1**.
- ✅ Tarif officiel : **10 $ pour 1 000 appels**, plus les jetons du contenu au tarif du modèle. *(Le tarif de 25 $ parfois cité concerne l'ancien outil `preview` associé à certains modèles non raisonnants, pas l'outil actuel.)*
- 🔎 C'est la famille dont l'utilisateur a l'expérience empirique la plus proche : les samples du benchmark en viennent.

### B1 — Brave Search API

- ✅ **`freshness` accepte `pd` (24 h), `pw`, `pm`, `py` et une plage personnalisée `2026-07-20to2026-08-20`.** Couvre à la fois le régime quotidien et le rejeu du benchmark.
- ✅ Ciblage `country` et `search_lang` ; **endpoint news** dédié ; URL d'origine renvoyées.
- ✅ Tarif : **5 $ pour 1 000 requêtes, avec 5 $ de crédits gratuits chaque mois.**
- ⚠️ `count` plafonné à 20 et `offset` à 9 : environ 200 résultats maximum par requête.
- ⚠️ **Clé API, donc compte à créer — non fait.**

### B2 — Tavily

- ✅ `topic=news`, `time_range` (d/w/m/y), `start_date` / `end_date` au format `YYYY-MM-DD`, `include_domains` (300) / `exclude_domains` (150), `search_depth` sur quatre niveaux, `include_raw_content` (markdown ou texte), `max_results` jusqu'à 20.
- ⚠️ **`country` n'est disponible que sur `topic=general`** : on ne peut pas cumuler le mode actualités et le ciblage pays.
- ✅ Crédits : basic / fast / ultra-fast = 1, **advanced = 2** ; 1 000 crédits gratuits par mois.
- ⚠️ **Clé API, donc compte à créer — non fait.**

### C1 — GDELT DOC 2.0

- ✅ **Aucune authentification, aucune clé, aucune limite de débit documentée.**
- ✅ `sourcelang` (65 langues dont le français), `sourcecountry`, et **URL primaire** de chaque article en mode `ArticleList` — la meilleure matière à déduplication des six.
- ✅ `STARTDATETIME` / `ENDDATETIME` au format `YYYYMMDDHHMMSS`.
- ⚠️ `MAXRECORDS` : **75 résultats par défaut, 250 au maximum** en mode `ArticleList`.
- ⚠️ **Fenêtre interrogeable limitée à 90 jours glissants.** Sans effet en production ; le seul effet est que le benchmark de juillet-août 2026 est jouable **maintenant** et cessera de l'être **vers fin octobre 2026**.

### C2 — Google News RSS

- ✅ Gratuit, sans clé, sans compte. **Édition française native** via `hl=fr&gl=FR&ceid=FR:fr`.
- ✅ Opérateurs temporels `when:` (heures, jours, mois) et `after:` / `before:` à la journée ; opérateurs `OR`, expression exacte, exclusion, `intitle:`, `inurl:`.
- ⚠️ **Plafond de 100 articles par appel.**
- ❓ **Les liens sont des URL de redirection Google**, à résoudre pour obtenir l'URL d'origine.
- ⚠️ **Aucune documentation officielle, aucun engagement de service.** Les capacités ci-dessus sont établies par de la documentation tierce reconstituée. C'est la solution la moins bien étayée des six, et **elle n'est pas classée première pour cette raison** — la v2 la promouvait au premier rang malgré ces réserves, ce qui était incohérent.

## 6. Sources

| Solution | Source | Niveau |
|---|---|---|
| A1 | [Web search tool — documentation Claude officielle](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) | **Primaire**, lue directement |
| A2 | [OpenAI — Web search tool](https://developers.openai.com/api/docs/guides/tools-web-search) · [OpenAI — page tarifaire officielle](https://developers.openai.com/api/docs/pricing) | **Primaire**, lues directement |
| B1 | [Brave Search API — paramètres de requête](https://api-dashboard.search.brave.com/app/documentation/web-search/query) · [tarification](https://brave.com/search/api/) | **Primaire**, lues directement |
| B2 | [Tavily — référence de l'endpoint `/search`](https://docs.tavily.com/documentation/api-reference/endpoint/search) | **Primaire**, lue directement |
| C1 | [GDELT — annonce officielle DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/) · [client Python](https://github.com/alex9smith/gdelt-doc-api) | **Primaire**, lue directement |
| C2 | [Paramètres Google News RSS (NewsCatcher)](https://www.newscatcherapi.com/blog-posts/google-news-rss-search-parameters-the-missing-documentaiton) · [guide des flux](https://www.wprssaggregator.com/google-news-rss-feed/) | **Tiers uniquement — aucune documentation officielle n'existe** |
| Flux RSS | [Atlas des flux — presse régionale](https://atlasflux.saynete.com/atlas_des_flux_rss_fra_presse_region.htm) | Tiers |
| Toutes | Journal du pilote, §3, §6, §9, §14 | Interne |

## 7. Tableau comparatif

**✅ confirmé** par documentation primaire · **🔎 hypothèse** à tester · **❓ inconnu** · **⚠️ contrainte établie**

| Critère | A — Agentique | B — API filtrable | C — Index gratuit |
|---|---|---|---|
| **Fenêtre de fraîcheur 24 h** | ⚠️ Aucun paramètre ; en prose, puis filtrage a posteriori sur `page_age` | ✅ `freshness=pd` (Brave) · `time_range=day` (Tavily) | ✅ `STARTDATETIME` (GDELT) · `when:` (Google News) |
| **Matière à déduplication** | 🔎 A1 : URL + `page_age`. A2 : **liste complète des URL consultées** | ✅ URL d'origine + date ; contenu brut chez Tavily | ✅ **URL primaire** (GDELT) · ❓ URL de redirection (Google News) |
| **Rejeu du benchmark** | ⚠️ Par le texte seulement | ✅ Plage de dates native | ⚠️ GDELT : 90 jours glissants · ✅ Google News : `after:`/`before:` |
| **Reformulation autonome** | ✅ **Propre à cette famille** | ❌ | ❌ |
| **Coût sur ~476 passes** *(hypothèse : 15 recherches/passe)* | 🔎 10 $/1 000 → **≈ 71 $** de frais de recherche + jetons du contenu, **non estimés** | 🔎 Brave 5 $/1 000 → ≈ 36 $, soit ~4,50 $/mois, **potentiellement couvert par les 5 $ de crédits mensuels** · Tavily ~1 800 crédits/mois → palier 30 $/mois | ✅ **0 $** |
| Couverture du Web français | 🔎 Suggérée par le pilote, avec un autre outil | 🔎 `country`/`search_lang` (Brave) ; ⚠️ `country` indisponible en mode news chez Tavily | 🔎 `sourcelang:fra` (GDELT) · ✅ édition FR native (Google News) |
| Presse locale et régionale | 🔎 **Enjeu central du test** | 🔎 **Enjeu central du test** | 🔎 **Enjeu central du test** |
| Audiences correctionnelles | ❓ Angle mort documenté du pilote — aucune solution n'est présumée le couvrir | ❓ | ❓ |
| Authentification | ❓ Clé API requise — **la disposer n'est pas établi**, ni chez Anthropic ni chez OpenAI (§9) | ⚠️ **Compte et clé à créer** (Brave et Tavily) | ✅ **Aucune** |
| Plafond par requête | 🔎 `max_uses` au choix | ⚠️ ~200 (Brave) · 20 (Tavily) | ⚠️ **250** (GDELT, 75 par défaut) · 100 (Google News) |
| Pérennité | ✅ Produits contractuels | ✅ Services commerciaux | ✅ GDELT, projet public · ⚠️ **Google News : sans engagement** |

**Toutes les lignes de coût reposent sur une hypothèse explicite — 15 recherches par passe — qui est précisément ce que le smoke test doit mesurer.** Les jetons du contenu rapporté ne sont estimés nulle part : c'est la part la plus incertaine du coût des familles A et B.

**Sur la reproductibilité entre deux passes** : la v2 qualifiait B et C de « déterministes ». C'est faux. Un index d'actualité évolue continuellement ; deux passes identiques peuvent légitimement différer. Ce qui distingue les familles n'est pas le déterminisme mais **la part de variation imputable à la solution plutôt qu'à l'index** — et cela relève du test, pas de la documentation.

## 8. Écartées avant test

| Écartée | Motif |
|---|---|
| **Agrégateurs généralistes payants** (Currents, NewsData.io, NewsAPI.org…) | Aucune différence fonctionnelle avec la famille C, qui est **gratuite**, ni avec B, mieux dotée en filtres. Aucun besoin d'un septième candidat |
| **Flux RSS des titres comme découverte principale** | Volume ingérable sans pré-filtre lexical, et un pré-filtre sur titres manquerait par construction l'angle mort du projet — C24, audience correctionnelle sans vocabulaire distinctif. **Conservés comme complément ciblé sur les organismes** (préfectures, parquets, MRAP, LDH, SOS Racisme), où le volume est faible et la pertinence élevée |
| **RetroNews, Gallica** | Archives 1631–1950 |
| **Scraping direct des sites de presse** | 403 répétés constatés pendant le pilote ; conditions d'utilisation non tranchées ; infrastructure disproportionnée |
| **Réseaux sociaux comme source de découverte** | Décision utilisateur acquise |

## 9. Trois finalistes — une par famille

| Famille | Finaliste | Motif du choix interne | Écartée du premier test |
|---|---|---|---|
| **A — Agentique** | **OpenAI web search** | C'est l'option la plus proche de l'expérience initiale du projet — les samples du benchmark en viennent — et **la seule de sa famille à exposer la liste complète des URL consultées** (`sources`), donc la seule à fournir une matière à déduplication comparable à celle des autres familles. Même tarif que l'alternative | Anthropic `web_search` |
| **B — API filtrable** | **Brave Search** | Moins chère que Tavily (5 $/1 000 contre un palier à 30 $/mois au même volume), et seule à cumuler endpoint news, `country`, `search_lang` et plage de dates personnalisée. Tavily ne peut pas cumuler mode actualités et ciblage pays | Tavily |
| **C — Index gratuit** | **GDELT** | Documentation officielle, URL primaires, aucune authentification. Google News RSS n'a **aucune documentation officielle ni engagement de service** : la tester d'emblée reviendrait à évaluer une interface non contractuelle avant des options documentées | Google News RSS |

**Les trois écartées restent des solutions de secours**, à reprendre si leur finaliste échoue. C'est particulièrement vrai pour Google News RSS, dont l'édition française native reste l'argument le plus prometteur sur la couverture locale — mais qui doit passer après.

> ⚠️ **La version 3 de cette section proposait quatre solutions tout en annonçant « une par famille ».** Contradiction corrigée : trois finalistes, trois familles.

### Deux points de décision qui vous reviennent

**1. Quels accès API possédez-vous réellement ?** Les deux finalistes A et B en supposent un, et je ne peux pas l'établir à votre place :

- **OpenAI** — disposez-vous d'une clé API, distincte d'un abonnement ChatGPT ? La recherche avancée que vous avez utilisée pour les samples passait par l'interface, pas nécessairement par l'API.
- **Anthropic** — une clé API utilisable pour l'outil `web_search` facturé ? *Le fait que Claude Code fonctionne ne le démontre pas.* La v2 justifiait le choix d'Anthropic par « aucun compte nouveau à créer » : ce motif reposait sur une supposition non vérifiée, et il disparaît avec la promotion d'OpenAI comme finaliste.

**2. Le compte Brave.** La famille B ne peut pas être testée sans compte et sans clé, ce que la consigne du Bloc 2 interdit. **Je ne créerai aucun compte à votre place.** Trois options : vous créez le compte et me fournissez la clé (5 $ de crédits mensuels gratuits — le test ne coûterait rien) ; on reporte B après les résultats de A et C ; on écarte B.

Selon vos réponses, le smoke test pourra porter sur trois familles, deux, ou la seule famille C — qui est la seule à ne rien exiger.

## 10. Protocole de smoke test — proposé, non exécuté

Porte sur les **trois finalistes du §9**, sur la fenêtre du 20 juillet au 20 août 2026 pour le volet 1. Le périmètre effectif dépend des réponses aux deux points de décision : à défaut d'accès API, seule la famille C est testable en l'état.

### Volet 1 — Rappel sur le benchmark

| Cas | Ce qu'il est | Ce qu'il éprouve |
|---|---|---|
| **C18** — micro BFMTV, 30 juillet | National, très visible | Le rappel de base |
| **C26** — Aurignac, 1er-2 août | Presse locale seule | La couverture locale, faiblesse établie du pilote |
| **C24** — Avignon, 21 juillet | Audience correctionnelle locale | L'angle mort documenté : sept requêtes thématiques du pilote l'avaient manqué |
| **C21** — testings SOS Racisme, 17 août | Source associative, composantes multiples | L'accès aux communiqués d'organisations |
| **C14** — Finistère, refusé | Hors périmètre | S'il remonte, il sert à mesurer le bruit et le tri. **Son absence n'est pas un résultat négatif** — la v2 écrivait qu'il « doit » remonter, ce qui était faux |

**Objectifs communs, formulations libres.** Quatre angles identiques pour toutes les solutions — thématique national · **par épisode** *(le plus productif du pilote)* · nominatif de lieu · par organisme — mais **les formulations littérales ne sont pas imposées**. Contraindre un agent à la requête écrite pour un moteur neutraliserait la reformulation autonome, qui est justement la capacité que le test doit évaluer. Pour les familles B et C, les requêtes sont fixées et consignées ; pour la famille A, c'est l'objectif qui est fixé, et **les requêtes réellement formulées par le modèle font partie des résultats à conserver**.

### Volet 2 — Passe incrémentale

Deux passes espacées de quelques heures, sur une fenêtre récente de 24 heures, avec la contrainte de fraîcheur propre à chaque solution.

Ce qu'il s'agit d'établir :

- **le recouvrement** entre les deux passes — non pour le pénaliser, mais pour dimensionner le travail de déduplication ;
- **l'identifiabilité mécanique des doublons** — reconnaissables sans appeler un modèle, ou pas ?
- **le respect réel de la contrainte de fraîcheur** ;
- **la part de variation** entre deux passes qui n'est pas imputable à l'évolution de l'index.

### Résultats à conserver

Volet 1, par couple (cas × solution) : retrouvé ou non, par quel angle, après combien de requêtes · **les requêtes effectivement émises** · URL, média, date de publication · rang · le retour brut · nombre de requêtes et coût observé.

Volet 2, par solution : taille des deux passes · recouvrement · part des doublons identifiables mécaniquement · écarts de fraîcheur.

### Conditions de disqualification

Une solution est **écartée** si elle ne restitue pas d'URL exploitable, ou si son coût extrapolé sur ~476 passes est manifestement disproportionné.

**Manquer C18 déclenche un diagnostic, pas une élimination.** Il faut d'abord établir si la cause est la requête, l'indexation de la source ou la solution elle-même. Éliminer sans ce diagnostic reviendrait à condamner un outil pour une requête mal formulée.

Une solution est **reclassée en complément** si elle échoue seulement sur la presse locale. Manquer C14 n'a aucune conséquence.

## 11. Inconnues

| Inconnue | Concerne | Enjeu |
|---|---|---|
| Profondeur de la **presse locale et régionale** | Les trois familles | Faiblesse établie du pilote ; une solution qui ne l'atteint pas ne résout pas le problème principal |
| **Jetons consommés par le contenu rapporté** | A, B | Part la plus incertaine du coût ; les frais par recherche sont désormais connus, pas ceux-là |
| Ampleur réelle de la gêne due à **l'absence de filtre de fraîcheur** | A | Établie en principe, jamais mesurée ; `page_age` en atténue peut-être l'effet |
| **Résolution et stabilité des URL de redirection Google** | C2 | Conditionne toute déduplication par URL |
| **Recouvrement entre deux passes** et part de doublons identifiables mécaniquement | Les trois familles | Dimensionne le travail de déduplication |
| Nombre réel de **requêtes par passe** | Toutes | Toutes les estimations de coût en dépendent |
| Volume de **bruit** renvoyé | C surtout | Un index sans classement éditorial peut noyer les faits utiles |
| Comportement sur les **audiences correctionnelles** | Les trois familles | Angle mort documenté |
| Stabilité de la **datation** renvoyée | Les trois familles | Le pilote a montré que date de fait et date de publication sont couramment confondues |
| **Accès API réellement disponibles** | A, B | Détermine quelles familles peuvent être testées ; c'est une question à trancher avant le test, pas pendant (§9) |
| Utilité réelle du champ **`sources`** d'OpenAI pour dédupliquer | A | C'est le motif principal du choix d'OpenAI plutôt qu'Anthropic dans sa famille |
| Sort du benchmark après **fin octobre 2026** | C1 | La fenêtre de 90 jours fera sortir juillet-août 2026 du domaine interrogeable |
