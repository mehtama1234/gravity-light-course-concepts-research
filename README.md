# Gravity and Light Course Concepts Research

Transcript-backed first-principles workspace for the International Winter School on
Gravity and Light 2015 central lecture course.

The goal is not a shallow playlist mirror. The generated lab should preserve the
course's mathematical arc: topology first, then manifolds, tangent spaces, fields,
connections, curvature, metric geometry, spacetime, Einstein gravity, black holes,
cosmology, perturbations, quantum matter, and gravitational waves.

## Source Playlist

- Playlist: Central Lecture Course
- URL: https://www.youtube.com/watch?v=7G4SqIboeig&list=PLFeEvEPtX_0S6vxxiiNPrJbLu9aK1UVC_
- Videos: 28

## Workflow

```bash
python3 scripts/download_youtube_course_transcripts.py
python3 scripts/download_external_notes.py
python3 scripts/build_first_principles_atlas.py
python3 scripts/build_site.py
python3 scripts/audit_goal_readiness.py
python3 scripts/validate_all.py
```

Open the local site at:

```text
site/index.html
```

## Quality Standard

Every lecture, concept, theme, subtheme, and family page must start from first
principles in plain everyday language. Formal terms are allowed only after the
page has explained the problem that forces the term to exist.

Every page must answer:

1. What ordinary problem is this mathematical idea solving?
2. What object does the lecture introduce?
3. What operation is performed on that object?
4. Why is that operation needed for gravity or light?
5. What breaks if the idea is missing?
6. What false picture does the idea replace?
7. Where does the idea reappear later in the course?
8. Which transcript span supports the explanation?

Evidence records must capture the lecture argument, not just a keyword hit.

The writing must avoid cliche, filler, and unexplained jargon. A sentence like
"curvature is important for general relativity" is not acceptable. A useful
sentence says what curvature measures, what operation reveals it, what physical
distinction it protects, and what later topic becomes confused without it.

## Source Recovery

The atlas distinguishes transcript-backed evidence, external-notes-backed
evidence, and unresolved placeholders. Unresolved canonical-formulation records
must be handled through `raw-material/manual-notes/` by direct lecture viewing
before they can be promoted.

An optional local speech-to-text helper exists at
`scripts/transcribe_audio_clip.py`. It expects `faster-whisper` in a local
`.venv-transcribe/` environment and audio files in `.cache/audio/`; both paths
are ignored by git. Use it to create timestamped raw material, then copy only
verified notes into `raw-material/manual-notes/`.
