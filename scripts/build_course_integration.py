#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"


PRESSURE_TESTS = {
    "tutorial-01": {
        "pressure_test": "Use open sets as the test of nearness before any ruler has been introduced. The tutorial pressure is to stop asking for distance and instead ask whether a proposed region gives each point enough local room, then whether a map sends open-set tests back to open-set tests.",
        "why_it_changes_concept": "This changes the concept page from a definition of topology into a habit of restraint. The reader has to earn every later word about smoothness, fields, and light cones by first checking that the weaker idea of nearness is stable.",
    },
    "tutorial-02": {
        "pressure_test": "Treat charts as local names, then test whether the names agree where patches overlap. The tutorial pressure is to keep the point and the coordinate label separate, especially when a statement appears true in one chart and must be carried through the atlas.",
        "why_it_changes_concept": "This turns manifold language into a guard against false singularities. The concept is no longer just local flatness; it is the discipline of asking whether a claimed geometric fact survives a change in local naming system.",
    },
    "tutorial-03": {
        "pressure_test": "Feed basis vectors into a tensor and watch components appear as a result of that choice. The tutorial pressure is to keep the rule with slots separate from the table of numbers produced after a basis has been chosen.",
        "why_it_changes_concept": "This makes tensor thinking practical. The reader has to see why Einstein's equation cannot be read as matching two arrays; it is matching two coordinate-independent measuring rules whose component displays change with the basis.",
    },
    "tutorial-04": {
        "pressure_test": "Construct the transition map between overlapping charts and ask whether it is smooth enough for calculus to be legal. The tutorial pressure is to make derivatives pass through chart changes instead of trusting the first coordinate picture that looks differentiable.",
        "why_it_changes_concept": "This turns smoothness into a permission rule. The concept page can now explain why later derivatives, connections, and curvature need chart compatibility before they can claim to describe spacetime rather than one drawing of spacetime.",
    },
    "tutorial-05": {
        "pressure_test": "Use a tangent vector by letting it act on functions. The tutorial pressure is to stop relying on a drawn arrow outside the manifold and instead ask what directional rate the vector assigns to each local function.",
        "why_it_changes_concept": "This makes tangent space internal. Motion, light direction, and observer velocity can now be explained without borrowing a surrounding flat space, because the direction is known by what it does at the point. That also prepares the later field picture: a field is built from these local actions point by point.",
    },
    "tutorial-06": {
        "pressure_test": "Build a field through bundle language: base, total space, projection, fiber, and section. The tutorial pressure is to make a field choose one allowed object above each base point, then check that projecting it back returns the point it came from.",
        "why_it_changes_concept": "This changes fields from a vague substance picture into pointwise assignment with bookkeeping. It explains why vector fields, tensor fields, matter fields, and observer fields all need a bundle-level home before they can be differentiated or compared.",
    },
    "tutorial-11": {
        "pressure_test": "Push the metric along a flow and ask whether the pulled-back metric is the same. The tutorial pressure is to prove sameness by preservation of structure, not by the visual impression that a diagram looks unchanged.",
        "why_it_changes_concept": "This makes symmetry responsible for conservation. The concept page can connect Killing fields and special spacetimes to what is actually preserved, which is why conserved quantities appear only when the geometry has the right kind of sameness.",
    },
    "tutorial-12": {
        "pressure_test": "Change charts inside an integral and track the determinant factor that appears. The tutorial pressure is to make the volume-form transformation cancel the chart-change factor so the total does not depend on the coordinates used to add it.",
        "why_it_changes_concept": "This makes integration a coordinate-independence test. Actions, fluxes, source totals, and boundary terms become physical accounting only after the adding rule gives the same answer across compatible charts and orientations. The concept is no longer about adding formulas; it is about making local additions survive a change of description.",
    },
    "tutorial-13": {
        "pressure_test": "Read Schwarzschild geodesics from the metric instead of from an outside force picture. The tutorial pressure is to decide which features come from coordinates, which come from causal reach, and which paths are permitted by the geometry.",
        "why_it_changes_concept": "This makes black-hole language less pictorial and more causal. Horizons and singular-looking metric components have to be tested through allowed light and particle paths, not through panic at one coordinate expression. The concept page can then ask what the metric permits before deciding what the black-hole surface means.",
    },
    "tutorial-15": {
        "pressure_test": "Let the scale factor carry the changing distance relations of the model. The tutorial pressure is to avoid imagining galaxies flying through an outside container and instead read expansion from a reduced geometry and matter equation.",
        "why_it_changes_concept": "This makes cosmology a spacetime statement. Redshift, Hubble rate, and matter content become connected through the changing scale factor, so observation is tied to geometry rather than to an ordinary explosion picture. The tutorial makes the concept answer a concrete model question: what changes when the scale changes?",
    },
    "tutorial-16": {
        "pressure_test": "Construct a Penrose diagram by choosing what the drawing preserves. The tutorial pressure is to keep light directions and causal order while giving up ordinary lengths, clock durations, and visual shape. The reader must ask what the diagram is allowed to claim before using it to reason about horizons or infinity.",
        "why_it_changes_concept": "This makes global causal structure readable. The concept page can explain why a diagram is not a map of distances; it is a compact account of who can signal to whom, including horizons and infinities.",
    },
    "evening-01": {
        "pressure_test": "Connect a small change in metric geometry to a measured change in relative length. The evening-lecture pressure is to explain gravitational waves without turning them into sound in a medium or a force pushing detector parts around.",
        "why_it_changes_concept": "This ties perturbation theory to evidence. The reader sees why interferometer strain is not an instrument detail bolted onto the end of the course; it is the measurable face of the metric idea built earlier.",
    },
    "evening-02": {
        "pressure_test": "Put classical geometry and quantum matter on opposite sides of the same proposed equation and ask what kind of object each side is. The evening-lecture pressure is to notice that a definite spacetime source is no longer straightforward when matter is treated quantum mechanically.",
        "why_it_changes_concept": "This makes quantum gravity a bookkeeping crisis, not a fashionable topic. The concept pages on constraints, source terms, and canonical formulation now point toward the place where classical spacetime stops being obviously self-contained. The reader sees why a source term is easy to write classically and hard to justify quantum mechanically.",
    },
}


