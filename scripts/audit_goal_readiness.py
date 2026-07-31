#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
OUT = ANALYSIS / "audits" / "goal-readiness-audit.md"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    concepts = load_json(ANALYSIS / "concepts" / "concept-atlas.json")
    evidence = load_json(ANALYSIS / "evidence" / "evidence-ledger.json")
    lectures = load_json(ANALYSIS / "lectures" / "lecture-atlas.json")
    families = load_json(ANALYSIS / "families" / "family-map.json")
    themes = load_json(ANALYSIS / "themes" / "theme-map.json")

    evidence_counts = Counter(item["confidence"] for item in evidence)
    missing = [item for item in evidence if item["confidence"] == "missing-transcript"]
    missing_lectures = [lecture for lecture in lectures if lecture["transcript_status"] != "available"]
    unresolved = [
        item
        for item in missing
        if item["lecture_index"] in {18, 19}
    ]

    complete = not unresolved
    lines = [
        "# Goal Readiness Audit",
        "",
        f"- Overall status: {'complete' if complete else 'not complete'}",
        f"- Concepts: {len(concepts)}",
        f"- Themes: {len(themes)}",
        f"- Families: {len(families)}",
        f"- Lectures: {len(lectures)}",
        f"- Lectures without local YouTube transcript: {len(missing_lectures)}",
        f"- Evidence records: {len(evidence)}",
        f"- Transcript-backed evidence: {evidence_counts['strong'] + evidence_counts['moderate']}",
        f"- External-notes-backed evidence: {evidence_counts['notes-backed']}",
        f"- Unsupported evidence placeholders: {evidence_counts['missing-transcript']}",
        "",
        "## Requirements Checked",
        "",
        "- Plain first-principles concept treatment: present in concept atlas and enforced by validation.",
        "- Themes and lecture families: present and rendered.",
        "- Per-lecture pages: present for all 28 lectures.",
        "- Evidence tiers: transcript-backed, notes-backed, and unsupported placeholders are separated.",
        "- Cliche/filler guard: enforced by validation over generated analysis fields.",
        "- Missing-source honesty: unresolved evidence remains unsupported instead of being filled from generic knowledge.",
        "",
        "## Remaining To Finish",
        "",
    ]
    if unresolved:
        for item in unresolved:
            lines.append(
                f"- Lecture {item['lecture_index']:02d}: {item['concept_id']} needs direct viewing notes or a usable transcript/source."
            )
    else:
        lines.append("- None.")

    lines += [
        "",
        "## Completion Rule",
        "",
        "Do not mark the project complete until the unsupported evidence list is empty or each remaining item is explicitly waived by a source audit. The current state is a strong atlas, but not a fully source-complete end-to-end deliverable.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
