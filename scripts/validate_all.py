#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw-material" / "youtube"
ANALYSIS = ROOT / "analysis"
SITE = ROOT / "site"

BANNED_PHRASES = (
    "deep dive",
    "math is the language",
    "unlock",
    "leveraging",
    "robust framework",
    "powerful framework",
    "game changer",
    "at the end of the day",
    "it is important because it is important",
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for key, value in attrs:
            if key == "href" and value:
                self.links.append(value)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def words(value: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", value))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def check_banned_phrases(label: str, value: str, errors: list[str]) -> None:
    lowered = value.lower()
    for phrase in BANNED_PHRASES:
        require(phrase not in lowered, f"{label} contains banned phrase: {phrase}", errors)


def validate() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    transcript_index = load_json(RAW / "transcript-index.json")
    notes_index_path = ROOT / "raw-material" / "external-notes" / "notes-index.json"
    recovery_report = ANALYSIS / "audits" / "source-recovery-report.md"
    readiness_report = ANALYSIS / "audits" / "goal-readiness-audit.md"
    manual_note_templates = [
        ROOT / "raw-material" / "manual-notes" / "lecture-18-canonical-formulation-gr-i.md",
        ROOT / "raw-material" / "manual-notes" / "lecture-19-canonical-formulation-gr-ii.md",
    ]
    concepts = load_json(ANALYSIS / "concepts" / "concept-atlas.json")
    evidence = load_json(ANALYSIS / "evidence" / "evidence-ledger.json")
    lectures = load_json(ANALYSIS / "lectures" / "lecture-atlas.json")
    themes = load_json(ANALYSIS / "themes" / "theme-map.json")
    families = load_json(ANALYSIS / "families" / "family-map.json")
    primitives = load_json(ANALYSIS / "throughlines" / "primitives.json")

    require(len(transcript_index) == 28, "transcript index must contain 28 records", errors)
    require(notes_index_path.exists(), "external notes index must exist", errors)
    require(recovery_report.exists(), "source recovery report must exist", errors)
    require(readiness_report.exists(), "goal readiness audit must exist", errors)
    for template in manual_note_templates:
        require(template.exists(), f"manual note template missing: {template.relative_to(ROOT)}", errors)
    available = [r for r in transcript_index if r["transcript_status"] == "available"]
    missing = [r for r in transcript_index if r["transcript_status"] != "available"]
    require(len(available) >= 20, "at least 20 transcripts should be available before atlas generation", errors)
    if missing:
        warnings.append(f"{len(missing)} lectures lack local transcripts and are marked for manual follow-up")

    for record in transcript_index:
        for key in ("id", "index", "expected_title", "title", "url", "transcript_status", "word_count", "cue_count"):
            require(key in record, f"transcript record {record.get('index')} missing {key}", errors)
        if record["transcript_status"] == "available":
            require(record["word_count"] > 1000, f"lecture {record['index']:02d} transcript is unexpectedly short", errors)
            require((ROOT / record["clean_txt"]).exists(), f"lecture {record['index']:02d} clean transcript missing", errors)
            require((ROOT / record["cue_json"]).exists(), f"lecture {record['index']:02d} cue json missing", errors)

    for lecture in lectures:
        for field in ("central_question", "first_principles_role", "reader_warning"):
            require(words(lecture[field]) >= 12, f"lecture {lecture['index']:02d} field {field} is too thin", errors)
        require("mathematical_objects_to_track" in lecture, f"lecture {lecture['index']:02d} missing objects to track", errors)

    concept_ids = {c["id"] for c in concepts}
    evidence_ids = {e["id"] for e in evidence}
    lecture_indexes = {l["index"] for l in lectures}
    require(len(concepts) >= 16, "concept atlas should contain at least 16 concepts", errors)
    require(len(concepts) >= 40, "robotics-grade atlas should contain at least 40 concepts", errors)
    require(len(evidence) >= 130, "robotics-grade atlas should contain at least 130 evidence records", errors)
    require(len(themes) >= 5, "theme map should contain at least 5 themes", errors)
    require(len(families) >= 6, "family map should contain at least 6 lecture families", errors)
    require(len(primitives) >= 4, "throughline primitives should contain at least 4 entries", errors)

    required_concept_fields = (
        "ordinary_problem",
        "naive_picture",
        "why_naive_fails",
        "mathematical_object",
        "operation",
        "why_for_gravity_light",
        "what_breaks_without_it",
        "worked_mini_example",
        "lecture_sequence_role",
        "common_confusion",
        "first_principles_walkthrough",
        "mathematical_detail_plain",
        "why_this_is_critical",
        "family_bridge",
        "connective_thread",
    )
    for concept in concepts:
        require(concept["id"], "concept has empty id", errors)
        for field in required_concept_fields:
            require(words(concept[field]) >= 12, f"{concept['id']} field {field} is too thin", errors)
            check_banned_phrases(f"{concept['id']} field {field}", concept[field], errors)
        for field in ("first_principles_walkthrough", "mathematical_detail_plain", "why_this_is_critical"):
            require(words(concept[field]) >= 65, f"{concept['id']} field {field} is not meaty enough", errors)
        require("prerequisite_ids" in concept, f"{concept['id']} missing prerequisite links", errors)
        require("later_use_ids" in concept, f"{concept['id']} missing later-use links", errors)
        require(words(concept["connective_thread"]) >= 35, f"{concept['id']} connective thread is too thin", errors)
        require(concept["evidence_ids"], f"{concept['id']} has no evidence ids", errors)
        for eid in concept["evidence_ids"]:
            require(eid in evidence_ids, f"{concept['id']} points to missing evidence {eid}", errors)

    for item in evidence:
        require(item["concept_id"] in concept_ids, f"evidence {item['id']} points to missing concept", errors)
        require(item["lecture_index"] in lecture_indexes, f"evidence {item['id']} points to missing lecture", errors)
        require(item["confidence"] in {"strong", "moderate", "notes-backed", "missing-transcript"}, f"evidence {item['id']} has invalid confidence", errors)
        if item["confidence"] in {"strong", "moderate"}:
            require(item["snippet"], f"transcript-backed evidence {item['id']} lacks snippet", errors)
            require(item["transcript_status"] == "available", f"evidence {item['id']} claims support without transcript", errors)
            require(item.get("source_type") == "youtube-transcript", f"evidence {item['id']} lacks youtube transcript source type", errors)
        if item["confidence"] == "notes-backed":
            require(item["snippet"], f"notes-backed evidence {item['id']} lacks snippet", errors)
            require(item["transcript_status"] == "missing", f"notes-backed evidence {item['id']} should not claim transcript availability", errors)
            require(item.get("source_type") == "external-notes", f"notes-backed evidence {item['id']} lacks external note source type", errors)
            require(item.get("note_source_id"), f"notes-backed evidence {item['id']} lacks note source id", errors)
        if item["confidence"] == "missing-transcript":
            require(not item["snippet"], f"missing-transcript evidence {item['id']} must not include snippet", errors)
            require(item.get("source_type") == "playlist-title", f"missing evidence {item['id']} must be playlist-title only", errors)
            require("manual" in item["caveat_or_warning"].lower() or "not treat" in item["caveat_or_warning"].lower(), f"missing evidence {item['id']} lacks caveat", errors)
        for field in ("lecture_argument", "mathematical_object", "operation", "why_span_matters", "caveat_or_warning"):
            require(words(item[field]) >= 8, f"evidence {item['id']} field {field} is too thin", errors)
            check_banned_phrases(f"evidence {item['id']} field {field}", item[field], errors)

    for theme in themes:
        require(theme["concept_ids"], f"theme {theme['id']} has no concepts", errors)
        require(words(theme["why_the_math_matters"]) >= 12, f"theme {theme['id']} why_the_math_matters is too thin", errors)
        for field in ("plain_question", "answer", "why_the_math_matters"):
            check_banned_phrases(f"theme {theme['id']} field {field}", theme[field], errors)

    for family in families:
        require(family["concept_ids"], f"family {family['id']} has no concepts", errors)
        for field in ("plain_problem", "mathematical_spine", "why_it_matters", "what_to_watch_for"):
            require(words(family[field]) >= 24, f"family {family['id']} field {field} is too thin", errors)
            check_banned_phrases(f"family {family['id']} field {field}", family[field], errors)

    validate_site(concepts, errors)
    return errors, warnings


def validate_site(concepts: list[dict[str, Any]], errors: list[str]) -> None:
    expected = [
        SITE / "index.html",
        SITE / "lectures.html",
        SITE / "concepts.html",
        SITE / "families.html",
        SITE / "themes.html",
        SITE / "evidence.html",
        SITE / "assets" / "styles.css",
    ]
    expected += [SITE / "concepts" / f"{concept['id']}.html" for concept in concepts]
    expected += [SITE / "lectures" / f"{index:02d}.html" for index in range(1, 29)]
    for path in expected:
        require(path.exists(), f"site file missing: {path.relative_to(ROOT)}", errors)

    for html_path in SITE.rglob("*.html"):
        parser = LinkParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        for href in parser.links:
            if href.startswith(("http://", "https://", "#")):
                continue
            target = (html_path.parent / href).resolve()
            require(target.exists(), f"broken local link from {html_path.relative_to(ROOT)} to {href}", errors)


def main() -> int:
    errors, warnings = validate()
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"validation failed with {len(errors)} errors")
        return 1
    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
