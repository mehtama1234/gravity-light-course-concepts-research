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

## Next Recovery Attempts

1. Retry lecture 10 YouTube captions later or through a different network/IP.
2. Check archived `gravity-and-light.org` or `gravity-and-light.herokuapp.com` snapshots for lecture/tutorial sheets.
3. Check mirrors such as Bilibili only for source availability, not as evidence unless captions or notes can be extracted and cited.
4. If no source exists for lecture 19, create a manual-notes workflow that requires human viewing notes before changing unsupported evidence to notes-backed.
