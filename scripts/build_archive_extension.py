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

MANUAL_ARCHIVE_NOTES = {
    "C4jJe_b0KMs": {
        "path": "raw-material/manual-notes/tutorial-06-fields.md",
        "timestamp": "00:00:30 - 00:03:47",
        "start_seconds": 30,
        "snippet": "The tutorial checks the definition of a bundle: it needs base space, total space, and a projection map. Fibers are preimages under that projection, and a section maps from the base into the total space so projection after section gives the identity on the base.",
    },
    "iwbJvfFNRh8": {
        "path": "raw-material/manual-notes/tutorial-12-integration.md",
        "timestamp": "00:00:31 - 00:03:52",
        "start_seconds": 31,
        "snippet": "The tutorial explains why integration on a manifold requires orientability. An integral defined through one chart must agree after changing charts; the chart-change formula introduces a determinant factor, and the volume-form transformation must cancel it.",
    },
}


SOURCE_SPAN_OVERRIDES = {
    "_XkhZQ-hNLs": {
        "timestamp": "00:01:38.040",
        "start_seconds": 98,
        "snippet": "At 00:01:38, the tutorial identifies topology as extra structure on a set and says it decides which subsets count as open.",
    },
    "ghfEQ3u_B6g": {
        "timestamp": "00:05:25.220",
        "start_seconds": 325,
        "snippet": "At 00:05:25, the tutorial checks continuity through charts in a maximal atlas, tying the manifold definition to agreement between chart descriptions.",
    },
    "5oeWX3NUhMA": {
        "timestamp": "00:04:07.800",
        "start_seconds": 247,
        "snippet": "At 00:04:07, tensor components are explained as what appears after plugging chosen basis vectors into the tensor.",
    },
    "FXPdKxOq1KA": {
        "timestamp": "00:09:07.519",
        "start_seconds": 547,
        "snippet": "At 00:09:07, the exercise asks students to construct the chart transition map, the test for whether local coordinates fit together smoothly.",
    },
    "mACNdkRdHEA": {
        "timestamp": "00:03:05.800",
        "start_seconds": 185,
        "snippet": "At 00:03:05, a tangent vector is described by its action: it maps a function on the manifold to a real number.",
    },
    "bYfvT-ky1lU": {
        "timestamp": "00:07:59.539",
        "start_seconds": 479,
        "snippet": "At 00:07:59, the tutorial checks when a Lie algebra gives a symmetry of a metric tensor field through pullback along the flow.",
    },
    "KQe2sqGIzTg": {
        "timestamp": "00:00:31.439",
        "start_seconds": 31,
        "snippet": "At 00:00:31, the exercise sets up geodesics in Schwarzschild spacetime by considering a manifold equipped with the Schwarzschild metric.",
    },
    "HuQ79CWcDac": {
        "timestamp": "00:35:23.560",
        "start_seconds": 2123,
        "snippet": "At 00:35:23, the tutorial discusses the scale factor and the condition that it should not decrease in the cosmological model under study.",
    },
    "w85vePX8TsA": {
        "timestamp": "00:14:14.559",
        "start_seconds": 854,
        "snippet": "At 00:14:14, the tutorial begins constructing a Penrose diagram for a radiation-filled universe as a worked causal-structure exercise.",
    },
    "udmiKlH7-AA": {
        "timestamp": "00:40:02.480",
        "start_seconds": 2402,
        "snippet": "At 00:40:02, the lecture says gravitational waves change distances between points in space and laser interferometers measure the tiny length changes.",
    },
    "bxzTD7usU1s": {
        "timestamp": "01:12:46.640",
        "start_seconds": 4366,
        "snippet": "At 01:12:46, the lecture introduces semiclassical Einstein equations: Einstein geometry on the left, quantum-matter expectation value on the right.",
    },
}


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


