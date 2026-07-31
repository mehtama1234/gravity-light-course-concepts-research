#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw-material" / "youtube"
ANALYSIS = ROOT / "analysis"


@dataclass(frozen=True)
class ConceptSeed:
    id: str
    name: str
    lecture_indexes: tuple[int, ...]
    keywords: tuple[str, ...]
    ordinary_problem: str
    naive_picture: str
    why_naive_fails: str
    mathematical_object: str
    operation: str
    why_for_gravity_light: str
    what_breaks_without_it: str
    worked_mini_example: str
    common_confusion: str
    theme: str
    subtheme: str


CONCEPTS: list[ConceptSeed] = [
    ConceptSeed(
        "topology-continuity",
        "Topology and Continuity",
        (1,),
        ("topology", "open", "continuous", "neighborhood"),
        "Before measuring distance, the course needs a way to say which points are near enough for a limiting process to make sense.",
        "It is tempting to start physics with rulers and coordinates, as though every space already arrives with lengths built in.",
        "General relativity cannot begin by assuming fixed rulers, because the gravitational field itself decides lengths and times. Topology keeps only the weaker idea of nearness.",
        "A topology is a chosen collection of open sets: enough information to talk about neighborhoods, limits, and continuous maps without yet talking about meters or seconds.",
        "The basic operation is checking whether inverse images of open sets are open, which is the coordinate-free test that a map preserves nearness.",
        "Light paths, fields, and observers must vary continuously before the theory can ask how fast or how curved that variation is.",
        "Without topology, a later derivative or field equation can hide discontinuous jumps behind smooth-looking coordinate formulas.",
        "Think of a weather map before numbers are printed on it. You can still ask whether warm regions touch cold regions or whether a path can move without jumping. Topology is that level of structure.",
        "Topology is not vague geometry. It is the exact minimum structure needed for continuity, and it deliberately refuses to decide distance.",
        "Foundations",
        "Nearness before measurement",
    ),
    ConceptSeed(
        "manifolds-local-flatness",
        "Manifolds and Local Flatness",
        (2, 4),
        ("manifold", "chart", "coordinate", "local"),
        "The course needs spaces that can be curved overall while still looking ordinary to a small local observer.",
        "One may picture curved spaces as surfaces sitting inside a bigger room, like a sphere inside three-dimensional space.",
        "Spacetime is not introduced as a surface inside a larger box. The theory must describe it from the inside, using local coordinate patches and agreement rules.",
        "A manifold is a space covered by charts, each chart translating a small patch into ordinary numbers while overlap maps say when two descriptions agree.",
        "The main operation is changing charts and checking that statements survive the change rather than depending on one chosen coordinate grid.",
        "Observers in gravity use local clocks and rods, while global spacetime may bend, contain horizons, or fail to admit one single coordinate system.",
        "Without manifolds, the theory confuses a coordinate accident with a physical effect and cannot cleanly handle horizons or global shape.",
        "A city map can use several neighborhood maps whose edges overlap. A street does not change when you switch pages; only its coordinates do. A manifold formalizes that.",
        "A manifold is not automatically a space with distances. It is the stage on which later metric and curvature data can be placed.",
        "Foundations",
        "Local descriptions",
    ),
    ConceptSeed(
        "multilinear-objects",
        "Multilinear Algebra",
        (3,),
        ("linear", "tensor", "dual", "basis", "multilinear"),
        "Physics needs quantities that accept directions, measurements, and flows while keeping track of how many slots they have.",
        "It is easy to treat all mathematical symbols as decorated vectors or matrices.",
        "Gravity uses objects with different jobs: vectors point, covectors measure, tensors combine many directional inputs. Collapsing them loses what is being measured.",
        "A tensor is a multilinear rule with specified input slots; it returns a number or another structured object in a way compatible with linear combinations.",
        "The key operation is feeding vectors and covectors into slots, changing basis, and contracting matching slots to produce coordinate-independent quantities.",
        "The metric, curvature, and stress-energy tensor all have slot structure; their physical meaning is carried by what they take in and return.",
        "Without multilinear discipline, Einstein's equation becomes symbol matching rather than a statement that two geometric/physical measuring rules are equal.",
        "A bill total is linear in item counts and prices separately: double the counts or double the prices and the total doubles. Multilinear algebra generalizes that slot-by-slot behavior.",
        "A tensor is not just an array of numbers. The array is only its coordinate display after a basis has been chosen.",
        "Foundations",
        "Slot structure",
    ),
    ConceptSeed(
        "tangent-spaces-fields",
        "Tangent Spaces and Fields",
        (5, 6),
        ("tangent", "vector field", "field", "derivation", "flow"),
        "The course needs a way to attach possible directions of motion to every event, then let physical quantities vary from event to event.",
        "One might imagine every tangent vector as a small arrow drawn in a surrounding Euclidean space.",
        "Spacetime has no required outside drawing board. Tangent directions must be defined internally by how functions change along possible motions.",
        "A tangent space is the vector space of directions available at one point; a field assigns a value, such as a vector or tensor, to each point.",
        "The basic operation is differentiating a function along a tangent direction and then doing this smoothly point by point across the manifold.",
        "Particles follow tangent directions, light has null tangent directions, and matter/gravity fields are pointwise assignments over spacetime.",
        "Without tangent spaces and fields, there is no intrinsic way to say velocity, acceleration, local measurement, or local law.",
        "On a hiking trail, your possible next steps at one spot are local directions, while wind speed at every spot is a field. Neither requires the whole mountain to be flattened.",
        "A field is not automatically a force. It is any smoothly assigned quantity; the kind of field depends on what is assigned.",
        "Foundations",
        "Local change",
    ),
    ConceptSeed(
        "connections-parallel-transport",
        "Connections and Parallel Transport",
        (7, 8),
        ("connection", "parallel", "transport", "covariant", "derivative"),
        "To compare directions at different points, the course needs a rule for carrying a direction along a path.",
        "A common intuition says two arrows at different places can be compared directly if they look parallel on the page.",
        "On a curved manifold there is no single page-level parallelism. Vectors live in different tangent spaces, so comparison needs extra structure.",
        "A connection is a rule for differentiating vector fields along directions and for transporting vectors from one tangent space to another.",
        "The central operation is covariant differentiation: measuring how a field changes after subtracting the change caused merely by moving through tangent spaces.",
        "Free fall, inertial motion, and bending light are expressed through transported directions and geodesics, not through ordinary second derivatives in a fixed grid.",
        "Without a connection, acceleration and straightness are undefined on a manifold, so gravity cannot be described as geometry.",
        "Walk north on a globe while keeping a pencil as parallel as possible. After a loop, it may point differently. The transport rule exposes curvature.",
        "A connection is not a force by itself. It is the bookkeeping rule that tells the theory what counts as unforced motion.",
        "Geometry of Gravity",
        "Comparing nearby directions",
    ),
    ConceptSeed(
        "curvature-geodesic-deviation",
        "Curvature",
        (8, 9),
        ("curvature", "riemann", "geodesic", "deviation"),
        "The theory needs a local test for whether transported directions come back changed after moving around a tiny loop.",
        "Curvature is often pictured only as visible bending in a drawing, as though an outside viewpoint were part of the theory.",
        "Spacetime curvature can be present without any outside visual bend. The intrinsic test is whether transport around loops and nearby free-fall paths fail to agree.",
        "Curvature is the tensorial failure of covariant derivatives to commute, equivalently the failure of parallel transport around small loops to return a vector unchanged.",
        "The operation is taking a commutator of covariant derivatives or comparing nearby geodesics to measure relative acceleration.",
        "Gravity becomes tidal behavior: not merely objects falling, but neighboring free-fall paths squeezing, spreading, or shearing because spacetime itself is curved.",
        "Without curvature, the course cannot distinguish a removable coordinate effect from a real gravitational field.",
        "Inside a falling elevator, one dropped ball may look weightless. Two separated balls can still drift together or apart. That relative drift is the kind of fact curvature captures.",
        "Curvature is not the same as a gravitational pull felt by one observer. It is about comparisons across nearby paths.",
        "Geometry of Gravity",
        "Tidal facts",
    ),
    ConceptSeed(
        "metric-measurement",
        "Metric Manifolds",
        (10, 13),
        ("metric", "length", "inner product", "lorentz", "spacetime"),
        "After building nearness and smoothness, the course needs a rule that tells clocks, rulers, and light cones what they measure.",
        "One may assume distance is a background grid laid down before physics begins.",
        "In relativity the metric is not background decoration; it is one of the main physical fields, and it determines which separations are time-like, space-like, or light-like.",
        "A metric is a smoothly varying inner product on tangent spaces, with Lorentzian signature in spacetime so that time and space enter differently.",
        "The operation is evaluating the metric on tangent vectors to compute intervals, norms, angles, volumes, and null directions.",
        "Light is defined by zero interval, clocks measure proper time, and Einstein gravity tells how the metric responds to matter.",
        "Without the metric, there are no light cones, no proper time, no causal order, and no precise statement of the Einstein equation.",
        "A road map without a scale can show connected streets but not travel time. A metric adds the scale, except in spacetime the scale also separates possible light signals from impossible ones.",
        "A metric is not just a distance formula. In spacetime it also encodes causal structure and is itself dynamical.",
        "Geometry of Gravity",
        "Measurement becomes a field",
    ),
    ConceptSeed(
        "symmetry-conservation",
        "Symmetry and Conservation",
        (11,),
        ("symmetry", "killing", "conservation", "invariant"),
        "The course needs a way to recognize when a geometry has sameness that produces simpler motion or conserved quantities.",
        "Symmetry can sound like visual prettiness or a decorative shape property, detached from measurement and calculation.",
        "In physics, symmetry is operational: a transformation changes the description while leaving the relevant structure unchanged.",
        "A symmetry is a structure-preserving map or flow, often expressed by a vector field whose motion leaves the metric unchanged.",
        "The operation is taking a Lie derivative or checking invariance under a flow to see whether geometric data changes.",
        "Symmetries make energy-like and angular-momentum-like quantities meaningful in spacetimes where such quantities may not exist globally.",
        "Without symmetry analysis, the course cannot explain why special solutions such as black holes or cosmologies become tractable.",
        "If a room looks the same after rotating a chair arrangement by half a turn, that rotation is a symmetry. In spacetime, the preserved thing may be the interval structure.",
        "Symmetry does not mean every point is the same; it means a particular transformation preserves the chosen structure.",
        "Dynamics and Matter",
        "Sameness as a calculation",
    ),
    ConceptSeed(
        "integration-on-manifolds",
        "Integration on Manifolds",
        (12,),
        ("integration", "form", "volume", "orientation", "stokes"),
        "The course needs a way to add local quantities over curved spaces without depending on one coordinate chart.",
        "Integration may look like an area-under-a-curve recipe tied to x-axes and y-axes.",
        "On a manifold, a region may require many charts, and the answer must not change when the chart changes.",
        "Differential forms and volume elements package what can be integrated in a coordinate-independent way.",
        "The operation is pulling forms back to charts or submanifolds, integrating them there, and using Stokes-type relations between boundary and bulk.",
        "Actions, matter totals, fluxes, and conservation laws need integration that respects the geometry of spacetime.",
        "Without manifold integration, the theory cannot move from local equations to global quantities or variational principles.",
        "Adding rainfall over a country should not depend on which map projection you used. Forms provide the correction built into the object being integrated.",
        "The integral is not merely a sum of numbers; the object being summed must transform correctly under coordinate changes.",
        "Dynamics and Matter",
        "Adding local facts",
    ),
    ConceptSeed(
        "stress-energy-matter",
        "Matter and Stress-Energy",
        (14, 15, 26),
        ("matter", "stress", "energy", "tensor", "source"),
        "Gravity needs a precise account of what matter contributes: not just mass, but energy, momentum, pressure, and stresses.",
        "A Newtonian habit says gravity is sourced by mass alone, with pressure and momentum treated as secondary details.",
        "Relativity treats energy and momentum as a unified local bookkeeping object, and pressure/stress also gravitate.",
        "The stress-energy tensor is the object that measures energy density, momentum flow, pressure, and stress through chosen directions or surfaces.",
        "The operation is evaluating its slots against observer directions and surface normals, then requiring local conservation through covariant divergence.",
        "Einstein gravity relates spacetime curvature to this full matter bookkeeping, which is why light, fields, and pressure affect gravity.",
        "Without stress-energy, Einstein's equation has no physically meaningful right-hand side and cannot couple geometry to matter.",
        "A flowing river carries water amount and push. Matter in relativity similarly has density and flow of momentum; stress-energy keeps all of that in one object.",
        "Stress-energy is not a bag of stuff. It is a local measuring rule for energy and momentum as seen through directions.",
        "Dynamics and Matter",
        "What gravitates",
    ),
    ConceptSeed(
        "einstein-equation",
        "Einstein Equation",
        (15,),
        ("einstein", "equation", "ricci", "curvature", "cosmological"),
        "The course needs the law that says how spacetime geometry and matter constrain each other.",
        "A shallow slogan says matter tells spacetime how to curve and spacetime tells matter how to move.",
        "The real content is sharper: a specific divergence-free combination of curvature equals a specific local matter tensor, with constants fixing units and observations.",
        "The Einstein tensor is built from curvature and the metric so that its covariant divergence vanishes, matching local conservation of stress-energy.",
        "The operation is equating the geometric tensor to stress-energy, then solving the resulting coupled nonlinear field equations under boundary or symmetry assumptions.",
        "This is the bridge from the earlier geometry lectures to cosmology, black holes, gravitational waves, and light propagation.",
        "Without this equation, the course has geometry and matter as separate languages with no rule for their mutual constraint.",
        "A budget rule must balance every entry using compatible units. Einstein's equation is a local balance rule between geometric curvature bookkeeping and matter bookkeeping.",
        "The equation is not one scalar formula. It is a coupled tensor equation whose difficulty comes from the metric appearing inside its own curvature.",
        "Dynamics and Matter",
        "Geometry coupled to matter",
    ),
    ConceptSeed(
        "optical-geometry",
        "Optical Geometry and Null Geodesics",
        (16, 17),
        ("optical", "light", "null", "geodesic", "lens"),
        "The course needs to explain why light follows paths fixed by spacetime geometry rather than by an external optical medium.",
        "It is tempting to say gravity pulls photons sideways like tiny balls.",
        "In relativity, light moves along null directions of the metric; bending follows from spacetime geometry and causal structure.",
        "Null geodesics are curves whose tangent has zero metric length and is parallel transported along itself.",
        "The operation is solving the geodesic equation under the null condition and comparing neighboring light rays through focusing or lensing.",
        "Light is both messenger and measuring device: horizons, lenses, time delays, and observations all depend on null geometry.",
        "Without null geodesics, the theory cannot connect spacetime models to what telescopes and detectors actually see.",
        "A fastest route on a curved map is not the straight-looking line on a projection. Light follows the spacetime version of the route dictated by the metric.",
        "Null does not mean zero motion. It means the spacetime interval along the light path is zero.",
        "Light and Observation",
        "Causal paths",
    ),
    ConceptSeed(
        "canonical-formulation",
        "Canonical Formulation and Constraints",
        (18, 19),
        ("canonical", "constraint", "hamiltonian", "initial", "adm"),
        "The course needs a way to describe spacetime evolution from data on a space-like slice while respecting coordinate freedom.",
        "One may expect general relativity to evolve like ordinary mechanics: choose positions and velocities, then march forward in one universal time.",
        "There is no preferred universal time built into the theory, and not every initial-looking dataset satisfies the geometric constraints.",
        "The canonical formulation rewrites spacetime geometry as slice geometry plus momentum-like data, constrained by the same physics in a different language.",
        "The operation is decomposing spacetime into space plus time, identifying constraints, and checking how allowed data evolves.",
        "This perspective matters for numerical relativity, gravitational waves, and attempts to quantize gravity.",
        "Without the constraints, one can feed impossible initial data into the theory and confuse coordinate motion with physical evolution.",
        "Planning a movie from snapshots requires more than each frame looking plausible; neighboring frames must fit a lawful motion. Canonical GR formalizes that fit for spacetime slices.",
        "The canonical formulation is not a separate theory. It is the same theory reorganized around initial data and constraints.",
        "Dynamics and Matter",
        "Allowed initial data",
    ),
    ConceptSeed(
        "cosmology-scale-factor",
        "Cosmology and Expansion",
        (20, 21),
        ("cosmology", "expansion", "scale", "universe", "friedmann"),
        "The course needs to apply the field equation to a whole-universe model without pretending every detail of the universe is tracked.",
        "Expansion is often pictured as galaxies flying through empty pre-existing space from a central explosion.",
        "Cosmological expansion is a change in the metric scale between comoving positions, not motion away from a center inside a larger room.",
        "A cosmological model uses symmetry assumptions plus a scale factor to reduce Einstein's equation to equations for large-scale evolution.",
        "The operation is imposing homogeneity/isotropy, deriving reduced evolution equations, and reading matter content from how the scale factor changes.",
        "Cosmology shows how geometry, matter, light propagation, and observation combine in one testable large-scale story.",
        "Without the scale-factor idea, redshift and cosmic history get misread as ordinary Doppler motion in fixed space.",
        "Dots on a stretching sheet get farther apart without walking across the sheet. The useful part of the image is changing separation, not the sheet as an outside object.",
        "Homogeneous models are controlled approximations. They explain large-scale structure while knowingly smoothing away local detail.",
        "Applications",
        "Large-scale geometry",
    ),
    ConceptSeed(
        "black-holes-horizons",
        "Black Holes and Horizons",
        (22, 23),
        ("black hole", "horizon", "schwarzschild", "penrose", "singularity"),
        "The course needs to understand regions where causal structure, not escape speed folklore, defines what can communicate outward.",
        "A black hole is often described as an object whose gravity is so strong that not even light can climb out.",
        "The deeper statement is global and causal: future-directed light paths from inside the horizon do not reach the outside region.",
        "An event horizon is a boundary in spacetime's causal structure; Penrose diagrams compress infinities to show which events can influence which others.",
        "The operation is tracing null directions and causal relations, often after a coordinate change that removes fake singular behavior.",
        "Black holes force the course's earlier ideas about coordinates, metrics, null paths, and global structure to work together.",
        "Without causal diagrams and horizon language, coordinate artifacts near horizons are easily mistaken for physical singularities.",
        "A river crossing a waterfall has a point where even a swimmer moving upstream cannot avoid going over. The black-hole version concerns future light directions in spacetime.",
        "The horizon is not a material surface. It is a causal boundary defined by the whole spacetime.",
        "Applications",
        "Causal boundaries",
    ),
    ConceptSeed(
        "perturbations-waves",
        "Perturbation Theory and Gravitational Waves",
        (24, 25, 27, 28),
        ("perturbation", "wave", "gravitational", "linear", "detector", "interferometer"),
        "The course needs a way to study small departures from a known spacetime and connect them to measurable signals.",
        "It is natural to think a gravitational wave is a vibration traveling through space like sound through air.",
        "In general relativity, the wave is a propagating disturbance of the metric itself, with gauge freedom that must be handled carefully.",
        "A perturbation is a controlled small change of the metric or matter fields around a background solution.",
        "The operation is linearizing the field equations, separating physical modes from coordinate changes, and predicting detector strain.",
        "This connects the abstract geometry to sources such as binaries and to interferometers that measure tiny relative length changes.",
        "Without perturbation theory, realistic waves are either unsolved nonlinear problems or misleading coordinate wiggles.",
        "To study a bridge's small vibration, engineers first know the resting bridge and then track tiny departures. GR does the same, except the vibrating object is spacetime geometry.",
        "Not every ripple in metric components is a physical wave; some ripples are changed coordinates.",
        "Light and Observation",
        "Small signals",
    ),
]


