# Journal de recherche pilote — 20 juillet au 20 août 2026

> **État : en cours.** Ce fichier est un support éditorial Markdown, pas un schéma technique. Les candidats restent non admis tant que leur examen n'est pas consigné.

## 1. Fenêtre et objectif

- **Fenêtre d'actualité recherchée :** 20 juillet 2026 → 20 août 2026 inclus.
- **Première passe :** 21 août 2026.
- **Approfondissement ciblé :** 21 août 2026 (deuxième passe).
- **Objectif :** rechercher largement les faits et épisodes d'actualité potentiellement liés au périmètre, puis comparer les résultats au benchmark informel des samples.

Un fait initial peut être antérieur à la fenêtre si une révélation, une décision judiciaire, une nouvelle diffusion ou une autre actualité significative intervient pendant celle-ci.

## 2. Règles de travail

1. Conserver les candidats plausibles avant de décider de leur admission.
2. Documenter chaque famille de requêtes et les principaux résultats.
3. Évaluer ce que chaque document rapporte sans confondre publication médiatique et confirmation du fait.
4. Rapprocher les résultats susceptibles de concerner le même fait ou la même série.
5. Comparer la découverte au benchmark sans considérer celui-ci comme validé ou exhaustif.

### Conservation minimale des consultations

Pour ce pilote, la conservation reste volontairement légère : noter l'URL directe, le média ou l'organisme, la date de publication, la date de consultation et ce que le document permet réellement d'établir. Si une page est inaccessible, conserver l'URL et signaler la limite ; ne pas remplacer une lecture manquante par une affirmation certaine.

## 3. Nature et statut du benchmark

> ⚠️ **Le benchmark n'est pas un matériau vérifié.** Cette section a été ajoutée lors de l'approfondissement du 21 août.

Les samples proviennent d'une **collecte assistée par IA**, et non d'un relevé humain. Les indices en sont matériels :

- `SAMPLES_EVENTS.md` contient des jetons `citeturnXXsearchYY`, marqueurs de citation propres à un assistant doté de recherche Web ;
- `FORGETED_SAMPLE.md` est le transcript d'un dialogue avec un assistant, et ses URLs portent le paramètre `utm_source=chatgpt.com` ;
- `SAMPLES_EVENTS.md` et `SAMPLES_EVENTS_2.md` étaient des **doublons exacts** — empreinte MD5 identique (`a3dd703309e3f587c9e63845c68eb339`). Le benchmark ne repose donc que sur un seul jeu de références, et non deux. *(Le doublon `SAMPLES_EVENTS_2.md` a été retiré du dépôt le 21 août ; `SAMPLES_EVENTS.md` conserve la même empreinte.)*

Conséquences retenues :

1. **Les attributions de source des samples ne valent pas vérification.** L'approfondissement en a confirmé plusieurs comme erronées : le bloc Finistère est attribué à *La Dépêche*, titre du Sud-Ouest, alors que les sources réelles sont Ouest-France et ICI ; Bois-d'Arcy est attribué au *Parisien*, alors que les sources retrouvées sont la préfecture des Yvelines, franceinfo et ICI.
2. **Le contenu factuel des samples peut être inexact.** B03 en donne l'exemple le plus net : le sample décrit « deux agressions distinctes », les sources rapportent une seule séquence faisant trois blessés.
3. **Le taux de recouvrement avec les samples n'est pas un taux de couverture du réel.** Il mesure l'accord entre deux collectes, dont l'une n'est pas validée.

Le benchmark est néanmoins **conservé** : il reste un instrument utile pour comparer les performances de recherche d'une passe à l'autre, à condition de ne jamais le lire comme une mesure d'exhaustivité.

## 4. Benchmark informel — état après approfondissement

Les 21 lignes proviennent des samples (20 de `SAMPLES_EVENTS.md`, 1 de `FORGETED_SAMPLE.md`). Elles ne correspondent pas nécessairement à 21 événements distincts.