LEARNING_PATH = [
    {
        "id": "nearness-before-distance",
        "title": "Earn Nearness Before Measuring",
        "plain_goal": "Start with the weakest structure that still lets a physical statement vary without jumping, before the course has earned any right to speak about distance, clocks, or rulers.",
        "concept_ids": ["topology-continuity", "open-sets-neighborhood-tests", "continuous-maps-preserve-nearness"],
        "archive_slugs": ["tutorial-01"],
        "reader_task": "Ask whether a region is locally roomy around each point and whether a map preserves that kind of room. Do not use meters yet.",
        "payoff": "This is the base layer for every later statement about smooth fields, light paths, and limits. If nearness is not stable, later derivatives are pretending.",
    },
    {
        "id": "local-names-without-mistaking-the-name",
        "title": "Use Coordinates Without Mistaking Them For Space",
        "plain_goal": "Learn to describe one space with many local naming systems while keeping the space separate from the names.",
        "concept_ids": ["manifolds-local-flatness", "charts-atlases-coordinate-overlap", "smoothness-change-rates"],
        "archive_slugs": ["tutorial-02", "tutorial-04"],
        "reader_task": "Move statements through overlap maps and transition maps. A claim is allowed to be geometric only if it survives the change of local chart.",
        "payoff": "This prepares the reader for horizons, singular-looking coordinates, and covariant derivatives. A bad chart should not be mistaken for bad spacetime.",
    },
    {
        "id": "slot-aware-quantities",
        "title": "Separate Objects From Their Component Displays",
        "plain_goal": "Learn why vectors, covectors, and tensors have jobs before they have coordinate lists, so the reader can tell an object from one chosen display of it.",
        "concept_ids": ["multilinear-objects", "dual-vectors-measure-directions", "tensor-components-versus-object"],
        "archive_slugs": ["tutorial-03"],
        "reader_task": "Feed basis vectors into tensor slots and watch component numbers appear. Then change the basis and keep track of what did not change.",
        "payoff": "This is what lets the metric, stress-energy, curvature, and Einstein tensor be read as physical measuring rules rather than arrays of symbols.",
    },
    {
        "id": "directions-and-fields",
        "title": "Make Direction And Field Internal",
        "plain_goal": "Build directions and fields without borrowing arrows from a surrounding flat room, then make point-by-point assignments precise enough to carry physical variables.",
        "concept_ids": ["tangent-spaces-fields", "tangent-vectors-as-derivatives", "vector-fields-as-local-instructions"],
        "archive_slugs": ["tutorial-05", "tutorial-06"],
        "reader_task": "Use a tangent vector by its action on functions, then build a field as a section choosing one allowed object over each point.",
        "payoff": "Observers, light rays, matter fields, and gravitational variables all depend on this point-by-point structure before the metric says what they measure.",
    },
    {
        "id": "compare-add-and-preserve",
        "title": "Compare, Add, And Preserve Geometric Facts",
        "plain_goal": "Learn the operations that make local geometry become physical accounting: comparison from point to point, adding over regions, and preserving structure under motion.",
        "concept_ids": ["connections-parallel-transport", "covariant-derivative-corrects-comparison", "symmetry-conservation", "killing-fields-symmetry-directions", "integration-on-manifolds", "stokes-boundary-bulk-accounting"],
        "archive_slugs": ["tutorial-11", "tutorial-12"],
        "reader_task": "Ask how to compare nearby directions, what a flow preserves, and how an integral stays the same after changing charts.",
        "payoff": "This is where conservation laws, actions, fluxes, and boundary terms stop being algebra tricks and become coordinate-independent statements.",
    },
    {
        "id": "matter-geometry-and-allowed-data",
        "title": "Couple Geometry To Matter Without Losing The Bookkeeping",
        "plain_goal": "Understand why the source side, geometry side, and initial data constraints must fit together before Einstein's equation can be treated as a physical law.",
        "concept_ids": ["stress-energy-matter", "einstein-equation", "einstein-tensor-conserved-geometry", "canonical-formulation", "initial-data-constraints"],
        "archive_slugs": ["evening-02"],
        "reader_task": "Ask what kind of object each side of the field equation is, and what becomes difficult when the source is quantum rather than classical.",
        "payoff": "This makes Einstein's equation a coupled accounting rule and shows why quantum gravity is a pressure point in the theory, not an optional epilogue.",
    },
    {
        "id": "causal-worlds-and-observation",
        "title": "Read Black Holes, Cosmology, And Waves As Geometry You Can Observe",
        "plain_goal": "Carry the foundations into the places where geometry becomes causal reach, expansion history, and measured signal rather than remaining abstract mathematical preparation.",
        "concept_ids": ["cosmology-scale-factor", "scale-factor-expansion-history", "hubble-rate-as-change-of-scale", "black-holes-horizons", "event-horizon-causal-boundary", "penrose-diagrams-compress-infinity", "perturbations-waves", "quadrupole-source-changing-shape", "strain-relative-length-change", "interferometer-light-as-ruler"],
        "archive_slugs": ["tutorial-13", "tutorial-15", "tutorial-16", "evening-01"],
        "reader_task": "Use metrics and diagrams to ask what light can reach, use the scale factor to read expansion, and use strain to connect metric disturbance to measurement.",
        "payoff": "This is the course becoming physics: horizons, redshift, waves, and detectors are no longer separate stories but consequences of the same geometric bookkeeping.",
    },
]


