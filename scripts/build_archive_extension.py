#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw-material" / "youtube"
ANALYSIS = ROOT / "analysis"
SITE = ROOT / "site"


VIDEO_DEPTH: dict[str, dict[str, Any]] = {
    "_XkhZQ-hNLs": {
        "concept_ids": ["topology-continuity", "open-sets-neighborhood-tests", "continuous-maps-preserve-nearness"],
        "ordinary_problem": "The tutorial turns the first lecture's idea of nearness into tests students can actually use.",
        "mathematical_object": "Open sets, neighborhoods, continuous maps, and the tests that decide whether nearness is preserved.",
        "operation": "Check whether a proposed region contains local room around each point, then pull open-set tests backward through maps.",
        "why_it_matters": "The later geometry needs continuity before it can speak about smooth fields, paths, metrics, or light cones.",
        "what_breaks": "Without these tests, later formulas can look smooth while hiding jumps or chart-dependent assumptions.",
    },
    "ghfEQ3u_B6g": {
        "concept_ids": ["manifolds-local-flatness", "charts-atlases-coordinate-overlap"],
        "ordinary_problem": "The tutorial practices how many local maps can describe one space without turning the maps into the space itself.",
        "mathematical_object": "Charts, atlases, overlap maps, and the points they name.",
        "operation": "Move between chart descriptions and check that overlap rules preserve the object being described.",
        "why_it_matters": "Spacetime often needs several coordinate patches, especially near horizons or awkward global regions.",
        "what_breaks": "Without overlap discipline, a bad coordinate patch can be mistaken for a real edge or singularity.",
    },
    "5oeWX3NUhMA": {
        "concept_ids": ["multilinear-objects", "dual-vectors-measure-directions", "tensor-components-versus-object"],
        "ordinary_problem": "The tutorial makes students handle slot-aware quantities instead of treating every symbol as a vector or matrix.",
        "mathematical_object": "Vectors, covectors, tensors, bases, components, and the multilinear slots that give each object its job.",
        "operation": "Feed objects into slots, change bases, and check which parts are the object and which parts are only its display.",
        "why_it_matters": "The metric, curvature, and stress-energy tensor all carry their meaning through slots and transformations.",
        "what_breaks": "Without this practice, Einstein's equation becomes symbol matching rather than a claim about geometric and physical measuring rules.",
    },
    "FXPdKxOq1KA": {
        "concept_ids": ["manifolds-local-flatness", "charts-atlases-coordinate-overlap", "smoothness-change-rates"],
        "ordinary_problem": "The tutorial turns differentiability on curved spaces into a checkable chart-change rule.",
        "mathematical_object": "Smooth structures, coordinate maps, and differentiable overlap maps.",
        "operation": "Test whether derivatives computed in one chart remain legitimate after changing charts.",
        "why_it_matters": "Curvature and field equations require derivatives that belong to spacetime, not to one drawing of spacetime.",
        "what_breaks": "Without smooth overlap rules, later derivatives can measure the map instead of the manifold.",
    },
    "mACNdkRdHEA": {
        "concept_ids": ["tangent-spaces-fields", "tangent-vectors-as-derivatives", "dual-vectors-measure-directions"],
        "ordinary_problem": "The tutorial practices the internal meaning of a direction at a point.",
        "mathematical_object": "Tangent vectors, curves through a point, derivations, and dual measuring rules.",
        "operation": "Use a direction to differentiate functions and compare that with the curve picture of velocity.",
        "why_it_matters": "Particles, observers, light rays, and fields all need local directions before the metric says which directions are time-like or null.",
        "what_breaks": "Without tangent-space practice, velocity and local change look imported from flat space.",
    },
    "C4jJe_b0KMs": {
        "concept_ids": ["tangent-spaces-fields", "vector-fields-as-local-instructions"],
        "ordinary_problem": "The tutorial should practice fields as point-by-point assignments rather than substances spread through space.",
        "mathematical_object": "Scalar fields, vector fields, tensor fields, and smooth assignments over a manifold.",
        "operation": "Assign a value at each point and check that the assignment varies smoothly enough for later differentiation.",
        "why_it_matters": "Matter, observer congruences, symmetry directions, and gravitational variables are all fields.",
        "what_breaks": "Without this practice, a field can be confused with a force or a material fluid instead of a structured assignment.",
    },
    "bYfvT-ky1lU": {
        "concept_ids": ["symmetry-conservation", "killing-fields-symmetry-directions"],
        "ordinary_problem": "The tutorial practices how sameness becomes a calculation instead of a visual impression.",
        "mathematical_object": "Symmetry maps, flows, vector fields, and preserved geometric structures.",
        "operation": "Check whether a transformation or flow leaves the relevant structure unchanged.",
        "why_it_matters": "Symmetry is what lets special spacetimes produce conserved quantities and tractable equations.",
        "what_breaks": "Without this practice, conservation laws appear as isolated facts rather than consequences of preserved structure.",
    },
    "iwbJvfFNRh8": {
        "concept_ids": ["integration-on-manifolds", "stokes-boundary-bulk-accounting"],
        "ordinary_problem": "The tutorial should make curved-space integration into a coordinate-independent adding rule.",
        "mathematical_object": "Forms, oriented regions, boundaries, and integrable geometric quantities.",
        "operation": "Add local data over a region and relate boundary accounting to bulk accounting.",
        "why_it_matters": "Actions, fluxes, conservation laws, and source totals all require adding local facts without depending on one chart.",
        "what_breaks": "Without this practice, boundary terms look like scraps of algebra instead of part of the physical accounting.",
    },
    "KQe2sqGIzTg": {
        "concept_ids": ["black-holes-horizons", "event-horizon-causal-boundary"],
        "ordinary_problem": "The tutorial practices reading a black-hole spacetime through geometry and causal reach.",
        "mathematical_object": "The Schwarzschild metric, radial coordinates, horizons, and causal directions.",
        "operation": "Track which coordinate features are removable and which causal boundaries remain after better descriptions are chosen.",
        "why_it_matters": "Black holes test whether metric, null paths, and coordinates have been separated cleanly.",
        "what_breaks": "Without this practice, a coordinate singularity can be mistaken for a physical surface.",
    },
    "HuQ79CWcDac": {
        "concept_ids": ["cosmology-scale-factor", "scale-factor-expansion-history", "hubble-rate-as-change-of-scale"],
        "ordinary_problem": "The tutorial practices how a simplified universe model turns geometry and matter into expansion history.",
        "mathematical_object": "Scale factor, homogeneous spatial slices, matter content, and reduced field equations.",
        "operation": "Use symmetry assumptions to reduce the field equation and read expansion from the changing scale factor.",
        "why_it_matters": "Cosmology connects the abstract metric to redshift, age, matter content, and observation.",
        "what_breaks": "Without this practice, expansion gets misread as motion through a fixed outside space.",
    },
    "w85vePX8TsA": {
        "concept_ids": ["penrose-diagrams-compress-infinity", "event-horizon-causal-boundary"],
        "ordinary_problem": "The tutorial practices drawing causal structure without pretending ordinary distances are preserved.",
        "mathematical_object": "Penrose diagrams, conformal rescaling, infinity, null directions, and causal boundaries.",
        "operation": "Compress the picture while keeping light directions and causal order visible.",
        "why_it_matters": "Horizons and infinities are global causal questions, not local drawing problems.",
        "what_breaks": "Without this practice, black-hole and cosmology diagrams become pictures with no clear rule for what they preserve.",
    },
    "udmiKlH7-AA": {
        "concept_ids": ["perturbations-waves", "quadrupole-source-changing-shape", "strain-relative-length-change"],
        "ordinary_problem": "The evening lecture connects gravitational waves to physical intuition and observable signals.",
        "mathematical_object": "Small metric disturbances, wave sources, and detector response.",
        "operation": "Follow how changing mass-energy motion produces a propagating disturbance and how detectors read relative length change.",
        "why_it_matters": "This makes the abstract wave machinery answer the ordinary question of what was actually measured.",
        "what_breaks": "Without this bridge, gravitational waves sound like a metaphor rather than a measured change in spacetime geometry.",
    },
    "bxzTD7usU1s": {
        "concept_ids": ["canonical-formulation", "initial-data-constraints", "stress-energy-matter"],
        "ordinary_problem": "The evening lecture frames why gravity and quantum theory strain against each other.",
        "mathematical_object": "Classical spacetime geometry, quantum matter, and the source side of gravity.",
        "operation": "Compare what is held fixed in classical geometry with what quantum theory makes variable or uncertain.",
        "why_it_matters": "The course needs this frontier view because canonical gravity and quantizable matter are not just extra topics; they expose what the classical theory has not settled.",
        "what_breaks": "Without this framing, quantum gravity looks like a fashionable add-on instead of a pressure point in the theory's basic bookkeeping.",
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def archive_slug(record: dict[str, Any]) -> str:
    prefix = "tutorial" if record["type"] == "tutorial" else "evening"
    return f"{prefix}-{record['type_index']:02d}"


def compact_snippet(text: str, max_words: int = 56) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(",.;:") + "..."


def choose_cue(record: dict[str, Any], depth: dict[str, Any]) -> dict[str, Any] | None:
    if record["transcript_status"] != "available":
        return None
    cues = load_json(ROOT / record["cue_json"])
    terms = []
    for field in ("mathematical_object", "operation", "why_it_matters"):
        terms.extend(word.lower().strip(".,;:") for word in depth[field].split() if len(word) > 6)
    for cue in cues:
        text = cue["text"].lower()
        if any(term in text for term in terms):
            return cue
    return cues[min(len(cues) - 1, max(0, len(cues) // 5))] if cues else None


def build_record(record: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    depth = VIDEO_DEPTH[record["id"]]
    cue = choose_cue(record, depth)
    source_type = "youtube-transcript" if cue else "unsupported-placeholder"
    confidence = "strong" if cue else "missing-transcript"
    evidence = {
        "id": f"archive-ev-{archive_slug(record)}",
        "video_id": record["id"],
        "archive_index": record["archive_index"],
        "video_type": record["type"],
        "type_index": record["type_index"],
        "title": record["expected_title"],
        "url": f"{record['url']}&t={int(cue['start_seconds'])}s" if cue else record["url"],
        "timestamp": cue["start"] if cue else None,
        "snippet": compact_snippet(cue["text"]) if cue else "",
        "source_type": source_type,
        "confidence": confidence,
        "caveat_or_warning": "This archive page is backed by a local YouTube caption file, so its claims should stay close to the cited span and avoid adding unsupported lecture detail." if cue else "Caption download failed or source is missing; this page is a scaffold until a transcript, external note, or manual timestamp note is added.",
    }
    page_data = {
        **record,
        **depth,
        "slug": archive_slug(record),
        "evidence_id": evidence["id"],
        "evidence_status": confidence,
        "source_type": source_type,
        "reader_warning": evidence["caveat_or_warning"],
    }
    return page_data, evidence


def page(title: str, body: str, prefix: str = "") -> str:
    nav = f"""
    <nav class="topbar">
      <a href="{prefix}index.html">Overview</a>
      <a href="{prefix}lectures.html">Lectures</a>
      <a href="{prefix}tutorials.html">Tutorials</a>
      <a href="{prefix}evening-lectures.html">Evening Lectures</a>
      <a href="{prefix}concepts.html">Concepts</a>
      <a href="{prefix}families.html">Families</a>
      <a href="{prefix}themes.html">Themes</a>
      <a href="{prefix}evidence.html">Evidence</a>
    </nav>
    """
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


def concept_links(concept_ids: list[str], prefix: str = "../") -> str:
    return " ".join(
        f'<a class="chip" href="{prefix}concepts/{esc(concept_id)}.html">{esc(concept_id)}</a>'
        for concept_id in concept_ids
    )


def render_index(path: Path, title: str, intro: str, records: list[dict[str, Any]]) -> None:
    rows = []
    for record in records:
        status = "transcript-backed" if record["evidence_status"] == "strong" else "needs notes"
        rows.append(
            f"""
            <article class="lecture-row">
              <div class="lecture-number">{record['type_index']:02d}</div>
              <div>
                <h2><a href="archive/{esc(record['slug'])}.html">{esc(record['expected_title'])}</a></h2>
                <p class="quiet">{esc(record['ordinary_problem'])}</p>
                <p><span class="status {esc(status.replace(' ', '-'))}">{esc(status)}</span> {concept_links(record['concept_ids'], '')}</p>
              </div>
            </article>
            """
        )
    body = f"<h1>{esc(title)}</h1><p class=\"lede\">{esc(intro)}</p>{''.join(rows)}"
    path.write_text(page(title, body), encoding="utf-8")


def render_detail(record: dict[str, Any], evidence: dict[str, Any]) -> None:
    snippet = f"<blockquote>{esc(evidence['snippet'])}</blockquote>" if evidence["snippet"] else "<p class=\"quiet\">No transcript snippet available yet.</p>"
    related = ", ".join(f"Lecture {item:02d}" for item in record.get("related_central_lectures", [])) or "No central lecture link recorded yet."
    body = f"""
    <p><a href="../{'tutorials.html' if record['type'] == 'tutorial' else 'evening-lectures.html'}">Back to archive section</a></p>
    <h1>{esc(record['expected_title'])}</h1>
    <p class="lede">{esc(record['ordinary_problem'])}</p>
    <div class="two-col">
      <section class="detail"><h2>Mathematical Object</h2><p>{esc(record['mathematical_object'])}</p></section>
      <section class="detail"><h2>Operation</h2><p>{esc(record['operation'])}</p></section>
      <section class="detail"><h2>Why It Matters</h2><p>{esc(record['why_it_matters'])}</p></section>
      <section class="detail"><h2>What Breaks Without It</h2><p>{esc(record['what_breaks'])}</p></section>
    </div>
    <section class="deep-read">
      <h2>First-Principles Role</h2>
      <p>This video is not extra decoration around the central lectures. It practices or stretches the same mathematical idea from a different angle. The ordinary task is: {esc(record['ordinary_problem'])} The object to keep in view is: {esc(record['mathematical_object'])} The work being done is: {esc(record['operation'])} That matters because {esc(record['why_it_matters'])}</p>
    </section>
    <section class="deep-read">
      <h2>Central Course Links</h2>
      <p>{esc(related)}</p>
      <p>{concept_links(record['concept_ids'])}</p>
    </section>
    <section>
      <h2>Evidence</h2>
      <p><a href="{esc(evidence['url'])}">Open video source</a></p>
      {snippet}
      <p><strong>Evidence status:</strong> {esc(evidence['confidence'])}</p>
      <p class="quiet">{esc(record['reader_warning'])}</p>
    </section>
    """
    out = SITE / "archive" / f"{record['slug']}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(record["expected_title"], body, "../"), encoding="utf-8")


def main() -> int:
    tutorial_index = load_json(RAW / "tutorial-transcript-index.json")
    evening_index = load_json(RAW / "evening-transcript-index.json")
    records: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    for item in tutorial_index + evening_index:
        page_data, ev = build_record(item)
        records.append(page_data)
        evidence.append(ev)
        render_detail(page_data, ev)
    tutorials = [record for record in records if record["type"] == "tutorial"]
    evenings = [record for record in records if record["type"] == "evening-lecture"]
    render_index(SITE / "tutorials.html", "Tutorials", "Practice sessions that make the central lecture mathematics concrete.", tutorials)
    render_index(SITE / "evening-lectures.html", "Evening Lectures", "Broader talks that connect the course machinery to waves, observation, and quantum gravity.", evenings)
    write_json(ANALYSIS / "archive" / "video-atlas.json", records)
    write_json(ANALYSIS / "archive" / "evidence-ledger.json", evidence)
    print(f"built {len(records)} archive video pages, {len(evidence)} archive evidence records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