THEMES = [
    {
        "id": "foundations",
        "name": "Foundations",
        "plain_question": "What must be built before gravity can be described without a preferred coordinate grid?",
        "answer": "The early lectures strip geometry down to nearness, local charts, slot-aware algebra, and local directions. This prevents later equations from smuggling in a flat background.",
    },
    {
        "id": "geometry-of-gravity",
        "name": "Geometry of Gravity",
        "plain_question": "How does the course turn falling into a statement about geometry?",
        "answer": "Connections define straight motion on a manifold, curvature measures when those local straightness rules fail to fit globally, and the metric turns measurement into a field.",
    },
    {
        "id": "dynamics-and-matter",
        "name": "Dynamics and Matter",
        "plain_question": "What does the field equation actually join together?",
        "answer": "It joins a divergence-free curvature object to stress-energy, so local conservation of matter and local geometry obey the same accounting rule.",
    },
    {
        "id": "light-and-observation",
        "name": "Light and Observation",
        "plain_question": "How does abstract spacetime become something seen by detectors?",
        "answer": "Null geodesics, lensing, wave perturbations, and interferometer strain translate metric structure into observed light paths and measured relative lengths.",
    },
    {
        "id": "applications",
        "name": "Applications",
        "plain_question": "Where do the foundations get stress-tested?",
        "answer": "Cosmology, black holes, and wave sources force local geometry, global causal structure, matter, and measurement to operate as one system.",
    },
]


