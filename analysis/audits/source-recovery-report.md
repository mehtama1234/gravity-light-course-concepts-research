# Source Recovery Report

## Current Result

- YouTube transcript-backed lectures: 21/28
- External-notes-backed missing-caption lectures: 10, 20, 23, 24, 25
- Manual-notes-backed missing-caption lectures: 18, 19
- Still unsupported concept evidence: none

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

## Canonical Lecture Recovery

Lectures 18 and 19 still have no official YouTube captions. Their canonical-formulation records are now supported by local audio transcription clips that were converted into filled manual timestamp notes:

- `raw-material/manual-notes/lecture-18-canonical-formulation-gr-i.md`
- `raw-material/manual-notes/lecture-19-canonical-formulation-gr-ii.md`

Lecture 18 supports the constrained-Hamiltonian framing around 00:03:17-00:04:19 and the four-constraints/six-evolution-equations split around 00:25:42-00:27:58. Lecture 19 supports the 3+1 metric split around 00:00:20-00:01:54 and the lapse/shift non-dynamical role around 00:26:04-00:26:46.

The supplemental external notes remain insufficient for these assigned canonical concepts. The atlas therefore uses the filled manual timestamp notes as `manual-notes-backed` evidence, not as `external-notes` evidence and not as official caption evidence.

## Archive Tutorial Check

The archived `gravity-and-light.herokuapp.com/tutorials` page was checked through the Wayback CDX index. Snapshots expose the known tutorial sheets for topology, topological manifolds, multilinear algebra, differentiable manifolds, connections, parallel transport and curvature, metric manifolds, symmetry, integration, Schwarzschild/relativistic spacetime, cosmology, diagrams, and perturbation theory. No canonical-formulation tutorial sheet for lectures 18 or 19 was found. Numeric S3 row ids such as `000/000/018` refer to stored file ids, not lecture numbers.

## Manual Notes Workflow

Manual templates now exist at:

- `raw-material/manual-notes/lecture-18-canonical-formulation-gr-i.md`
- `raw-material/manual-notes/lecture-19-canonical-formulation-gr-ii.md`

These files now contain filled timestamp spans and concept ids for lectures 18 and 19. The builder reads only filled table rows as `manual-notes-backed` evidence.

## Local Speech-To-Text Attempt

A local transcription path was added with `scripts/transcribe_audio_clip.py`. It uses `faster-whisper` inside an ignored `.venv-transcribe/` environment and reads ignored audio files from `.cache/audio/`.

What was tried:

- Installed `faster-whisper` in `.venv-transcribe/`.
- Downloaded lecture 18 low-bitrate audio format 139 to `.cache/audio/018-sOiifkFYck4.m4a`.
- Downloaded lecture 19 low-bitrate audio format 139 to `.cache/audio/019-GSxuLzmHyyU.m4a`.
- Tested full-lecture transcription with `tiny.en`; it stalled in VAD before useful output.
- Patched the script to decode only requested time windows with PyAV.
- Tested 90-second and 30-second clips with VAD disabled.
- Completed 10-minute windows for lectures 18 and 19 with `tiny.en`, then promoted only selected timestamped observations to the manual-note files.

Conclusion: the transcription route is viable for targeted evidence windows on this machine. It is still not being treated as an official transcript source; promoted evidence is classified separately as `manual-notes-backed`.

## Next Recovery Attempts

1. Retry lecture 10 YouTube captions later or through a different network/IP.
2. Check archived `gravity-and-light.org` snapshots for any lecture-specific pages not exposed by the Heroku tutorial index.
3. Check mirrors such as Bilibili only for source availability, not as evidence unless captions or notes can be extracted and cited.
4. Optionally run full lecture 18/19 transcription on a faster machine/GPU if an official-quality local transcript is needed.
5. Review the filled manual-note rows against direct video playback before treating them as polished lecture notes outside this atlas.
