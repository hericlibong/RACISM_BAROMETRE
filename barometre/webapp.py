"""Interface locale de consultation et de relecture du baromètre."""

from __future__ import annotations

from calendar import monthrange
from collections import Counter
from contextlib import closing
from datetime import date, datetime, timedelta
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import secrets
from urllib.parse import parse_qsl, quote, urlsplit

from .storage import attach_article, connect, detach_article, load_collection, normalize_text, update_event, utc_now

CSS = Path(__file__).with_name("webapp.css")
EVENT_PATH = re.compile(r"/(evenements|public|relecture)/(E[0-9]{6,})")
STATUS = {
    "admis": "Admis au comptage", "incertain": "Incertain", "refuse": "Hors comptage",
    "brouillon": "Brouillon",
}
SOURCE_ROLE = {"source": "Relate le fait", "reaction": "Réaction", "analyse": "Analyse"}
FIELDS = {
    "summary": "Résumé destiné au public", "date_start": "Date du fait ou début de la période",
    "date_end": "Fin de la période du fait",
    "date_precision": "Ce que représente la date du fait", "episode_date_start": "Date du nouvel épisode ou début",
    "episode_date_end": "Fin du nouvel épisode", "episode_date_precision": "Ce que représente sa date",
    "location": "Lieu", "nature": "Nature du fait", "target_dimension": "Personnes visées",
    "context": "Contexte", "notes": "Notes internes",
}
FIELD_HELP = {
    "summary": "Décrivez le fait et attribuez les affirmations contestées à leur source. Ce texte figure dans la fiche publique après validation.",
    "date_start": "Date établie du fait, de sa découverte ou du début de la période connue.",
    "date_end": "Facultatif pour une date unique. Si vous connaissez seulement une borne de fin, renseignez uniquement ce champ.",
    "date_precision": "Par exemple « jour de découverte » ou « date estimée ».",
    "episode_date_start": "Par exemple, la date d’une plainte, d’une décision ou d’une révélation liée au même dossier.",
    "episode_date_end": "Facultatif. À renseigner si ce nouvel épisode s’étend sur plusieurs jours.",
    "episode_date_precision": "Par exemple « annonce du parquet ». La date d’un article est renseignée dans ses sources.",
    "location": "Lieu tel qu’il apparaît sur la fiche, par exemple Lodève (Hérault). Les coordonnées pour une carte ne sont pas encore enregistrées.",
    "nature": "Ce qui s’est produit. Par exemple « inscriptions racistes et menaces ». Plusieurs éléments peuvent coexister.",
    "target_dimension": "Précisez qui est visé selon les sources, lorsque c’est établi.",
    "context": "Cadre du fait, par exemple « lieu de culte », « sport » ou « réseaux sociaux ». Libellé modifiable.",
    "notes": "Consignez une décision de tri, une incertitude ou une piste à vérifier. Visible dans le dossier de travail.",
}
FILTERS = {"nature": "Nature", "target_dimension": "Personnes visées", "context": "Contexte",
           "location": "Territoire"}
PERIODS = {"day": "Jour", "week": "Semaine", "month": "Mois"}
MONTHS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
          "septembre", "octobre", "novembre", "décembre")


def h(value):
    return escape(str(value) if value is not None else "", quote=True)


def bounds(value):
    if not value:
        return None
    if re.fullmatch(r"[0-9]{4}", value):
        year = int(value)
        return date(year, 1, 1), date(year, 12, 31)
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}", value):
        year, month = map(int, value.split("-"))
        return date(year, month, 1), date(year, month, monthrange(year, month)[1])
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        day = date.fromisoformat(value)
        return day, day
    raise ValueError("Utilisez AAAA, AAAA-MM ou AAAA-MM-JJ pour les dates.")


def event_bounds(event):
    try:
        start = bounds(event["date_start"])
        end = bounds(event["date_end"])
    except ValueError:
        return None, None
    return start[0] if start else None, (end or start)[1] if end or start else None


def display_date(value):
    try:
        first, _ = bounds(value)
    except (ValueError, TypeError):
        return value or "Date inconnue"
    if len(value) == 4:
        return value
    month = f"{MONTHS[first.month - 1]} {first.year}"
    return f"{first.day} {month}" if len(value) == 10 else month


def date_label(start, end):
    if start and end and start != end:
        return f"{display_date(start)} – {display_date(end)}"
    if end and not start:
        return f"Au plus tard {display_date(end)}"
    return display_date(start)


