#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ANALYSIS = ROOT / "analysis"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def page(title: str, body: str, prefix: str = "") -> str:
    nav = """
    <nav class="topbar">
      <a href="{prefix}index.html">Overview</a>
      <a href="{prefix}lectures.html">Lectures</a>
      <a href="{prefix}concepts.html">Concepts</a>
      <a href="{prefix}families.html">Families</a>
      <a href="{prefix}themes.html">Themes</a>
      <a href="{prefix}evidence.html">Evidence</a>
    </nav>
    """.format(prefix=prefix)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{prefix}assets/styles.css">
</head>
<body>
{nav}
<main>
{body}
</main>
</body>
</html>
"""


def concept_link(concept: dict[str, Any]) -> str:
    return f"concepts/{concept['id']}.html"


def lecture_link(lecture: dict[str, Any]) -> str:
    return f"lectures/{lecture['index']:02d}.html"


def render_home(concepts: list[dict[str, Any]], lectures: list[dict[str, Any]], themes: list[dict[str, Any]], evidence: list[dict[str, Any]], families: list[dict[str, Any]]) -> None:
    available = sum(1 for lecture in lectures if lecture["transcript_status"] == "available")
    missing = len(lectures) - available
    body = f"""
    <section class="intro">
      <p class="eyebrow">Gravity and Light Central Lecture Course</p>
      <h1>First-principles concept atlas</h1>
      <p class="lede">A transcript-grounded map of the mathematical ideas in the course, written from everyday starting points and kept honest about missing evidence.</p>
    </section>

    <section class="metrics">
      <div><strong>{len(lectures)}</strong><span>lectures</span></div>
      <div><strong>{available}</strong><span>transcript-backed</span></div>
      <div><strong>{len(concepts)}</strong><span>concept pages</span></div>
      <div><strong>{len(families)}</strong><span>families</span></div>
      <div><strong>{len(evidence)}</strong><span>evidence records</span></div>
      <div><strong>{missing}</strong><span>needs notes</span></div>
    </section>

    <section>
      <h2>Lecture Families</h2>
      <div class="theme-list">
        {''.join(render_family_summary(family) for family in families)}
      </div>
    </section>

    <section>
      <h2>Course Spine</h2>
      <div class="theme-list">
        {''.join(render_theme_summary(theme) for theme in themes)}
      </div>
    </section>

    <section>
      <h2>High-Priority Audit Gaps</h2>
      <ul class="plain-list">
        {''.join(f"<li>Lecture {lecture['index']:02d}: {esc(lecture['title'])}</li>" for lecture in lectures if lecture['transcript_status'] != 'available')}
      </ul>
    </section>
    """
    write(SITE / "index.html", page("Gravity and Light Concept Atlas", body))


def render_theme_summary(theme: dict[str, Any]) -> str:
    return f"""
    <article class="row-block">
      <h3>{esc(theme['name'])}</h3>
      <p><strong>Question:</strong> {esc(theme['plain_question'])}</p>
      <p>{esc(theme['answer'])}</p>
      <p class="quiet">{esc(theme['why_the_math_matters'])}</p>
    </article>
    """


def render_family_summary(family: dict[str, Any]) -> str:
    return f"""
    <article class="row-block">
      <h3>{esc(family['name'])}</h3>
      <p><strong>Problem:</strong> {esc(family['plain_problem'])}</p>
      <p>{esc(family['mathematical_spine'])}</p>
      <p class="quiet">{esc(family['audit_note'])}</p>
    </article>
    """


def render_lectures(lectures: list[dict[str, Any]], concepts_by_id: dict[str, dict[str, Any]]) -> None:
    rows = []
    for lecture in lectures:
        links = " ".join(
            f"<a class=\"chip\" href=\"{concept_link(concepts_by_id[cid])}\">{esc(concepts_by_id[cid]['name'])}</a>"
            for cid in lecture["concept_ids"]
        )
        if lecture["transcript_status"] == "available":
            status = "transcript-backed"
        elif lecture.get("external_notes_status") == "available":
            status = "notes-backed"
        else:
            status = "needs notes"
        rows.append(
            f"""
            <article class="lecture-row">
              <div class="lecture-number">{lecture['index']:02d}</div>
              <div>
                <h2><a href="{lecture_link(lecture)}">{esc(lecture['title'])}</a></h2>
                <p class="quiet">{esc(lecture['audit_note'])}</p>
                <p><a href="{esc(lecture['url'])}">YouTube source</a></p>
                <p><span class="status {esc(status.replace(' ', '-'))}">{esc(status)}</span> {links}</p>
              </div>
            </article>
            """
        )
    write(SITE / "lectures.html", page("Lectures", "<h1>Lectures</h1>" + "\n".join(rows)))


def render_lecture_pages(lectures: list[dict[str, Any]], concepts_by_id: dict[str, dict[str, Any]], families: list[dict[str, Any]]) -> None:
    family_by_lecture = {}
    for family in families:
        for index in family["lecture_indexes"]:
            family_by_lecture[index] = family
    for lecture in lectures:
        concept_blocks = []
        for cid in lecture["concept_ids"]:
            concept = concepts_by_id[cid]
            concept_blocks.append(
                f"""
                <article class="row-block">
                  <h2><a href="../concepts/{esc(concept['id'])}.html">{esc(concept['name'])}</a></h2>
                  <p>{esc(concept['ordinary_problem'])}</p>
                  <p><strong>Object:</strong> {esc(concept['mathematical_object'])}</p>
                  <p><strong>Operation:</strong> {esc(concept['operation'])}</p>
                </article>
                """
            )
        objects = "".join(f"<li>{esc(item)}</li>" for item in lecture["mathematical_objects_to_track"]) or "<li>No object assigned yet.</li>"
        family = family_by_lecture.get(lecture["index"])
        family_text = f"{family['name']}: {family['plain_problem']}" if family else "No family assigned."
        note_sources = "".join(
            f"<li><a href=\"{esc(source['url'])}\">{esc(source['title'])}</a></li>"
            for source in lecture.get("external_note_sources", [])
        )
        note_block = f"<ul>{note_sources}</ul>" if note_sources else "<p class=\"quiet\">No external notes linked for this lecture.</p>"
        manual_note = lecture.get("manual_note_template")
        manual_block = (
            f"<p class=\"quiet\">Manual note template: {esc(manual_note)}</p>"
            if manual_note
            else "<p class=\"quiet\">No manual note template required for this lecture.</p>"
        )
        body = f"""
        <p><a href="../lectures.html">Back to lectures</a></p>
        <h1>Lecture {lecture['index']:02d}: {esc(lecture['title'])}</h1>
        <p class="lede">{esc(lecture['central_question'])}</p>
        <section class="deep-read">
          <h2>Family Role</h2>
          <p>{esc(family_text)}</p>
        </section>
        <section class="deep-read">
          <h2>First-Principles Role</h2>
          <p>{esc(lecture['first_principles_role'])}</p>
        </section>
        <section class="deep-read">
          <h2>Objects To Track</h2>
          <ul>{objects}</ul>
        </section>
        <section class="deep-read">
          <h2>Evidence Status</h2>
          <p>{esc(lecture['reader_warning'])}</p>
          <p><a href="{esc(lecture['url'])}">Open YouTube lecture</a></p>
          <h3>External Notes</h3>
          {note_block}
          <h3>Manual Notes</h3>
          {manual_block}
        </section>
        <section>
          <h2>Linked Concepts</h2>
          {''.join(concept_blocks) if concept_blocks else '<p>No concepts assigned yet.</p>'}
        </section>
        """
        write(SITE / "lectures" / f"{lecture['index']:02d}.html", page(lecture["title"], body, "../"))


def render_concepts(concepts: list[dict[str, Any]]) -> None:
    cards = []
    for concept in concepts:
        cards.append(
            f"""
            <a class="concept-card" href="{concept_link(concept)}">
              <span>{esc(concept['theme'])}</span>
              <h2>{esc(concept['name'])}</h2>
              <p>{esc(concept['ordinary_problem'])}</p>
            </a>
            """
        )
    write(SITE / "concepts.html", page("Concepts", "<h1>Concepts</h1><div class=\"concept-grid\">" + "\n".join(cards) + "</div>"))


def render_concept_pages(concepts: list[dict[str, Any]], evidence_by_id: dict[str, dict[str, Any]]) -> None:
    concepts_by_id = {concept["id"]: concept for concept in concepts}
    for concept in concepts:
        ev_items = []
        for eid in concept["evidence_ids"]:
            ev = evidence_by_id[eid]
            snippet = f"<blockquote>{esc(ev['snippet'])}</blockquote>" if ev["snippet"] else "<p class=\"quiet\">No local transcript snippet available yet.</p>"
            ev_items.append(
                f"""
                <article class="evidence-item">
                  <h3>Lecture {ev['lecture_index']:02d}: {esc(ev['lecture_title'])}</h3>
                  <p><a href="{esc(ev['url'])}">{esc(ev['url'])}</a></p>
                  {snippet}
                  <p><strong>Evidence status:</strong> {esc(ev['confidence'])}</p>
                  <p>{esc(ev['lecture_argument'])}</p>
                </article>
                """
            )
        body = f"""
        <p><a href="../concepts.html">Back to concepts</a></p>
        <h1>{esc(concept['name'])}</h1>
        <p class="lede">{esc(concept['ordinary_problem'])}</p>
        <div class="two-col">
          {section('Naive Picture', concept['naive_picture'])}
          {section('Why It Fails', concept['why_naive_fails'])}
          {section('Mathematical Object', concept['mathematical_object'])}
          {section('Operation', concept['operation'])}
          {section('Why It Matters', concept['why_for_gravity_light'])}
          {section('What Breaks Without It', concept['what_breaks_without_it'])}
          {section('Mini Example', concept['worked_mini_example'])}
          {section('Common Confusion', concept['common_confusion'])}
        </div>
        <section class="deep-read">
          <h2>First-Principles Walkthrough</h2>
          <p>{esc(concept['first_principles_walkthrough'])}</p>
        </section>
        <section class="deep-read">
          <h2>Mathematical Detail In Plain Language</h2>
          <p>{esc(concept['mathematical_detail_plain'])}</p>
        </section>
        <section class="deep-read">
          <h2>Why This Cannot Be Skipped</h2>
          <p>{esc(concept['why_this_is_critical'])}</p>
        </section>
        <section class="deep-read">
          <h2>Where It Sits In The Course</h2>
          <p>{esc(concept['family_bridge'])}</p>
        </section>
        <section class="deep-read">
          <h2>Connective Thread</h2>
          <p>{esc(concept['connective_thread'])}</p>
          <div class="related-grid">
            {render_related('Depends On', concept['prerequisite_ids'], concepts_by_id)}
            {render_related('Used Later By', concept['later_use_ids'], concepts_by_id)}
          </div>
        </section>
        <section>
          <h2>Evidence</h2>
          {''.join(ev_items)}
        </section>
        """
        write(SITE / "concepts" / f"{concept['id']}.html", page(concept["name"], body, "../"))


def section(title: str, text: str) -> str:
    return f"<section class=\"detail\"><h2>{esc(title)}</h2><p>{esc(text)}</p></section>"


def render_related(title: str, ids: list[str], concepts_by_id: dict[str, dict[str, Any]]) -> str:
    if not ids:
        return f"<article><h3>{esc(title)}</h3><p class=\"quiet\">No linked concept assigned.</p></article>"
    links = " ".join(
        f"<a class=\"chip\" href=\"{esc(concepts_by_id[cid]['id'])}.html\">{esc(concepts_by_id[cid]['name'])}</a>"
        for cid in ids
        if cid in concepts_by_id
    )
    return f"<article><h3>{esc(title)}</h3><p>{links}</p></article>"


def render_themes(themes: list[dict[str, Any]], concepts_by_id: dict[str, dict[str, Any]]) -> None:
    blocks = []
    for theme in themes:
        links = " ".join(f"<a class=\"chip\" href=\"{concept_link(concepts_by_id[cid])}\">{esc(concepts_by_id[cid]['name'])}</a>" for cid in theme["concept_ids"])
        blocks.append(
            f"""
            <article class="row-block">
              <h2>{esc(theme['name'])}</h2>
              <p><strong>{esc(theme['plain_question'])}</strong></p>
              <p>{esc(theme['answer'])}</p>
              <p>{esc(theme['why_the_math_matters'])}</p>
              <p>{links}</p>
            </article>
            """
        )
    write(SITE / "themes.html", page("Themes", "<h1>Themes and Subthemes</h1>" + "\n".join(blocks)))


def render_families(families: list[dict[str, Any]], concepts_by_id: dict[str, dict[str, Any]]) -> None:
    blocks = []
    for family in families:
        links = " ".join(
            f"<a class=\"chip\" href=\"{concept_link(concepts_by_id[cid])}\">{esc(concepts_by_id[cid]['name'])}</a>"
            for cid in family["concept_ids"]
        )
        missing = ", ".join(f"{index:02d}" for index in family["missing_transcript_lectures"]) or "none"
        blocks.append(
            f"""
            <article class="family-block">
              <h2>{esc(family['name'])}</h2>
              <p><strong>Lectures:</strong> {esc(', '.join(f'{index:02d}' for index in family['lecture_indexes']))}</p>
              <p><strong>Plain problem:</strong> {esc(family['plain_problem'])}</p>
              <p><strong>Mathematical spine:</strong> {esc(family['mathematical_spine'])}</p>
              <p><strong>Why it matters:</strong> {esc(family['why_it_matters'])}</p>
              <p><strong>What to watch for:</strong> {esc(family['what_to_watch_for'])}</p>
              <p class="quiet">Missing local transcripts: {esc(missing)}</p>
              <p>{links}</p>
            </article>
            """
        )
    write(SITE / "families.html", page("Lecture Families", "<h1>Lecture Families</h1>" + "\n".join(blocks)))


def render_evidence(evidence: list[dict[str, Any]]) -> None:
    rows = []
    for ev in evidence:
        snippet = esc(ev["snippet"]) if ev["snippet"] else "No transcript snippet available."
        source = ev.get("source_type", ev["confidence"])
        if ev.get("note_source_title"):
            source = f"{source}: {ev['note_source_title']}"
        rows.append(
            f"""
            <tr>
              <td>{esc(ev['id'])}</td>
              <td>{ev['lecture_index']:02d}</td>
              <td>{esc(ev['confidence'])}</td>
              <td>{esc(source)}</td>
              <td><a href="{esc(ev['url'])}">{esc(ev['lecture_title'])}</a></td>
              <td>{snippet}</td>
            </tr>
            """
        )
    table = f"""
    <h1>Evidence Ledger</h1>
    <table>
      <thead><tr><th>ID</th><th>Lecture</th><th>Status</th><th>Evidence Type</th><th>Source</th><th>Snippet</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    """
    write(SITE / "evidence.html", page("Evidence", table))


def write_css() -> None:
    css = """