Trois statuts sont utilisés : **corroboré** (au moins une source solide lue, fait et date établis), **repris de la 1re passe** (non réexaminé lors de l'approfondissement), **non corroboré**.

| ID | Référence du sample | Statut après approfondissement | Sources et précisions |
|---|---|---|---|
| B01 | Marboz — chants racistes | **Corroboré** | Fait : 25 juillet, Féria de Marboz (Ain). [Le Progrès, 28 juillet](https://www.leprogres.fr/societe/2026/07/28/un-chant-raciste-ternit-la-feria-de-marboz-la-licra-veut-porter-plainte), [MRAP](https://mrap.fr/le-mrap-depose-plainte-apres-des-chants-racistes-a-la-feria-de-marboz.html), [relais AFP/Yahoo](https://fr.news.yahoo.com/naime-bougnoules-apr%C3%A8s-chants-racistes-161132809.html). Plainte Licra annoncée le **29 juillet** ; préfet de l'Ain saisit le parquet. Le détail du sample « sept gardes à vue, cinq poursuivies » n'est corroboré par aucune source lue. |
| B02 | Nanterre — insultes antisémites contre un rabbin | **Corroboré** *(source stable substituée)* | Fait : dimanche 26 juillet, magasin Lidl. Plainte déposée le jour même ; parquet de Nanterre ouvre une enquête pour **injure publique à raison de l'origine, l'ethnie, la nation, la race ou la religion** ; auteur non identifié à ce stade. [franceinfo](https://www.franceinfo.fr/societe/antisemitisme/une-enquete-ouverte-apres-une-plainte-du-rabbin-de-nanterre-pour-des-injures-antisemites_8128964.html), [CNews, 30 juillet](https://www.cnews.fr/faits-divers/2026-07-30/sale-juif-retourne-en-israel-le-rabbin-de-nanterre-victime-dune-agression), [Defense-92 — **page d'article stable**](https://www.defense-92.fr/faits-divers/une-enquete-ouverte-apres-la-plainte-dun-rabbin-de-nanterre-cible-dinsultes-antisemites-88374). Le fil d'activité dynamique retenu en 1re passe est abandonné. |
| B03 | Machecoul-Saint-Même — « deux agressions racistes » | **Corroboré, mais le sample est inexact** | Fait : 30 juillet en début de soirée. Les sources rapportent **un homme à trottinette blessant trois personnes à l'arme blanche en tenant des propos racistes** — une séquence, trois victimes, et non « deux agressions distinctes ». Chronologie judiciaire : suspect interpellé et placé en garde à vue le **5 août** ; l'enquête retient le caractère raciste le **6 août**, une **expertise psychiatrique** est demandée ; le parquet requiert l'incarcération en détention provisoire le **7 août**. Source lue : [index relayant Ouest-France](https://faitsdivers365.fr/pays-de-la-loire/loire-atlantique/machecoul/) (titres et dates vérifiés). Article primaire Ouest-France non ouvert. |
| B04 | Aurignac — agression d'un adolescent demandeur d'asile | **Corroboré** *(deux sources)* | Fait : nuit du 1er au 2 août, en marge de la fête du village. Garçon de 16 ans originaire d'Asie centrale, hébergé au Prahda, insulté puis roué de coups par un groupe de 7 à 8 personnes ; points de suture au visage ; plainte déposée avec le soutien du maire. [Petite République, 17 août](https://www.petiterepublique.com/2026/08/17/acte-de-violence-raciste-inqualifiable-a-aurignac-le-communique-de-la-mairie-et-des-associations/) et [InfOccitanie](https://infoccitanie.fr/carole-delga-le-racisme-gagne-du-terrain-nous-le-combattrons-sans-relache/) (déplacement de la présidente de région au Prahda). |
| B05 | La Flèche — graffitis néonazis | Repris de la 1re passe | [L'Est Républicain, 4 août](https://www.estrepublicain.fr/faits-divers-justice/2026/08/04/des-actes-odieux-une-enquete-ouverte-apres-des-tags-neo-nazis-a-la-fleche) |
| B06 | Trélissac — fresque de Louise Michel dégradée | Repris de la 1re passe | [Le Parisien, 7 août](https://www.leparisien.fr/faits-divers/dordogne-une-fresque-en-hommage-a-louise-michel-degradee-un-tag-antisemite-et-des-inscriptions-antifeministes-decouverts-07-08-2026-PUOTK5KUYBEATFELVVLKRQDSUU.php) |
| B07 | Caen — agression d'adolescentes voilées | Repris de la 1re passe | [Anadolu, 10 août](https://www.aa.com.tr/fr/journal-de-lislamophobie/france-une-vid%C3%A9o-montrant-l-agression-raciste-d-une-adolescente-%C3%A0-caen-suscite-l-indignation/4023156) |
| B08 | Paris — racisme dénoncé dans la Garde républicaine | Repris de la 1re passe | [Péyi Guyane, 8 août](https://peyiguyane.com/post/faits-divers/une-gendarme-guyanaise-denonce-des-faits-de-racisme-au-sein-de-la-garde-republicaine-1786289333) |
| B09 | Rennes — véhicule de Régine Komokoli dégradé | Repris de la 1re passe | [TF1 Info, 12 août](https://www.tf1info.fr/justice-faits-divers/une-elue-lfi-a-rennes-victime-d-injures-racistes-et-de-degradations-une-procedure-ouverte-2458450.html) |
| B10 | Talence — agression dénoncée par Aminata Pouye | Repris de la 1re passe | [Le Parisien, 10 août](https://www.leparisien.fr/faits-divers/gironde-la-candidate-lfi-aux-senatoriales-denonce-une-attaque-raciste-et-annonce-porter-plainte-10-08-2026-W3HTDG7U3RHVBAI4PKWRNFQDTY.php) |
| B11 | Migennes — inscriptions racistes | **Corroboré** *(source régionale substituée)* | Tags sous un pont à Migennes : « Sauvons la France », « Ligature des trompes aux bougnoules », « Bougnoules dehors ». Selon la présidente du MRAP 89, ils étaient **présents depuis plusieurs semaines** au 15 août — la date du fait est donc diffuse, et le « 11 août » du sample ne correspond qu'au signalement. **Signalement au procureur de Sens** ; le MRAP se réserve le droit de porter plainte. Précédent de mars 2026 près de Bassou. [France 3 Bourgogne-Franche-Comté](https://france3-regions.franceinfo.fr/bourgogne-franche-comte/yonne/des-tags-racistes-appelant-a-la-sterilisation-des-bougn-ules-dans-l-yonne-un-inquietant-faisceau-de-montee-de-la-haine-3402001.html). L'index d'agrégateur de la 1re passe est abandonné. |
| B12 | Avignon — menaces antisémites contre des touristes juifs | Repris de la 1re passe | [Communiqué ministériel, 13 août](https://presse.economie.gouv.fr/serge-papin-et-aurore-berge-condamnent-avec-la-plus-grande-fermete-les-menaces-antisemites-visant-un-couple-de-touristes-juifs-en-france/) |
| B13 | Les Deux-Alpes — propos antisémites d'une commerçante | Repris de la 1re passe | [Place Gre'net, 16 août](https://www.placegrenet.fr/2026/08/16/les-deux-alpes-une-enquete-ouverte-apres-les-propos-dune-commercante-visant-la-communaute-juive-dans-une-video/687408). Précision : vidéo diffusée le 14 août, enquête de la gendarmerie annoncée le 15 août par le ministre de l'Intérieur. |
| B14 | Espaly / Le Puy-en-Velay — condamnation | Repris de la 1re passe | [Courrier de l'Atlas, 18 août](https://www.lecourrierdelatlas.com/condamnation-injures-racistes-enfants-haute-loire/) |
| B15 | Bois-d'Arcy — croix gammée sur la police municipale | **Corroboré** *(trois sources, dont institutionnelle)* | Faits : week-end du **15-16 août**. Croix gammée et slogans nationalistes (« Bois d'Arcy nationaliste ») sur les murs du poste de police municipale. Plainte de la mairie, vidéosurveillance analysée. [Préfecture des Yvelines — communiqué](https://www.yvelines.gouv.fr/Actualites/Communiques-de-presse2/Bois-d-Arcy-le-prefet-des-Yvelines-condamne-fermement-les-inscriptions-haineuses), [franceinfo](https://www.franceinfo.fr/societe/antisemitisme/une-violence-politique-des-slogans-nationalistes-et-une-croix-gammee-tagues-sur-les-murs-de-la-police-municipale-de-bois-d-arcy-dans-les-yvelines-la-mairie-porte-plainte_8155409.html), [ICI](https://www.ici.fr/ile-de-france/yvelines-78/bois-d-arcy/yvelines-une-croix-gammee-et-des-slogans-nationalistes-tagues-sur-les-murs-de-la-police-municipale-de-bois-d-arcy-7207374). |
| B16 | Plobannalec-Lesconil — « Parigot, dehors » | **Corroboré** *(nombre de véhicules incertain)* | Voir §5. Fait : **vendredi 14 août**. |
| B17 | Plobannalec-Lesconil — « Non aux Parisiens » | **Corroboré** | Voir §5. Inscription distincte, avec fautes, sur la portière d'un autre véhicule. |
| B18 | Penmarc'h — « Touristes, go home » | **Corroboré** *(sources substituées)* | Fait : **16 août**, tag sur un mur. [ICI, 18 août](https://www.ici.fr/emissions/l-info-d-ici-ici-breizh-izel/parigots-dehors-touristes-go-home-des-tags-anti-touristes-retrouves-a-penmarch-et-plobannalec-lesconil-5687587?at_locale=20), [Ouest-France via Yahoo, 20 août](https://fr.news.yahoo.com/sport/bretagne-parigot-dehors-voitures-touristes-040236236.html). La source secondaire étrangère de la 1re passe est abandonnée. |
| B19 | Penmarc'h — personne extérieure prise à partie | **Corroboré** | Fait : **16 août**. Une **joggeuse** est interpellée verbalement puis insultée, des personnes lui demandant « si elle était d'ici ». Mêmes sources que B18. Le vocabulaire du sample (« femme extérieure à la commune ») expliquait l'échec de la 1re passe. |
| B20 | Plogoff — pancarte « Parisiens dehors » | **Non corroboré — confusion de commune possible** | Trois requêtes distinctes, dont deux ciblées sur la seule commune : aucune source. Plogoff n'apparaît **dans aucun** des articles couvrant la séquence bigoudène, qui ne citent que Plobannalec-Lesconil et Penmarc'h. Une piste de confusion existe : [ICI documente des tags anti-touristes dans le Cap Sizun — dont dépend Plogoff — mais en **mai 2020**](https://www.ici.fr/infos/faits-divers-justice/deconfinement-des-tensions-avec-les-touristes-dans-le-cap-sizun-finistere-1589919345), lors du déconfinement. **Absence de résultat n'est pas preuve de fabrication** : la ligne reste conservée avec ce statut. |
| B21 | HuffPost / randonneurs racisés | Repris de la 1re passe | [HuffPost, 18 août](https://www.huffingtonpost.fr/life/video/ces-randonneurs-racises-repondent-a-ceux-qui-ne-veulent-pas-d-eux-en-montagne_307109.html) |

### Décompte après approfondissement

| Statut | Nombre |
|---|---|
| Corroborés lors de l'approfondissement | 10 *(B01, B02, B03, B04, B11, B15, B16, B17, B18, B19)* |
| Repris de la 1re passe, non réexaminés | 10 *(B05–B10, B12–B14, B21)* |
| Non corroborés | 1 *(B20)* |
| **Total** | **21** |

Les dix lignes « reprises » ne sont pas des lignes vérifiées : elles portent le statut que leur avait donné la première passe, sans contrôle indépendant. Aucun décompte ne doit les présenter autrement.

## 5. Bloc Finistère — dates, occurrences et périmètre

Le tableau de la première passe datait les cinq lignes du Finistère au « 20 août ». C'est faux : le 20 août est une date de **publication**, pas la date des faits.

### Chronologie établie

| Élément | Date matérielle | Date de signalement / publication |
|---|---|---|
| Véhicules rayés « Parigot, dehors », Plobannalec-Lesconil | **vendredi 14 août** | ICI le 18 août ; Ouest-France le 20 août |
| Véhicule gravé « Non aux Parisiens » (avec fautes), Plobannalec-Lesconil | **14 août** | idem |
| Tag « Touristes, go home » sur un mur, Penmarc'h | **16 août** | idem |
| Joggeuse prise à partie verbalement, Penmarc'h | **16 août** | idem |
| Pancarte « Parisiens dehors », Plogoff | — | aucune source |

### Nombre de véhicules — divergence non résolue

Les deux sources ne concordent pas :

- **ICI (18 août)** : « trois voitures » immatriculées en région parisienne rayées « Parigots dehors » à Plobannalec-Lesconil ;
- **Ouest-France via Yahoo (20 août)** : une voiture rouge gravée « Parigot, dehors », **plus** une autre portant « Non aux Parisiens ».

Le total possible va donc de **2 à 4 véhicules**. La divergence n'est pas tranchée et ne doit pas l'être par arbitrage arbitraire : elle attend la lecture d'une source primaire complète.

### Occurrences distinctes ou regroupement

Sur la base des dates et des lieux, on distingue au minimum :

- **deux communes** : Plobannalec-Lesconil et Penmarc'h ;
- **deux dates** : 14 août et 16 août ;
- **trois natures d'acte** : dégradation de véhicules, tag sur mur, prise à partie verbale d'une personne.

Le regroupement en une « séquence médiatique » unique reste défendable au plan éditorial, mais **il ne s'agit pas d'une occurrence unique**. Le regroupement provisoire C14 est conservé pour cette raison, sans préjuger du découpage final.

### Périmètre — réserve substantielle

Un élément rapporté par ICI change la lecture du dossier : **les propriétaires des véhicules rayés sont des résidents locaux ayant migré à Paris pour le travail**. Les personnes visées ne sont donc ni des touristes ni des Parisiens, mais des habitants de la région identifiés par leur plaque d'immatriculation.

Les maires des deux communes qualifient ces actes d'« isolés ». Aucune plainte ni enquête n'est mentionnée dans les sources lues.

**Question tranchée le 21 août 2026 :** l'hostilité envers des estivants ou des Franciliens n'entre pas dans le périmètre du baromètre, la cible étant une provenance géographique intérieure à la France ou le statut de touriste. Le candidat C14 est **refusé** ; le dossier reste conservé comme cas méthodologique.

## 6. Journal des recherches

| Date | Passe | Famille de requêtes | Résultats utiles |
|---|---|---|---|
| 21 août | 1re | Requêtes nationales : racisme, antisémitisme, xénophobie, néonazisme + France + juillet/août 2026 | Plusieurs samples retrouvés ; nouveaux candidats Crépol, Joris, BFMTV, Saint-Nazaire |
| 21 août | 1re | Requêtes avec `plainte`, `enquête`, `condamnation`, `justice` | Crépol, Espaly, Joris, Sarcelles ; confirme que la date du fait seul est insuffisante |
| 21 août | 1re | Requêtes par organismes : MRAP, SOS Racisme, Licra, OJF, ministères | Marboz, Avignon, Les Deux-Alpes, campagne de testings |
| 21 août | 1re | Requêtes locales ciblées sur B01 à B15 | 12 retrouvés, 1 partiellement, 2 non retrouvés |
| 21 août | 1re | Requêtes ciblées Finistère et randonneurs | Série B16–B18 et B21 retrouvée ; B19–B20 non retrouvés |
| 21 août | 2e | Requêtes nominatives et institutionnelles sur B02, B04, B11, B15 | **Quatre corroborations**, dont un communiqué de préfecture et une source France 3 régions |
| 21 août | 2e | Lecture directe de l'index Ouest-France pour B03 | Chronologie judiciaire complète ; **inexactitude du sample établie** |
| 21 août | 2e | Lecture directe des deux articles Finistère (ICI, Ouest-France/Yahoo) | Dates matérielles, nombre de véhicules, statut des victimes |
| 21 août | 2e | Trois requêtes ciblées sur Plogoff seul | Aucun résultat ; précédent Cap Sizun de mai 2020 identifié |
| 21 août | 2e | Requêtes nominatives sur C16 à C22 | Dates, statuts judiciaires et sources primaires précisés pour les sept |
| 21 août | 2e | Requêtes sur Thionville + lecture du communiqué MRAP | Fait et publications antérieurs à la fenêtre — voir §8 |
| 21 août | 3e | Sept requêtes ciblées sur le 20–24 juillet : faits divers datés, lieux de culte, associations antiracistes, élus, Roms et gens du voyage, incendies | **Aucun fait nouveau survenu dans ces cinq jours.** Deux fausses pistes écartées — voir §10 |
| 21 août | 3e | Requête sur les incendies et la vidéo au micro BFMTV | Précisions sur C18 : incendies de **Gironde**, séquence tournée hors antenne après un direct |
| 21 août | 3e | Requêtes et lecture directe sur le rapport annuel CNCDH | Chiffres de contexte enfin sourcés — voir §10 |

## 7. Candidats

Ce tableau présente les candidats **avant leur qualification** : il conserve les décisions provisoires prises au fil de la découverte. Les statuts définitifs figurent au **[§12](#12-qualification-minimale-des-candidats)**.

> Deux candidats — **C26 Aurignac** et **C27 Bois-d'Arcy** — n'apparaissent pas ici : ils ont été ajoutés le 22 août depuis les lignes corroborées B04 et B15, omises lors de la qualification initiale. Le §12 en compte donc 27.

| ID | Fait ou épisode candidat | Date du fait | Épisode dans la fenêtre | Lieu | Documents | Benchmark | Décision provisoire |
|---|---|---|---|---|---|---|---|
| C01 | Chants racistes à la féria de Marboz | 25 juillet | 28–29 juillet (plaintes Licra, MRAP) | Marboz (Ain) | [Le Progrès](https://www.leprogres.fr/societe/2026/07/28/un-chant-raciste-ternit-la-feria-de-marboz-la-licra-veut-porter-plainte), [MRAP](https://mrap.fr/le-mrap-depose-plainte-apres-des-chants-racistes-a-la-feria-de-marboz.html) | B01 | Conserver |
| C02 | Insultes antisémites contre le rabbin de Nanterre | 26 juillet | 26 juillet (plainte), 30 juillet (médiatisation) | Nanterre | [franceinfo](https://www.franceinfo.fr/societe/antisemitisme/une-enquete-ouverte-apres-une-plainte-du-rabbin-de-nanterre-pour-des-injures-antisemites_8128964.html), [CNews](https://www.cnews.fr/faits-divers/2026-07-30/sale-juif-retourne-en-israel-le-rabbin-de-nanterre-victime-dune-agression) | B02 | Conserver ; enquête en cours, auteur non identifié |
| C03 | Un homme blesse trois personnes à l'arme blanche en tenant des propos racistes | 30 juillet | 5–7 août (interpellation, réquisitions) | Machecoul-Saint-Même | [index relayant Ouest-France](https://faitsdivers365.fr/pays-de-la-loire/loire-atlantique/machecoul/) | B03 | Conserver ; **une séquence, trois victimes** — corriger le sample. Expertise psychiatrique demandée : incidence sur la qualification à examiner |
| C04 | Graffitis néonazis en centre-ville | 3–4 août | 4 août | La Flèche | [L'Est Républicain](https://www.estrepublicain.fr/faits-divers-justice/2026/08/04/des-actes-odieux-une-enquete-ouverte-apres-des-tags-neo-nazis-a-la-fleche) | B05 | Conserver |
| C05 | Dégradation de la fresque Louise Michel | 6 août | 7 août | Trélissac | [Le Parisien](https://www.leparisien.fr/faits-divers/dordogne-une-fresque-en-hommage-a-louise-michel-degradee-un-tag-antisemite-et-des-inscriptions-antifeministes-decouverts-07-08-2026-PUOTK5KUYBEATFELVVLKRQDSUU.php) | B06 | Conserver ; qualification du symbole à examiner en contexte |
| C06 | Agression et insultes visant des adolescentes voilées | 8 août | 10 août | Caen | [Anadolu](https://www.aa.com.tr/fr/journal-de-lislamophobie/france-une-vid%C3%A9o-montrant-l-agression-raciste-d-une-adolescente-%C3%A0-caen-suscite-l-indignation/4023156) | B07 | Conserver ; source primaire française à retrouver |
| C07 | Racisme et harcèlement dénoncés dans la Garde républicaine | antérieur et continu | 8 août | Paris | [Péyi Guyane](https://peyiguyane.com/post/faits-divers/une-gendarme-guyanaise-denonce-des-faits-de-racisme-au-sein-de-la-garde-republicaine-1786289333) | B08 | Série alléguée ; séparer les occurrences si les sources le permettent |
| C08 | Dégradation du véhicule de Régine Komokoli dans un contexte de menaces racistes | 8 août | 12 août | Rennes | [TF1 Info](https://www.tf1info.fr/justice-faits-divers/une-elue-lfi-a-rennes-victime-d-injures-racistes-et-de-degradations-une-procedure-ouverte-2458450.html) | B09 | Ne pas déduire automatiquement un mobile raciste à la dégradation |
| C09 | Agression dénoncée par Aminata Pouye | 9 août | 10 août | Talence | [Le Parisien](https://www.leparisien.fr/faits-divers/gironde-la-candidate-lfi-aux-senatoriales-denonce-une-attaque-raciste-et-annonce-porter-plainte-10-08-2026-W3HTDG7U3RHVBAI4PKWRNFQDTY.php) | B10 | Stade du signalement et de la plainte |
| C10 | Inscriptions racistes sous un pont, près de Migennes Plages | **présentes depuis plusieurs semaines** | 15 août (signalement MRAP au procureur de Sens) | Migennes | [France 3 BFC](https://france3-regions.franceinfo.fr/bourgogne-franche-comte/yonne/des-tags-racistes-appelant-a-la-sterilisation-des-bougn-ules-dans-l-yonne-un-inquietant-faisceau-de-montee-de-la-haine-3402001.html) | B11 | Conserver ; **datation du fait indéterminée** — cas utile pour la règle de datation |
| C11 | Menaces antisémites contre un couple de touristes juifs | vers le 11 août | 13 août (condamnation ministérielle) | Avignon | [Communiqué ministériel](https://presse.economie.gouv.fr/serge-papin-et-aurore-berge-condamnent-avec-la-plus-grande-fermete-les-menaces-antisemites-visant-un-couple-de-touristes-juifs-en-france/) | B12 | Conserver |
| C12 | Propos visant les Juifs tenus par une commerçante | 14 août (diffusion vidéo) | 15 août (enquête annoncée), 16 août | Les Deux-Alpes | [Place Gre'net](https://www.placegrenet.fr/2026/08/16/les-deux-alpes-une-enquete-ouverte-apres-les-propos-dune-commercante-visant-la-communaute-juive-dans-une-video/687408), [OJF](https://ojdf.org/2026/08/les-deux-alpes-des-propos-visant-les-juifs-et-un-possible-refus-de-vente-lojf-saisit-la-justice/) | B13 | Propos rapportés ; refus de vente seulement allégué |
| C13 | Condamnation après tirs près d'enfants et injures racistes | 19 avril | 17–18 août (condamnation) | Espaly-Saint-Marcel / Le Puy-en-Velay | [LDH](https://www.ldh-france.org/coups-de-feu-et-injures-racistes-envers-des-enfants-a-espaly-saint-marcel-la-ldh-se-mobilise-aux-cotes-des-victimes/), [Courrier de l'Atlas](https://www.lecourrierdelatlas.com/condamnation-injures-racistes-enfants-haute-loire/) | B14 | Épisode judiciaire d'un fait antérieur ; ne pas recompter le fait |
| C14 | Dégradations et prise à partie hostiles aux « Parisiens » et touristes | **14 août** (Plobannalec) et **16 août** (Penmarc'h) | 18–20 août | Plobannalec-Lesconil, Penmarc'h | [ICI](https://www.ici.fr/emissions/l-info-d-ici-ici-breizh-izel/parigots-dehors-touristes-go-home-des-tags-anti-touristes-retrouves-a-penmarch-et-plobannalec-lesconil-5687587?at_locale=20), [Ouest-France via Yahoo](https://fr.news.yahoo.com/sport/bretagne-parigot-dehors-voitures-touristes-040236236.html) | B16–B19 | Regroupement provisoire ; **pertinence pour le périmètre non établie** — voir §5 |
| C15 | Réponses de randonneurs racisés à une séquence virale | faits initiaux anciens | 18 août | France / réseaux sociaux | [HuffPost](https://www.huffingtonpost.fr/life/video/ces-randonneurs-racises-repondent-a-ceux-qui-ne-veulent-pas-d-eux-en-montagne_307109.html) | B21 | Réactivation et circulation, pas automatiquement un nouveau fait compté |
| C16 | Double enquête après le décès de Joris Laurencin et des accusations de harcèlement raciste | décès **13 juillet** ; harcèlement allégué sur plusieurs années ; injures alléguées à la fête du 30 juin | **20 juillet** — ouverture par le parquet de Vienne d'une double enquête (causes de la mort, harcèlement) ; plainte des parents le 17 juillet | Châtonnay (Isère) | [info.fr — enquête](https://info.fr/isere-enquete-ouverte-suicide-joris-21-ans-harcelement-raciste/), [info.fr — appel à témoins](https://info.fr/chatonnay-appel-temoins-suicide-joris-laurencin-harcelement-raciste/), [Observalgérie, 21 juillet](https://observalgerie.com/2026/07/21/faits-divers/bougnoule-algerien-paysan-apres-le-suicide-de-joris-la-justice-francaise-enquete) | Nouveau | Conserver. **Causalité alléguée, non établie.** Enquêtes en cours ; la famille demande un dépaysement. Vocabulaire d'allégation obligatoire |
| C17 | Circonstance aggravante de racisme dans l'affaire de Crépol | faits du **18–19 novembre 2023** | **deux épisodes dans la fenêtre** — voir ci-dessous | Crépol (Drôme) | [Le Monde, 24 juillet](https://www.lemonde.fr/societe/article/2026/07/24/coup-de-theatre-dans-l-affaire-du-meurtre-de-thomas-perotto-a-crepol-la-justice-retient-in-extremis-la-circonstance-aggravante-de-racisme_6731528_3224.html), [CNews, 17 août](https://www.cnews.fr/france/2026-08-17/meurtre-de-thomas-crepol-le-racisme-anti-blanc-ecarte-par-le-parquet-1906098), [actu17](https://actu17.fr/justice/meurtre-de-thomas-perotto-a-crepol-le-parquet-soppose-de-nouveau-a-la-circonstance-aggravante-de-racisme.html) | Nouveau | Conserver ; **aucune position judiciaire à trancher** — voir ci-dessous |
| C18 | Vidéo raciste tournée avec un micro BFMTV pris sans autorisation | avant le 30 juillet, hors antenne après un direct, en marge de la couverture des **incendies de Gironde** | **30 juillet** — viralité TikTok et plainte de la chaîne | France / réseaux sociaux | [Puremédias — réaction de la chaîne](https://www.ozap.com/actu/une-video-a-titre-prive-sans-autorisation-en-marge-de-la-couverture-des-incendies-des-individus-semparent-dun-micro-bfmtv-et-tiennent-des-propos-racistes-la-chaine-reagit/656260), [Puremédias — plainte](https://www.ozap.com/actu/bfmtv-porte-plainte-pour-usurpation-didentite-apres-la-diffusion-dune-video-contenant-des-propos-racistes-tournee-avec-un-micro-de-la-chaine/656268) | Nouveau | Conserver. Propos rapportés : « pour les incendies, il n'y a pas un noir, pas un arabe ». **Ne pas attribuer les propos à BFMTV** : la chaîne dément avoir tourné la séquence. La plainte porte sur l'**usurpation d'identité**, non sur les propos racistes eux-mêmes |
| C19 | Publication de Jean Messiha visant des adolescentes photographiées à leur insu | **8 juillet** (baignade à Belle-Île, lors d'un séjour voile du 7 au 10 juillet) | **24 juillet** — le maire de Saint-Nazaire annonce porter plainte | Belle-Île / Saint-Nazaire | [France 3 Pays de la Loire](https://france3-regions.franceinfo.fr/pays-de-la-loire/loire-atlantique/saint-nazaire/les-reseaux-sociaux-sont-devenus-le-receptacle-de-messages-de-haine-le-maire-de-saint-nazaire-va-porter-plainte-contre-jean-messiha-apres-un-tweet-raciste-3391633.html), [Saint-Nazaire Infos](https://saintnazaire-infos.fr/des-associations-de-saint-nazaire-denoncent-une-publication-de-jean-messiha/) | Nouveau | Conserver. Photo prise à l'insu, cadrant des jeunes filles en burkini, publiée avec un texte mis en cause. LDH et MRAP demandent le retrait. Mineures concernées : **prudence sur toute donnée identifiante** |
| C20 | Campagne d'affichage municipale d'Agde accusée de stigmatisation | visuel publié **fin juillet** dans le magazine municipal puis affiché | **5–7 août** — polémique et retrait des visuels | Agde (Hérault) | [Yahoo/relais](https://fr.news.yahoo.com/ta-chicha-et-ta-musique-on-nen-veut-pas---une-affiche-de-la-mairie-rn-dagde-fait-polemique-132642681.html), [Epoch Times](https://www.epochtimes.fr/agde-laffiche-de-la-mairie-contre-les-incivilites-a-la-plage-retiree-apres-des-accusations-de-racisme-3322989.html), [Parlons Politique](https://www.parlons-politique.fr/politique-locale/a-agde-une-affiche-contre-les-incivilites-a-tourne-a-la-mise-a-lecart-et-force-la-mairie-a-reculer_24900/) | Nouveau | Conserver. Visuel **généré par IA**, montrant trois hommes autour d'un narguilé et d'une enceinte ; slogan « Ta chicha et ta musique, on n'en veut pas ! Nos vacances, tu les respectes ! ». SOS Racisme évoque « un fond raciste assez clair ». **Accusation contestée, aucune infraction établie** |
| C21 | Huit plaintes après une campagne de testings | testings menés les **24, 25 et 26 juillet** — donc dans la fenêtre | **17 août** — dépôt des huit plaintes | Nice, Marseille, Montpellier | [SOS Racisme — communiqué](https://sos-racisme.org/actualites/un-testing-de-sos-racisme-revele-la-persistance-des-discriminations-dans-les-plages-privees-et-les-etablissements-de-nuit/), [Courrier de l'Atlas](https://www.lecourrierdelatlas.com/sos-racisme-plaintes-testing-plages-boites-nuit/), [Toulouse7, 17 août](https://toulouse7.com/2026/08/17/discrimination-sos-racisme-depose-8-plaintes/) | Nouveau | **Événement unique.** La campagne est l'événement ; observations, résultats et plaintes lui sont rattachés. 40 établissements testés (23 plages privées, 17 établissements de nuit) ; 17 % des plages et 30 % des établissements de nuit concernés. Répartition des plaintes : **5 au parquet de Nice, 2 à Montpellier, 1 à Marseille**. La campagne est l'unité ; les situations observées et les huit plaintes en sont les composantes |
| C22 | Six mises en examen après la découverte d'un véhicule armé près d'une synagogue | véhicule découvert le **11 juillet**, à 500 m d'une synagogue | **21 juillet** (huit interpellations) et **25 juillet** (six mises en examen et écrous) | Sarcelles (Val-d'Oise) | [franceinfo](https://www.franceinfo.fr/faits-divers/terrorisme/six-hommes-presentes-a-la-justice-dans-l-enquete-sur-des-soupcons-de-projet-d-attaque-a-la-synagogue-de-sarcelles_8121929.html), [CNews, 25 juillet](https://www.cnews.fr/faits-divers/2026-07-25/soupcons-de-projet-dattaque-visant-une-synagogue-sarcelles-six-hommes) | Nouveau | Conserver avec la **plus grande prudence**. Les six sont mis en examen pour des **infractions de droit commun** (vol en bande organisée, transport et cession d'armes). Selon les sources, **l'enquête n'a pas établi à ce stade leur connaissance du projet terroriste**. L'information initiale de la DGSI portait sur un « possible attentat islamiste visant une synagogue ». Le caractère antisémite relève d'un projet soupçonné et non établi |
| C23 | Inscriptions antisémites sur le portail de la synagogue de Thionville | 8 juillet ou 16–17 juillet selon les sources | **aucun épisode établi dans la fenêtre** | Thionville (Moselle) | voir §8 | Nouveau | **Piste examinée — classée hors fenêtre** en l'état |
| C24 | Condamnation après une agression et des injures racistes visant deux mères et leurs trois enfants | **27 mai 2026**, parking d'un centre commercial | **21 juillet** — audience, jugement et rassemblement devant le tribunal | Avignon (Vaucluse) | [ICI Vaucluse — jugement](https://www.ici.fr/emissions/l-info-d-ici-ici-vaucluse/sales-negres-une-peine-de-6-mois-de-prison-prononcee-contre-l-homme-juge-pour-avoir-agresse-une-famille-a-avignon-7375028), [ICI — rassemblement](https://www.ici.fr/provence-alpes-cote-d-azur/vaucluse-84/avignon/contre-le-racisme-un-rassemblement-organise-apres-une-audience-devant-le-tribunal-d-avignon-2003837) | Nouveau | Conserver. Injures rapportées : « sales nègres ». Peine de **six mois de prison** et interdiction du territoire français de cinq ans ; auteur de 23 ans, de nationalité italienne. Rassemblement « contre le racisme » le même jour, à l'appel du collectif Résiliantes. **Décision de première instance ; voies de recours non connues.** La mention « ferme » n'est pas établie par les sources lues |
| C25 | Interruption violente d'un concert de Barbara Butch — enquête et plaintes | **18 juillet 2026** (concert interrompu) | **21 juillet** (ouverture d'enquête) et **24 juillet** (nouvelle plainte de la Ville) | Grenoble (Isère) | [Place Gre'net, 21 juillet](https://www.placegrenet.fr/2026/07/21/le-parquet-de-grenoble-ouvre-une-enquete-preliminaire-apres-linterruption-violente-du-concert-de-barbara-butch/686112), [France 24, 21 juillet](https://www.france24.com/fr/france/20260721-interruption-du-concert-de-barbara-butch-enqu%C3%AAte-ouverte-pour-d%C3%A9lit-d-entrave), [France 3 Auvergne-Rhône-Alpes — nouvelle plainte](https://france3-regions.franceinfo.fr/auvergne-rhone-alpes/isere/grenoble/concert-interrompu-de-barbara-butch-des-videos-montrent-des-faits-qui-sont-graves-la-maire-de-grenoble-depose-une-nouvelle-plainte-3391675.html) | Nouveau | **Conserver comme cas de périmètre à trancher, pas comme fait admis** — voir la note ci-dessous |

### C25 — un cas de périmètre qui ne doit pas être tranché par défaut

Le concert de Barbara Butch à Grenoble a été interrompu le 18 juillet par une centaine de militants pro-palestiniens lui reprochant son soutien à une proposition de loi. Selon la municipalité et des témoignages, des projectiles — bouteilles de verre, gravier, liquides — ont été lancés vers la scène et un sabotage électrique a mis en danger le public, les techniciens et l'artiste, qui a dû quitter la scène.

Épisodes dans la fenêtre :

- **21 juillet** — le parquet de Grenoble ouvre une enquête préliminaire pour **délit d'entrave concertée aux libertés**.
- **24 juillet** — après une première plainte contre X déposée au lendemain des faits, la maire de Grenoble annonce en conférence de presse une **nouvelle plainte** contre X, visant des violences volontaires en réunion avec arme par destination, des violences accompagnées de gestes insultants sexistes, des dégradations, une mise en danger de la vie d'autrui et une entrave concertée à la liberté de création par menaces.

**Aucune des qualifications judiciaires retenues à ce stade n'est de nature raciste ou antisémite.** Le caractère antisémite est allégué et publiquement discuté ; il n'est ni retenu par le parquet ni établi.

Le cas est conservé parce qu'il est réel, documenté et situé dans la fenêtre. Mais il pose une question de périmètre que le pilote doit trancher **explicitement** : un fait visant une personne juive, dans un contexte de conflit politique, sans qualification antisémite retenue par la justice, entre-t-il au baromètre ? Y répondre par défaut — en l'incluant parce que la victime est juive, ou en l'excluant parce que la justice ne retient pas l'antisémitisme — serait dans les deux cas un arbitrage non assumé.

### C17 — les deux épisodes judiciaires de la fenêtre

L'affaire porte sur des faits de la nuit du 18 au 19 novembre 2023 à Crépol, au cours desquels Thomas Perotto, 16 ans, a été mortellement blessé. Quatorze personnes sont mises en examen.

Trois positions judiciaires successives doivent être rapportées sans être départagées :

1. **Juin 2026** — le parquet de Valence écarte la qualification raciste.
2. **23 juillet 2026** *(dans la fenêtre)* — les deux juges d'instruction retiennent la circonstance aggravante de racisme à l'encontre de l'ensemble des mis en cause.
3. **17 août 2026** *(dans la fenêtre)* — dans des réquisitions supplétives, le parquet conteste de nouveau ce caractère, estimant les témoignages évoquant des propos racistes « très minoritaires », « imprécis et parfois contradictoires ».

Les juges d'instruction demeurent libres de suivre ou non ces réquisitions. **Aucun fait n'est jugé ; aucune qualification n'est définitive.** Le journal se borne à consigner les positions en présence.

Observation éditoriale à verser au dossier : la couverture de l'épisode du 17 août est très majoritairement le fait de titres marqués politiquement. Ce déséquilibre de sources est une donnée à prendre en compte, pas un motif d'exclusion.

## 8. Thionville — piste examinée, classée hors fenêtre

Faits : croix gammées et inscriptions à la gloire d'Hitler, dont « Vive Hitler », sur un portail de la synagogue de Thionville. Le portail a dû être entièrement repeint. Une enquête a été ouverte, l'exploitation de la vidéosurveillance étant évoquée.

**Datation contradictoire selon les sources :**

- franceinfo et ICI situent la découverte au **mercredi 8 juillet 2026** ;
- le [communiqué du MRAP Moselle-Ouest](https://moselle-ouest.mrap.fr/Inscriptions-antisemites-sur-la-synagogue-de-Thionville.html), **publié le 17 juillet 2026**, situe la découverte aux **16 et 17 juillet 2026**.

Dans les deux hypothèses, le fait est **antérieur au 20 juillet**.

**Recherche d'un épisode dans la fenêtre :** aucune interpellation, aucun développement judiciaire, aucun rassemblement postérieur au 20 juillet n'a pu être établi. La seule page portant une date située dans la fenêtre est celle de la Ligue de défense juive (URL datée du 20 juillet) — source partisane qui ne peut suffire à établir un épisode. Les dates de publication des articles franceinfo et ICI n'ont pas pu être déterminées (accès refusé en lecture directe).

**Conclusion :** piste réelle et documentée, mais **entrée dans la fenêtre non établie**. Conservée comme C23 avec ce statut, à réexaminer si une date de publication franceinfo ou ICI comprise entre le 20 juillet et le 20 août est confirmée.

## 9. Pourquoi la première passe a manqué certaines références

L'explication avancée en première passe — « pages locales mal indexées, sources bloquées » — ne résiste pas à l'approfondissement. Trois des quatre références déclarées non retrouvées l'ont été à la première requête de la deuxième passe. Les causes réelles sont distinctes et instructives :

| Référence | Cause réelle du manque | Ce que cela enseigne |
|---|---|---|
| **B15** Bois-d'Arcy | **Requête trop étroite** et absence de recherche institutionnelle. Un communiqué de la préfecture des Yvelines existait et ressort en tête de résultats | Interroger systématiquement les sites préfectoraux et ministériels, pas seulement la presse |
| **B04** Aurignac | **Source déjà nommée par le sample non exploitée.** Le sample citait « La Petite République » ; il suffisait de la chercher directement | Utiliser les attributions du benchmark comme piste de recherche, même quand elles sont peu fiables |
| **B19** Penmarc'h | **Différence de vocabulaire.** Le sample dit « une femme extérieure à la commune » ; les sources disent « une joggeuse » | Varier les désignations de personnes, ne pas reprendre le lexique du benchmark |
| **B20** Plogoff | **Référence potentiellement erronée du benchmark**, avec confusion de commune plausible : le Cap Sizun a connu des tags anti-touristes réels, mais en mai 2020 | Une absence répétée doit faire suspecter le benchmark, sans conclure à la fabrication |
| **B03** Machecoul | **Source primaire non ouverte.** L'index citait Ouest-France ; l'ouvrir livrait la chronologie judiciaire complète et révélait l'inexactitude du sample | Ouvrir les agrégateurs plutôt que les citer |
| **B02** Nanterre | **Page dynamique retenue** alors qu'une page d'article stable existait sur le même site | Préférer systématiquement une URL d'article à un fil d'activité |
| **B11** Migennes | **Recherche régionale insuffisante.** France 3 Bourgogne-Franche-Comté couvrait le sujet en détail | Interroger les déclinaisons régionales de France 3 et d'ICI |
| **B18** Penmarc'h | **Source secondaire étrangère retenue** faute d'avoir cherché la presse régionale | Même remarque |

Aucun de ces manques ne relève d'un défaut d'indexation. Ils relèvent de la **profondeur et de la diversité des requêtes**, et de la discipline consistant à ouvrir les sources plutôt qu'à les citer de seconde main.

Enseignement transposable : la recherche par **épisode** (`plainte`, `enquête`, `condamnation`, `réquisitions`) et par **organisme** (préfectures, parquets, MRAP, LDH, SOS Racisme, OJF) est ce qui a produit à la fois les nouveaux candidats et la quasi-totalité des corroborations de la deuxième passe.

## 10. Couverture du 20 au 24 juillet

Les samples démarrent au 25 juillet. Les cinq premiers jours de la fenêtre n'avaient donc jamais été explorés pour eux-mêmes. Sept requêtes ciblées y ont été consacrées.

### Chronologie établie

> ⚠️ **Cette section a été corrigée le 21 août après une revue Codex.** Une première version concluait que « chaque jour de la période est documenté » sur la base de cinq épisodes. **C'était faux sur deux points** : deux épisodes avaient été manqués, et le 22 juillet ne comportait — et ne comporte toujours — aucune entrée.

| Date | Épisode | Candidat | Fait initial |
|---|---|---|---|
| **20 juillet** | Ouverture par le parquet de Vienne d'une double enquête (causes de la mort, harcèlement) | C16 | décès du 13 juillet ; harcèlement allégué sur plusieurs années |
| **21 juillet** | Huit interpellations en Île-de-France | C22 | véhicule armé découvert le 11 juillet |
| **21 juillet** | **Condamnation à six mois de prison et rassemblement devant le tribunal** | **C24** | agression et injures racistes du 27 mai |
| **21 juillet** | **Ouverture d'une enquête préliminaire pour délit d'entrave concertée** | **C25** | concert interrompu le 18 juillet |
| **22 juillet** | **— aucune entrée** | — | — |
| **23 juillet** | Les juges d'instruction retiennent la circonstance aggravante de racisme | C17 | faits des 18-19 novembre 2023 |
| **24 juillet** | Le maire de Saint-Nazaire annonce porter plainte | C19 | publication du 8 juillet |
| **24 juillet** | Premier jour de la campagne de testings (24, 25 et 26 juillet) | C21 | — le fait est dans la fenêtre |
| **24 juillet** | **Nouvelle plainte de la Ville de Grenoble, annoncée en conférence de presse** | **C25** | concert interrompu le 18 juillet |

**Huit épisodes sur quatre jours. Le 22 juillet reste vide.**

Aucun de ces épisodes ne provient des samples. Tous ont été trouvés par recherche d'épisode — six lors des passes précédentes, deux signalés par la revue Codex et vérifiés indépendamment ici.

### Ce que la recherche par date n'a pas produit

Sept requêtes organisées autour des faits — faits divers datés, dégradations de lieux de culte, communiqués d'associations antiracistes, propos d'élus, Roms et gens du voyage, contexte des incendies — n'ont produit **aucun fait matériel survenu entre le 20 et le 24 juillet**, hors le premier jour de la campagne de testings.

Ce résultat négatif est faible, et la suite l'a démontré : deux épisodes réels et bien sourcés lui ont échappé. Il n'établit donc pas qu'il ne s'est rien passé le 22 juillet — seulement qu'aucun des angles employés n'a rien fait remonter pour cette date.

### Deux fausses pistes écartées

- **Tags antisémites sur le campus d'HEC** (croix gammées, croix celtiques, « Juden ») : remontés par une requête sur l'antisémitisme en juillet 2026, mais les faits datent du **12 octobre 2018**. Écarté.
- **Dégradations de mosquées** (Crépy-en-Valois, Carpentras) : faits anciens remontés sans datation dans les résultats. Écartés après vérification.

Ces deux écartements sont consignés parce qu'ils illustrent un risque réel de la recherche par mots-clés thématiques : elle fait remonter des faits sans date, qu'une lecture rapide daterait de la fenêtre.

### Contexte enfin sourcé — rapport annuel de la CNCDH

Le cadrage mentionnait des chiffres SSMSI et CNCDH repris sans référence vérifiable. La source primaire est désormais identifiée : le **rapport annuel 2025 de la CNCDH sur la lutte contre le racisme, l'antisémitisme et la xénophobie**, publié en **juillet 2026**.

Chiffres retenus : **9 737 crimes et délits** à caractère raciste, xénophobe ou antireligieux enregistrés en 2025, en **hausse de 5 %** par rapport à 2024 ; la commission souligne que **97 % des personnes s'estimant victimes de racisme ne portent pas plainte**. Sources de reprise consultées : [CNDH Romeurope, 15 juillet 2026](https://www.romeurope.org/rapport-annuel-cncdh-2025/) et [Association William Penn, 28 juillet 2026](https://associationwilliampenndaideauxroms.wordpress.com/2026/07/28/rapport-2025-de-la-cncdh-sur-la-lutte-contre-le-racisme-lantisemitisme-et-la-xenophobie/).

Deux réserves : la publication du rapport est **antérieure au 20 juillet** et n'entre donc pas dans la fenêtre ; et un rapport statistique n'est **pas un fait** au sens du baromètre. Il s'agit de contexte, à ne jamais présenter comme une justification du projet. Le chiffre de « 16 400 infractions » avancé dans `brainstorm.md` reste, lui, non sourcé — seul le sous-total de 9 737 crimes et délits est établi.

### Conséquence méthodologique

Ce résultat renforce l'enseignement de la deuxième passe. Une fenêtre ne se couvre pas en cherchant des faits par date : elle se couvre en cherchant des **épisodes** — ouvertures d'enquête, interpellations, mises en examen, décisions, plaintes, réquisitions, publications. Les cinq premiers jours de la fenêtre n'existent quasiment que par ce canal.

Deux enseignements supplémentaires, tirés des épisodes manqués :

1. **Les audiences correctionnelles ordinaires sont un angle mort.** C24 est une condamnation pour injures et agression racistes prononcée dans la fenêtre. Aucune requête thématique ne l'a fait remonter : ce type de décision est couvert par la presse locale, sans vocabulaire distinctif. Il faut interroger explicitement les **tribunaux judiciaires** et les **rassemblements associatifs** qui les accompagnent.
2. **Un événement peut être massivement couvert sans apparaître sous les mots du périmètre.** C25 a fait l'objet de tribunes, de réactions politiques nationales et de plusieurs plaintes, mais aucune source ne le désigne comme un fait raciste ou antisémite établi. Une recherche par mots-clés du périmètre ne pouvait pas le trouver.

### Une conclusion à ne pas tirer

Le fait qu'aucune entrée ne concerne le 22 juillet **ne signifie pas que rien ne s'est produit ce jour-là**. Compte tenu de deux manques déjà avérés sur cette même période, la lecture prudente est qu'il subsiste probablement d'autres épisodes non détectés — le 22 juillet comme ailleurs dans la fenêtre.

## 11. Points ouverts

- **Couverture du 20 au 24 juillet — partiellement traitée, voir §10.** Huit épisodes documentés sur quatre jours ; **le 22 juillet reste sans aucune entrée**. Deux épisodes ayant déjà échappé à une passe dédiée, la période ne peut pas être déclarée close.
- **C25 Grenoble** : cas de périmètre à trancher explicitement — aucune qualification raciste ou antisémite n'est retenue par la justice.
- **C24 Avignon** : vérifier si la peine est ferme et si un appel a été interjeté.
- **B20 Plogoff** : statut à réexaminer si une source apparaît.
- **Nombre de véhicules dans le Finistère** : divergence 2 à 4 non résolue.
- **C03 Machecoul** : l'expertise psychiatrique demandée peut affecter la qualification ; suivre.
- **C21 testings** : événement unique — la campagne — dont les situations observées et les plaintes sont des composantes à rattacher.
- **C22 Sarcelles** : le caractère antisémite tient à un projet soupçonné, non établi, et non aux chefs de mise en examen retenus.
- **C23 Thionville** : dates de publication franceinfo et ICI à établir.
- **Sources primaires non ouvertes** : Ouest-France (B03, Finistère), Le Progrès (B01), Le Parisien (B06, B10).

## 12. Qualification minimale des candidats

> Qualification initiale de **25 candidats** le 21 août 2026, **complétée le 22 août** par C26 Aurignac et C27 Bois-d'Arcy — deux lignes du benchmark corroborées mais omises au premier passage. Les deux étapes se sont faites **à partir du matériau déjà réuni, sans aucune recherche complémentaire** : chaque candidat disposait de quoi décider, rattacher, classer et formuler. « Admis » ne signifie pas « prêt à publier ».

| ID | Formulation factuelle | Date du fait | Lieu | Nature | Cible / dimension | Contexte | Statut | Rattachement ou réserve |
|---|---|---|---|---|---|---|---|---|
| C01 | Des chants racistes comportant le mot « bougnoules » sont filmés lors de la féria ; la vidéo circule largement et la Licra dépose plainte. | 25 juillet | Marboz (Ain) | Propos public | Racisme anti-Arabes / Maghrébins | Espace public | **Admis** | — |
| C02 | Le rabbin de Nanterre déclare avoir été insulté (« sale juif », « retourne en Israël ») dans un supermarché ; plainte déposée et enquête ouverte pour injure publique. | 26 juillet | Nanterre (Hauts-de-Seine) | Insulte | Antisémitisme | Espace public | **Admis** | Auteur non identifié ; enquête en cours |
| C03 | Un homme blesse trois personnes à l'arme blanche en tenant des propos racistes ; un suspect est interpellé et l'enquête retient le caractère raciste. | 30 juillet | Machecoul-Saint-Même (Loire-Atlantique) | Agression | Non déterminée | Espace public | **Admis** | Expertise psychiatrique demandée |
| C04 | Des croix gammées et des croix celtiques sont découvertes en plusieurs points du centre-ville ; le parquet ouvre une enquête. | 3–4 août | La Flèche (Sarthe) | Dégradation ; symbole néonazi | Néonazisme | Espace public | **Admis** | — |
| C05 | Une fresque en hommage à Louise Michel est dégradée par une étoile de David peinte sur le visage et d'autres inscriptions ; la municipalité porte plainte. | 6 août | Trélissac (Dordogne) | Dégradation | Antisémitisme | Espace public | **Admis** | Qualification antisémite portée par les sources |
| C06 | Trois adolescentes voilées déclarent avoir été prises à partie et insultées à la terrasse d'un café ; une enquête est ouverte pour violences et injures à raison de l'origine. | 8 août | Caen (Calvados) | Agression ; insulte | Racisme anti-Arabes / Maghrébins ; dimension antimusulmane | Espace public | **Admis** | Une seule source consultée |
| C07 | Une gendarme originaire de Guyane déclare avoir subi des messages racistes et divers actes hostiles, et avoir signalé les faits à sa hiérarchie et à la justice. | Antérieur et continu | Paris | Discrimination ; harcèlement | Racisme anti-Noirs | Institution | **Admis** | Série alléguée traitée comme **un seul dossier** |
| C08 | Une élue déclare recevoir des messages et menaces racistes depuis plusieurs semaines et découvre son véhicule forcé et saccagé ; une procédure est ouverte. | 8 août | Rennes (Ille-et-Vilaine) | Menace ; dégradation | Racisme anti-Noirs | Politique | **Admis** | Mobile raciste de la dégradation non établi |
| C09 | Une candidate aux sénatoriales dénonce une agression à caractère raciste et annonce déposer plainte. | 9 août | Talence (Gironde) | Agression | Racisme anti-Noirs | Politique | **Admis** | Fait rapporté par la personne visée |
| C10 | Des inscriptions racistes (« Bougnoules dehors », « Ligature des trompes aux bougnoules ») sont signalées sous un pont ; le MRAP saisit le procureur de Sens. | Indéterminée — présentes depuis plusieurs semaines | Migennes (Yonne) | Dégradation ; propos public | Racisme anti-Arabes / Maghrébins | Espace public | **Admis** | Date du fait non déterminable |
| C11 | Un couple de touristes juifs est pris à partie dans un supermarché ; la séquence comporte une menace de mort et le gouvernement condamne les faits. | Vers le 11 août | Avignon (Vaucluse) | Menace | Antisémitisme | Espace public | **Admis** | — |
| C12 | Une commerçante tient des propos visant la communauté juive dans une vidéo diffusée en ligne ; une enquête est ouverte pour provocation à la haine. | 14 août | Les Deux-Alpes (Isère) | Propos public | Antisémitisme | Espace public | **Admis** | Refus de vente seulement allégué |
| C13 | Un homme ayant tiré à la carabine à proximité d'enfants en proférant des injures racistes est condamné à quinze mois de prison avec sursis probatoire. | 19 avril | Espaly-Saint-Marcel / Le Puy-en-Velay (Haute-Loire) | Menace ; insulte | Racisme anti-Noirs / anti-Arabes | Justice | **Admis** | **Épisode judiciaire d'un fait antérieur à la fenêtre** — ne pas recompter le fait |
| C14 | Des véhicules immatriculés en région parisienne sont rayés et un tag « Touristes, go home » est découvert ; une joggeuse est prise à partie. | 14 et 16 août | Plobannalec-Lesconil et Penmarc'h (Finistère) | Dégradation ; insulte | Hostilité territoriale | Espace public | **Refusé** | **Hors périmètre** : la cible est une provenance géographique intérieure à la France ou le statut de touriste, non une origine ethnique, nationale ou religieuse. Conservé au journal méthodologique |
| C15 | Des randonneurs racisés répondent publiquement, par une série de vidéos, à des publications et commentaires présentant la montagne comme un espace réservé aux Blancs. | 18 août (réponses) ; propos antérieurs, dont 2024 | France / en ligne | Propos public | Racisme anti-Noirs / anti-Arabes | Média | **Admis** | **Événement de réponses relié à des propos antérieurs**, sans fusion entre eux |
| C16 | Les parents d'un homme de 21 ans mort le 13 juillet déposent plainte pour harcèlement raciste ; le parquet ouvre une double enquête sur les causes de la mort et sur le harcèlement. | 13 juillet ; harcèlement allégué antérieur | Châtonnay (Isère) | Harcèlement | Racisme anti-Arabes / Maghrébins | Espace public | **Admis** | **Causalité alléguée, non établie** ; enquêtes en cours |
| C17 | Dans l'affaire du meurtre de Crépol, les juges d'instruction retiennent la circonstance aggravante de racisme le 23 juillet ; le parquet la conteste de nouveau le 17 août. | 18–19 novembre 2023 | Crépol (Drôme) | Agression | Non déterminée — qualification contestée | Justice | **Incertain** | Qualification raciste retenue par les juges, contestée par le parquet ; aucun fait jugé |
| C18 | Une vidéo diffusée en ligne montre un homme tenant des propos racistes avec un micro d'une chaîne d'information pris sans autorisation ; la chaîne dément et porte plainte pour usurpation d'identité. | Avant le 30 juillet | France / en ligne | Propos public | Racisme anti-Noirs et anti-Arabes | Média | **Admis** | **Ne pas attribuer les propos à la chaîne** |
| C19 | Une photographie prise à leur insu de jeunes filles en baignade est publiée par une personnalité avec un texte mis en cause ; le maire de Saint-Nazaire annonce porter plainte. | 8 juillet | Belle-Île / Saint-Nazaire | Propos public | Dimension antimusulmane | Média | **Admis** | Mineures concernées : aucune donnée identifiante |
| C20 | Une campagne d'affichage municipale contre les incivilités sur les plages est accusée par SOS Racisme et d'autres acteurs de véhiculer une représentation stigmatisante des personnes perçues comme maghrébines ; la mairie conteste cette lecture et retire les visuels. | Fin juillet | Agde (Hérault) | Communication publique mise en cause | Racisme anti-Arabes / Maghrébins — qualification attribuée et contestée | Institution | **Admis** | Qualification portée par des tiers, contestée par la municipalité ; aucune infraction établie |
| C21 | Une campagne de testings menée dans des plages privées et des établissements de nuit donne lieu au dépôt de huit plaintes auprès de trois parquets. | 24–26 juillet | Nice, Marseille, Montpellier | Discrimination | Racisme anti-Noirs / anti-Arabes | Espace public | **Admis** | **Événement unique** : la campagne est l'événement ; observations, résultats et huit plaintes lui sont rattachés sans devenir plusieurs événements |
| C22 | Six hommes sont mis en examen et écroués pour des infractions de droit commun, dans une enquête ouverte sur des soupçons de projet d'attaque visant une synagogue. | Véhicule découvert le 11 juillet | Sarcelles (Val-d'Oise) | Menace — soupçonnée | Antisémitisme — allégué | Justice | **Incertain** | Aucun chef antisémite retenu ; connaissance du projet non établie à ce stade |
| C23 | Des croix gammées et des inscriptions à la gloire d'Hitler sont découvertes sur un portail de la synagogue ; une enquête est ouverte. | 8 juillet ou 16–17 juillet | Thionville (Moselle) | Dégradation ; symbole néonazi | Antisémitisme | Espace public | **Refusé** | Hors fenêtre : aucun épisode établi entre le 20 juillet et le 20 août |
| C24 | Un homme est condamné à six mois de prison et à une interdiction du territoire pour une agression et des injures racistes visant deux mères et leurs trois enfants ; un rassemblement se tient devant le tribunal. | 27 mai | Avignon (Vaucluse) | Agression ; insulte | Racisme anti-Noirs | Justice | **Admis** | **Épisode judiciaire d'un fait antérieur à la fenêtre** — ne pas recompter le fait. Décision de première instance |
| C25 | Un concert est interrompu par des militants ; le parquet ouvre une enquête pour entrave concertée aux libertés et la Ville dépose une nouvelle plainte. | 18 juillet | Grenoble (Isère) | Agression ; entrave | Antisémitisme — allégué, non retenu | Politique | **Incertain** | Aucune qualification raciste ou antisémite retenue par la justice ; périmètre à trancher |
| C26 | Un adolescent de 16 ans hébergé dans un centre d'accueil de demandeurs d'asile est insulté puis roué de coups par un groupe en marge de la fête du village ; la mairie et des associations dénoncent un acte raciste et une plainte est déposée. | Nuit du 1er au 2 août | Aurignac (Haute-Garonne) | Agression ; insulte | Xénophobie — victime demandeuse d'asile | Espace public | **Admis** | Qualification portée par la mairie et des associations. **Ajouté le 22 août** depuis la ligne corroborée B04, omise lors de la qualification initiale |
| C27 | Une croix gammée et des slogans nationalistes sont tagués sur les murs du poste de police municipale ; la mairie porte plainte et le préfet condamne les faits. | Week-end du 15-16 août | Bois-d'Arcy (Yvelines) | Dégradation ; symbole néonazi | Néonazisme | Institution | **Admis** | **Ajouté le 22 août** depuis la ligne corroborée B15, omise lors de la qualification initiale |

### Décompte

| Statut | Nombre |
|---|---|
| Admis | **22** |
| Incertain | **3** |
| Refusé | **2** |
| Rattaché | **0** |
| **Total** | **27** |

*Décompte après les arbitrages utilisateur du 21 août — C20 et C15 admis, C14 refusé — et après l'ajout, le 22 août, de **C26 Aurignac** et **C27 Bois-d'Arcy** : deux lignes du benchmark corroborées en deuxième passe mais omises lors de la qualification initiale. Elles ont été qualifiées à partir des sources déjà réunies, sans recherche nouvelle.*

### Arbitrages utilisateur du 21 août

Trois statuts ont été corrigés sur décision explicite de l'utilisateur, confirmée par la revue Codex :

- **C14 → refusé, hors périmètre.** *« Les Parisiens ne sont pas une communauté racisée, cet acte n'a rien à faire là. »* La cible est une provenance géographique intérieure à la France ou le statut de touriste, non une origine ethnique, nationale ou religieuse. Le dossier reste disponible comme cas méthodologique.
- **C15 → admis** comme **événement de réponses relié à des propos antérieurs**, sans fusion entre eux. La dimension raciste est identifiable et les réponses sont datées du 18 août. L'ancienneté des propos visés n'empêche pas l'admission de l'événement de réponses ; elle interdit seulement de confondre les deux.
- **C20 → admis**, avec **qualification attribuée et contestée**. Le baromètre n'a pas à décider si l'affiche est intrinsèquement raciste : il documente qu'une communication institutionnelle a été publiquement accusée de stigmatisation raciste, contestée, puis retirée.

Ces arbitrages tranchent aussi une question de méthode : **l'admission ne signifie pas que le baromètre certifie lui-même le mobile raciste.** Une qualification portée par une personne, une association, un média ou une autorité peut suffire, à condition d'être clairement attribuée dans la formulation.

### Observations utiles à la suite

- **Aucun rattachement.** Aucun candidat ne s'est révélé être le doublon ou l'épisode d'un autre candidat de la liste. Les deux dossiers qui sont des épisodes judiciaires — C13 et C24 — se rattachent à des faits antérieurs à la fenêtre, absents du corpus. C15 est relié à des propos antérieurs qui ne figurent pas au corpus.
- **C21 est un événement unique** : la campagne ; ses observations, résultats et huit plaintes lui sont rattachés sans devenir automatiquement plusieurs événements.
- **Les trois « incertains » restants — C17, C22, C25 — sont des dossiers vivants**, confirmés comme tels par l'utilisateur le 21 août. Ce qui les distingue des admis n'est pas le degré de racisme de l'acte, ni la simple existence d'une procédure : **de nombreux candidats admis font aussi l'objet d'une enquête en cours** (C02, C03, C04, C06, C10, C12, C16). Un dossier reste incertain lorsque les éléments encore susceptibles d'évoluer peuvent modifier **son admission, son appartenance au périmètre ou sa formulation centrale** — ce qui est le cas de la qualification disputée à Crépol, du lien antisémite non établi à Sarcelles et de la nature même du fait à Grenoble. À l'inverse, C20 est admis bien que sa qualification soit contestée : l'état de connaissance y est stabilisé et la contestation fait partie du fait.
- **Les incertains restent dans la base**, classés à part des admis. Leur mode de présentation — recherche complémentaire pour lever le doute, ou formulation permettant de les conserver sans les confondre avec les admis — reste à déterminer.
- **Catégories relevées** : voir le §13, qui reprend et complète ce point sur les trois axes.
- **Vérification faite** : C17, C22 et C25 ont été réexaminés le 21 août et **maintenus en incertain** sur décision de l'utilisateur. Après l'ajout de C26 et C27 le 22 août, le décompte est de **22 admis / 3 incertains / 2 refusés / 0 rattaché**.

## 13. Catégories apparues

> Relevé **descriptif et provisoire**, établi à partir des trois colonnes du §12. Ce n'est ni une taxonomie, ni une liste fermée, ni une hiérarchie. Un candidat peut relever de plusieurs catégories sur un même axe.

### Axe 1 — Nature

39 mentions pour 27 candidats.

| Catégorie | Candidats | Remarque |
|---|---|---|
| Propos public | C01, C10, C12, C15, C18, C19 | |
| Agression | C03, C06, C09, C17, C24, C25, C26 | |
| Dégradation | C04, C05, C08, C10, C14, C23, C27 | |
| Insulte | C02, C06, C13, C14, C24, C26 | Se combine souvent avec agression ou dégradation |
| Menace | C08, C11, C13, C22 | |
| Symbole néonazi | C04, C23, C27 | Toujours associé à une dégradation |
| Discrimination | C07, C21 | |
| Harcèlement | C07, C16 | Chevauche discrimination en C07 |
| Communication publique mise en cause | C20 | **Nouvelle** — absente des repères de départ |
| Entrave | C25 | **Nouvelle** — absente des repères de départ |

### Axe 2 — Cible / dimension

28 mentions pour 27 candidats.

| Catégorie | Candidats | Remarque |
|---|---|---|
| Antisémitisme | C02, C05, C11, C12, C22, C23, C25 | Deux mentions alléguées ou non retenues (C22, C25) |
| Racisme anti-Arabes / Maghrébins | C01, C06, C10, C16, C20 | |
| Racisme anti-Noirs | C07, C08, C09, C24 | |
| Racisme anti-Noirs **et** anti-Arabes | C13, C15, C18, C21 | Étiquette combinée employée quand l'acte vise les deux ou quand les sources ne distinguent pas — **chevauche les deux précédentes** |
| Dimension antimusulmane | C06, C19 | Secondaire en C06 |
| Néonazisme | C04, C27 | **Désigne une idéologie, non un groupe visé** — voir remarque ci-dessous |
| Xénophobie | C26 | **Nouvelle** — victime demandeuse d'asile ; seule occurrence visant une personne étrangère comme telle |
| Hostilité territoriale | C14 | Hors périmètre ; catégorie née d'un refus |
| Non déterminée | C03, C17 | |

**Remarque sur cet axe.** Il mêle deux choses différentes : le **groupe visé** (Noirs, Arabes, Juifs, musulmans) et l'**idéologie exprimée** (néonazisme). L'écart apparaît nettement entre C04 et C23, deux dégradations à croix gammées classées l'une en « néonazisme », l'autre en « antisémitisme » selon la cible atteinte. Ce point est signalé, non tranché.

### Axe 3 — Contexte

27 mentions pour 27 candidats — un seul contexte par candidat.

| Catégorie | Candidats | Remarque |
|---|---|---|
| Espace public | C01, C02, C03, C04, C05, C06, C10, C11, C12, C14, C16, C21, C23, C26 | **Plus de la moitié du corpus** — catégorie fourre-tout |
| Justice | C13, C17, C22, C24 | Désigne le contexte de l'**épisode**, non du fait initial |
| Média | C15, C18, C19 | |
| Politique | C08, C09, C25 | |
| Institution | C07, C20, C27 | |

**Remarques sur cet axe.** « Espace public » regroupe des situations très différentes — commerce, fête de village, plage, voie publique — et pourrait devoir être précisé si le déséquilibre persiste sur d'autres fenêtres. « Justice » ne décrit pas le lieu du fait mais celui de son épisode : les faits initiaux de C13, C17, C22 et C24 relèvent d'autres contextes.

## 14. Journal des frictions

> Relevé **volontairement court**. Une difficulté n'y figure que si elle a modifié une décision, obligé à préciser une règle nécessaire, révèle un risque de répétition, ou servira à évaluer une solution plus tard. Les particularités d'un seul candidat, les enquêtes en cours et les qualifications contestées n'y figurent pas : elles relèvent du traitement ordinaire.

| Cas ou situation | Difficulté réellement utile | Décision déjà acquise | Utilité pour la suite |
|---|---|---|---|
| **Benchmark emprunté** (samples) | Un corpus de référence hérité s'est révélé être une collecte assistée par IA, non vérifiée : attributions de source erronées, une ligne non corroborée, un fait mal décrit. | Le benchmark est conservé pour comparer des performances de recherche, jamais comme mesure d'exhaustivité. | Tout corpus repris d'ailleurs devra être éprouvé avant de servir de référence. |
| **Couverture d'une fenêtre** | Chercher les faits par leur date de survenue laisse des jours entiers vides ; ce sont les **épisodes** — ouverture d'enquête, plainte, mise en examen, condamnation, réquisitions — qui font remonter la période. | La recherche a été élargie et complétée par la recherche d'épisodes. La fenêtre n'est pas pour autant déclarée close. | Point de départ de toute stratégie de recherche future. |
| **Audiences correctionnelles locales** | Une condamnation pour injures et agression racistes (C24) n'est remontée sous aucun mot-clé du périmètre : ce type de décision est couvert par la seule presse locale, sans vocabulaire distinctif. | Retrouvée par une autre voie et admise. | Angle mort reproductible sur les épisodes judiciaires locaux. |
| **Accès aux sources primaires** | Plusieurs titres majeurs sont restés illisibles (403, pages dynamiques, agrégateurs à la place de l'article), de façon répétée et non ponctuelle. | Le travail s'est appuyé sur des relais, en signalant la limite. | À prendre en compte lors de toute évaluation ultérieure de faisabilité. |
| **Critère de tri implicite** | Le tri a d'abord suivi un critère jamais écrit — le degré de contestation publique de la qualification — qui a produit un classement incohérent et a dû être corrigé par arbitrage. | Trois statuts revus ; le critère d'admission a été explicité. | Un critère de tri doit être écrit avant le tri, sous peine de dériver sans être détectable. |
| **C14 — « Parisiens dehors »** | Exemple négatif : ce type de résultat remonte lors d'une recherche large. | Refusé. L'hostilité envers une provenance géographique intérieure à la France ou envers des touristes est hors périmètre. | Cas de test pour vérifier qu'une détection large sait écarter ce bruit. |
| **C15 — randonneurs** | Besoin de relier deux événements, le second — les réponses — découlant du premier. | Admis comme événement de réponses relié à des propos antérieurs, sans fusion entre eux. | Montre qu'il faudra pouvoir relier deux événements sans les fusionner ni les compter comme un seul. |
| **C21 — campagne de testings** | Besoin de rattacher plusieurs observations et résultats à un même événement. | Admis. La campagne est l'événement unique ; observations, résultats et plaintes lui sont rattachés sans devenir plusieurs événements. | Même besoin de rattachement, sur un cas non temporel. |
| **Corroboration sans passage au corpus** | Deux références corroborées en deuxième passe — B04 Aurignac, B15 Bois-d'Arcy — ne sont jamais devenues des candidats : le travail de vérification n'a pas rejoint la liste qualifiée. | Ajoutées le 22 août en C26 et C27, à partir des sources déjà réunies. | S'est produit deux fois : le passage de la corroboration au corpus n'est pas garanti par le seul travail manuel. |

## 15. Charge observée jusqu'à la qualification minimale

> **Limites de la mesure.** Bilan ponctuel reconstitué à partir des traces déjà consignées — journal des recherches, tableaux du benchmark et des candidats, §12, §14, arbitrages. **Aucune durée n'a été chronométrée** : rien n'a été mesuré en temps. Les comptages portent sur des opérations traçables, non sur un coût. Un cas reste limite et est signalé comme tel.

| Question | Résultat | Identifiants |
|---|---|---|
| Qualifiables directement | **11 / 27** (41 %) | C01, C04, C05, C06, C07, C08, C09, C11, C12, C13, C15 |
| Recherche ciblée indispensable | **15 / 27** (56 %) | C03, C10, C14, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26, C27 |
| Non déterminable | **1 / 27** (4 %) | C02 |
| Arbitrage particulier | **7 candidats** | C14, C15, C17, C20, C21, C22, C25 |

**Base des « directement qualifiables ».** Dix correspondent aux lignes du benchmark marquées *repris de la 1re passe*, jamais réexaminées ; C01 s'y ajoute, sa vérification ultérieure n'ayant rien apporté d'indispensable.

**Ce qui manquait pour les recherches ciblées.** Chronologie judiciaire et correction d'un fait mal décrit (C03) ; date réelle du fait, indéterminée (C10) ; dates matérielles et statut des personnes visées (C14) ; dates, chefs retenus et sources primaires (C16 à C22) ; datation contradictoire (C23) ; existence même du candidat (C24, C25, issus de la revue croisée) ; corroboration institutionnelle et locale (C26, C27).

**Non déterminable.** Les traces ne permettent pas de trancher pour **C02** : la source de première passe était un fil dynamique, remplacé ensuite par une page d'article stable, mais rien n'établit que la qualification était impossible sans cette substitution. Le candidat n'est forcé dans aucune des deux catégories.

**Arbitrages comptés.** C14 refusé comme hors périmètre ; C15 admis comme événement de réponses relié à des propos antérieurs ; C20 admis avec qualification attribuée et contestée ; C21 ramené à un événement unique ; C17, C22 et C25 maintenus en incertain après examen contradictoire — une proposition de bascule en admis avait été formulée puis écartée.

### Où l'effort s'est concentré

L'effort se répartit très inégalement entre les opérations.

**Ce qui a produit le plus de travail** — la recherche et la couverture de la fenêtre (14 familles de requêtes consignées sur 3 passes, plus une revue croisée) ; l'accès et la confrontation des sources (3 sources substituées, plusieurs lectures directes, accès refusés répétés) ; les arbitrages et corrections (3 statuts modifiés, 2 candidats ajoutés tardivement, 4 formulations corrigées sur C21, 2 énoncés obsolètes rectifiés).

**Ce qui est resté léger** — le rapprochement des faits, épisodes et reprises (1 événement unique à observations multiples, 1 relation entre deux événements, aucun doublon) et surtout la qualification finale elle-même : les candidats ont été qualifiés en une passe, **sans aucune recherche complémentaire**.

### Soutenabilité

**Oui, avec certaines limites.**

L'étape de qualification elle-même est légère et tient manuellement : produire les lignes du §12 n'a demandé aucune recherche supplémentaire. Ce n'est pas là que le travail se joue.

L'effort se concentre en amont — trouver, puis atteindre et confronter les sources — et en aval, dans les corrections. Plus de la moitié des candidats ont exigé une recherche qui leur était propre.

Trois points à garder en mémoire pour la réflexion technique ultérieure : l'**accès aux sources primaires** a été un obstacle répété ; l'**absence de critère de tri écrit à l'avance** a engendré des allers-retours de correction qui ont pesé davantage que la qualification elle-même ; et **deux faits corroborés ont échappé au passage en candidat**, ce qui montre que le lien entre corroboration et corpus n'est pas assuré par le seul travail manuel.
