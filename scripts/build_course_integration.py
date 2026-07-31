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
    print(f"built {len(entries)} concept/archive integration records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