:root {
  --ink: #171717;
  --muted: #62615d;
  --line: #d8d6cf;
  --paper: #f7f6f2;
  --panel: #ffffff;
  --accent: #255f85;
  --accent-2: #7a3f2a;
  --ok: #2f6f4e;
  --warn: #8a5a00;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font: 16px/1.55 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 3px; }
.topbar {
  position: sticky;
  top: 0;
  z-index: 2;
  display: flex;
  gap: 18px;
  align-items: center;
  min-height: 52px;
  padding: 0 28px;
  border-bottom: 1px solid var(--line);
  background: rgba(247, 246, 242, 0.96);
}
main { width: min(1160px, calc(100% - 36px)); margin: 34px auto 70px; }
h1 { font-size: clamp(2rem, 4vw, 4rem); line-height: 1.02; margin: 0 0 18px; letter-spacing: 0; }
h2 { font-size: 1.25rem; margin: 0 0 10px; letter-spacing: 0; }
h3 { margin: 0 0 8px; }
.intro { max-width: 850px; margin-bottom: 28px; }
.eyebrow { color: var(--accent-2); text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.08em; font-weight: 700; }
.lede { font-size: 1.25rem; color: #343330; max-width: 850px; }
.quiet { color: var(--muted); }
.metrics {
  display: grid;
  grid-template-columns: repeat(6, minmax(120px, 1fr));
  gap: 1px;
  border: 1px solid var(--line);
  background: var(--line);
  margin: 28px 0 38px;
}
.metrics div { background: var(--panel); padding: 18px; }
.metrics strong { display: block; font-size: 2rem; line-height: 1; }
.metrics span { color: var(--muted); }
.theme-list, .two-col, .concept-grid, .related-grid { display: grid; gap: 14px; }
.theme-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.two-col { grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start; }
.concept-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.related-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.row-block, .detail, .evidence-item, .concept-card, .lecture-row, .family-block, .deep-read {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 18px;
}
.concept-card { display: block; min-height: 220px; text-decoration: none; color: var(--ink); }
.concept-card span { color: var(--accent-2); font-size: 0.82rem; font-weight: 700; }
.lecture-row { display: grid; grid-template-columns: 54px 1fr; gap: 16px; margin-bottom: 12px; }
.lecture-number { color: var(--accent-2); font-weight: 800; font-size: 1.2rem; }
.chip {
  display: inline-block;
  margin: 4px 6px 4px 0;
  padding: 3px 8px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: #fbfaf7;
  font-size: 0.88rem;
}
.status { font-weight: 700; margin-right: 10px; }
.status.transcript-backed { color: var(--ok); }
.status.notes-backed { color: var(--accent); }
.status.needs-notes { color: var(--warn); }
.plain-list li { margin-bottom: 8px; }
blockquote { margin: 10px 0; padding-left: 14px; border-left: 3px solid var(--accent); color: #353430; }
.deep-read, .family-block { margin: 14px 0; }
.deep-read p, .family-block p { max-width: 880px; }
table { width: 100%; border-collapse: collapse; background: var(--panel); }
th, td { border: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top; }
th { background: #ece9df; }
@media (max-width: 820px) {
  .topbar { overflow-x: auto; padding: 0 16px; }
  main { width: min(100% - 24px, 1160px); }
  .metrics, .theme-list, .two-col, .concept-grid, .related-grid { grid-template-columns: 1fr; }
  .lecture-row { grid-template-columns: 1fr; }
}
"""
    write(SITE / "assets" / "styles.css", css)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    concepts = load_json(ANALYSIS / "concepts" / "concept-atlas.json")
    evidence = load_json(ANALYSIS / "evidence" / "evidence-ledger.json")
    lectures = load_json(ANALYSIS / "lectures" / "lecture-atlas.json")
    themes = load_json(ANALYSIS / "themes" / "theme-map.json")
    families = load_json(ANALYSIS / "families" / "family-map.json")
    concepts_by_id = {concept["id"]: concept for concept in concepts}
    evidence_by_id = {item["id"]: item for item in evidence}
    render_home(concepts, lectures, themes, evidence, families)
    render_lectures(lectures, concepts_by_id)
    render_lecture_pages(lectures, concepts_by_id, families)
    render_concepts(concepts)
    render_concept_pages(concepts, evidence_by_id)
    render_families(families, concepts_by_id)
    render_themes(themes, concepts_by_id)
    render_evidence(evidence)
    write_css()
    print(f"wrote site to {SITE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
