# Environnement local du banc d'essai — Bloc 2

Guide pour Windows PowerShell. Il prépare uniquement l'environnement : **aucun test de solution n'est lancé à ce stade**.

> ⚠️ **Les clés ne se communiquent jamais dans une conversation avec Claude ou Codex.** Elles sont inscrites localement dans `.env`, qui n'est pas suivi par Git, et lues par les futurs scripts. Ni Claude ni Codex n'ont besoin de les voir pour travailler.

## 1. Obtenir une clé API OpenAI

1. Ouvrir <https://platform.openai.com/api-keys> et se connecter.
2. Créer une clé dédiée à ce projet — la nommer par exemple `barometre-collecte` — plutôt que réutiliser une clé existante : elle pourra être révoquée seule.
3. **Copier la clé immédiatement** : elle n'est affichée qu'une fois.
4. Vérifier qu'un moyen de paiement ou un crédit est associé au compte : l'outil de recherche Web est facturé à l'usage.

### La clé API n'est pas l'abonnement ChatGPT

Un abonnement **ChatGPT Plus / Pro** paie l'interface Web. L'**API** est un service distinct, avec sa propre facturation à l'usage. Disposer de l'un ne donne pas l'autre : il faut un crédit ou un moyen de paiement sur la plateforme API, même si ChatGPT est déjà payé.

## 2. Brave Search — reporté

**Décision utilisateur : Brave est reporté.** Le premier smoke test porte sur **OpenAI web search**, puis sur **GDELT**, qui n'exige ni compte ni clé. Brave ne sera reconsidéré que si ces deux essais laissent un besoin concret non couvert.

Il n'y a donc **rien à faire dans cette section pour l'instant** : `BRAVE_SEARCH_API_KEY` reste volontairement vide.

Si Brave est repris plus tard, l'accès suppose d'ouvrir <https://api-dashboard.search.brave.com/>, de créer un compte puis de **souscrire** : l'API est tarifée et la souscription demande des informations de paiement, y compris pour le palier assorti de 5 $ de crédits mensuels. La clé se génère ensuite dans le tableau de bord.

## 3. Préparer le fichier `.env`

Le fichier `.env` existe déjà à la racine du dépôt, vide. S'il manque, le recréer depuis l'exemple :

```powershell
Copy-Item .env.example .env
```

Puis l'ouvrir et inscrire les deux clés **après le signe `=`, sans guillemets et sans espace** :

```powershell
notepad .env
```

```env
OPENAI_API_KEY=coller_ici_la_cle_openai
BRAVE_SEARCH_API_KEY=coller_ici_la_cle_brave
```

Les valeurs ci-dessus sont des **placeholders**. Enregistrer, puis fermer.

**En l'état, seule `OPENAI_API_KEY` est à renseigner.** `BRAVE_SEARCH_API_KEY` reste vide tant que Brave est reporté (section 2) : le script la signalera comme absente, ce qui est le comportement attendu.

## 4. Activer l'environnement Python

Depuis la racine du dépôt :

```powershell
.\.venv\Scripts\Activate.ps1
```

L'invite devient `(.venv) PS C:\...`.

### Si PowerShell bloque l'activation

Un message `l'exécution de scripts est désactivée sur ce système` signifie que la stratégie d'exécution interdit le script d'activation. Deux solutions :

**a. Autoriser les scripts pour l'utilisateur courant** (une fois pour toutes) :

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**b. Ne pas activer du tout** — appeler directement le Python de l'environnement, ce qui fonctionne toujours :

```powershell
.\.venv\Scripts\python.exe prototype\bloc-2\check_env.py
```

La solution **b** est suffisante pour tout ce qui suit.

## 5. Installer ou réinstaller les dépendances

```powershell
.\.venv\Scripts\python.exe -m pip install -r prototype\bloc-2\requirements.txt
```

Si l'environnement est à recréer de zéro :

```powershell
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r prototype\bloc-2\requirements.txt
```

## 6. Vérifier les clés, sans appel réseau

```powershell
.\.venv\Scripts\python.exe prototype\bloc-2\check_env.py
```

Sortie attendue dans la configuration actuelle — OpenAI renseignée, Brave reportée :

```
OPENAI_API_KEY : configurée
BRAVE_SEARCH_API_KEY : absente
```

Le script n'affiche **jamais** la valeur d'une clé, ni son préfixe, ni sa longueur. Il ne contacte aucun service. Codes de sortie : `0` tout est configuré, `1` une clé manque, `2` le fichier `.env` est introuvable.

> **Le code `1` est normal tant que Brave est reporté.** Ce script est un diagnostic global, pas un feu vert : il ne conditionne aucun test. Chaque smoke test vérifiera **uniquement son propre prérequis** — le test OpenAI n'a besoin que de `OPENAI_API_KEY`, le test GDELT d'aucune clé.

Avant d'avoir rempli `.env`, il est normal que les deux lignes affichent `absente`.

## 7. Vérifier que `.env` est bien ignoré par Git

```powershell
git check-ignore -v .env
git status --short
```

La première commande doit désigner la règle `.env` de `.gitignore`. La seconde ne doit **jamais** faire apparaître `.env` ni `.venv/`. Si `.env` apparaît dans `git status`, ne rien committer et corriger `.gitignore` avant toute autre opération.

Seul `.env.example`, qui ne contient aucune valeur, est suivi par Git.

## 8. Si une clé a été exposée

Une clé collée dans un chat, un ticket, une capture d'écran ou un fichier commité est **compromise**, même si le message a été supprimé ensuite. Agir dans cet ordre :

1. **Révoquer immédiatement** la clé chez le fournisseur — OpenAI : <https://platform.openai.com/api-keys>, bouton de suppression ; Brave : tableau de bord API, suppression de la clé.
2. **En générer une nouvelle**, dédiée au projet.
3. Remplacer la valeur dans `.env` uniquement.
4. Si la clé a été commitée, la révocation reste la seule mesure efficace : réécrire l'historique Git ne la retire pas des copies déjà distribuées.
5. Vérifier la consommation facturée sur le tableau de bord du fournisseur.

Révoquer d'abord, s'expliquer ensuite : une clé révoquée ne coûte plus rien.