DEPENDENCY_MAP = [
    {
        "id": "skip-topology",
        "concept_id": "topology-continuity",
        "depends_on": [],
        "breaks": "Continuity becomes a slogan. Later fields can jump, limits can be chart accidents, and smooth-looking formulas can hide discontinuities.",
        "repair": "Return to open sets and inverse-image tests before speaking about smoothness, paths, or field equations.",
    },
    {
        "id": "skip-chart-discipline",
        "concept_id": "charts-atlases-coordinate-overlap",
        "depends_on": ["topology-continuity"],
        "breaks": "Coordinates become the space. Horizons, poles, and chart edges are misread as physical edges or singularities.",
        "repair": "Check overlap maps and ask whether the geometric claim survives changing charts before treating a coordinate feature as a physical feature of spacetime.",
    },
    {
        "id": "skip-smoothness",
        "concept_id": "smoothness-change-rates",
        "depends_on": ["charts-atlases-coordinate-overlap"],
        "breaks": "Derivatives measure the chosen map instead of the manifold. Connections, curvature, and geodesics lose their right to be geometric.",
        "repair": "Make transition maps smooth enough for calculus to pass from one chart to another, then allow derivatives only when that compatibility has been checked.",
    },
    {
        "id": "skip-tensor-slots",
        "concept_id": "tensor-components-versus-object",
        "depends_on": ["multilinear-objects"],
        "breaks": "Einstein's equation becomes array matching. A coordinate artifact can be mistaken for a physical tensor statement.",
        "repair": "Track the slot rule first, then treat components as one chosen display of that rule whose numbers may change when the basis changes.",
    },
    {
        "id": "skip-tangent-fields",
        "concept_id": "vector-fields-as-local-instructions",
        "depends_on": ["tangent-vectors-as-derivatives"],
        "breaks": "Velocity, observer fields, and matter fields are imported from flat-space intuition instead of built on the manifold.",
        "repair": "Define tangent vectors by what they do to functions, then define fields as smooth pointwise assignments.",
    },
    {
        "id": "skip-comparison",
        "concept_id": "covariant-derivative-corrects-comparison",
        "depends_on": ["vector-fields-as-local-instructions"],
        "breaks": "Change from place to place is confused with coordinate drift. Curvature and free motion become ordinary derivative mistakes.",
        "repair": "Use a connection to specify how nearby directions are compared before asking what changes, so change is not confused with coordinate drift.",
    },
    {
        "id": "skip-integration",
        "concept_id": "integration-on-manifolds",
        "depends_on": ["smoothness-change-rates"],
        "breaks": "Actions, fluxes, and source totals depend on the chart used to add them. Boundary terms look like algebra scraps.",
        "repair": "Use forms, orientation, and chart-change cancellation so adding local facts gives one geometric answer rather than a chart-dependent total.",
    },
    {
        "id": "skip-symmetry",
        "concept_id": "killing-fields-symmetry-directions",
        "depends_on": ["covariant-derivative-corrects-comparison"],
        "breaks": "Conserved quantities look arbitrary. Energy and angular momentum are assumed even when the spacetime has no structure to support them.",
        "repair": "Check what a flow preserves before claiming a conservation law, and only then attach conserved quantities to that spacetime.",
    },
    {
        "id": "skip-source-accounting",
        "concept_id": "stress-energy-matter",
        "depends_on": ["tensor-components-versus-object", "integration-on-manifolds"],
        "breaks": "Matter is reduced to mass alone, and Einstein's equation loses the pressure, momentum, and stress information that actually gravitates.",
        "repair": "Treat stress-energy as the local accounting object for what matter contributes to geometry, including pressure, momentum flow, and stress.",
    },
    {
        "id": "skip-causal-structure",
        "concept_id": "event-horizon-causal-boundary",
        "depends_on": ["metric-signature-light-cones", "geodesics-free-motion"],
        "breaks": "Black holes become pictures of dark surfaces rather than claims about what signals can reach, and horizons are mistaken for material walls.",
        "repair": "Read horizons through future-directed light paths and global causal reach, then use Penrose diagrams only for what they preserve.",
    },
    {
        "id": "skip-scale-factor",
        "concept_id": "scale-factor-expansion-history",
        "depends_on": ["metric-measurement", "stress-energy-matter"],
        "breaks": "Cosmic expansion is misread as motion through a fixed outside space. Redshift and Hubble rate lose their geometric meaning.",
        "repair": "Use the scale factor as the model's changing distance relation and connect it to matter content through the reduced equations.",
    },
    {
        "id": "skip-wave-measurement",
        "concept_id": "strain-relative-length-change",
        "depends_on": ["perturbations-waves", "interferometer-light-as-ruler"],
        "breaks": "Gravitational waves become metaphorical ripples with no clear measured quantity, and detectors look disconnected from the earlier geometry.",
        "repair": "Connect the small metric disturbance to relative length change read by light in an interferometer, so the measured strain has a geometric meaning.",
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    archive_videos = load_json(ANALYSIS / "archive" / "video-atlas.json")
    concept_atlas = load_json(ANALYSIS / "concepts" / "concept-atlas.json")
    concept_ids = {concept["id"] for concept in concept_atlas}
    entries: list[dict[str, Any]] = []

    for video in archive_videos:
        authored = PRESSURE_TESTS[video["slug"]]
        for concept_id in video["concept_ids"]:
            if concept_id not in concept_ids:
                raise ValueError(f"archive video {video['slug']} points to missing concept {concept_id}")
            entries.append(
                {
                    "concept_id": concept_id,
                    "archive_slug": video["slug"],
                    "video_title": video["expected_title"],
                    "video_type": video["type"],
                    "archive_url": f"archive/{video['slug']}.html",
                    "evidence_id": video["evidence_id"],
                    "evidence_status": video["evidence_status"],
                    "pressure_test": authored["pressure_test"],
                    "why_it_changes_concept": authored["why_it_changes_concept"],
                    "source_span_read": video["source_span_read"],
                }
            )

    write_json(ANALYSIS / "integration" / "concept-archive-integration.json", entries)
    write_json(ANALYSIS / "integration" / "learning-path.json", LEARNING_PATH)
    write_json(ANALYSIS / "integration" / "dependency-map.json", DEPENDENCY_MAP)
    print(f"built {len(entries)} concept/archive integration records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