def bucket(day, unit):
    if unit == "week":
        return day - timedelta(days=day.weekday())
    if unit == "month":
        return day.replace(day=1)
    return day


def bucket_label(day, unit):
    if unit == "month":
        return f"{MONTHS[day.month - 1].capitalize()} {day.year}"
    if unit == "week":
        return f"Semaine du {display_date(day.isoformat())}"
    return display_date(day.isoformat())


def series(events, unit, after, before):
    counts = Counter()
    undated = 0
    for event in events:
        if event["editorial_status"] != "admis":
            continue
        start, end = event_bounds(event)
        if (start and end and start <= end and bucket(start, unit) == bucket(end, unit)
                and (not after or start >= after) and (not before or end <= before)):
            counts[bucket(start, unit)] += 1
        else:
            undated += 1
    return counts, undated


def source_url(value):
    try:
        parsed = urlsplit(value or "")
    except ValueError:
        return None
    if parsed.scheme in {"http", "https"} and parsed.hostname and not parsed.username:
        return value
    return None


def options(values, current):
    return "".join(f'<option value="{h(key)}"{" selected" if key == current else ""}>'
                   f'{h(label)}</option>' for key, label in values.items())


def page(title, content, public=False):
    navigation = ('<a href="/public">Aperçu public</a>' if public else
                  '<a href="/">Chronologie</a><a href="/relecture">Relecture</a>'
                  '<a href="/public">Aperçu public</a>')
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{h(title)} · Baromètre</title><link rel="stylesheet" href="/style.css">
</head><body><a class="skip" href="#contenu">Aller au contenu</a>
<header class="top"><div class="wrap"><a class="brand" href="{"/public" if public else "/"}">Baromètre</a>
<nav aria-label="Navigation">{navigation}
<a href="/methode">Méthode</a></nav></div></header>
<main id="contenu" class="wrap">{content}</main></body></html>"""


def windows_for(db):
    imports = db.execute("""SELECT DISTINCT window_start, window_end, source_path
                            FROM collection_imports ORDER BY window_start, window_end""")
    windows = set()
    latest_collection = None
    for row in imports:
        windows.add((date.fromisoformat(row["window_start"]), date.fromisoformat(row["window_end"])))
        try:
            payload, _ = load_collection(Path(row["source_path"]))
            stamp = datetime.fromisoformat(payload["collected_at_utc"])
            if latest_collection is None or stamp > latest_collection:
                latest_collection = stamp
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return sorted(windows), latest_collection


def coverage_note(db, after, before):
    windows, latest = windows_for(db)
    periods = " · ".join(f"{display_date(start.isoformat())} au {display_date(end.isoformat())}"
                         for start, end in windows)
    stamp = latest.astimezone().date().isoformat() if latest else None
    text = f"<p><strong>Fenêtres de collecte intégrées</strong> {h(periods or 'Aucune')}</p>"
    text += f"<p><strong>Dernière collecte intégrée</strong> {h(display_date(stamp) if stamp else 'Date indisponible')}</p>"
    if after or before:
        start = after or (windows[0][0] if windows else before)
        end = before or (max(last for _, last in windows) if windows else after)
        if not any(first <= end and last >= start for first, last in windows):
            text += "<p>La période demandée est hors des fenêtres de collecte intégrées.</p>"
        else:
            cursor = start
            for first, last in windows:
                if first <= cursor <= last:
                    if last >= end:
                        break
                    cursor = last + timedelta(days=1)
            else:
                text += "<p>Une partie de la période demandée est hors collecte.</p>"
    return f'<aside class="coverage" aria-label="Couverture">{text}</aside>'


def event_list(db, params, public=False, review=False):
    after = date.fromisoformat(params["from"]) if params.get("from") else None
    before = date.fromisoformat(params["to"]) if params.get("to") else None
    if after and before and before < after:
        raise ValueError("La date de fin doit être postérieure ou égale à la date de début.")
    status = params.get("statut", "tous")
    unit = params.get("unite", "month")
    if unit not in PERIODS or status not in {"tous", *STATUS}:
        raise ValueError("Filtre inconnu.")
    events = db.execute("""SELECT e.*, COUNT(ea.article_id) AS source_count FROM events e
                           LEFT JOIN event_articles ea ON ea.event_id=e.id
                           GROUP BY e.id""").fetchall()
    events = sorted(events, key=lambda e: (event_bounds(e)[0] or event_bounds(e)[1]
                                          or date.min, e["id"]), reverse=True)
    matches = []
    for event in events:
        if public and not is_public(event):
            continue
        if review and (event["publication_validated_at"] or event["editorial_status"] == "refuse"):
            continue
        if not public and status != "tous" and event["editorial_status"] != status:
            continue
        start, end = event_bounds(event)
        if (after or before) and not (start or end):
            continue
        if (after and end and end < after) or (before and start and start > before):
            continue
        if any(normalize_text(params.get(key, "")) not in normalize_text(event[key] or "")
               for key in FILTERS):
            continue
        matches.append(event)

    route = "/public" if public else "/relecture" if review else "/"
    title = "Aperçu public" if public else "Dossiers à relire" if review else "Chronologie des faits"
    intro = ("Cet aperçu présente les faits validés par une personne." if public else
             "Ouvrez une fiche pour vérifier sa formulation et décider de sa publication." if review else
             "Faits liés au racisme, à l’antisémitisme, à la xénophobie et au néonazisme documentés en France.")
    content = f'<section class="intro"><h1>{title}</h1><p>{intro}</p></section>'
    if review:
        content += '<p><a class="button primary" href="/relecture/ajouter">Ajouter un fait</a></p>'
    filter_inputs = "".join(input_field(key, label, params.get(key, "")) for key, label in FILTERS.items())
    status_input = "" if public else select_field("statut", "Statut", {"tous": "Tous", **STATUS}, status)
    unit_input = "" if review else select_field("unite", "Compteurs par", PERIODS, unit)
    content += f"""<form class="filters panel" action="{route}" method="get">
    <h2>Filtres</h2><div class="grid">
    {input_field("from", "Du", params.get("from"), kind="date")}
    {input_field("to", "Au", params.get("to"), kind="date")}
    {filter_inputs}{status_input}{unit_input}</div>
    <div class="actions"><button class="primary">Appliquer</button>
    <a href="{route}">Réinitialiser</a></div></form>"""
    content += coverage_note(db, after, before)
    if not review:
        counts, undated = series(matches, unit, after, before)
        count = sum(counts.values()) + undated
        heading = "Événements validés" if public else "Événements admis au comptage"
        bars = "".join(f"<li><span>{h(bucket_label(day, unit))}</span><strong>{n}</strong></li>"
                       for day, n in sorted(counts.items(), reverse=True))
        content += f"""<section class="panel counts"><h2>{heading}</h2>
        <p class="total" data-count="{count}">{count} <span>dans la sélection</span></p>
        <ul>{bars}</ul>"""
        if undated:
            content += f"<p>{undated} avec une date insuffisamment précise pour ce découpage ou cette période.</p>"
        content += "</section>"
    prefix = "/public/" if public else "/relecture/" if review else "/evenements/"
    content += f'<section><h2>Dossiers <span class="muted">({len(matches)})</span></h2>'
    for event in matches:
        public_id = event["public_id"]
        label = "À relire" if review else STATUS[event["editorial_status"]]
        status_badge = "" if public else f'<span class="badge">{label}</span>'
        article_count = event["source_count"]
        article_label = "articles liés" if article_count != 1 else "article lié"
        content += f"""<article class="entry"><div class="meta">
        <span>{h(date_label(event["date_start"], event["date_end"]))}</span>{status_badge}</div>
        <h3><a href="{prefix}{h(public_id)}">{h(event["summary"])}</a></h3>
        <p>{h(event["location"] or "Lieu non précisé")} · {article_count} {article_label}</p>
        </article>"""
    if not matches:
        content += "<p>Aucun dossier dans cette sélection.</p>"
    return page(title, content + "</section>", public)


def is_public(event):
    return event["editorial_status"] == "admis" and bool(event["publication_validated_at"])


def field_hint(name, help_text):
    if not help_text:
        return "", ""
    return (f' aria-describedby="help-{name}"',
            f'<small class="hint" id="help-{name}">{h(help_text)}</small>')


def input_field(name, label, value="", *, kind="text", required=False, help_text=""):
    described, hint = field_hint(name, help_text)
    return (f'<div><label>{h(label)}<input type="{kind}" name="{name}" value="{h(value)}"'
            f'{described}{" required" if required else ""}></label>{hint}</div>')


def select_field(name, label, values, current=""):
    return f'<label>{h(label)}<select name="{name}">{options(values, current)}</select></label>'


def text_field(name, label, value="", required=False, help_text=""):
    described, hint = field_hint(name, help_text)
    rows = 5 if name == "summary" else 3
    return (f'<div><label>{h(label)}<textarea name="{name}" rows="{rows}"{described}{" required" if required else ""}>'
            f'{h(value)}</textarea></label>{hint}</div>')


def hidden(name, value):
    return f'<input type="hidden" name="{name}" value="{h(value)}">'


def fields_form(event):
    def fields(*keys):
        return "".join(input_field(key, FIELDS[key], event.get(key), help_text=FIELD_HELP[key])
                       for key in keys)

    def textarea(key, required=False):
        return text_field(key, FIELDS[key], event.get(key), required, FIELD_HELP[key])

    has_episode = any(event.get(key) for key in
                      ("episode_date_start", "episode_date_end", "episode_date_precision"))
    return (
        textarea("summary", required=True)
        + '<fieldset><legend>Quand le fait a eu lieu</legend>'
        + '<p class="hint">Formats possibles : AAAA, AAAA-MM ou AAAA-MM-JJ.</p><div class="grid">'
        + fields("date_start", "date_end", "date_precision") + '</div></fieldset>'
        + '<fieldset><legend>Description du fait</legend><div class="grid">'
        + fields("location", "nature", "target_dimension", "context") + '</div></fieldset>'
        + f'<details class="optional"{" open" if has_episode else ""}>'
        + '<summary>Ajouter ou modifier une suite du dossier (facultatif)</summary>'
        + '<p class="hint">Un épisode ultérieur garde sa date dans cette fiche. Le comptage reste rattaché à la date du fait.</p>'
        + '<div class="grid">'
        + fields("episode_date_start", "episode_date_end", "episode_date_precision")
        + '</div></details>' + textarea("notes")
    )


def show_event(db, event, mode, params, token):
    review = mode == "relecture"
    preview = review and params.get("apercu") == "1"
    public = mode == "public" or preview
    review = review and not preview
    public_id = event["public_id"]
    rows = db.execute("""SELECT a.*, ea.role AS link_role FROM event_articles ea
                         JOIN articles a ON a.id=ea.article_id WHERE ea.event_id=?
                         ORDER BY CASE ea.role WHEN 'source' THEN 0 WHEN 'reaction' THEN 1 ELSE 2 END,
                         a.published_at DESC, a.id""", (event["id"],)).fetchall()
    facts = {
        "Date du fait": date_label(event["date_start"], event["date_end"]),
        "Précision": event["date_precision"],
        "Date d’une suite": date_label(event["episode_date_start"], event["episode_date_end"])
            if event["episode_date_start"] or event["episode_date_end"] else None,
        "Précision de la suite": event["episode_date_precision"],
        "Lieu": event["location"],
        "Nature": event["nature"],
        "Personnes visées": event["target_dimension"],
        "Contexte": event["context"],
    }
    parts = [f'<div class="intro"><p class="meta">{h(public_id)}</p><h1>{h(event["summary"])}</h1></div>',
             '<dl class="grid panel">']
    if preview:
        parts.insert(0, '<aside class="coverage"><strong>Aperçu de la fiche enregistrée</strong>'
                     '<p>Voici le rendu public de cette version. Ouvrir cet aperçu ne publie rien.</p>'
                     f'<a href="/relecture/{h(public_id)}">Revenir à la relecture</a></aside>')
    for label, value in facts.items():
        if value:
            parts.append(f'<div><dt>{h(label)}</dt><dd>{h(value)}</dd></div>')
    parts.append('</dl>')
    if not public:
        review_status = ("Validé pour publication" if is_public(event) else
                         "Hors publication" if event["editorial_status"] == "refuse" else "À relire")
        parts.append(f'<p>{STATUS[event["editorial_status"]]} · {review_status}'
                     f'{" · Ajout manuel" if event["origin"] == "manuel" else ""}</p>')
        if event["notes"]:
            parts.append(f'<details class="panel"><summary>Notes internes</summary><p>{h(event["notes"])}</p></details>')
        if not review:
            parts.append(f'<p><a class="button" href="/relecture/{h(public_id)}">Relire ou corriger</a></p>')
    if review:
        parts.append(f'<nav class="actions review-actions" aria-label="Actions de relecture">'
                     f'<a class="button primary" href="#sources">Lire les articles</a>'
                     f'<a class="button" href="/relecture/{h(public_id)}?modifier=1#fiche">Corriger la fiche</a>'
                     f'<a class="button" href="/relecture/{h(public_id)}?apercu=1">Voir la fiche côté lecteur</a></nav>')
        if params.get("saved") == "1":
            parts.append('<p class="notice" role="status">Modification enregistrée.</p>')
    relations = db.execute("""SELECT e.*, r.relation FROM event_relations r
        JOIN events e ON e.id=r.related_event_id WHERE r.event_id=? ORDER BY e.id""", (event["id"],))
    links = [f'<li>{h(row["relation"])} · <a href="/{"public" if public else "evenements"}/'
             f'{h(row["public_id"])}">{h(row["summary"])}</a></li>'
             for row in relations if not public or is_public(row)]
    if links:
        parts.append(f'<section><h2>Faits liés</h2><ul>{"".join(links)}</ul></section>')
    parts.append(f'<section id="sources"><h2>Articles et réactions ({len(rows)})</h2>')
    if not public:
        counts = Counter(row["link_role"] for row in rows)
        parts.append(f'<p class="muted">Relatent le fait ({counts["source"]}) · '
                     f'Réactions ({counts["reaction"]}) · Analyses ({counts["analyse"]})</p>')
    if review:
        parts.append('<p>Ouvrez un article pour comparer son contenu au résumé et à la date du fait. '
                     'Si plusieurs médias relatent la même chose, leurs articles restent dans cette fiche.</p>')
    for row in rows:
        role = row["link_role"]
        media = row["media"] or "Source"
        published = display_date(row["published_at"][:10]) if row["published_at"] else "Date inconnue"
        title = f"{media} · {published}" if public else row["title"]
        url = source_url(row["original_url"] or row["google_url"])
        heading = f'<a href="{h(url)}" rel="noreferrer">{h(title)}</a>' if url else h(title)
        actions = source_editor(db, row, event, params, token) if review else ""
        parts.append(f'<article class="entry" id="article-{row["id"]}"><p class="meta">{SOURCE_ROLE[role]} · {h(media)} · '
                     f'{h(published)}</p><h3>{heading}</h3>{actions}</article>')
    if not rows:
        parts.append("<p>Aucun article rattaché.</p>")
    parts.append("</section>")
    if review:
        parts.append(article_search(db, public_id, params, token))
        parts.append(editor(event, params, token))
    return page(event["summary"], "".join(parts), public)


def form_open(public_id, action, token):
    return (f'<form method="post" action="/relecture/{h(public_id)}">'
            + hidden("action", action) + hidden("token", token))


def editor(event, params, token):
    public_id = event["public_id"]
    result = (f'<details id="fiche" class="panel"{" open" if params.get("modifier") == "1" else ""}>'
              '<summary>Modifier les informations de la fiche</summary>')
    result += (form_open(public_id, "save", token)
               + '<p>Vérifiez le résumé et les <a href="#sources">articles rattachés</a>, puis enregistrez vos corrections.</p>'
               + f'<div class="editor-fields">{fields_form(dict(event))}'
               + select_field("editorial_status", "Statut du dossier", STATUS, event["editorial_status"])
               + '<p class="hint">« Admis au comptage » alimente la chronologie de travail. « Incertain » signale un doute à lever et '
               '« Brouillon » une fiche en cours de rédaction. Seuls les dossiers admis sont comptés.</p>'
               + '</div><div class="actions"><button class="primary">Enregistrer la fiche</button></div></form>')
    result += '</details><section class="panel"><h2>Décision de publication</h2>'
    result += (f'<p><a href="/relecture/{h(public_id)}?apercu=1">Voir la fiche côté lecteur</a></p>'
               '<p class="hint">La validation porte sur la dernière version enregistrée, exige au moins une source du fait avec un lien '
               'et rend la fiche visible dans l’aperçu public local. « Classer hors publication » retire aussi le dossier du comptage et conserve sa fiche.</p>'
               '<div class="actions">')
    for action, label in (("approve", "Valider la version enregistrée pour publication"),
                          ("reject", "Classer hors publication")):
        result += form_open(public_id, action, token) + f'<button>{label}</button></form>'
    return result + '</div></section>'


def article_search(db, public_id, params, token):
    opened = " open" if params.get("article") else ""
    result = (f'<details class="panel"{opened}><summary>Ajouter un article à ce fait</summary>'
              '<p>Si un autre article parle de ce fait, cherchez-le parmi les articles déjà collectés ou ajoutez son lien direct.</p>')
    result += (f'<form method="get" action="/relecture/{h(public_id)}#rattacher" id="rattacher">'
               + input_field("article", "Mots du titre ou nom du média", params.get("article"),
                             help_text="La recherche porte sur les articles déjà présents dans la base.")
               + '<div class="actions"><button>Rechercher dans la base</button></div></form>')
    search = normalize_text(params.get("article", ""))
    if search:
        candidates = db.execute("SELECT id, title, media FROM articles ORDER BY published_at DESC, id").fetchall()
        matches = {a["id"]: f'{a["title"]} ({a["media"] or "source"})' for a in candidates
                   if search in normalize_text(f'{a["title"]} {a["media"] or ""}')}
        if matches:
            result += (form_open(public_id, "link", token)
                       + select_field("article_id", "Article", dict(list(matches.items())[:25]))
                       + select_field("link_role", "Rôle", SOURCE_ROLE, "source")
                       + '<div class="actions"><button>Rattacher</button></div></form>')
            if len(matches) > 25:
                result += '<p>Les 25 premiers résultats sont affichés. Affinez la recherche pour les autres.</p>'
        else:
            result += '<p>Aucun article trouvé dans la base. Si vous avez son adresse, ajoutez-le ci-dessous.</p>'
    result += ('<details class="optional"><summary>Ajouter un article par son lien</summary>'
               + form_open(public_id, "link-url", token)
               + f'<div class="grid">{manual_source_fields()}'
               + select_field("link_role", "Rôle dans ce dossier", SOURCE_ROLE, "source") + '</div>'
               + '<p class="hint">Collez le lien direct, puis saisissez les informations relevées sur le site du média.</p>'
               + '<div class="actions"><button>Ajouter et rattacher</button></div></form></details>')
    return result + "</details>"


def source_editor(db, row, event, params, token):
    public_id = event["public_id"]
    anchor = f'#article-{row["id"]}'
    base = f'/relecture/{h(public_id)}'
    moving = params.get("deplacer") == str(row["id"])
    opened = ' open' if moving else ''
    return (f'<details{opened}><summary>Corriger le classement de cet article</summary>'
            + form_open(public_id, "link", token) + hidden("article_id", row["id"])
            + select_field("link_role", "Ce que l’article apporte à cette fiche", SOURCE_ROLE, row["link_role"])
            + '<div class="actions"><button>Enregistrer le rôle</button></div></form>'
            + '<p class="hint">Si cet article parle d’un autre fait, déplacez uniquement cet article vers la fiche correspondante.</p>'
            + (move_form(db, row, event, token)
               + f'<p><a href="{base}{anchor}">Annuler le déplacement</a></p>' if moving
               else f'<p><a href="{base}?deplacer={row["id"]}{anchor}">Choisir une autre fiche</a></p>')
            + form_open(public_id, "unlink", token) + hidden("article_id", row["id"])
            + '<p class="hint">Si cet article a été ajouté par erreur, vous pouvez le retirer de cette fiche. Il restera dans la base.</p>'
            + '<div class="actions"><button>Retirer de cette fiche</button></div></form></details>')


def move_form(db, article, event, token):
    destinations = db.execute("""SELECT public_id, summary, location, date_start, date_end FROM events
                                 WHERE id<>? ORDER BY COALESCE(date_start, date_end) DESC, id DESC""",
                              (event["id"],)).fetchall()
    if not destinations:
        return '<p>Il n’y a pas encore d’autre fiche dans le baromètre.</p>'
    labels = {}
    for destination in destinations:
        summary = destination["summary"]
        if len(summary) > 105:
            summary = summary[:105].rsplit(" ", 1)[0] + "…"
        labels[destination["public_id"]] = " · ".join(filter(None, (
            date_label(destination["date_start"], destination["date_end"]), destination["location"], summary)))
    return (form_open(event["public_id"], "move", token) + hidden("article_id", article["id"])
            + hidden("link_role", article["link_role"])
            + '<label>Fiche qui correspond à cet article<select name="destination" required>'
            + '<option value="">Choisir par date, lieu ou résumé</option>' + options(labels, "") + '</select></label>'
            + '<div class="actions"><button>Déplacer cet article</button></div></form>')


def manual_source_fields():
    return (input_field("source_url", "Adresse de l’article", kind="url", required=True)
            + input_field("media", "Média ou organisme", required=True)
            + input_field("article_title", "Titre de l’article (facultatif)")
            + input_field("published_at", "Date de publication (facultative)", kind="date"))


def manual_form(token):
    return page("Ajouter un fait", '<div class="intro"><h1>Ajouter un fait</h1></div>'
                '<form class="panel" method="post" action="/relecture/ajouter">'
                + hidden("token", token) + f'<div class="editor-fields">{fields_form({})}'
                + f'<fieldset><legend>Source du fait</legend><div class="grid">{manual_source_fields()}</div></fieldset>'
                + '</div><div class="actions"><button class="primary">Ajouter à la relecture</button></div></form>')


def event_changes(form):
    changes = {key: form[key] for key in FIELDS if key in form}
    for start, end in (("date_start", "date_end"), ("episode_date_start", "episode_date_end")):
        left = bounds(changes.get(start))
        right = bounds(changes.get(end))
        if left and right and left[0] > right[1]:
            raise ValueError("La date de fin précède la date de début.")
    return changes


def manual_article(db, form, role):
    url = source_url(form.get("source_url"))
    media = form.get("media")
    if not url or not media:
        raise ValueError("Indiquez le média et une adresse d’article http ou https.")
    published_at = form.get("published_at")
    if published_at:
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", published_at):
            raise ValueError("Pour la publication, indiquez une date complète ou laissez le champ vide.")
        published_at = date.fromisoformat(published_at).isoformat()
    row = db.execute("SELECT id FROM articles WHERE original_url=? OR google_url=? ORDER BY id LIMIT 1",
                     (url, url)).fetchone()
    if row:
        return row[0]
    stamp = utc_now()
    return db.execute("""INSERT INTO articles
        (source_key, original_url, title, normalized_title, media, published_at, first_seen_at_utc,
         last_seen_at_utc, role, role_note, reviewed_at_utc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Article ajouté manuellement', ?)""",
        ("editorial:" + url, url, form.get("article_title") or f"Source signalée · {media}",
         "source manuelle " + url, media, published_at, stamp, stamp,
         "source_evenement" if role == "source" else role, stamp)).lastrowid