FAMILIES = [
    {
        "id": "build-space-before-measuring",
        "name": "Build space before measuring it",
        "lecture_indexes": [1, 2, 3, 4, 5, 6],
        "plain_problem": "A theory of gravity cannot begin by assuming a fixed grid, fixed rulers, or a surrounding room. These lectures build the minimum language needed to speak about places, change, and physical quantities before distance has been granted.",
        "mathematical_spine": "Topology supplies nearness. Manifolds supply local coordinate patches. Multilinear algebra supplies slot-aware quantities. Tangent spaces and fields supply local directions and point-by-point variation.",
        "why_it_matters": "If this family is shallow, the rest of the course becomes a pile of formulas. If it is understood, later objects such as the metric, curvature, and stress-energy tensor have clear jobs instead of mysterious names.",
        "what_to_watch_for": "The central discipline is not to confuse a coordinate display with the object being displayed. Numbers on a chart are allowed, but the claim must survive changing the chart.",
    },
    {
        "id": "turn-falling-into-geometry",
        "name": "Turn falling into geometry",
        "lecture_indexes": [7, 8, 9, 10],
        "plain_problem": "The course must explain free motion without saying that every path is judged against an invisible flat background. It needs its own rule for straightness and its own test for real gravitational curvature.",
        "mathematical_spine": "Connections define how directions are compared along paths. Parallel transport applies that comparison. Curvature measures the failure of those comparisons to fit around loops. The metric later says what clocks, rulers, and light cones measure.",
        "why_it_matters": "This is where gravity stops being a force pasted onto space and becomes a statement about what local inertial motion and neighboring paths do.",
        "what_to_watch_for": "One observer's felt acceleration is not the same thing as curvature. Curvature is detected by comparison: nearby free paths drift relative to one another in a way no coordinate trick removes.",
    },
    {
        "id": "make-laws-coordinate-free",
        "name": "Make laws coordinate-free",
        "lecture_indexes": [11, 12, 13, 14, 15],
        "plain_problem": "Once geometry exists, the course needs laws that can be stated without picking a favorite observer or map. It also needs a precise object for what matter contributes to gravity.",
        "mathematical_spine": "Symmetry identifies transformations that preserve structure. Integration adds local geometric quantities over regions. Spacetime supplies the Lorentzian stage. Stress-energy states what matter carries. Einstein's equation couples the geometry side to the matter side.",
        "why_it_matters": "The field equation is not a slogan. It is a compatibility statement: the geometry object and the matter object have matching conservation behavior, so the left and right sides can be equated without breaking local energy-momentum accounting.",
        "what_to_watch_for": "Mass alone is not the source in relativity. Energy, momentum, pressure, and stress all enter because the source must match the spacetime geometry being solved for.",
    },
    {
        "id": "read-spacetime-with-light",
        "name": "Read spacetime with light",
        "lecture_indexes": [16, 17],
        "plain_problem": "The course needs a bridge from equations to observation. Light is the bridge because it follows the causal structure set by the metric and carries information to detectors.",
        "mathematical_spine": "Null directions are tangent directions whose spacetime interval is zero. Null geodesics are light paths. Families of such paths focus, shear, delay, or bend according to the geometry.",
        "why_it_matters": "Most astronomical evidence about gravity arrives through light. If null geometry is weakly understood, lensing, horizons, redshift, and signal travel times become disconnected facts.",
        "what_to_watch_for": "A null path is not a path with no motion. It is a path with zero spacetime interval, which is exactly what makes it a light path.",
    },
    {
        "id": "solve-evolution-and-global-shape",
        "name": "Solve evolution and global shape",
        "lecture_indexes": [18, 19, 20, 21, 22, 23],
        "plain_problem": "The course then asks how whole spacetimes behave: how valid initial data evolves, how the universe expands, and how causal boundaries such as horizons are understood.",
        "mathematical_spine": "Canonical GR rewrites spacetime as slice data plus constraints. Cosmology uses symmetry to reduce the field equation. Black holes and Penrose diagrams track causal reach rather than visual shape.",
        "why_it_matters": "These lectures test whether the earlier machinery can handle time evolution, large-scale structure, and regions where coordinates can mislead badly. They are where local definitions must survive contact with whole-spacetime questions.",
        "what_to_watch_for": "Several lectures in this family lack local transcripts, so the current atlas marks them as scaffolds that need manual notes before being treated as detailed evidence.",
    },
    {
        "id": "extract-small-signals",
        "name": "Extract small signals",
        "lecture_indexes": [24, 25, 26, 27, 28],
        "plain_problem": "Exact solutions are rare, but real detectors measure small changes in realistic systems. The course needs controlled approximations that separate physical effects from coordinate changes and connect source motion to measurable detector strain.",
        "mathematical_spine": "Perturbation theory studies small metric changes around a known background. Quantizable matter raises how matter fields source gravity. Wave-source and detector lectures connect those changes to strain in interferometers.",
        "why_it_matters": "This is where the abstract course pays off experimentally: the same metric idea that defined light cones also predicts tiny changing distances measured by gravitational-wave detectors.",
        "what_to_watch_for": "Not every changing metric component is a physical wave. The course must separate real measured strain from a changed description, then explain how source dynamics, propagation, and interferometer readout refer to the same disturbance.",
    },
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_records() -> list[dict[str, Any]]:
    return json.loads((RAW / "transcript-index.json").read_text(encoding="utf-8"))


def load_cues(record: dict[str, Any]) -> list[dict[str, Any]]:
    if record.get("transcript_status") != "available":
        return []
    return json.loads((ROOT / record["cue_json"]).read_text(encoding="utf-8"))


def compact_snippet(text: str, max_words: int = 46) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(",.;:") + "..."


def concept_deep_layers(seed: ConceptSeed) -> dict[str, str]:
    first_principles = (
        f"Start with the ordinary problem: {seed.ordinary_problem} "
        f"The tempting shortcut is this: {seed.naive_picture} "
        f"That shortcut fails because {seed.why_naive_fails} "
        f"So the course introduces a specific object instead of a vague picture: {seed.mathematical_object} "
        f"The point is not to admire the object. The point is to perform a controlled operation on it: {seed.operation} "
        f"Once that operation is available, the later gravity-and-light argument has a stable step to stand on."
    )
    mathematical_detail = (
        f"The mathematical principle is that a physical claim should name what is being held fixed, what is being changed, and what comparison is allowed. "
        f"For {seed.name.lower()}, the held object is: {seed.mathematical_object} "
        f"The permitted action is: {seed.operation} "
        f"This matters because the course repeatedly moves from local descriptions to statements that must survive a change of coordinates, observer, or path. "
        f"Without that discipline, a calculation can report a feature of the chosen description while pretending it has found a feature of spacetime."
    )
    why_critical = (
        f"This concept is critical for the course because {seed.why_for_gravity_light} "
        f"If it is skipped or reduced to a slogan, this is what breaks: {seed.what_breaks_without_it} "
        f"The practical test is whether a student can explain both the object and the operation in everyday language, then say why the next lecture needs them. "
        f"That is the level needed for gravity, light, curvature, matter, horizons, waves, and detectors to feel like one chain rather than separate topics."
    )
    return {
        "first_principles_walkthrough": first_principles,
        "mathematical_detail_plain": mathematical_detail,
        "why_this_is_critical": why_critical,
        "family_bridge": sequence_role(seed.lecture_indexes),
    }


def find_evidence(seed: ConceptSeed, records_by_index: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    evidence = []
    for lecture_index in seed.lecture_indexes:
        record = records_by_index[lecture_index]
        evidence_id = f"ev-{seed.id}-l{lecture_index:02d}"
        if record.get("transcript_status") != "available":
            evidence.append(
                {
                    "id": evidence_id,
                    "concept_id": seed.id,
                    "lecture_index": lecture_index,
                    "lecture_title": record["expected_title"],
                    "url": record["url"],
                    "timestamp": None,
                    "snippet": "",
                    "transcript_status": "missing",
                    "confidence": "missing-transcript",
                    "lecture_argument": "The lecture title places this concept in the sequence, but the local transcript is missing and the claim still needs manual notes or another source.",
                    "mathematical_object": seed.mathematical_object,
                    "operation": seed.operation,
                    "why_span_matters": seed.why_for_gravity_light,
                    "caveat_or_warning": "Do not treat this as transcript-backed evidence until a transcript or lecture notes are added.",
                }
            )
            continue

        cues = load_cues(record)
        chosen = None
        lowered_keywords = [k.lower() for k in seed.keywords]
        for cue in cues:
            text = cue["text"]
            low = text.lower()
            if any(k in low for k in lowered_keywords):
                chosen = cue
                break
        if chosen is None and cues:
            midpoint = min(len(cues) - 1, max(0, len(cues) // 3))
            chosen = cues[midpoint]
        snippet = compact_snippet(chosen["text"]) if chosen else ""
        evidence.append(
            {
                "id": evidence_id,
                "concept_id": seed.id,
                "lecture_index": lecture_index,
                "lecture_title": record["expected_title"],
                "url": f"{record['url']}&t={int(chosen['start_seconds'])}s" if chosen else record["url"],
                "timestamp": chosen["start"] if chosen else None,
                "snippet": snippet,
                "transcript_status": "available",
                "confidence": "strong" if chosen and any(k in snippet.lower() for k in lowered_keywords) else "moderate",
                "lecture_argument": f"This lecture supplies the local course context for {seed.name.lower()}: {seed.ordinary_problem}",
                "mathematical_object": seed.mathematical_object,
                "operation": seed.operation,
                "why_span_matters": seed.why_for_gravity_light,
                "caveat_or_warning": seed.common_confusion,
            }
        )
    return evidence


def build() -> None:
    records = load_records()
    records_by_index = {r["index"]: r for r in records}
    evidence_records: list[dict[str, Any]] = []
    concepts: list[dict[str, Any]] = []

    for seed in CONCEPTS:
        ev = find_evidence(seed, records_by_index)
        evidence_records.extend(ev)
        concepts.append(
            {
                "id": seed.id,
                "name": seed.name,
                "theme": seed.theme,
                "subtheme": seed.subtheme,
                "lecture_indexes": list(seed.lecture_indexes),
                "ordinary_problem": seed.ordinary_problem,
                "naive_picture": seed.naive_picture,
                "why_naive_fails": seed.why_naive_fails,
                "mathematical_object": seed.mathematical_object,
                "operation": seed.operation,
                "why_for_gravity_light": seed.why_for_gravity_light,
                "what_breaks_without_it": seed.what_breaks_without_it,
                "worked_mini_example": seed.worked_mini_example,
                "lecture_sequence_role": sequence_role(seed.lecture_indexes),
                "common_confusion": seed.common_confusion,
                **concept_deep_layers(seed),
                "evidence_ids": [item["id"] for item in ev],
            }
        )

    lecture_atlas = []
    concept_by_lecture: dict[int, list[str]] = {}
    for concept in concepts:
        for index in concept["lecture_indexes"]:
            concept_by_lecture.setdefault(index, []).append(concept["id"])
    for record in records:
        lecture_concept_ids = concept_by_lecture.get(record["index"], [])
        lecture_atlas.append(
            {
                "index": record["index"],
                "id": record["id"],
                "title": record["expected_title"],
                "url": record["url"],
                "transcript_status": record["transcript_status"],
                "word_count": record.get("word_count", 0),
                "concept_ids": lecture_concept_ids,
                "audit_note": lecture_audit_note(record),
                "central_question": lecture_central_question(record, lecture_concept_ids, concepts),
                "first_principles_role": lecture_first_principles_role(record, lecture_concept_ids, concepts),
                "mathematical_objects_to_track": lecture_objects_to_track(lecture_concept_ids, concepts),
                "reader_warning": lecture_reader_warning(record),
            }
        )

    theme_map = []
    for theme in THEMES:
        theme_concepts = [c for c in concepts if slugify(c["theme"]) == theme["id"]]
        theme_map.append(
            {
                **theme,
                "concept_ids": [c["id"] for c in theme_concepts],
                "subthemes": sorted({c["subtheme"] for c in theme_concepts}),
                "why_the_math_matters": theme_why(theme["id"]),
            }
        )

    primitives = [
        {
            "id": "object-operation-meaning",
            "name": "Object, operation, meaning",
            "description": "Every mathematical idea is tracked as a thing, an action performed on it, and the physical distinction that action protects.",
        },
        {
            "id": "coordinate-independence",
            "name": "Coordinate independence",
            "description": "A formula earns its place only when it describes something that survives a change of chart or frame.",
        },
        {
            "id": "local-to-global",
            "name": "Local to global",
            "description": "The course repeatedly builds local rules first, then asks what happens when they are carried around loops, regions, or whole spacetimes.",
        },
        {
            "id": "measurement-as-structure",
            "name": "Measurement as structure",
            "description": "Distances, times, angles, volumes, and light cones are not assumed; each enters through a named mathematical object.",
        },
    ]

    write_json(ANALYSIS / "concepts" / "concept-atlas.json", concepts)
    write_json(ANALYSIS / "evidence" / "evidence-ledger.json", evidence_records)
    write_json(ANALYSIS / "lectures" / "lecture-atlas.json", lecture_atlas)
    write_json(ANALYSIS / "themes" / "theme-map.json", theme_map)
    write_json(ANALYSIS / "families" / "family-map.json", build_family_map(concepts, lecture_atlas))
    write_json(ANALYSIS / "throughlines" / "primitives.json", primitives)
    write_audit(concepts, evidence_records, lecture_atlas, theme_map, FAMILIES)
    print(f"built {len(concepts)} concepts, {len(evidence_records)} evidence records, {len(theme_map)} themes, {len(FAMILIES)} families")


def build_family_map(concepts: list[dict[str, Any]], lectures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    concept_by_id = {concept["id"]: concept for concept in concepts}
    out = []
    for family in FAMILIES:
        indexes = set(family["lecture_indexes"])
        family_concepts = [
            concept
            for concept in concepts
            if any(index in indexes for index in concept["lecture_indexes"])
        ]
        family_lectures = [lecture for lecture in lectures if lecture["index"] in indexes]
        missing = [lecture["index"] for lecture in family_lectures if lecture["transcript_status"] != "available"]
        out.append(
            {
                **family,
                "concept_ids": [concept["id"] for concept in family_concepts],
                "subthemes": sorted({concept_by_id[concept["id"]]["subtheme"] for concept in family_concepts}),
                "transcript_backed_lectures": [lecture["index"] for lecture in family_lectures if lecture["transcript_status"] == "available"],
                "missing_transcript_lectures": missing,
                "audit_note": "Transcript-backed except listed gaps." if missing else "Transcript-backed for every lecture in this family.",
            }
        )
    return out


def sequence_role(indexes: tuple[int, ...]) -> str:
    start = min(indexes)
    if start <= 6:
        return "Builds the language needed before curvature, metric measurement, and field equations can be stated without hidden background assumptions."
    if start <= 12:
        return "Turns the early language into geometric operations: comparison, curvature, symmetry, and integration."
    if start <= 17:
        return "Connects geometry to matter, Einstein's equation, and light as the observational carrier."
    if start <= 23:
        return "Applies the field equation to evolution, cosmology, horizons, and global causal structure."
    return "Moves from exact structures to small measurable departures, physical source models, and detector response."


def lecture_audit_note(record: dict[str, Any]) -> str:
    if record["transcript_status"] == "available":
        return f"Transcript-backed with {record.get('word_count', 0)} words available for snippet-level evidence."
    return "Needs manual lecture notes or another transcript source before detailed claims should be treated as supported."


def lecture_central_question(record: dict[str, Any], concept_ids: list[str], concepts: list[dict[str, Any]]) -> str:
    if not concept_ids:
        return "What does this lecture contribute to the course sequence, and what source material is still needed to explain it responsibly?"
    names = ", ".join(concept["name"] for concept in concepts if concept["id"] in concept_ids)
    return f"How does this lecture use {names} to move the course from everyday geometric intuition toward a usable theory of gravity and light?"


def lecture_first_principles_role(record: dict[str, Any], concept_ids: list[str], concepts: list[dict[str, Any]]) -> str:
    matched = [concept for concept in concepts if concept["id"] in concept_ids]
    if not matched:
        return "This lecture is present in the playlist but has no assigned concept yet. It should be audited before any polished explanation claims to cover the whole course."
    ordinary = " ".join(concept["ordinary_problem"] for concept in matched)
    operations = " ".join(concept["operation"] for concept in matched)
    return (
        f"Lecture {record['index']:02d} should be read as a step in the course's construction, not as an isolated topic. "
        f"The ordinary problem is: {ordinary} "
        f"The mathematical work to watch is: {operations} "
        f"A good writeup should make that operation visible before using later terms from relativity."
    )


def lecture_objects_to_track(concept_ids: list[str], concepts: list[dict[str, Any]]) -> list[str]:
    return [concept["mathematical_object"] for concept in concepts if concept["id"] in concept_ids]


def lecture_reader_warning(record: dict[str, Any]) -> str:
    if record["transcript_status"] == "available":
        return "This lecture has local transcript evidence. Claims should cite snippets or timestamps when they interpret the lecture's argument."
    return "This lecture is not locally transcript-backed. Treat its page as a roadmap for future notes, not as a finished explanation of the lecture."


def theme_why(theme_id: str) -> str:
    return {
        "foundations": "These ideas prevent later gravity from depending on a preferred picture, grid, or surrounding flat space.",
        "geometry-of-gravity": "These ideas turn the felt fact of falling into precise comparisons of local directions and measurements.",
        "dynamics-and-matter": "These ideas explain why the field equation is a constrained balance between geometry and matter, not a slogan.",
        "light-and-observation": "These ideas explain how spacetime geometry becomes observations through light paths and detector response.",
        "applications": "These ideas show why the machinery was built: it handles universe-scale evolution, horizons, and waves.",
    }[theme_id]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_audit(concepts: list[dict[str, Any]], evidence: list[dict[str, Any]], lectures: list[dict[str, Any]], themes: list[dict[str, Any]], families: list[dict[str, Any]]) -> None:
    missing = [l for l in lectures if l["transcript_status"] != "available"]
    strong = [e for e in evidence if e["confidence"] == "strong"]
    moderate = [e for e in evidence if e["confidence"] == "moderate"]
    missing_ev = [e for e in evidence if e["confidence"] == "missing-transcript"]
    lines = [
        "# Atlas Audit",
        "",
        f"- Concepts: {len(concepts)}",
        f"- Themes: {len(themes)}",
        f"- Lecture families: {len(families)}",
        f"- Lecture pages: {len(lectures)}",
        f"- Evidence records: {len(evidence)}",
        f"- Strong transcript matches: {len(strong)}",
        f"- Moderate transcript-backed records: {len(moderate)}",
        f"- Missing-transcript placeholders: {len(missing_ev)}",
        f"- Lectures with transcripts: {len(lectures) - len(missing)}/{len(lectures)}",
        "",
        "## Missing Transcript Coverage",
        "",
    ]
    if missing:
        for lecture in missing:
            lines.append(f"- Lecture {lecture['index']:02d}: {lecture['title']} - {lecture['audit_note']}")
    else:
        lines.append("- None.")
    lines += [
        "",
        "## Depth Standard",
        "",
        "Every concept page is required to explain the ordinary problem, the tempting but insufficient picture, the mathematical object, the operation performed on that object, why the idea matters for gravity and light, and what breaks without it.",
        "",
        "## Current Limitation",
        "",
        "This is a transcript-grounded first atlas, not a finished lecture-note replacement. Missing subtitle lectures are scaffolded from playlist titles only and are deliberately marked as unsupported until more source material is added.",
        "",
    ]
    (ANALYSIS / "audits").mkdir(parents=True, exist_ok=True)
    (ANALYSIS / "audits" / "atlas-validation-report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build()
