# Rapport Claude — test Google News RSS : 20 des 22 faits attendus, gratuitement

**Date :** 24 août 2026
**Statut : test exécuté et concluant. Meilleur résultat des trois solutions testées, et le seul sans dépense ni compte.**

## 1. Résultat

| Mesure | Résultat |
|---|---|
| **Faits admis retrouvés** | **20 / 22** |
| Incertains retrouvés | 1 / 3 |
| **Bruit connu remonté** | **0 / 2** — C14 et C23 absents |
| Articles rapportés | 439 |
| Titres distincts | 387 |
| **Médias distincts** | **139** |
| Durée | ~25 secondes |
| **Coût** | **0,00 $** — aucune clé, aucun compte |

Comparaison avec les tests précédents, sur le même banc d'essai :

| | Sol, 4 appels | Luna, 1 appel | **Google News RSS** |
|---|---|---|---|
| Admis retrouvés | 12/22 | 5/22 | **20/22** |
| Coût | 1,95 $ | 0,088 $ | **0 $** |
| Compte requis | oui | oui | **non** |
| Filtre de dates | aucun | aucun | **natif** |

## 2. Ce qui a été fait

Fichier créé : **`prototype/bloc-2/test_gnews.py`**

| Élément | Valeur |
|---|---|
| Endpoint | `https://news.google.com/rss/search` |
| Édition | `hl=fr&gl=FR&ceid=FR:fr` — **édition française native** |
| Fenêtre | `after:2026-07-20 before:2026-08-21` — filtre natif, pas une consigne en prose |
| Requêtes | 12 requêtes lexicales, **identiques à celles du test GDELT** pour comparabilité |
| Corpus pilote | **non transmis** — aucun lieu, aucun identifiant C01-C27 |
| Dépendance ajoutée | **aucune** — parsing XML par la bibliothèque standard |

`comparer_benchmark.py` a été étendu pour lire ce format d'index d'actualités, qui n'a qu'un seul niveau de mesure : l'article est rapporté, ou il ne l'est pas. Il n'y a pas de couche de synthèse, donc pas de perte possible entre recherche et restitution — le défaut central des deux tests OpenAI **n'existe pas ici**.

## 3. Contrôle manuel — une correction

La mesure automatique annonçait 21/22. Le contrôle des titres, exigé par la méthode, a révélé **un faux positif** :

- **C15** — le motif « montagne » correspondait au **nom du média « La Montagne »**, pas au sujet. L'événement des randonneurs racisés n'est pas trouvé. Compté **non retrouvé**.

Toutes les autres correspondances ont été vérifiées sur les titres et sont exactes. Quelques exemples, qui montrent la précision de l'appariement :

- **C07** — *« Une gendarme guyanaise dénonce des faits de racisme au sein de la Garde républicaine »*, Radio Télé Peyi Guyane. Ce cas avait échappé aux deux tests OpenAI.
- **C16** — *« À Châtonnay, émotion après le suicide de Joris, victime d'injures racistes »*, ici.fr.
- **C18** — 13 articles sur la vidéo au micro BFMTV, le repère national que Sol avait rencontré sans le restituer et que Luna n'avait pas rencontré.
- **C19** — *« David Samzun déposera plainte contre Jean Messiha après un tweet visant des mineures nazairiennes en séjour à Belle-Île »*, Ouest-France.
- **C26 Aurignac**, **C27 Bois-d'Arcy**, **C03 Machecoul**, **C10 Migennes** — tous retrouvés, alors qu'ils relèvent de la couverture strictement locale, faiblesse établie du pilote.

## 4. Les deux admis manqués, et pourquoi

**C20 (Agde)** et **C15 (randonneurs)** ne sont pas remontés — ainsi que **C17 (Crépol)** parmi les incertains.

La cause n'est pas l'index : c'est **mon lexique de requêtes**. Ces trois affaires ne sont pas décrites par les termes cherchés. Crépol relève de la « circonstance aggravante de racisme », Agde d'une « campagne d'affichage stigmatisante », les randonneurs d'un débat sur la montagne « réservée aux Blancs » — aucun de ces cas ne contient « propos racistes », « agression raciste » ou « tags racistes ».

C'est corrigible en élargissant les termes, et cela n'a rien coûté à vérifier. **Le plafond réel de cette solution est donc supérieur à 20/22.**

## 5. Qualité de la matière rapportée

**Bon :**
- **Date de publication présente sur 439 articles sur 439**, au format RFC 822 exploitable.
- Média identifié pour chaque article, avec son domaine (`media_url`).
- 139 médias, dont beaucoup de titres locaux — *L'Yonne Républicaine*, *Radio SCOOP*, *Le Maine Libre*, *EVASION*, *Radio Télé Peyi Guyane*.
- Plusieurs articles par événement, ce qui donne de la matière au recoupement.

**Limites confirmées :**
- **Les 439 liens sont des URL de redirection Google**, sans exception. Le média est identifiable, l'URL d'origine de l'article ne l'est pas sans résolution supplémentaire. Cette résolution n'a **pas** été faite : un appel HTTP par article serait disproportionné à ce stade.
- **Une requête a saturé** à 100 résultats (« propos racistes ») : le plafond par appel est réel et impose de découper les requêtes trop larges.
- La date rapportée est celle de **publication**, pas celle du fait.
- Aucune documentation officielle, aucun engagement de service — la réserve de la présélection reste entière.

## 6. Fichiers

| Fichier | État |
|---|---|
| `prototype/bloc-2/test_gnews.py` | **créé** |
| `prototype/bloc-2/test_gdelt.py` | **créé** — GDELT bloqué par limite d'IP, aucun résultat |
| `prototype/bloc-2/comparer_benchmark.py` | **modifié** — lecture des formats d'index d'actualités |
| `resultats/gnews-serie-20260824T001159Z.json` | 439 articles + traces |
| `resultats/gnews-sonde-*.json`, `gdelt-sonde-*.json` | sondes |

Corpus pilote, banc d'essai, `docs/`, `SELECTION.md` et `RESULTATS-OPENAI.md` inchangés.

## 7. Confirmations

- **Aucune dépense.** Aucun appel OpenAI dans cette tâche.
- Aucune clé en cause : Google News RSS n'en demande pas.
- **Aucun commit, staging ou tag.** Le dernier commit reste `26ba1e1`.
- **Roadmap et méthodologie inchangées** ; aucune case cochée, aucun candidat admis ni requalifié.

## 8. Ce que cela change pour la comparaison

La présélection avait relégué Google News RSS au rang de secours, faute de documentation officielle. **Sur les faits, c'est la solution la plus performante des trois testées, la plus rapide, la seule gratuite et la seule sans compte** — et la seule dont la couverture locale, faiblesse centrale du pilote, est démontrée.

Son défaut réel n'est pas le rappel mais la **traçabilité des URL** et l'**absence d'engagement de service**. Ce sont deux questions à trancher avant d'en faire la solution retenue.
