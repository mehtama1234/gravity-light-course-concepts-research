# Source Recovery Report

## Current Result

- YouTube transcript-backed lectures: 21/28
- External-notes-backed missing-caption lectures: 10, 20, 23, 24, 25
- External notes exist but do not currently support assigned concepts: 18
- Still unresolved: 19

## YouTube Caption Check

`yt-dlp --list-subs` reports English automatic captions for lecture 10, but direct subtitle download currently fails with HTTP 429. It reports no subtitles and no automatic captions for lectures 18, 19, 20, 23, 24, and 25.

## 2026-07-31 Caption Retry

Lecture 10 was retried through three routes:

- system `yt-dlp` subtitle download with longer sleeps
- venv `yt-dlp` with `curl_cffi` installed and Chrome impersonation
- direct `curl_cffi` request against the extracted YouTube `timedtext` VTT URL

All three routes returned HTTP 429 for the caption payload. No partial VTT was left in `raw-material/youtube/transcripts/gravity-light-central-lecture-course/raw-vtt/`.

## External Sources Added

- `richie-dadhley-gravity-light-notes`: course notes PDF with sections covering 1-17, 20-26.
- `ernestyalumni-gravity-notes-grande`: supplemental notes PDF with partial course coverage.

The atlas uses these sources only as `notes-backed` evidence. It does not count them as transcript-backed evidence.

## Remaining Gap

Lecture 19, "Canonical Formulation of GR II", remains unresolved. The Richie Dadhley notes contain a lecture-19 heading, but the extracted section has no substantive notes. The current atlas keeps lecture-19 canonical evidence as unsupported instead of filling it from generic canonical-GR material.

Lecture 18 remains unresolved at the assigned-concept level. The supplemental notes index includes a lecture-18 section, but the extracted text is mostly symmetry/tutorial material and does not contain enough canonical-formulation support for the assigned concepts. It is therefore marked as a source gap, not promoted to notes-backed evidence.

## Archive Tutorial Check

The archived `gravity-and-light.herokuapp.com/tutorials` page was checked through the Wayback CDX index. Snapshots expose the known tutorial sheets for topology, topological manifolds, multilinear algebra, differentiable manifolds, connections, parallel transport and curvature, metric manifolds, symmetry, integration, Schwarzschild/relativistic spacetime, cosmology, diagrams, and perturbation theory. No canonical-formulation tutorial sheet for lectures 18 or 19 was found. Numeric S3 row ids such as `000/000/018` refer to stored file ids, not lecture numbers.

## Manual Notes Workflow

Manual templates now exist at:

- `raw-material/manual-notes/lecture-18-canonical-formulation-gr-i.md`
- `raw-material/manual-notes/lecture-19-canonical-formulation-gr-ii.md`

These templates are not evidence yet. They become evidence only after direct video viewing fills timestamp spans, observations, concept ids, object, operation, why it matters, and caveats.

## Local Speech-To-Text Attempt

A local transcription path was added with `scripts/transcribe_audio_clip.py`. It uses `faster-whisper` inside an ignored `.venv-transcribe/` environment and reads ignored audio files from `.cache/audio/`.

What was tried:

- Installed `faster-whisper` in `.venv-transcribe/`.
- Downloaded lecture 18 low-bitrate audio format 139 to `.cache/audio/018-sOiifkFYck4.m4a`.
- Tested full-lecture transcription with `tiny.en`; it stalled in VAD before useful output.
- Patched the script to decode only requested time windows with PyAV.
- Tested 90-second and 30-second clips with VAD disabled; both reached Whisper generation but were too slow for interactive completion on the current CPU.

Conclusion: the transcription route is viable as tooling, but not practical on this machine/session without faster hardware, a smaller/faster runtime, or a hosted speech-to-text service. No machine transcript was promoted to evidence.

## Next Recovery Attempts

1. Retry lecture 10 YouTube captions later or through a different network/IP.
2. Check archived `gravity-and-light.org` snapshots for any lecture-specific pages not exposed by the Heroku tutorial index.
3. Check mirrors such as Bilibili only for source availability, not as evidence unless captions or notes can be extracted and cited.
4. Run `scripts/transcribe_audio_clip.py` on a faster machine/GPU, then fill the manual-notes templates from timestamped transcript spans.
5. Fill the manual-notes templates by direct video viewing before changing unsupported evidence to notes-backed.
