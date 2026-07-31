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
NOTES_INDEX = ROOT / "raw-material" / "external-notes" / "notes-index.json"


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


CONCEPTS.extend(
    [
        ConceptSeed(
            "open-sets-neighborhood-tests",
            "Open Sets As Neighborhood Tests",
            (1,),
            ("open", "neighborhood", "set", "continuous"),
            "The first lecture needs a way to test whether a small move stays inside an allowed region before it has any distance formula.",
            "A common shortcut is to think nearness always means a numerical distance has already been measured.",
            "That shortcut fails because the course has not yet earned a ruler. It only needs to know which regions count as roomy enough around a point.",
            "An open set is a region that contains a little breathing room around each of its points, stated without choosing units of length.",
            "The operation is to ask whether a point has a neighborhood contained inside the region, then use that test to define continuity.",
            "Gravity needs this because smooth fields and light paths must vary without sudden tears before any metric can say how long a direction is.",
            "Without open-set tests, later claims about smoothness can quietly depend on a hidden distance rule that the theory has not introduced.",
            "A train station concourse can be open around you if you can take a few steps without leaving it. That idea is about room to move, not a measured radius.",
            "Open does not mean physically uncovered or infinite. It means every point has enough local room for continuity tests.",
            "Foundations",
            "Nearness before measurement",
        ),
        ConceptSeed(
            "continuous-maps-preserve-nearness",
            "Continuous Maps Preserve Nearness",
            (1,),
            ("continuous", "map", "inverse", "open"),
            "The course needs a way to say one description respects nearness in another description.",
            "It is tempting to call a map continuous only when its graph can be drawn without lifting a pen.",
            "That picture fails for the spaces used later, because there may be no single graph paper where both spaces live.",
            "A continuous map is a rule between spaces whose inverse image of any open region is open in the starting space.",
            "The operation is pulling an open test region backward through the map and checking whether it remains an open test region.",
            "This matters for gravity and light because fields, coordinate maps, and observer descriptions must carry local variation without creating artificial jumps.",
            "Without this idea, a coordinate change can break the ordinary meaning of nearby events staying nearby.",
            "If a thermostat display changes smoothly as room temperature changes, nearby temperatures produce nearby readings. Continuity says that without needing a picture of the graph.",
            "Continuity is not sameness. It permits stretching and bending; it forbids tearing the neighborhood relation.",
            "Foundations",
            "Nearness before measurement",
        ),
        ConceptSeed(
            "charts-atlases-coordinate-overlap",
            "Charts, Atlases, and Overlap Rules",
            (2, 4),
            ("chart", "atlas", "overlap", "coordinate"),
            "The course needs many local maps that can cover one space without pretending one map works everywhere.",
            "A first picture says coordinates are the space itself, so changing coordinates changes the thing being studied.",
            "That fails because curved spaces and spacetime regions may need several coordinate patches, while the physical point remains the same.",
            "A chart assigns numbers to points in one patch, and an atlas is a compatible collection of such charts.",
            "The operation is comparing charts on their overlaps and requiring the change from one chart to another to behave smoothly.",
            "Gravity needs this because horizons, poles, and other awkward regions can make one coordinate system fail while spacetime itself remains meaningful.",
            "Without overlap rules, a bad coordinate patch can be mistaken for a physical singularity or a real boundary.",
            "Two subway maps can draw the same station differently. The station is not duplicated; the overlap rule tells you how the drawings refer to the same place.",
            "A chart is a local naming scheme, not the object. The overlap map is what keeps several naming schemes honest.",
            "Foundations",
            "Local descriptions",
        ),
        ConceptSeed(
            "smoothness-change-rates",
            "Smoothness As Allowed Change",
            (4,),
            ("smooth", "differentiable", "derivative", "chart"),
            "The course needs to know when change is regular enough for derivatives to make sense across chart boundaries.",
            "One may think smooth simply means visually rounded or free of sharp corners in a drawing.",
            "That drawing test fails because the object may not be drawn in one surrounding space, and the relevant test must survive coordinate changes.",
            "A smooth structure is the rule that says which chart changes are differentiable enough for calculus to be done consistently.",
            "The operation is taking derivatives in one chart and checking that another chart gives the same kind of admissible calculation.",
            "Fields, particle paths, and curvature all require repeated change-rate operations, so smoothness is the license for later differential geometry.",
            "Without smoothness, the theory can write derivatives that depend on the map used rather than on the spacetime being studied.",
            "A recipe translated between languages should still have steps that make sense. Smooth chart changes are the translation rules that preserve calculus steps.",
            "Smoothness is not extra decoration. It decides whether derivatives are legal operations on the space.",
            "Foundations",
            "Local descriptions",
        ),
        ConceptSeed(
            "dual-vectors-measure-directions",
            "Dual Vectors Measure Directions",
            (3, 5),
            ("dual", "covector", "one-form", "basis"),
            "The course needs a way to distinguish an arrow-like direction from a measuring rule applied to that direction.",
            "A common shortcut treats every linear object as a vector with components in a column.",
            "That fails because some objects point along possible motion while others take a direction as input and return a measured number.",
            "A dual vector, also called a covector or one-form, is a linear measuring rule on vectors.",
            "The operation is feeding a vector into the covector and getting a number that changes correctly when coordinates change.",
            "Gravity uses this distinction in gradients, differential forms, metric operations, and stress-energy measurements.",
            "Without dual vectors, the course loses track of what points, what measures, and why slot positions in tensors matter.",
            "A wind arrow points east, while a toll gate counts how much eastward traffic crosses it. The gate is not another arrow; it measures arrows.",
            "A covector is not a vector drawn backwards. Its job is measurement, and that job determines how it transforms.",
            "Foundations",
            "Slot structure",
        ),
        ConceptSeed(
            "tensor-components-versus-object",
            "Tensor Components Versus The Object",
            (3,),
            ("tensor", "component", "basis", "coordinate"),
            "The course needs students to separate a tensor itself from the list of numbers used to display it in one basis.",
            "It is easy to believe the indexed array written on the page is the tensor.",
            "That fails because the numbers change when the basis changes, while the physical measuring rule should remain the same.",
            "The tensor is the coordinate-independent multilinear rule; components are the rule's numbers after choosing basis vectors and dual basis covectors.",
            "The operation is transforming components under a basis change while preserving the tensor's action on its input slots.",
            "The metric, curvature, and matter source are tensors, so their meaning cannot be tied to one convenient coordinate display.",
            "Without this distinction, students can mistake a zero, infinity, or simple-looking component for a coordinate-independent fact.",
            "A song can be printed in different keys. The notes on the page change, but the musical relation being represented is the same song.",
            "Components are useful. The mistake is treating them as the whole object rather than one display of the object.",
            "Foundations",
            "Slot structure",
        ),
        ConceptSeed(
            "tangent-vectors-as-derivatives",
            "Tangent Vectors As Derivatives",
            (5,),
            ("tangent", "derivation", "function", "direction"),
            "The course needs an internal definition of a direction at a point without drawing an arrow in a larger space.",
            "One first pictures a tangent vector as a tiny arrow touching a curve from outside.",
            "That picture fails for spacetime because there is no required outside room where the arrow is drawn.",
            "A tangent vector can be understood as a rule that tells how functions change at a point along a possible direction.",
            "The operation is applying the tangent vector to a function and reading the directional rate of change.",
            "Particle velocity, light direction, and field variation all depend on this internal notion of direction.",
            "Without this definition, tangent vectors look like imported Euclidean arrows instead of objects belonging to the manifold itself.",
            "Standing on a hillside, a direction tells how your height would change if you stepped that way. The direction can be recognized by what it does to height.",
            "A tangent vector is not merely a drawn arrow; it is a local change operator at one point.",
            "Foundations",
            "Local change",
        ),
        ConceptSeed(
            "vector-fields-as-local-instructions",
            "Vector Fields As Local Instructions",
            (6,),
            ("field", "vector field", "flow", "section"),
            "The course needs a way to assign a possible motion or instruction at every event in a region.",
            "One may imagine a field as a substance spread through space, like a colored fog.",
            "That picture fails because a field is defined by what value it assigns at each point, not by being material stuff.",
            "A vector field assigns one tangent vector to each point of the manifold in a smooth way.",
            "The operation is following the assigned directions to form flow lines or using the field to differentiate other quantities.",
            "Observers, matter flows, and symmetry directions are all described through fields that vary across spacetime.",
            "Without vector fields, the theory cannot describe continuous families of observers or local motions over a region.",
            "A traffic map with an arrow at every intersection tells drivers which way to go locally. The collection of arrows is the field.",
            "A vector field is not automatically a force field. It is any smooth assignment of directions.",
            "Foundations",
            "Local change",
        ),
        ConceptSeed(
            "covariant-derivative-corrects-comparison",
            "Covariant Derivative Corrects Comparison",
            (7,),
            ("covariant", "derivative", "connection", "change"),
            "The course needs a derivative of vector fields that does not compare vectors as if all tangent spaces were the same room.",
            "The naive move is to subtract nearby vector components the same way one subtracts ordinary arrows on graph paper.",
            "That fails because vectors at different points live in different tangent spaces, and component changes can be caused by the coordinate grid itself.",
            "A covariant derivative is the corrected change of a vector field along a direction, using a connection to say how nearby tangent spaces are compared.",
            "The operation is differentiating the field and subtracting the change caused by the moving basis or comparison rule.",
            "Free fall, geodesics, curvature, and conservation laws all require this corrected notion of change.",
            "Without the correction, the theory calls coordinate artifacts physical acceleration and loses coordinate-independent equations.",
            "If a moving walkway carries your measuring tape, a raw change in position mixes your motion with the walkway's motion. The covariant derivative separates them.",
            "Covariant does not mean complicated for its own sake. It means the derivative respects the geometric comparison rule.",
            "Geometry of Gravity",
            "Comparing nearby directions",
        ),
        ConceptSeed(
            "geodesics-free-motion",
            "Geodesics As Free Motion",
            (7, 8, 16),
            ("geodesic", "connection", "free", "motion"),
            "The course needs a precise replacement for straight-line motion when spacetime may be curved.",
            "A first picture says a free object should move in the line that looks straight on a drawing.",
            "That fails because straight-looking depends on the drawing, while free motion must be stated inside spacetime.",
            "A geodesic is a curve whose tangent direction is transported along itself according to the connection.",
            "The operation is checking whether the curve's tangent has zero covariant change along the curve.",
            "Massive particles and light rays use geodesic ideas, with the metric deciding which kind of tangent direction is allowed.",
            "Without geodesics, the phrase unforced motion has no precise meaning in curved spacetime.",
            "An airplane route on Earth may look curved on a flat map but locally follows the straightest available path on the globe.",
            "A geodesic is not always the shortest path globally. It is the path that is locally straight according to the connection.",
            "Geometry of Gravity",
            "Comparing nearby directions",
        ),
        ConceptSeed(
            "parallel-transport-loop-test",
            "Parallel Transport Loop Test",
            (8,),
            ("parallel", "transport", "loop", "curvature"),
            "The course needs an operational test for curvature that does not rely on seeing a surface bend.",
            "The visual shortcut says curvature is present only when a shape bends in a surrounding space.",
            "That fails because spacetime curvature must be detectable from operations carried out inside spacetime.",
            "The loop test carries a vector around a closed path using the connection and compares the returned vector with the starting one.",
            "The operation is parallel transport around a small loop and reading the mismatch as evidence of curvature.",
            "This matters because gravitational tidal effects are about path-dependent comparison, not visual bending.",
            "Without the loop test, curvature remains a picture instead of a measurable failure of comparison.",
            "If you carry a compass-like arrow around a triangle on a globe, it may return rotated. The rotation tells you the surface has intrinsic curvature.",
            "A nonzero loop mismatch is not bad bookkeeping. It is the geometric fact the bookkeeping reveals.",
            "Geometry of Gravity",
            "Tidal facts",
        ),
        ConceptSeed(
            "riemann-curvature-commutator",
            "Riemann Curvature As Noncommuting Change",
            (8, 9),
            ("riemann", "curvature", "commutator", "derivative"),
            "The course needs a compact way to record how two small changes in different orders fail to agree.",
            "A naive picture says small moves should commute: go north then east, or east then north, and nothing important changes.",
            "That fails on curved geometry because the comparison of directions can depend on the path taken.",
            "The Riemann curvature tensor records the failure of two covariant derivatives, taken in different orders, to give the same result.",
            "The operation is comparing the two orders of corrected differentiation and measuring the leftover mismatch.",
            "Gravity uses this because real curvature shows up as order-dependent comparison and as relative acceleration of nearby paths.",
            "Without this object, the theory cannot localize the tidal content of gravity in a coordinate-independent way.",
            "On a tilted parking ramp, two tiny moves may leave your cart facing differently depending on the order. Curvature is the exact version of that mismatch.",
            "Riemann curvature is not merely a collection of symbols. It is the record of noncommuting local comparison.",
            "Geometry of Gravity",
            "Tidal facts",
        ),
        ConceptSeed(
            "ricci-curvature-volume-change",
            "Ricci Curvature As Volume Change",
            (9, 15),
            ("ricci", "curvature", "volume", "einstein"),
            "The course needs the part of curvature that measures how a small bundle of freely moving paths changes size.",
            "It is tempting to think all curvature information must be kept in one undigested object.",
            "That fails for the field equation, which needs the curvature part tied to matter's local energy and momentum accounting.",
            "Ricci curvature is a contraction of the full curvature tensor that captures focusing or spreading of nearby geodesic families.",
            "The operation is contracting slots of the Riemann tensor to keep the part relevant for volume change.",
            "Einstein gravity uses Ricci-type curvature to connect geometry with stress-energy in the field equation.",
            "Without Ricci curvature, the bridge from tidal geometry to matter source terms becomes too blunt to state the equation cleanly.",
            "A crowd of runners can keep their individual directions but bunch together or spread out. Ricci curvature tracks that bunching behavior for free paths.",
            "Ricci curvature is not all curvature. Some curvature can remain without Ricci curvature, which matters for gravitational waves.",
            "Dynamics and Matter",
            "Geometry coupled to matter",
        ),
        ConceptSeed(
            "metric-signature-light-cones",
            "Metric Signature And Light Cones",
            (10, 13, 16),
            ("metric", "signature", "light cone", "null"),
            "The course needs a measurement rule that separates possible time-like motion, space-like separation, and light-like travel.",
            "A first distance habit says every nonzero separation should have a positive length.",
            "That fails in spacetime because time and space enter the interval differently, and light sits on a zero-interval boundary.",
            "Lorentzian signature is the metric's time-space sign pattern, and light cones are the resulting boundaries of causal influence.",
            "The operation is evaluating the metric on tangent directions and sorting them into time-like, space-like, or null.",
            "This is how gravity tells observers which events can affect which other events and which paths light can follow.",
            "Without signature and light cones, spacetime loses causal order and black holes lose their defining feature.",
            "On a road map, allowed travel may be limited by one-way streets. In spacetime, light cones are the local allowed directions for signals.",
            "A null direction is not a zero vector. It is a nonzero direction whose spacetime interval is zero.",
            "Light and Observation",
            "Causal paths",
        ),
        ConceptSeed(
            "proper-time-clock-reading",
            "Proper Time As Clock Reading",
            (10, 13),
            ("proper time", "clock", "metric", "interval"),
            "The course needs a way to say what a clock actually records along its own path through spacetime.",
            "A simple habit says time is one shared background number assigned to the whole universe.",
            "That fails in relativity because different paths through spacetime can accumulate different elapsed times.",
            "Proper time is the time measured along a time-like path by integrating the metric interval along that path.",
            "The operation is evaluating the metric on the path's tangent and adding the resulting clock increments along the path.",
            "Gravity affects clock readings because the metric that defines those increments is the gravitational field.",
            "Without proper time, gravitational time dilation and observer-dependent elapsed time become vague stories.",
            "Two travelers can leave and meet again with different wristwatch readings. Proper time is the path-based quantity their watches record.",
            "Proper time is not coordinate time. It belongs to a particular path, not to a chosen chart's time label.",
            "Geometry of Gravity",
            "Measurement becomes a field",
        ),
        ConceptSeed(
            "killing-fields-symmetry-directions",
            "Killing Fields As Symmetry Directions",
            (11,),
            ("killing", "symmetry", "field", "metric"),
            "The course needs a way to express a continuous symmetry as a direction of motion through spacetime.",
            "One may treat symmetry as a static picture that either looks balanced or does not.",
            "That fails because physical symmetry often means sliding or rotating along a flow while preserving the metric.",
            "A Killing field is a vector field whose flow leaves the metric unchanged.",
            "The operation is checking that the metric's change along the field is zero.",
            "These fields give conserved quantities for particles and make special spacetimes easier to solve.",
            "Without Killing fields, time-translation or rotation symmetry cannot be used cleanly to simplify black holes and cosmologies.",
            "If every seat in a circular theater sees the same stage after rotating labels, the rotation direction describes a preserved structure.",
            "A Killing field is not a person or observer. It is a symmetry direction in the geometry.",
            "Dynamics and Matter",
            "Sameness as a calculation",
        ),
        ConceptSeed(
            "stokes-boundary-bulk-accounting",
            "Stokes' Theorem As Boundary-Bulk Accounting",
            (12,),
            ("stokes", "boundary", "form", "integration"),
            "The course needs a rule connecting what is accumulated inside a region with what crosses its boundary.",
            "A first integration habit treats boundary terms as technical leftovers after calculation.",
            "That fails because conservation laws and variational principles depend on boundary-bulk relations having geometric meaning.",
            "Stokes' theorem says the integral of a derivative-like form over a region equals the integral of the original form over the boundary.",
            "The operation is replacing a bulk derivative integral by a boundary integral, or reading boundary data as a bulk statement.",
            "This matters for actions, conserved currents, fluxes, and the way local equations produce global statements.",
            "Without boundary-bulk accounting, the course cannot explain how local field laws control total quantities over regions.",
            "Counting people who entered a room can be done by watching the door instead of recounting the whole room. Stokes' theorem is the geometric version.",
            "The boundary term is not a nuisance. It is often where the physical accounting becomes visible.",
            "Dynamics and Matter",
            "Adding local facts",
        ),
        ConceptSeed(
            "einstein-tensor-conserved-geometry",
            "Einstein Tensor As Conserved Geometry",
            (15,),
            ("einstein tensor", "divergence", "conservation", "bianchi"),
            "The course needs the geometry side of the field equation to have the same local conservation behavior as matter.",
            "A loose picture says any curvature measure could be placed across from the matter source.",
            "That fails because the matter side obeys a conservation law, so the geometry side must have matching bookkeeping.",
            "The Einstein tensor is the curvature combination whose covariant divergence vanishes automatically.",
            "The operation is combining Ricci curvature, scalar curvature, and the metric so the result has the required conservation property.",
            "This is what makes Einstein's equation a consistent local balance between geometry and stress-energy.",
            "Without this tensor, the equation would demand matter conservation on one side while giving geometry with incompatible bookkeeping on the other.",
            "A ledger cannot balance if one column uses rules the other column does not obey. The Einstein tensor is the compatible geometry column.",
            "The Einstein tensor is not chosen because it looks elegant. It is chosen because its conservation behavior matches the source.",
            "Dynamics and Matter",
            "Geometry coupled to matter",
        ),
        ConceptSeed(
            "cosmological-constant-vacuum-term",
            "Cosmological Constant As Vacuum Term",
            (15, 21),
            ("cosmological", "constant", "vacuum", "lambda"),
            "The course needs room for a uniform term in the field equation that behaves like spacetime itself carries energy.",
            "A first source picture says only ordinary matter in a region can influence cosmic expansion.",
            "That fails because the equation permits a constant geometry-compatible term that affects large-scale evolution.",
            "The cosmological constant is a constant term in Einstein's equation, often read as a vacuum energy contribution.",
            "The operation is adding this term to the field equation and studying how it changes expansion without clumping like matter.",
            "This matters for late-time cosmology, where observed expansion cannot be explained by ordinary matter alone.",
            "Without this term or an equivalent idea, the course cannot explain why empty-looking space can affect cosmic dynamics.",
            "A monthly account can include a fixed charge even when no new item is bought. The cosmological constant is a fixed term in the gravitational account.",
            "The cosmological constant is not a small ordinary substance sprinkled through space. It acts uniformly through the equation.",
            "Applications",
            "Large-scale geometry",
        ),
        ConceptSeed(
            "redshift-as-stretched-light",
            "Redshift As Stretched Light",
            (16, 21),
            ("redshift", "light", "expansion", "wavelength"),
            "The course needs to explain how geometry changes the light that finally reaches an observer.",
            "The simple picture says redshift is always ordinary motion through fixed space, like a siren moving away.",
            "That fails in cosmology and strong gravity because the spacetime metric itself affects the measured wavelength.",
            "Redshift is the change in measured light frequency between emission and observation along a null path.",
            "The operation is comparing the light's wave direction with the emitter's and observer's time directions.",
            "This connects spacetime geometry to telescope data, cosmological expansion, and gravitational time effects.",
            "Without redshift as a geometric measurement, observations of the universe are misread as only ordinary motion.",
            "A stretched tape makes marks farther apart even if the marks did not crawl along the tape. Expanding geometry stretches light in that sense.",
            "Redshift is not one single cause. Motion, gravity, and expansion can all change the measured frequency.",
            "Light and Observation",
            "Causal paths",
        ),
        ConceptSeed(
            "gravitational-lensing-focusing",
            "Gravitational Lensing And Focusing",
            (16, 17),
            ("lensing", "focusing", "light", "geodesic"),
            "The course needs to explain why masses can change apparent positions and brightness of distant sources.",
            "A common picture says light is simply pulled sideways like a thrown pebble.",
            "That fails because light follows null geodesics of the spacetime metric, not a Newtonian projectile path.",
            "Lensing is the bending and focusing of families of null geodesics by spacetime curvature.",
            "The operation is tracking neighboring light paths and measuring how the bundle changes direction, area, or shape.",
            "This matters because lensing is one of the clearest observational ways to read gravity through light.",
            "Without lensing geometry, images, arcs, time delays, and magnification become separate tricks rather than one effect.",
            "A glass lens changes where rays meet by changing their paths. Gravity acts through spacetime geometry instead of glass.",
            "Lensing is not proof that photons have ordinary rest mass. It is a consequence of null paths in curved spacetime.",
            "Light and Observation",
            "Causal paths",
        ),
        ConceptSeed(
            "initial-data-constraints",
            "Initial Data Must Satisfy Constraints",
            (18, 19),
            ("initial", "constraint", "data", "slice"),
            "The course needs to explain why not every imagined snapshot of space can be the start of a valid spacetime.",
            "The ordinary mechanics habit says choose positions and velocities freely, then evolve them.",
            "That fails in general relativity because the geometry of one slice and its change must already satisfy constraint equations.",
            "Initial data consists of spatial geometry plus momentum-like change data that obeys Hamiltonian and momentum constraints.",
            "The operation is checking the constraint equations before using the data as a lawful starting point.",
            "This matters for numerical gravity, black-hole mergers, and wave prediction, where bad initial data creates fake physics.",
            "Without constraints, a calculation can evolve a snapshot that no solution of Einstein's equation could contain.",
            "A bridge blueprint cannot choose every beam angle independently; the pieces must already fit before construction starts.",
            "Constraints are not optional extra equations. They decide whether the starting slice belongs to any spacetime solution.",
            "Dynamics and Matter",
            "Allowed initial data",
        ),
        ConceptSeed(
            "scale-factor-expansion-history",
            "Scale Factor As Expansion History",
            (20, 21),
            ("scale factor", "expansion", "cosmology", "friedmann"),
            "The course needs one changing quantity that records how large-scale distances evolve in a smoothed universe model.",
            "A common picture says the universe expands into empty space around it.",
            "That fails because the model describes changing distances within spacetime, not motion into an outside container.",
            "The scale factor is the time-dependent multiplier that converts fixed comoving separations into physical separations.",
            "The operation is solving equations for this multiplier from matter content, curvature assumptions, and possible vacuum terms.",
            "This matters because redshift, age, expansion rate, and late-time acceleration are all read through the scale factor.",
            "Without the scale factor, cosmology becomes a story about moving galaxies instead of changing spacetime geometry.",
            "Dots printed on an elastic band get farther apart as the band stretches. The scale factor records the stretch, not a central explosion.",
            "The scale factor belongs to a simplified large-scale model. It does not describe every local gravitational detail.",
            "Applications",
            "Large-scale geometry",
        ),
        ConceptSeed(
            "hubble-rate-as-change-of-scale",
            "Hubble Rate As Change Of Scale",
            (21,),
            ("hubble", "rate", "expansion", "cosmology"),
            "The course needs a way to measure how quickly cosmic scale is changing at a given time.",
            "A first picture treats the Hubble rate as a speed of galaxies through fixed empty space.",
            "That fails because the quantity measures fractional change of the scale factor, not one object's ordinary velocity.",
            "The Hubble rate is the rate of change of the scale factor divided by the scale factor itself.",
            "The operation is comparing how fast the cosmic scale changes to the current size of that scale.",
            "This matters for reading observations into an expansion history and for connecting matter content to cosmic evolution.",
            "Without this rate, late-time cosmology cannot compare models against observed redshift-distance relations.",
            "If a rubber band grows by one centimeter, that means different things for a short band and a long band. The Hubble rate measures fractional growth.",
            "The Hubble rate is not a universal local speed limit. It is a large-scale expansion measure.",
            "Applications",
            "Large-scale geometry",
        ),
        ConceptSeed(
            "event-horizon-causal-boundary",
            "Event Horizon As Causal Boundary",
            (22, 23),
            ("event horizon", "causal", "black hole", "light"),
            "The course needs a definition of a black-hole boundary that depends on what signals can do, not on a material surface.",
            "The common picture treats the horizon as the surface of a dark object sitting in space.",
            "That fails because an event horizon is defined by the future reach of light paths in the whole spacetime.",
            "An event horizon is the boundary separating events that can send light to distant outside observers from events that cannot.",
            "The operation is tracing future-directed null paths and deciding which events can communicate outward.",
            "This matters because black holes are defined by causal structure, not by a locally visible wall.",
            "Without the causal-boundary idea, coordinate trouble near horizons is easily confused with a physical surface.",
            "A point in a river beyond the waterfall line cannot send a floating message upstream, even if nothing solid marks the line.",
            "The event horizon is global. Knowing it exactly can require knowing the future structure of spacetime.",
            "Applications",
            "Causal boundaries",
        ),
        ConceptSeed(
            "penrose-diagrams-compress-infinity",
            "Penrose Diagrams Compress Infinity",
            (23,),
            ("penrose", "diagram", "infinity", "causal"),
            "The course needs a way to draw causal structure, including infinity, without losing which light paths are possible.",
            "A normal spacetime drawing can make far-away or far-future regions impossible to see on one page.",
            "That fails for black holes because the important question is often whether signals reach infinity or a singular boundary.",
            "A Penrose diagram is a rescaled picture that preserves light-cone directions while bringing infinity to a finite edge.",
            "The operation is conformally rescaling the metric so causal directions remain visible while distances are compressed.",
            "This matters because horizons and singularities are easiest to understand by seeing causal reach at once.",
            "Without Penrose diagrams, global causal claims about black holes remain trapped in coordinate-dependent pictures.",
            "A subway map compresses long distances while preserving which stations connect. A Penrose diagram compresses spacetime while preserving light directions.",
            "A Penrose diagram does not preserve ordinary distances. It preserves causal order and null directions.",
            "Applications",
            "Causal boundaries",
        ),
        ConceptSeed(
            "gauge-versus-physical-change",
            "Gauge Change Versus Physical Change",
            (24, 25, 27),
            ("gauge", "coordinate", "physical", "perturbation"),
            "The course needs to separate a real small disturbance from a small change in how the same spacetime is described.",
            "A tempting shortcut says any change in metric components is a physical gravitational wave.",
            "That fails because changing coordinates can also change components while leaving the physical geometry unchanged.",
            "Gauge freedom is the freedom to change description without changing the physical situation.",
            "The operation is identifying which perturbation changes can be removed by a coordinate change and which remain measurable.",
            "This matters for gravitational waves because detectors respond to physical strain, not to arbitrary coordinate wiggles.",
            "Without this separation, wave calculations can report motion of the coordinate grid as if it were a real signal.",
            "Renaming streets changes the map labels but not where the buildings are. Gauge changes are the spacetime version of relabeling.",
            "Gauge is not a synonym for unimportant. It names description freedom that must be handled before identifying physical content.",
            "Light and Observation",
            "Small signals",
        ),
        ConceptSeed(
            "linearized-equations-small-disturbances",
            "Linearized Equations For Small Disturbances",
            (24, 25, 27),
            ("linearized", "perturbation", "equation", "wave"),
            "The course needs an approximation that keeps the first small effect while discarding higher-order complications.",
            "A naive split says a small problem is automatically simple without saying what has been kept or dropped.",
            "That fails because general relativity is nonlinear, so the metric affects the equation it appears in.",
            "Linearization writes the metric as a known background plus a small change and keeps only first-order terms in that change.",
            "The operation is expanding the field equation and discarding terms quadratic or higher in the small disturbance.",
            "This matters because gravitational waves and weak fields can be calculated without solving the full nonlinear equation.",
            "Without linearization, many observational predictions would be buried inside equations too hard to solve directly.",
            "For a small dent in a table, you can first estimate the height change without recalculating the whole table shape. Linearization is that controlled estimate.",
            "Linearized does not mean false. It means valid only when the small terms really remain small.",
            "Light and Observation",
            "Small signals",
        ),
        ConceptSeed(
            "quadrupole-source-changing-shape",
            "Quadrupole Sources Need Changing Shape",
            (27,),
            ("quadrupole", "source", "wave", "binary"),
            "The course needs to explain what kind of matter motion can radiate gravitational waves.",
            "A first guess says any moving mass should radiate gravity waves the way any moving charge might radiate light.",
            "That fails because mass-energy conservation removes simpler radiation patterns from the gravitational case.",
            "The quadrupole moment records the changing nonspherical distribution of mass-energy in a source.",
            "The operation is tracking how that shape-measure changes in time to estimate emitted gravitational waves.",
            "This matters because binary systems radiate strongly when their mass distribution changes shape as they orbit.",
            "Without the quadrupole idea, source lectures cannot explain why some motions radiate and others do not.",
            "Two equal dancers spinning around each other change the pattern of weight in the room. The changing pattern, not just motion, is the source clue.",
            "A single mass moving uniformly is not enough. The relevant source is changing shape in the mass-energy distribution.",
            "Light and Observation",
            "Small signals",
        ),
        ConceptSeed(
            "strain-relative-length-change",
            "Strain As Relative Length Change",
            (28,),
            ("strain", "length", "detector", "interferometer"),
            "The course needs to say what a gravitational-wave detector actually measures in ordinary terms.",
            "A loose picture says the detector hears a wave passing through it.",
            "That fails because the measured quantity is a tiny relative change in distances between freely suspended test masses.",
            "Strain is fractional length change: change in separation divided by the original separation.",
            "The operation is comparing two perpendicular arm lengths over time and reading the changing difference.",
            "This matters because interferometers turn spacetime strain into changing light interference at the detector.",
            "Without strain, gravitational-wave detection sounds mystical instead of a precise measurement of relative distance change.",
            "If a one-meter ruler changes by a hair-width and a two-meter ruler changes by twice that, the fractional strain is the shared measure.",
            "Strain is not ordinary sound pressure. It is a dimensionless measure of changing separation.",
            "Light and Observation",
            "Small signals",
        ),
        ConceptSeed(
            "interferometer-light-as-ruler",
            "Interferometer Light As A Ruler",
            (28,),
            ("interferometer", "laser", "light", "detector"),
            "The course needs to connect gravitational-wave geometry to the instrument that reads it.",
            "A simple picture says the detector directly sees spacetime stretch with a mechanical ruler.",
            "That fails because the effect is far too small and is read through light phase differences.",
            "An interferometer uses split laser light traveling along different arms as an extremely sensitive ruler.",
            "The operation is recombining the light and measuring changes in interference caused by different travel times along the arms.",
            "This matters because gravitational waves are observed through light, even though the signal is a metric disturbance.",
            "Without the interferometer idea, the final lecture cannot explain how abstract strain becomes a recorded signal.",
            "Two synchronized swimmers leaving and returning can reveal if one path took slightly longer. The interferometer does this with light.",
            "The laser is not detecting a force on photons. It is comparing path lengths through phase.",
            "Light and Observation",
            "Small signals",
        ),
    ]
)


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