def create_manual(db, form):
    changes = event_changes(form)
    if not changes.get("summary"):
        raise ValueError("Un résumé est requis.")
    # La transaction protège le dossier et sa source même si la saisie échoue.
    stamp = utc_now()
    with db:
        cursor = db.execute("""INSERT INTO events
            (summary, origin, created_at_utc, updated_at_utc) VALUES (?, 'manuel', ?, ?)""",
            (changes["summary"], stamp, stamp))
        public_id = f"E{cursor.lastrowid:06d}"
        db.execute("UPDATE events SET public_id=? WHERE id=?", (public_id, cursor.lastrowid))
        article_id = manual_article(db, form, "source")
        attach_article(db, public_id, article_id, "source", commit=False)
        update_event(db, public_id, **changes)
    return public_id


def apply_review(db, event, form):
    action = form.get("action")
    public_id = event["public_id"]
    if action == "save":
        update_event(db, public_id, **event_changes(form), editorial_status=form.get("editorial_status"))
    elif action == "reject":
        update_event(db, public_id, editorial_status="refuse")
    elif action == "link-url":
        role = form.get("link_role")
        if role not in SOURCE_ROLE:
            raise ValueError("Choisissez le rôle de cet article.")
        with db:
            db.execute("BEGIN IMMEDIATE")
            article_id = manual_article(db, form, role)
            if db.execute("SELECT 1 FROM event_articles WHERE event_id=? AND article_id=?",
                          (event["id"], article_id)).fetchone():
                raise ValueError("Cet article est déjà rattaché. Son rôle se modifie dans Articles et réactions.")
            attach_article(db, public_id, article_id, role, commit=False)
    elif action == "approve":
        with db:
            db.execute("BEGIN IMMEDIATE")
            sources = db.execute("""SELECT COALESCE(a.original_url, a.google_url)
                FROM event_articles ea JOIN articles a ON a.id=ea.article_id
                WHERE ea.event_id=? AND ea.role='source'""", (event["id"],))
            if not any(source_url(row[0]) for row in sources):
                raise ValueError("Rattachez au moins un lien vers une source du fait avant de valider.")
            stamp = utc_now()
            db.execute("UPDATE events SET editorial_status='admis', updated_at_utc=? WHERE id=?",
                       (stamp, event["id"]))
            db.execute("UPDATE events SET publication_validated_at=? WHERE id=?", (stamp, event["id"]))
    elif action in {"link", "unlink", "move"}:
        article_id = int(form.get("article_id", "0"))
        role = form.get("link_role")
        if action == "unlink":
            detach_article(db, public_id, article_id)
        elif action == "link":
            attach_article(db, public_id, article_id, role)
        else:
            destination = form.get("destination", "").upper()
            if destination == public_id:
                raise ValueError("Choisissez un dossier de destination différent.")
            with db:
                attach_article(db, destination, article_id, role, commit=False)
                detach_article(db, public_id, article_id)
    else:
        raise ValueError("Action inconnue.")


