# Lecture Depth Quality Audit

- Overall status: in progress
- Central lecture pages checked: 28
- Lectures with authored teaching overrides: 16
- Remaining central lectures still using source-composed teaching layer: 12

## Finding

The lecture pages now carry a deeper teaching layer, but the first implementation
used repeated scaffolding across all lectures. That passed structural depth checks
while still reading too mechanically in places.

The repeated phrases found across all 28 pages were:

- `This lecture starts from a concrete obstruction`
- `It should not be read as a lecture about terminology`
- `The mathematical turn is to choose the right object`
- `By the time the lecture reaches`

## Work Completed

Lectures 1-16 now have authored replacements for:

- first-principles role;
- starting problem;
- mathematical turn;
- worked path through the lecture.

These cover the foundation, curvature, metric, symmetry, integration, spacetime,
matter, Einstein-equation, and first optical-geometry arc. Validation now rejects
the repeated template phrases for lectures 1-16 and checks that their
first-principles role is no longer the old generated scaffold.

## Remaining Work

Lectures 17-28 still need the same treatment. They are structurally deeper than
the old pages, but their teaching layer is still composed from concept fields.
The next pass should hand-author the remaining optical, canonical, cosmology,
black-hole, perturbation, source, and detector pages in the same style used for
lectures 1-16.