def load_notes_sections() -> dict[int, list[dict[str, str]]]:
    if not NOTES_INDEX.exists():
        return {}
    sections: dict[int, list[dict[str, str]]] = {}
    for source in json.loads(NOTES_INDEX.read_text(encoding="utf-8")):
        for lecture, rel_path in source.get("lecture_sections", {}).items():
            path = ROOT / rel_path
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            sections.setdefault(int(lecture), []).append(
                {
                    "source_id": source["id"],
                    "source_title": source["title"],
                    "source_url": source["url"],
                    "text": text,
                }
            )
    return sections


def compact_snippet(text: str, max_words: int = 46) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(",.;:") + "..."


def note_snippet(section: str, keywords: tuple[str, ...], max_words: int = 54) -> str:
    compact = re.sub(r"\s+", " ", section).strip()
    lowered = compact.lower()
    best_start = 0
    for keyword in keywords:
        pos = lowered.find(keyword.lower())
        if pos >= 0:
            best_start = max(0, pos - 160)
            break
    words = compact[best_start:].split()
    return " ".join(words[:max_words]).rstrip(",.;:") + "..."


def find_note_evidence(seed: ConceptSeed, lecture_index: int, notes_sections: dict[int, list[dict[str, str]]]) -> dict[str, Any] | None:
    for section in notes_sections.get(lecture_index, []):
        text = section["text"]
        lowered = text.lower()
        if len(text.split()) < 80:
            continue
        if not any(keyword.lower() in lowered for keyword in seed.keywords):
            continue
        return {
            "id": f"ev-{seed.id}-l{lecture_index:02d}-notes",
            "concept_id": seed.id,
            "lecture_index": lecture_index,
            "lecture_title": f"Lecture {lecture_index:02d}",
            "url": section["source_url"],
            "timestamp": None,
            "snippet": note_snippet(text, seed.keywords),
            "transcript_status": "missing",
            "source_type": "external-notes",
            "note_source_id": section["source_id"],
            "note_source_title": section["source_title"],
            "confidence": "notes-backed",
            "lecture_argument": f"External notes for this lecture support the course placement of {seed.name.lower()}: {seed.ordinary_problem}",
            "mathematical_object": seed.mathematical_object,
            "operation": seed.operation,
            "why_span_matters": seed.why_for_gravity_light,
            "caveat_or_warning": "This is notes-backed because local YouTube captions are missing; verify against the video manually before treating it as transcript-backed.",
        }
    return None


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


