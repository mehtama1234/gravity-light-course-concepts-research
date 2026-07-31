#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
SITE = ROOT / "site"


SECTIONS: list[dict[str, Any]] = [
    {
        "id": "open-sets",
        "title": "Open Sets: Nearness Before Distance",
        "concept_ids": ["topology-continuity", "open-sets-neighborhood-tests", "continuous-maps-preserve-nearness"],
        "archive_slugs": ["tutorial-01"],
        "ordinary_problem": "You want to say that a path, field, or measurement changes without a jump, but you are not yet allowed to assume a ruler. General relativity cannot start with fixed distances because distance will later be decided by the metric field itself.",
        "mathematical_move": "The course replaces distance with a weaker object: a chosen list of open sets. An open set is a room test. If a point is inside, there is enough local room around it to wiggle without immediately leaving. A continuous map is then one that sends every open-set test backward to another open-set test.",
        "worked_example": "Imagine a hallway map before anyone has measured lengths. You can still mark which doorways lead into the same open room and which walls block passage. A route is continuous if small moves in the hallway do not suddenly place you in an unrelated room. No meter stick was needed; only the room test was used.",
        "calculation": [
            "Start with a point x in one space and its image f(x) in another space.",
            "Pick an allowed room U around f(x). This is the output-side nearness test.",
            "Pull that room backward: collect every input point whose image lands in U. That set is f^{-1}(U).",
            "Continuity says this pulled-back set must also be an allowed room around x. Nearby inputs then stay inside the promised output room.",
        ],
        "why_it_works": "The open-set test works because it keeps exactly the information needed for limits and continuity while throwing away measurement. Later smoothness, tangent vectors, fields, and light cones all need the promise that nearby inputs do not jump to unrelated outputs.",
        "payoff": "This is why topology is not decorative background. It is the first safeguard against using smooth formulas on a space whose basic nearness has not been checked. Every later chart, field, and light path relies on this quieter promise.",
    },
    {
        "id": "charts",
        "title": "Charts: Local Names Are Not The Space",
        "concept_ids": ["manifolds-local-flatness", "charts-atlases-coordinate-overlap", "smoothness-change-rates"],
        "archive_slugs": ["tutorial-02", "tutorial-04"],
        "ordinary_problem": "A curved space may not have one clean global naming system. You still need to calculate, so you use local coordinate charts, but a coordinate name can fail even when the space itself has no physical problem.",
        "mathematical_move": "The mathematical object is an atlas: many local charts plus overlap rules. The operation is to translate from one chart to another on the region where both charts describe the same points. A statement earns geometric status only if it survives that translation.",
        "worked_example": "Think of two street maps of the same neighborhood, one rotated and one using different block labels. A shop is not created or destroyed when you switch maps. If a route exists on one map, the overlap rule should let you find the same route on the other map.",
        "calculation": [
            "Chart X names a point by numbers (u, v), while chart Y names the same point by numbers (r, s).",
            "The overlap rule is the conversion Y after X^{-1}: first turn (u, v) back into the point, then rename it as (r, s).",
            "A derivative is trusted only when this conversion changes smoothly as (u, v) changes.",
            "If the conversion has a kink or tear, calculus is measuring the bad naming system instead of the space.",
        ],
        "why_it_works": "Charts work because they let calculus happen locally while the overlap maps police the boundary between local descriptions. Smooth transition maps are the rule that stops a derivative from measuring the chosen map instead of the underlying manifold.",
        "payoff": "This is the habit needed near horizons, poles, and singular-looking coordinates. First ask whether the chart failed; only then ask whether spacetime failed. The same habit keeps black-hole and cosmology calculations from confusing bad labels with physical trouble.",
    },
    {
        "id": "tensors",
        "title": "Tensors: The Rule Comes Before The Numbers",
        "concept_ids": ["multilinear-objects", "dual-vectors-measure-directions", "tensor-components-versus-object"],
        "archive_slugs": ["tutorial-03"],
        "ordinary_problem": "Physics needs quantities that mean the same thing to observers using different coordinates. A table of numbers is not enough, because the table changes when the basis changes.",
        "mathematical_move": "The mathematical object is a slot rule. A vector can be inserted into one kind of slot, a covector measures a vector, and a tensor has several such slots. Components are the numbers produced after choosing a basis and feeding basis vectors into those slots.",
        "worked_example": "A recipe is not the same as one grocery receipt. The receipt changes if the store sells in grams instead of ounces, but the recipe's instruction is the same. Tensor components are like the receipt; the tensor is the rule that says what gets combined with what.",
        "calculation": [
            "Let v be a direction and let a be a measuring rule that eats directions.",
            "In one basis, the measured number is the summed product a_i v^i.",
            "Change the basis. The vector numbers and covector numbers change in opposite ways.",
            "The paired sum stays the same, so the object is the rule and the table of numbers is only one display.",
        ],
        "why_it_works": "The slot rule works because it tells exactly how the numbers must change when the basis changes. That keeps the underlying object stable while allowing many coordinate displays.",
        "payoff": "Einstein's equation is not two arrays being matched. It is a statement that two tensor objects of the same type balance each other. That distinction is what lets the equation mean the same thing after a change of coordinates.",
    },
    {
        "id": "tangent-fields",
        "title": "Tangent Vectors And Fields: Direction Without An Outside Room",
        "concept_ids": ["tangent-spaces-fields", "tangent-vectors-as-derivatives", "vector-fields-as-local-instructions"],
        "archive_slugs": ["tutorial-05", "tutorial-06"],
        "ordinary_problem": "A direction at a point is usually drawn as an arrow sticking out of a surface. That picture quietly uses an outside flat space, but spacetime in the course must be understood from the inside.",
        "mathematical_move": "The course defines a tangent vector by what it does: it takes a function and returns the directional rate of change at a point. A field then becomes a smooth point-by-point choice of one allowed object over each base point, described cleanly by bundle and section language.",
        "worked_example": "If you stand in fog, you may not see a whole road, but you can test a direction by asking how fast temperature rises if you step that way. A tangent vector is that local testing action. A vector field assigns one such instruction at every point.",
        "calculation": [
            "Choose a function f on the space, such as temperature or clock reading.",
            "Choose a curve gamma(t) passing through the point at t = 0.",
            "Compute the rate d/dt f(gamma(t)) at t = 0. That rate is what the direction does to the test function.",
            "Two drawn curves count as the same tangent vector when they give the same rate for every possible test function.",
        ],
        "why_it_works": "This works because functions live on the manifold, so differentiating them does not require an outside arrow. Bundles then keep each point's allowed directions separate while still letting a field choose one direction per point.",
        "payoff": "Observers, velocities, light rays, matter fields, and gravitational variables all need this internal pointwise language before the metric can classify directions as time-like, space-like, or null.",
    },
    {
        "id": "connection",
        "title": "Connections: Comparing Nearby Directions",
        "concept_ids": ["connections-parallel-transport", "covariant-derivative-corrects-comparison", "geodesics-free-motion"],
        "archive_slugs": ["tutorial-05"],
        "ordinary_problem": "To say a direction changed from one point to the next, you first need a rule for comparing directions that live in different tangent spaces. Without that rule, change can be confused with coordinate drift.",
        "mathematical_move": "The mathematical object is a connection. Its operation is to say how to carry a direction nearby and how to correct an ordinary derivative so it becomes a covariant derivative, meaning a derivative that respects the manifold's comparison rule.",
        "worked_example": "Suppose two hikers compare compass arrows while walking over a hill. If one keeps the arrow as steady as possible along the path, the final disagreement says something about the terrain and the route, not just about a bad drawing of the hill.",
        "calculation": [
            "A vector at point p and a vector at nearby point q live in different tangent spaces.",
            "Before subtracting them, the connection tells how to carry the vector at p toward q.",
            "The covariant derivative subtracts the carried comparison from the vector found at q.",
            "The remaining difference is treated as real change, not change caused by shifting coordinate labels.",
        ],
        "why_it_works": "A connection works because it adds the missing comparison instruction. It separates real change in a vector field from the fake change caused by using a curving coordinate grid.",
        "payoff": "Free-fall motion, geodesics, curvature, and observer fields all depend on this comparison rule. It is where local direction becomes geometry rather than picture-making. Without it, the course could name changing fields but could not say which change is real.",
    },
    {
        "id": "curvature",
        "title": "Curvature: Failed Return As A Measurement",
        "concept_ids": ["curvature-geodesic-deviation", "parallel-transport-loop-test", "riemann-curvature-commutator", "ricci-curvature-volume-change"],
        "archive_slugs": ["tutorial-13"],
        "ordinary_problem": "Curvature is hard to see locally because a small enough patch can look flat. The course needs a test that detects curvature without relying on an outside view of a bent surface.",
        "mathematical_move": "The operation is to compare the result of moving around a tiny loop or changing directions in two different orders. If the transported vector or derivative result fails to return the same way, curvature has been measured internally.",
        "worked_example": "Carry an arrow around a triangular walking route on Earth while keeping it as steady as possible. When you return, the arrow may point a different way. You did not need to view Earth from space; the failed return was the test.",
        "calculation": [
            "Carry one arrow east and then north around a tiny rectangle.",
            "Carry a second copy north and then east around the same rectangle.",
            "In a flat comparison rule, the two final arrows agree.",
            "Curvature is the size and direction of the disagreement, scaled by the tiny area enclosed.",
        ],
        "why_it_works": "The loop test works because flat spaces let nearby comparisons fit together consistently. Curved spaces do not. Riemann curvature records the mismatch; Ricci curvature compresses part of that mismatch into volume-change information.",
        "payoff": "This is how the course turns gravity from a force picture into tidal geometry: nearby free-falling paths separate or squeeze because the comparison rules fail to fit globally.",
    },
    {
        "id": "metric",
        "title": "Metric: Measurement Becomes A Field",
        "concept_ids": ["metric-measurement", "metric-signature-light-cones", "proper-time-clock-reading"],
        "archive_slugs": ["tutorial-13"],
        "ordinary_problem": "Physics needs lengths, times, and light cones, but general relativity cannot treat rulers and clocks as fixed background equipment. Measurement itself must be part of the geometry, because gravity changes what clocks read and which paths light can take.",
        "mathematical_move": "The mathematical object is the metric: a rule at each point that takes directions and returns measured intervals. Its signature separates time-like, space-like, and null directions, and proper time is what a clock reads along a time-like path.",
        "worked_example": "A city map with a changing scale bar is different from a normal map. One block may count differently in different neighborhoods. The metric is that local scale and sign rule for spacetime directions.",
        "calculation": [
            "Pick two directions u and v at the same event.",
            "The metric returns one number g(u, v), which tells how those directions measure against each other.",
            "For one direction, g(u, u) says whether the direction is clock-like, space-like, or light-like.",
            "Along a clock path, proper time is found by adding the small local clock readings supplied by the metric.",
        ],
        "why_it_works": "The metric works because it turns tangent directions into measured intervals locally. Once that local measuring rule varies from point to point, gravity can change what clocks read and which directions light can follow.",
        "payoff": "Black holes, cosmological expansion, lensing, and gravitational waves are all later readings of this one idea: the measuring rule is physical. Once the metric is a field, observation becomes a way of reading geometry rather than looking through a fixed stage.",
    },
    {
        "id": "integration",
        "title": "Integration: Adding Local Facts Without Chart Dependence",
        "concept_ids": ["integration-on-manifolds", "stokes-boundary-bulk-accounting"],
        "archive_slugs": ["tutorial-12"],
        "ordinary_problem": "The course needs to add local quantities over curved regions: action terms, fluxes, source totals, and boundary contributions. The total should not change just because the region was named with different coordinates.",
        "mathematical_move": "The object is a form on an oriented region. The operation is to add it in charts while making the volume-form transformation cancel the determinant factor created by a chart change. Stokes' theorem then relates boundary accounting to bulk accounting.",
        "worked_example": "If two people use different grid paper to estimate paint needed for the same wall, the answer should agree after correcting for cell size. The determinant is the cell-size correction; the form carries the correction so the total is about the wall, not the grid.",
        "calculation": [
            "In one chart, a small cell is named by dx^1 dx^2 and the local quantity is added over those cells.",
            "Switch charts and the same physical cell may look stretched or squeezed by a determinant factor.",
            "A form changes with the compensating factor, so the product being added stays attached to the region.",
            "Stokes' theorem is the same accounting habit: what changes inside a region is matched by what crosses its boundary.",
        ],
        "why_it_works": "The cancellation works because coordinate changes stretch coordinate volume in a predictable way. Forms transform oppositely, so the product being added represents the same geometric quantity. The total is therefore attached to the region and the form, not to the grid used during the calculation.",
        "payoff": "This is why actions and conservation laws are not chart recipes. They are adding rules that survive the change of description. The same idea explains why boundary terms matter: they are part of the accounting, not algebra left over after the real work.",
    },
    {
        "id": "einstein-equation",
        "title": "Einstein Equation: Geometry And Matter Must Balance",
        "concept_ids": ["einstein-equation", "einstein-tensor-conserved-geometry", "stress-energy-matter"],
        "archive_slugs": ["evening-02"],
        "ordinary_problem": "The course needs one law connecting the geometry side and the matter side. A slogan about matter curving spacetime is not enough, because the two sides must be objects of the same kind and must obey the same conservation bookkeeping.",
        "mathematical_move": "The Einstein tensor is built from curvature and the metric so its covariant divergence vanishes. The stress-energy tensor records local matter, energy, momentum, pressure, and stress. The operation is to equate them with constants that fix units and observed strength.",
        "worked_example": "A budget cannot balance if one side lists dollars and the other lists hours. Einstein's equation works only after geometry and matter have been written as compatible local accounting objects.",
        "calculation": [
            "Build curvature from the connection and metric, then compress the useful balance information into the Einstein tensor G.",
            "The construction gives G zero covariant divergence, which means geometry has local bookkeeping built in.",
            "Matter is written as stress-energy T, whose entries record energy, momentum, pressure, and stress locally.",
            "The equation G = constant times T is possible because both sides are tensor objects with matching conservation behavior.",
        ],
        "why_it_works": "The equation works as a law because the geometry side has built-in conservation behavior matching the matter side. It is not a curve-anything-anyhow rule; it is a constrained balance between two tensor objects.",
        "payoff": "Cosmology, black holes, light bending, and waves are not separate miracles. They are different ways of solving or approximating this balance rule. The course becomes one chain because the same equation ties measurement, curvature, and matter bookkeeping together.",
    },
    {
        "id": "horizons",
        "title": "Horizons And Penrose Diagrams: Who Can Signal To Whom",
        "concept_ids": ["black-holes-horizons", "event-horizon-causal-boundary", "penrose-diagrams-compress-infinity"],
        "archive_slugs": ["tutorial-13", "tutorial-16"],
        "ordinary_problem": "A black hole is often pictured as a surface in space, but the course needs a sharper idea: a boundary in what future-directed signals can reach. Ordinary diagrams are too large to show infinity and horizons clearly.",
        "mathematical_move": "The object is causal structure: the order of possible light signals. A Penrose diagram rescales the metric to fit infinity on the page while preserving null directions and causal order, not ordinary lengths.",
        "worked_example": "A subway map does not preserve street distances, but it preserves which stops connect to which. A Penrose diagram is similar: it sacrifices measured distances so the signal connections remain readable.",
        "calculation": [
            "At each event, use the metric to draw the future light directions.",
            "Follow all future-directed light paths and ask which ones can reach far-away outside observers.",
            "If no such future light path escapes, the event is inside the black-hole region.",
            "The event horizon is the boundary of that no-escape set, not a solid surface sitting in space.",
        ],
        "why_it_works": "Light directions define causal reach. If a diagram preserves those directions, it can answer global questions about escape, trapping, infinity, and singularity reach without pretending to preserve clock times or lengths.",
        "payoff": "This is the clean way to understand horizons: not as material walls, but as causal boundaries. It also explains why Penrose diagrams are useful only when read correctly: they preserve signaling order, not ordinary distance or visual shape.",
    },
    {
        "id": "cosmology",
        "title": "Cosmology: Expansion As A Changing Measuring Rule",
        "concept_ids": ["cosmology-scale-factor", "scale-factor-expansion-history", "hubble-rate-as-change-of-scale", "redshift-as-stretched-light"],
        "archive_slugs": ["tutorial-15"],
        "ordinary_problem": "Cosmic expansion is easy to misunderstand as galaxies flying through a fixed outside space. The course instead models large-scale sameness and asks how the metric's distance rule changes over time.",
        "mathematical_move": "The central object is the scale factor. The operation is to reduce Einstein's equation using homogeneity and isotropy, then read expansion from the scale factor and its rate of change. Light redshift records that changing scale along its travel.",
        "worked_example": "Dots drawn on an inflating balloon move farther apart even if none of the dots crawls across the rubber. The useful lesson is not the balloon surface itself; it is that distances between marked points can change because the measuring rule changes.",
        "calculation": [
            "Start with a fixed reference separation between two large-scale comoving points.",
            "The model says the measured separation at time t is a(t) times that reference separation.",
            "The Hubble rate is the fractional change a'(t) / a(t), not just a raw speed through space.",
            "Light wavelength stretches with the same scale factor, so redshift records the history of that changing measure.",
        ],
        "why_it_works": "Symmetry works here by throwing away details the model declares irrelevant at large scale. That leaves a few time-dependent quantities, so geometry, matter content, redshift, and Hubble rate can be tied together.",
        "payoff": "The expansion history becomes a geometric object that observations can test, instead of a story about motion through empty background space. Redshift and Hubble rate then become readings of the model's changing scale, not just catalog facts about distant galaxies.",
    },
    {
        "id": "waves",
        "title": "Gravitational Waves: Tiny Metric Change As A Measured Length Change",
        "concept_ids": ["perturbations-waves", "linearized-equations-small-disturbances", "quadrupole-source-changing-shape", "strain-relative-length-change", "interferometer-light-as-ruler"],
        "archive_slugs": ["evening-01"],
        "ordinary_problem": "A gravitational wave should not be explained as sound in a medium or as a force pushing detector parts around. The course needs to connect a small change in spacetime geometry to the thing a detector actually measures.",
        "mathematical_move": "The mathematical move is to write the metric as a background part plus a small disturbance, keep the leading terms, and track how that disturbance changes relative separation. Strain is the measured fractional change in length.",
        "worked_example": "If two marks on a stretchy ruler move from 100 units apart to 100.001 units apart, the important number is the fractional change, not an absolute shove. An interferometer uses light to compare such tiny relative changes along its arms.",
        "calculation": [
            "Write the metric as a steady background plus a small change h.",
            "Keep only terms that are first order in h, because the wave is tiny compared with the background.",
            "A detector arm changes by a fraction called strain: strain = change in length divided by original length.",
            "The interferometer compares light phases in two arms, turning that tiny metric change into a readable signal.",
        ],
        "why_it_works": "The approximation works because weak waves are small enough that the field equations can be linearized. The detector reading works because light compares path lengths, so a metric disturbance becomes a phase difference.",
        "payoff": "This is where the course closes the loop from abstract metric geometry to observation: the same measuring rule that defines light cones can tremble, travel, and be detected.",
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def page(title: str, body: str) -> str:
    nav = """
    <nav class="topbar">
      <a href="index.html">Overview</a>
      <a href="lectures.html">Lectures</a>
      <a href="tutorials.html">Tutorials</a>
      <a href="evening-lectures.html">Evening Lectures</a>
      <a href="concepts.html">Concepts</a>
      <a href="families.html">Families</a>
      <a href="themes.html">Themes</a>
      <a href="learning-path.html">Learning Path</a>
      <a href="what-breaks.html">What Breaks</a>
      <a href="the-math-why.html">Math Why</a>
      <a href="evidence.html">Evidence</a>
      <a href="archive-evidence.html">Archive Evidence</a>
    </nav>
    """
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
{nav}
<main>
{body}
</main>
</body>
</html>
"""


def concept_links(ids: list[str], concepts_by_id: dict[str, dict[str, Any]]) -> str:
    return " ".join(
        f'<a class="chip" href="concepts/{esc(concept_id)}.html">{esc(concepts_by_id[concept_id]["name"])}</a>'
        for concept_id in ids
        if concept_id in concepts_by_id
    )


def archive_links(slugs: list[str], archive_by_slug: dict[str, dict[str, Any]]) -> str:
    return " ".join(
        f'<a class="chip" href="archive/{esc(slug)}.html">{esc(archive_by_slug[slug]["expected_title"])}</a>'
        for slug in slugs
        if slug in archive_by_slug
    )


def render() -> None:
    concepts = load_json(ANALYSIS / "concepts" / "concept-atlas.json")
    archive_videos = load_json(ANALYSIS / "archive" / "video-atlas.json")
    concepts_by_id = {concept["id"]: concept for concept in concepts}
    archive_by_slug = {video["slug"]: video for video in archive_videos}
    blocks = []
    for index, section in enumerate(SECTIONS, start=1):
        calculation_steps = "".join(f"<li>{esc(step)}</li>" for step in section["calculation"])
        blocks.append(
            f"""
            <article class="family-block" id="{esc(section['id'])}">
              <p class="eyebrow">Move {index:02d}</p>
              <h2>{esc(section['title'])}</h2>
              <p><strong>What is hard:</strong> {esc(section['ordinary_problem'])}</p>
              <p><strong>The mathematical move:</strong> {esc(section['mathematical_move'])}</p>
              <div class="worked">
                <div class="wl">Worked example</div>
                <p>{esc(section['worked_example'])}</p>
              </div>
              <div class="worked">
                <div class="wl">Step-by-step calculation</div>
                <ol>{calculation_steps}</ol>
              </div>
              <p><strong>Why it works:</strong> {esc(section['why_it_works'])}</p>
              <p><strong>Where it pays off:</strong> {esc(section['payoff'])}</p>
              <p>{concept_links(section['concept_ids'], concepts_by_id)}</p>
              <p>{archive_links(section['archive_slugs'], archive_by_slug)}</p>
            </article>
            """
        )
    body = f"""
    <section class="intro">
      <p class="eyebrow">Gravity and Light mathematical companion</p>
      <h1>The Mathematical Why</h1>
      <p class="lede">The course has one repeated demand: turn a physical question into an object and an operation that survive a change of description. This page takes that demand slowly, with plain worked examples before the formal names.</p>
    </section>
    <section class="deep-read">
      <h2>The One Move</h2>
      <p>Gravity and light look hard because the thing being studied is also the thing used to measure. The course therefore keeps making the same move: name the object, name the operation allowed on it, test the move in a small calculation, then ask what would break if that operation depended on a coordinate choice, a drawing, or an outside ruler.</p>
    </section>
    {''.join(blocks)}
    """
    write_json(ANALYSIS / "integration" / "math-why.json", SECTIONS)
    (SITE / "the-math-why.html").write_text(page("The Mathematical Why", body), encoding="utf-8")
    print(f"built math why page with {len(SECTIONS)} sections")


def main() -> int:
    render()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
