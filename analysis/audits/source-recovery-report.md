# Source Recovery Report

## Current Result

- YouTube transcript-backed lectures: 21/28
- External-notes-backed missing-caption lectures: 10, 20, 23, 24, 25
- External notes exist but do not currently support assigned concepts: 18
- Still unresolved: 19

## YouTube Caption Check

`yt-dlp --list-subs` reports English automatic captions for lecture 10, but direct subtitle download currently fails with HTTP 429. It reports no subtitles and no automatic captions for lectures 18, 19, 20, 23, 24, and 25.

## External Sources Added

- `richie-dadhley-gravity-light-notes`: course notes PDF with sections covering 1-17, 20-26.
- `ernestyalumni-gravity-notes-grande`: supplemental notes PDF with partial course coverage.

The atlas uses these sources only as `notes-backed` evidence. It does not count them as transcript-backed evidence.

## Remaining Gap

Lecture 19, "Canonical Formulation of GR II", remains unresolved. The Richie Dadhley notes contain a lecture-19 heading, but the extracted section has no substantive notes. The current atlas keeps lecture-19 canonical evidence as unsupported instead of filling it from generic canonical-GR material.

Lecture 18 remains unresolved at the assigned-concept level. The supplemental notes index includes a lecture-18 section, but the extracted text does not contain enough canonical-formulation support for the assigned concepts. It is therefore not promoted to notes-backed evidence.

## Archive Tutorial Check

The archived `gravity-and-light.herokuapp.com/tutorials` page was checked through the Wayback CDX index. Snapshots expose the known tutorial sheets for topology, topological manifolds, multilinear algebra, differentiable manifolds, connections, parallel transport and curvature, metric manifolds, symmetry, integration, Schwarzschild/relativistic spacetime, cosmology, diagrams, and perturbation theory. No canonical-formulation tutorial sheet for lectures 18 or 19 was found. Numeric S3 row ids such as `000/000/018` refer to stored file ids, not lecture numbers.

## Manual Notes Workflow

Manual templates now exist at:

- `raw-material/manual-notes/lecture-18-canonical-formulation-gr-i.md`
- `raw-material/manual-notes/lecture-19-canonical-formulation-gr-ii.md`

These templates are not evidence yet. They become evidence only after direct video viewing fills timestamp spans, observations, concept ids, object, operation, why it matters, and caveats.

## Next Recovery Attempts

1. Retry lecture 10 YouTube captions later or through a different network/IP.
2. Check archived `gravity-and-light.org` snapshots for any lecture-specific pages not exposed by the Heroku tutorial index.
3. Check mirrors such as Bilibili only for source availability, not as evidence unless captions or notes can be extracted and cited.
4. Fill the manual-notes templates by direct video viewing before changing unsupported evidence to notes-backed.