def find_evidence(seed: ConceptSeed, records_by_index: dict[int, dict[str, Any]], notes_sections: dict[int, list[dict[str, str]]]) -> list[dict[str, Any]]:
    evidence = []
    for lecture_index in seed.lecture_indexes:
        record = records_by_index[lecture_index]
        if record.get("transcript_status") != "available":
            note_evidence = find_note_evidence(seed, lecture_index, notes_sections)
            if note_evidence is not None:
                note_evidence["lecture_title"] = record["expected_title"]
                evidence.append(note_evidence)
                continue
            evidence_id = f"ev-{seed.id}-l{lecture_index:02d}"
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
                    "source_type": "playlist-title",
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
        lowered_keywords = [k.lower() for k in seed.keywords]
        chosen_cues = []
        for cue in cues:
            text = cue["text"]
            low = text.lower()
            if any(k in low for k in lowered_keywords):
                if not chosen_cues or cue["start_seconds"] - chosen_cues[-1]["start_seconds"] > 90:
                    chosen_cues.append(cue)
            if len(chosen_cues) >= 3:
                break
        if not chosen_cues and cues:
            indexes = sorted({min(len(cues) - 1, max(0, len(cues) // div)) for div in (4, 2, 3)})
            chosen_cues = [cues[index] for index in indexes[:2]]
        for offset, chosen in enumerate(chosen_cues, start=1):
            snippet = compact_snippet(chosen["text"]) if chosen else ""
            evidence_id = f"ev-{seed.id}-l{lecture_index:02d}-{offset}"
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
                    "source_type": "youtube-transcript",
                    "confidence": "strong" if chosen and any(k in snippet.lower() for k in lowered_keywords) else "moderate",
                    "lecture_argument": f"This lecture supplies the local course context for {seed.name.lower()}: {seed.ordinary_problem}",
                    "mathematical_object": seed.mathematical_object,
                    "operation": seed.operation,
                    "why_span_matters": seed.why_for_gravity_light,
                    "caveat_or_warning": seed.common_confusion,
                }
            )
    return evidence


def attach_concept_connections(concepts: list[dict[str, Any]]) -> None:
    ordered = sorted(concepts, key=lambda item: (min(item["lecture_indexes"]), item["name"]))
    for pos, concept in enumerate(ordered):
        previous_items = ordered[max(0, pos - 3) : pos]
        later_items = ordered[pos + 1 : pos + 4]
        concept["prerequisite_ids"] = [item["id"] for item in previous_items]
        concept["later_use_ids"] = [item["id"] for item in later_items]
        prereq_names = ", ".join(item["name"] for item in previous_items) or "the ordinary idea of local comparison"
        later_names = ", ".join(item["name"] for item in later_items) or "the course's final detector story"
        concept["connective_thread"] = (
            f"This page should be read after {prereq_names}. It prepares {later_names}. "
            f"The connection is not a name chain: the earlier pages supply the object and operation that this page reuses, "
            f"and the later pages depend on this page to avoid hiding a coordinate choice, a missing measurement rule, or an unsupported physical claim."
        )


def build() -> None:
    records = load_records()
    records_by_index = {r["index"]: r for r in records}
    notes_sections = load_notes_sections()
    evidence_records: list[dict[str, Any]] = []
    concepts: list[dict[str, Any]] = []

    for seed in CONCEPTS:
        ev = find_evidence(seed, records_by_index, notes_sections)
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
    attach_concept_connections(concepts)

    lecture_atlas = []
    concept_by_lecture: dict[int, list[str]] = {}
    for concept in concepts:
        for index in concept["lecture_indexes"]:
            concept_by_lecture.setdefault(index, []).append(concept["id"])
    for record in records:
        lecture_concept_ids = concept_by_lecture.get(record["index"], [])
        lecture_notes = notes_sections.get(record["index"], [])
        lecture_atlas.append(
            {
                "index": record["index"],
                "id": record["id"],
                "title": record["expected_title"],
                "url": record["url"],
                "transcript_status": record["transcript_status"],
                "external_notes_status": "available" if lecture_notes else "missing",
                "external_note_sources": [
                    {
                        "id": item["source_id"],
                        "title": item["source_title"],
                        "url": item["source_url"],
                    }
                    for item in lecture_notes
                ],
                "word_count": record.get("word_count", 0),
                "concept_ids": lecture_concept_ids,
                "audit_note": lecture_audit_note(record, lecture_notes),
                "central_question": lecture_central_question(record, lecture_concept_ids, concepts),
                "first_principles_role": lecture_first_principles_role(record, lecture_concept_ids, concepts),
                "mathematical_objects_to_track": lecture_objects_to_track(lecture_concept_ids, concepts),
                "reader_warning": lecture_reader_warning(record, lecture_notes),
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


def lecture_audit_note(record: dict[str, Any], lecture_notes: list[dict[str, str]]) -> str:
    if record["transcript_status"] == "available":
        return f"Transcript-backed with {record.get('word_count', 0)} words available for snippet-level evidence."
    if lecture_notes:
        titles = ", ".join(item["source_title"] for item in lecture_notes)
        return f"Local transcript missing, but external notes are available from: {titles}."
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


def lecture_reader_warning(record: dict[str, Any], lecture_notes: list[dict[str, str]]) -> str:
    if record["transcript_status"] == "available":
        return "This lecture has local transcript evidence. Claims should cite snippets or timestamps when they interpret the lecture's argument."
    if lecture_notes:
        return "This lecture lacks local YouTube captions, but external notes are available. Treat notes-backed claims as useful but not identical to transcript evidence."
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
    notes_backed = [e for e in evidence if e["confidence"] == "notes-backed"]
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
        f"- External-notes-backed records: {len(notes_backed)}",
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
        "## External Notes Coverage",
        "",
    ]
    if notes_backed:
        for item in sorted(notes_backed, key=lambda ev: (ev["lecture_index"], ev["concept_id"])):
            lines.append(
                f"- Lecture {item['lecture_index']:02d}: {item['concept_id']} - notes-backed by {item.get('note_source_title', item.get('note_source_id', 'external notes'))}"
            )
    else:
        lines.append("- None.")
    lines += [
        "",
        "## Still Unsupported Concept Evidence",
        "",
    ]
    if missing_ev:
        for item in sorted(missing_ev, key=lambda ev: (ev["lecture_index"], ev["concept_id"])):
            lines.append(f"- Lecture {item['lecture_index']:02d}: {item['concept_id']} - no local transcript or notes-backed source yet.")
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
        "This is a transcript-grounded and notes-augmented atlas, not a finished lecture-note replacement. Missing subtitle lectures are separated into notes-backed records and still-unsupported placeholders.",
        "",
    ]
    (ANALYSIS / "audits").mkdir(parents=True, exist_ok=True)
    (ANALYSIS / "audits" / "atlas-validation-report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build()