METHOD = """<div class="intro"><h1>Méthode et périmètre</h1>
<p>Le baromètre suit les faits liés à la France rapportés par des sources médiatiques.</p></div>
<section class="panel"><h2>Ce qui est compté</h2>
<p>Un événement compte une fois. Ses reprises dans la presse et les réactions qui s’y rapportent sont rattachées à la fiche.</p>
<p>Les dates de publication des articles et les dates des faits sont distinctes. Une date approximative garde son degré de précision.</p>
<p>Les totaux décrivent les faits documentés par le baromètre. La collecte repose principalement sur Google News RSS et sa couverture dépend des sources et de leur indexation.</p>
<h2>Relecture</h2><p>L’aperçu public affiche les dossiers validés par une personne. Les fiches incertaines restent accessibles dans l’espace de travail.</p></section>"""


class LocalApp(ThreadingHTTPServer):
    def __init__(self, database, port):
        self.database = database
        self.token = secrets.token_urlsafe(32)
        super().__init__(("127.0.0.1", port), Request)


class Request(BaseHTTPRequestHandler):
    def respond(self, status, body, content_type="text/html; charset=utf-8"):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'self'; "
                         "form-action 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(payload)

    def local_host(self):
        port = self.server.server_port
        return self.headers.get("Host") in {f"127.0.0.1:{port}", f"localhost:{port}"}

    def do_GET(self):
        if not self.local_host():
            self.send_error(403)
            return
        try:
            target = urlsplit(self.path)
            params = dict(parse_qsl(target.query, max_num_fields=16))
            if target.path == "/style.css":
                self.respond(200, CSS.read_text(encoding="utf-8"), "text/css; charset=utf-8")
                return
            with closing(connect(self.server.database)) as db:
                if target.path in {"/", "/public", "/relecture"}:
                    body = event_list(db, params, target.path == "/public", target.path == "/relecture")
                elif target.path == "/methode":
                    body = page("Méthode", METHOD)
                elif target.path == "/relecture/ajouter":
                    body = manual_form(self.server.token)
                elif match := EVENT_PATH.fullmatch(target.path):
                    mode, public_id = match.groups()
                    event = db.execute("SELECT * FROM events WHERE public_id=?", (public_id,)).fetchone()
                    if event is None or (mode == "public" and not is_public(event)):
                        self.send_error(404)
                        return
                    body = show_event(db, event, mode, params, self.server.token)
                else:
                    self.send_error(404)
                    return
            self.respond(200, body)
        except ValueError as exc:
            self.respond(400, page("Filtre invalide", f'<h1>Filtre invalide</h1><p>{h(exc)}</p>'))

    def do_POST(self):
        if not self.local_host():
            self.send_error(403)
            return
        path = urlsplit(self.path).path
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 32768:
                raise ValueError("Taille de formulaire invalide.")
            form = {key: value.strip() for key, value in
                    parse_qsl(self.rfile.read(size).decode("utf-8"), keep_blank_values=True, max_num_fields=30)}
            if not secrets.compare_digest(form.get("token", "").encode(), self.server.token.encode()):
                self.send_error(403)
                return
            with closing(connect(self.server.database)) as db:
                if path == "/relecture/ajouter":
                    public_id = create_manual(db, form)
                elif (match := EVENT_PATH.fullmatch(path)) and match[1] == "relecture":
                    public_id = match[2]
                    event = db.execute("SELECT * FROM events WHERE public_id=?", (public_id,)).fetchone()
                    if event is None:
                        self.send_error(404)
                        return
                    apply_review(db, event, form)
                else:
                    self.send_error(404)
                    return
            self.send_response(303)
            self.send_header("Location", f"/relecture/{quote(public_id)}?saved=1")
            self.send_header("Content-Length", "0")
            self.end_headers()
        except ValueError as exc:
            self.respond(400, page("Correction refusée", f'<h1>Correction refusée</h1><p>{h(exc)}</p>'
                                   f'<p><a href="{h(path)}">Revenir au formulaire</a></p>'))


def serve(database, port):
    if not database.is_file():
        raise ValueError(f"Base absente : {database}. Importez d’abord une collecte avec prepare.")
    with closing(connect(database)):
        pass
    with LocalApp(database, port) as app:
        print(f"Baromètre local : http://127.0.0.1:{app.server_port}/", flush=True)
        try:
            app.serve_forever()
        except KeyboardInterrupt:
            pass