AUTHORED_SECTIONS: dict[str, dict[str, str]] = {
    "_XkhZQ-hNLs": {
        "first_principles_role": "This tutorial is where topology stops being a word for shape and becomes a working test. The central lecture says the course must talk about nearness before it has earned distance. The tutorial makes that exact move concrete: instead of asking how many meters apart two points are, it asks which regions count as roomy around a point and which maps preserve that room. That is the first defense against smuggling a ruler into a theory where the ruler will later be part of the gravitational field.",
        "mathematical_detail_plain": "The important object is not a picture of a surface. It is a collection of open sets. An open set is a local permission test: if a point is inside, there is still some room to move while staying inside. A continuous map is then checked by pulling an open test region backward and seeing whether it remains open. This is plain but strict: the operation does not need coordinates, lengths, or an outside drawing.",
        "course_connection": "This tutorial supports the first lectures because every later derivative, field, path, and light cone assumes that nearby inputs do not jump to unrelated outputs. If topology is treated as vague background, smoothness later becomes unearned. The tutorial gives students the small checks that keep later spacetime claims honest.",
    },
    "ghfEQ3u_B6g": {
        "first_principles_role": "This tutorial works on the problem of describing one space with many local naming systems. A manifold is easy to say and hard to use responsibly: a chart gives numbers to a patch, but the chart is not the space. The tutorial makes students compare overlapping charts so they can see which facts survive the change of names.",
        "mathematical_detail_plain": "The object to track is the overlap map. When two charts cover the same points, the overlap map tells how one set of coordinate labels is translated into the other. The operation is to move a point or expression through that translation and check that the statement still means the same thing. This is why a manifold can be studied with coordinates without becoming a coordinate grid.",
        "course_connection": "This matters later at horizons, poles, and other places where one coordinate system misbehaves. Without this tutorial's discipline, a student can mistake a broken chart for a broken spacetime. The tutorial is a rehearsal for reading black-hole coordinates without panic: first ask which patch is failing, then ask whether the underlying geometric claim survives in another patch.",
    },
    "5oeWX3NUhMA": {
        "first_principles_role": "This tutorial is the course's antidote to treating every indexed expression as a fancy matrix. Gravity needs objects that point, objects that measure, and objects that take several inputs at once. The tutorial makes those jobs separate before the metric, curvature, and stress-energy tensor arrive.",
        "mathematical_detail_plain": "The central object is a multilinear rule with slots. A vector can be inserted into one kind of slot; a covector is a rule that eats a vector and returns a number; a tensor has several such places. Components are only the numbers you see after choosing a basis. The operation is to feed inputs into the correct slots, change the basis, and verify that the underlying rule did not change.",
        "course_connection": "Einstein's equation cannot be understood as two arrays being set equal. It equates two geometric measuring rules of the same type. This tutorial gives the slot discipline needed before that equation can be read as physics rather than symbol matching. It also prepares the distinction between a tensor and its component display, which later prevents coordinate artifacts from being mistaken for physical facts.",
    },
    "FXPdKxOq1KA": {
        "first_principles_role": "This tutorial turns differentiability into a permission rule for calculus on a curved space. The central lecture introduces smooth manifolds; the tutorial asks what must be checked before derivatives are allowed to mean something independent of one chosen chart. The everyday issue is simple: if two maps name the same region, a legal change-rate calculation should not depend on which map happened to be used first.",
        "mathematical_detail_plain": "The object is the smooth structure: a compatible set of charts whose overlap maps are differentiable enough. The operation is to compute a change rate in one chart and then pass through another chart to see whether that computation remains legal. Smoothness is not visual roundness; it is the rule that protects derivatives from depending on the map used.",
        "course_connection": "Connections, curvature, field equations, and geodesics all use derivatives. If smoothness is hand-waved, every one of those later operations can silently depend on a bad coordinate choice. This tutorial is where calculus earns the right to enter the course. It makes the later covariant derivative feel less mysterious because students have already seen why ordinary chart derivatives need compatibility rules.",
    },
    "mACNdkRdHEA": {
        "first_principles_role": "This tutorial handles the local meaning of direction. A tangent vector is often drawn as a little arrow, but the course cannot depend on an outside space where that arrow is drawn. The tutorial pushes the internal meaning: a direction at a point is known by what it does to functions.",
        "mathematical_detail_plain": "The object is the tangent space at a point, together with curves through the point and derivations acting on functions. The operation is to apply a tangent vector to a function and read the directional rate of change. That turns a direction from a picture into an action.",
        "course_connection": "Observers, particle velocities, light directions, vector fields, and geodesics all start here. Without this tutorial, later claims about motion in spacetime keep borrowing flat-space arrows that the theory never promised. The tutorial also prepares the field viewpoint: once a direction at one point is understood internally, a vector field becomes a smooth assignment of such directions across a region.",
    },
    "C4jJe_b0KMs": {
        "first_principles_role": "This tutorial is about how local objects are collected over a whole manifold. It uses bundles, fibers, projections, and sections to make the word field precise. The key move is that a field is not a mist spread through space; it is a disciplined choice of one allowed object over each base point.",
        "mathematical_detail_plain": "The manual notes catch the important checks. A bundle needs a base space, a total space, and a projection from total space down to base. The fiber over a point is the preimage of that point. A section goes the other way, choosing one element upstairs over each point downstairs, with projection after section returning the original base point. The tangent bundle is built as a disjoint union of tangent spaces, not by intersecting them.",
        "course_connection": "This is the machinery behind vector fields, tensor fields, matter fields, observer fields, and later gravitational variables. Without it, a field can sound like a physical substance rather than an assignment with a precise pointwise job. The tutorial is also the bridge from tangent spaces to sections: once the total bundle is built, a field is a rule that chooses one permitted element over each point.",
    },
    "bYfvT-ky1lU": {
        "first_principles_role": "This tutorial makes symmetry operational. A symmetry is not prettiness in a diagram. It is a transformation that changes the description while preserving the structure under study. The tutorial practices the checks that turn sameness into calculation. The everyday question is whether a move has changed the thing itself or only moved us to an equivalent description of the same structure.",
        "mathematical_detail_plain": "The object is a map or flow acting on the space and on the structures placed on it. The operation is to ask what is unchanged by that action. For metric geometry, that means checking whether the metric is preserved along the relevant transformation or vector-field flow.",
        "course_connection": "Conserved quantities in special spacetimes are not magic labels. They come from preserved structure. This tutorial prepares the later use of Killing fields, black-hole symmetries, and simplified cosmological models. It also explains why a spacetime can lack a useful global energy unless it has the right kind of sameness to define one.",
    },
    "iwbJvfFNRh8": {
        "first_principles_role": "This tutorial asks how to add local data on a manifold without letting the answer depend on the chart used to do the addition. That is the ordinary problem behind manifold integration: the same region should not acquire a different total merely because it was named with different coordinates.",
        "mathematical_detail_plain": "The manual notes identify the essential calculation. If an integral is defined in one chart and then the chart is changed, the ordinary change-of-variables formula introduces a determinant factor. The volume-form term must transform so that this factor is cancelled in the right way. Orientability controls the sign consistency needed for this to work across charts.",
        "course_connection": "Actions, fluxes, conserved currents, matter totals, and Stokes-type arguments all depend on this. Without the tutorial's chart-independence check, later integral formulas are just coordinate recipes pretending to be geometry. This matters for gravity because the action and source integrals must add local quantities over spacetime regions without changing when the region is described by another chart.",
    },
    "KQe2sqGIzTg": {
        "first_principles_role": "This tutorial uses Schwarzschild spacetime to test whether students can separate geometry from coordinates. The ordinary problem is that a formula can look singular even when the spacetime fact being described is not the same kind of singularity. The tutorial asks students to slow down and decide whether a bad-looking expression marks a true geometric obstruction or only a poor way of naming events.",
        "mathematical_detail_plain": "The object is the Schwarzschild metric and the causal structure it defines. The operation is to examine radial behavior, horizon behavior, and coordinate changes while keeping null directions and physical invariants in view. The horizon is not treated as a material wall; it is read through what future-directed light can do.",
        "course_connection": "This tutorial prepares the black-hole and Penrose-diagram lectures. It forces the earlier manifold and metric lessons to work together: coordinates are useful displays, but causal reach is the physical question. That is why the horizon cannot be understood by staring only at one metric component; one must track allowed light directions and whether signals can reach outside observers.",
    },
    "HuQ79CWcDac": {
        "first_principles_role": "This tutorial turns cosmology from a story about galaxies flying away into a calculation about changing geometry. The simplified universe model is not pretending that every local detail is tracked. It asks what follows when large-scale sameness lets the field equation collapse to a few evolving quantities.",
        "mathematical_detail_plain": "The object is the scale factor inside a homogeneous and isotropic metric ansatz. The operation is to use symmetry to reduce Einstein's equation and then read the expansion history from the scale factor and its rate of change. Matter content enters by changing the equation for that scale.",
        "course_connection": "This tutorial links the metric, matter, redshift, and observation. Without it, cosmic expansion is easily misread as ordinary motion through a fixed container instead of changing distance relations within spacetime. It also prepares the later observational story: redshift and distance data become statements about the scale factor only after the geometric model has been set up carefully.",
    },
    "w85vePX8TsA": {
        "first_principles_role": "This tutorial is about drawing spacetime without lying about what the drawing preserves. A normal diagram cannot show infinity and horizon structure cleanly at the same time. Penrose diagrams solve a narrow problem: keep causal directions visible while compressing unreachable distances into a finite page.",
        "mathematical_detail_plain": "The object is a conformal diagram. The operation is to rescale the metric so null directions and causal order survive, while ordinary distances do not. That means the diagram is not a map of lengths. It is a map of who can signal to whom.",
        "course_connection": "This supports black holes and cosmology because many of their important claims are global. Whether light reaches infinity, hits a singularity, or remains trapped is not answered by staring at one coordinate patch. The tutorial makes clear what the diagram promises: it preserves the causal skeleton, not the measured lengths, clock times, or visual shape of spacetime.",
    },
    "udmiKlH7-AA": {
        "first_principles_role": "This evening lecture widens the gravitational-wave story from formal perturbation equations to the physical question of what a wave is and how it becomes evidence. The point is not to decorate the central lectures with a public talk. It connects the mathematical object, a small change in metric geometry, to the ordinary act of measuring changing separations.",
        "mathematical_detail_plain": "The object is a propagating disturbance of spacetime geometry sourced by changing mass-energy motion. The operation is to follow that disturbance from source behavior to detector response, where the measured quantity is relative length change rather than a push on a material medium. In plain terms, the detector is not hearing space like air; it is comparing separations with light.",
        "course_connection": "This ties together perturbation theory, quadrupole sources, light as a measuring device, and interferometer strain. Without this bridge, the final detector lectures can feel like instrument facts disconnected from the geometry built earlier. The evening lecture gives the big picture in which the same metric idea that made light cones also becomes the thing whose tiny change is measured.",
    },
    "bxzTD7usU1s": {
        "first_principles_role": "This evening lecture sits at the pressure point between the course's classical geometry and quantum matter. The ordinary problem is not that two famous theories have different branding. It is that general relativity treats spacetime geometry as a classical field while quantum theory changes what can be meant by a definite matter source.",
        "mathematical_detail_plain": "The objects in tension are spacetime geometry, stress-energy, and quantum states of matter. The operation is comparison: ask what each theory holds fixed, what it lets vary, and what kind of measurement claim it allows. That comparison exposes why quantizing gravity is not a small patch to Einstein's equation.",
        "course_connection": "This links canonical formulation, constraints, and quantizable matter. It explains why the course's careful bookkeeping of initial data and source terms matters when the source itself is no longer an ordinary classical object. The evening lecture also justifies why the central course spent so much effort on object, operation, and constraint: those are exactly the pressure points when classical spacetime meets quantum matter.",
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
    authored = AUTHORED_SECTIONS[record["id"]]
    cue = choose_cue(record, depth)
    source_override = SOURCE_SPAN_OVERRIDES.get(record["id"]) if cue else None
    manual_note = MANUAL_ARCHIVE_NOTES.get(record["id"]) if cue is None else None
    source_type = "youtube-transcript" if cue else "manual-notes" if manual_note else "unsupported-placeholder"
    confidence = "strong" if cue else "manual-notes-backed" if manual_note else "missing-transcript"
    timestamp = source_override["timestamp"] if source_override else cue["start"] if cue else manual_note["timestamp"] if manual_note else None
    start_seconds = source_override["start_seconds"] if source_override else int(cue["start_seconds"]) if cue else manual_note["start_seconds"] if manual_note else None
    snippet = source_override["snippet"] if source_override else compact_snippet(cue["text"]) if cue else manual_note["snippet"] if manual_note else ""
    evidence = {
        "id": f"archive-ev-{archive_slug(record)}",
        "video_id": record["id"],
        "archive_index": record["archive_index"],
        "video_type": record["type"],
        "type_index": record["type_index"],
        "title": record["expected_title"],
        "url": f"{record['url']}&t={start_seconds}s" if start_seconds is not None else record["url"],
        "timestamp": timestamp,
        "snippet": snippet,
        "source_type": source_type,
        "confidence": confidence,
        "manual_note_path": manual_note["path"] if manual_note else None,
        "caveat_or_warning": "This archive page is backed by a local YouTube caption file, so its claims should stay close to the cited span and avoid adding unsupported lecture detail." if cue else "This archive page is backed by filled manual timestamp notes because YouTube caption download failed; use it as local evidence, not as an official caption." if manual_note else "Caption download failed or source is missing; this page is a scaffold until a transcript, external note, or manual timestamp note is added.",
    }
    page_data = {
        **record,
        **depth,
        **authored,
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
      <a href="{prefix}archive-evidence.html">Archive Evidence</a>
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
        status = "transcript-backed" if record["evidence_status"] == "strong" else "manual-notes-backed" if record["evidence_status"] == "manual-notes-backed" else "needs notes"
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
      <p>{esc(record['first_principles_role'])}</p>
    </section>
    <section class="deep-read">
      <h2>Mathematical Detail In Plain Language</h2>
      <p>{esc(record['mathematical_detail_plain'])}</p>
    </section>
    <section class="deep-read">
      <h2>How It Connects</h2>
      <p>{esc(record['course_connection'])}</p>
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


def render_archive_evidence(records: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> None:
    record_by_id = {record["id"]: record for record in records}
    rows = []
    for ev in evidence:
        record = record_by_id[ev["video_id"]]
        rows.append(
            f"""
            <tr>
              <td><a href="archive/{esc(record['slug'])}.html">{esc(record['expected_title'])}</a></td>
              <td>{esc(record['type'])}</td>
              <td>{esc(ev['timestamp'] or 'not available')}</td>
              <td>{esc(ev['confidence'])}</td>
              <td>{esc(ev['source_type'])}</td>
              <td><a href="{esc(ev['url'])}">source</a></td>
              <td>{esc(ev['snippet'] or 'No source span available yet.')}</td>
            </tr>
            """
        )
    body = f"""
    <h1>Archive Evidence</h1>
    <p class="lede">Tutorial and evening-lecture source accounting for the full 41-video archive.</p>
    <table>
      <thead><tr><th>Video</th><th>Type</th><th>Timestamp</th><th>Status</th><th>Evidence Type</th><th>Link</th><th>Source Span</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    """
    (SITE / "archive-evidence.html").write_text(page("Archive Evidence", body), encoding="utf-8")


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
    render_archive_evidence(records, evidence)
    write_json(ANALYSIS / "archive" / "video-atlas.json", records)
    write_json(ANALYSIS / "archive" / "evidence-ledger.json", evidence)
    print(f"built {len(records)} archive video pages, {len(evidence)} archive evidence records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
