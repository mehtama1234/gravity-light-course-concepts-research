# Full Archive Scope Audit

## Current Inventory

- Full Gravity and Light channel videos identified: 41
- Central lectures already represented in the atlas: 28
- Tutorial videos rendered in the archive extension: 11
- Evening lectures rendered in the archive extension: 2
- Tutorial transcripts recovered: 9/11
- Evening lecture transcripts recovered: 2/2
- Manual-note-backed tutorial pages: 2/11

## New Source Of Truth

The full archive inventory is stored at:

- `raw-material/youtube/course-manifests/gravity-light-full-archive.json`

This manifest separates videos into:

- `central-lecture`
- `tutorial`
- `evening-lecture`

## Done State

The generated site now includes tutorial and evening-lecture archive pages in addition to the 28 central lecture pages. The central concept atlas and family maps still mainly operate on the 28 central lectures; the archive extension is a separate layer that links back to central concepts.

Tutorial caption gaps after the first recovery pass:

- Tutorial 6: Fields (`C4jJe_b0KMs`) failed subtitle download with HTTP 429.
- Tutorial 12: Integration (`iwbJvfFNRh8`) failed subtitle download with HTTP 429.

Those two gaps are now covered by timestamped local manual notes built from short audio transcription clips:

- `raw-material/manual-notes/tutorial-06-fields.md`
- `raw-material/manual-notes/tutorial-12-integration.md`

The following source-tier caveat remains after completion:

- Retry the two missing tutorial caption downloads when YouTube rate limits clear, so the manual-note-backed pages can become official-caption-backed.

## Completion Judgment

The full archive is represented in source data, rendered pages, evidence accounting, validation, audits, and source-span read-polished archive writing. The remaining caption retry is tracked as a provenance upgrade, not as missing local deliverable work.
