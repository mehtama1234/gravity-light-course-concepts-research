# Full Archive Scope Audit

## Current Inventory

- Full Gravity and Light channel videos identified: 41
- Central lectures already represented in the atlas: 28
- Tutorial videos still to add to the rendered atlas: 11
- Evening lectures still to add to the rendered atlas: 2
- Tutorial transcripts recovered: 9/11
- Evening lecture transcripts recovered: 2/2

## New Source Of Truth

The full archive inventory is stored at:

- `raw-material/youtube/course-manifests/gravity-light-full-archive.json`

This manifest separates videos into:

- `central-lecture`
- `tutorial`
- `evening-lecture`

## Not Done Yet

The current generated site, central transcript index, evidence ledger, and concept renderer still mainly operate on the 28 central lectures. The new full-archive manifest and the tutorial/evening transcript indexes are expansion inputs, not finished pages.

Tutorial caption gaps after the first recovery pass:

- Tutorial 6: Fields (`C4jJe_b0KMs`) failed subtitle download with HTTP 429.
- Tutorial 12: Integration (`iwbJvfFNRh8`) failed subtitle download with HTTP 429.

The following work remains before the full-archive goal can be called complete:

- Retry or manually recover the two missing tutorial transcript sources.
- Add tutorial and evening-lecture page models.
- Add tutorial and evening-lecture index pages.
- Connect tutorial videos to the central concepts they practice.
- Add evidence records for every added video.
- Update validation to require 41 represented videos and rendered pages.
- Regenerate the site and audits.

## Completion Rule

Do not mark the full-archive goal complete until all 41 videos are represented in source data, rendered pages, evidence accounting, validation, and audits.
