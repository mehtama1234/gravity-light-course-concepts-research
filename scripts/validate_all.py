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
    full_archive_manifest = load_json(RAW / "course-manifests" / "gravity-light-full-archive.json")
    tutorial_transcript_index = load_json(RAW / "tutorial-transcript-index.json")
    evening_transcript_index = load_json(RAW / "evening-transcript-index.json")
    notes_index_path = ROOT / "raw-material" / "external-notes" / "notes-index.json"
    recovery_report = ANALYSIS / "audits" / "source-recovery-report.md"
    readiness_report = ANALYSIS / "audits" / "goal-readiness-audit.md"
    full_archive_readiness_report = ANALYSIS / "audits" / "full-archive-readiness-audit.md"
    integrated_companion_readiness_report = ANALYSIS / "audits" / "integrated-companion-readiness-audit.md"
    archive_evidence_page = SITE / "archive-evidence.html"
    learning_path_page = SITE / "learning-path.html"
    dependency_map_page = SITE / "what-breaks.html"
    math_why_page = SITE / "the-math-why.html"
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
    archive_videos = load_json(ANALYSIS / "archive" / "video-atlas.json")
    archive_evidence = load_json(ANALYSIS / "archive" / "evidence-ledger.json")
    integration = load_json(ANALYSIS / "integration" / "concept-archive-integration.json")
    learning_path = load_json(ANALYSIS / "integration" / "learning-path.json")
    dependency_map = load_json(ANALYSIS / "integration" / "dependency-map.json")
    math_why = load_json(ANALYSIS / "integration" / "math-why.json")

    require(len(transcript_index) == 28, "transcript index must contain 28 records", errors)
    full_archive_videos = full_archive_manifest.get("videos", [])
    full_archive_ids = [item.get("id") for item in full_archive_videos]
    full_archive_types = [item.get("type") for item in full_archive_videos]
    require(len(full_archive_videos) == 41, "full archive manifest must contain 41 videos", errors)
    require(len(set(full_archive_ids)) == 41, "full archive manifest must contain 41 unique video ids", errors)
    require(full_archive_types.count("central-lecture") == 28, "full archive manifest must contain 28 central lectures", errors)
    require(full_archive_types.count("tutorial") == 11, "full archive manifest must contain 11 tutorials", errors)
    require(full_archive_types.count("evening-lecture") == 2, "full archive manifest must contain 2 evening lectures", errors)
    for item in full_archive_videos:
        for key in ("archive_index", "type", "type_index", "id", "title"):
            require(key in item, f"full archive video missing {key}: {item}", errors)
    require(len(tutorial_transcript_index) == 11, "tutorial transcript index must contain 11 records", errors)
    require(len(evening_transcript_index) == 2, "evening transcript index must contain 2 records", errors)
    require(sum(item["transcript_status"] == "available" for item in tutorial_transcript_index) >= 9, "at least 9 tutorial transcripts should be recovered", errors)
    require(sum(item["transcript_status"] == "available" for item in evening_transcript_index) == 2, "both evening lectures should have transcripts", errors)
    for item in tutorial_transcript_index:
        require(item.get("type") == "tutorial", f"tutorial transcript record has wrong type: {item.get('id')}", errors)
    for item in evening_transcript_index:
        require(item.get("type") == "evening-lecture", f"evening transcript record has wrong type: {item.get('id')}", errors)
    require(notes_index_path.exists(), "external notes index must exist", errors)
    require(recovery_report.exists(), "source recovery report must exist", errors)
    require(readiness_report.exists(), "goal readiness audit must exist", errors)
    require(full_archive_readiness_report.exists(), "full archive readiness audit must exist", errors)
    require(integrated_companion_readiness_report.exists(), "integrated companion readiness audit must exist", errors)
    require(archive_evidence_page.exists(), "archive evidence page must exist", errors)
    require(learning_path_page.exists(), "learning path page must exist", errors)
    require(dependency_map_page.exists(), "what-breaks dependency page must exist", errors)
    require(math_why_page.exists(), "mathematical why page must exist", errors)
    require("Overall status: complete" in full_archive_readiness_report.read_text(encoding="utf-8"), "full archive readiness audit must say complete", errors)
    require("Overall status: complete" in integrated_companion_readiness_report.read_text(encoding="utf-8"), "integrated companion readiness audit must say complete", errors)
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
        require(
            lecture.get("external_notes_support_status") in {"not-needed-transcript-backed", "missing", "supports-assigned-concepts", "source-present-no-assigned-support"},
            f"lecture {lecture['index']:02d} has invalid external notes support status",
            errors,
        )
        require("notes_supported_concept_ids" in lecture, f"lecture {lecture['index']:02d} missing notes-supported concept ids", errors)
        require(
            lecture.get("manual_notes_support_status") in {"missing", "supports-assigned-concepts"},
            f"lecture {lecture['index']:02d} has invalid manual notes support status",
            errors,
        )
        require("manual_notes_supported_concept_ids" in lecture, f"lecture {lecture['index']:02d} missing manual-notes-supported concept ids", errors)

    concept_ids = {c["id"] for c in concepts}
    evidence_ids = {e["id"] for e in evidence}
    lecture_indexes = {l["index"] for l in lectures}
    require(len(concepts) >= 16, "concept atlas should contain at least 16 concepts", errors)
    require(len(concepts) >= 40, "robotics-grade atlas should contain at least 40 concepts", errors)
    require(len(evidence) >= 130, "robotics-grade atlas should contain at least 130 evidence records", errors)
    require(len(themes) >= 5, "theme map should contain at least 5 themes", errors)
    require(len(families) >= 6, "family map should contain at least 6 lecture families", errors)
    require(len(primitives) >= 4, "throughline primitives should contain at least 4 entries", errors)
    require(len(archive_videos) == 13, "archive video atlas must contain 13 tutorial/evening records", errors)
    require(len(archive_evidence) == 13, "archive evidence ledger must contain 13 records", errors)
    require(len(integration) >= 20, "concept/archive integration should contain tutorial pressure-test links", errors)
    require(len(learning_path) >= 7, "learning path should contain the main course route", errors)
    require(len(dependency_map) >= 10, "dependency map should contain major failure modes", errors)
    require(len(math_why) >= 12, "mathematical why companion should contain major course moves", errors)
    require(sum(item["type"] == "tutorial" for item in archive_videos) == 11, "archive video atlas must contain 11 tutorials", errors)
    require(sum(item["type"] == "evening-lecture" for item in archive_videos) == 2, "archive video atlas must contain 2 evening lectures", errors)
    for item in archive_videos:
        for field in ("ordinary_problem", "mathematical_object", "operation", "why_it_matters", "what_breaks", "reader_warning"):
            require(words(item[field]) >= 8, f"archive video {item['slug']} field {field} is too thin", errors)
            check_banned_phrases(f"archive video {item['slug']} field {field}", item[field], errors)
        for field in ("first_principles_role", "mathematical_detail_plain", "course_connection", "source_span_read"):
            require(words(item[field]) >= 45, f"archive video {item['slug']} authored field {field} is too thin", errors)
            check_banned_phrases(f"archive video {item['slug']} authored field {field}", item[field], errors)
    for item in archive_evidence:
        require(item["confidence"] in {"strong", "manual-notes-backed", "missing-transcript"}, f"archive evidence {item['id']} has invalid confidence", errors)
        if item["confidence"] == "strong":
            require(item["snippet"], f"archive evidence {item['id']} lacks snippet", errors)
            require(item["source_type"] == "youtube-transcript", f"archive evidence {item['id']} has wrong source type", errors)
        if item["confidence"] == "manual-notes-backed":
            require(item["snippet"], f"archive manual evidence {item['id']} lacks snippet", errors)
            require(item["source_type"] == "manual-notes", f"archive manual evidence {item['id']} has wrong source type", errors)
            require(item.get("manual_note_path"), f"archive manual evidence {item['id']} lacks manual note path", errors)
        if item["confidence"] == "missing-transcript":
            require(item["source_type"] == "unsupported-placeholder", f"archive missing evidence {item['id']} has wrong source type", errors)

    archive_slugs = {item["slug"] for item in archive_videos}
    archive_evidence_ids = {item["id"] for item in archive_evidence}
    integrated_concepts = {item["concept_id"] for item in integration}
    archive_concept_ids = {concept_id for item in archive_videos for concept_id in item["concept_ids"]}
    require(archive_concept_ids <= integrated_concepts, "every archive-supported concept must have an integration pressure test", errors)
    for item in integration:
        require(item["concept_id"] in concept_ids, f"integration points to missing concept {item.get('concept_id')}", errors)
        require(item["archive_slug"] in archive_slugs, f"integration points to missing archive page {item.get('archive_slug')}", errors)
        require(item["evidence_id"] in archive_evidence_ids, f"integration points to missing archive evidence {item.get('evidence_id')}", errors)
        for field in ("pressure_test", "why_it_changes_concept", "source_span_read"):
            require(words(item[field]) >= 35, f"integration {item['concept_id']} via {item['archive_slug']} field {field} is too thin", errors)
            check_banned_phrases(f"integration {item['concept_id']} via {item['archive_slug']} field {field}", item[field], errors)
    for item in learning_path:
        require(item["concept_ids"], f"learning path {item.get('id')} lacks concepts", errors)
        require(item["archive_slugs"], f"learning path {item.get('id')} lacks archive links", errors)
        for concept_id in item["concept_ids"]:
            require(concept_id in concept_ids, f"learning path {item.get('id')} points to missing concept {concept_id}", errors)
        for slug in item["archive_slugs"]:
            require(slug in archive_slugs, f"learning path {item.get('id')} points to missing archive page {slug}", errors)
        for field in ("plain_goal", "reader_task", "payoff"):
            require(words(item[field]) >= 18, f"learning path {item.get('id')} field {field} is too thin", errors)
            check_banned_phrases(f"learning path {item.get('id')} field {field}", item[field], errors)
    for item in dependency_map:
        require(item["concept_id"] in concept_ids, f"dependency map points to missing concept {item.get('concept_id')}", errors)
        for dep in item["depends_on"]:
            require(dep in concept_ids, f"dependency map {item.get('id')} points to missing dependency {dep}", errors)
        for field in ("breaks", "repair"):
            require(words(item[field]) >= 16, f"dependency map {item.get('id')} field {field} is too thin", errors)
            check_banned_phrases(f"dependency map {item.get('id')} field {field}", item[field], errors)
    for item in math_why:
        require(item["concept_ids"], f"math why {item.get('id')} lacks concepts", errors)
        require(item["archive_slugs"], f"math why {item.get('id')} lacks archive links", errors)
        require(len(item.get("calculation", [])) >= 4, f"math why {item.get('id')} lacks step-by-step calculation", errors)
        for concept_id in item["concept_ids"]:
            require(concept_id in concept_ids, f"math why {item.get('id')} points to missing concept {concept_id}", errors)
        for slug in item["archive_slugs"]:
            require(slug in archive_slugs, f"math why {item.get('id')} points to missing archive page {slug}", errors)
        for field in ("ordinary_problem", "mathematical_move", "worked_example", "why_it_works", "payoff"):
            require(words(item[field]) >= 28, f"math why {item.get('id')} field {field} is too thin", errors)
            check_banned_phrases(f"math why {item.get('id')} field {field}", item[field], errors)
        for step_index, step in enumerate(item.get("calculation", []), start=1):
            require(words(step) >= 10, f"math why {item.get('id')} calculation step {step_index} is too thin", errors)
            check_banned_phrases(f"math why {item.get('id')} calculation step {step_index}", step, errors)

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
        require(item["confidence"] in {"strong", "moderate", "notes-backed", "manual-notes-backed", "missing-transcript"}, f"evidence {item['id']} has invalid confidence", errors)
        if item["confidence"] in {"strong", "moderate"}:
            require(item["snippet"], f"transcript-backed evidence {item['id']} lacks snippet", errors)
            require(item["transcript_status"] == "available", f"evidence {item['id']} claims support without transcript", errors)
            require(item.get("source_type") == "youtube-transcript", f"evidence {item['id']} lacks youtube transcript source type", errors)
        if item["confidence"] == "notes-backed":
            require(item["snippet"], f"notes-backed evidence {item['id']} lacks snippet", errors)
            require(item["transcript_status"] == "missing", f"notes-backed evidence {item['id']} should not claim transcript availability", errors)
            require(item.get("source_type") == "external-notes", f"notes-backed evidence {item['id']} lacks external note source type", errors)
            require(item.get("note_source_id"), f"notes-backed evidence {item['id']} lacks note source id", errors)
        if item["confidence"] == "manual-notes-backed":
            require(item["snippet"], f"manual-notes-backed evidence {item['id']} lacks snippet", errors)
            require(item["transcript_status"] == "manual-notes", f"manual-notes-backed evidence {item['id']} should use manual-notes transcript status", errors)
            require(item.get("source_type") == "manual-notes", f"manual-notes-backed evidence {item['id']} lacks manual note source type", errors)
            require(item.get("manual_note_path"), f"manual-notes-backed evidence {item['id']} lacks manual note path", errors)
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
        SITE / "tutorials.html",
        SITE / "evening-lectures.html",
        SITE / "concepts.html",
        SITE / "families.html",
        SITE / "themes.html",
        SITE / "learning-path.html",
        SITE / "what-breaks.html",
        SITE / "the-math-why.html",
        SITE / "evidence.html",
        SITE / "assets" / "styles.css",
    ]
    expected += [SITE / "concepts" / f"{concept['id']}.html" for concept in concepts]
    expected += [SITE / "lectures" / f"{index:02d}.html" for index in range(1, 29)]
    expected += [SITE / "archive" / f"{item['slug']}.html" for item in load_json(ANALYSIS / "archive" / "video-atlas.json")]
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

    integration = load_json(ANALYSIS / "integration" / "concept-archive-integration.json")
    for concept_id in {item["concept_id"] for item in integration}:
        concept_page = SITE / "concepts" / f"{concept_id}.html"
        if concept_page.exists():
            require("Tutorial Pressure Tests" in concept_page.read_text(encoding="utf-8"), f"concept page lacks tutorial pressure tests: {concept_id}", errors)
    families_page = SITE / "families.html"
    themes_page = SITE / "themes.html"
    learning_path_page = SITE / "learning-path.html"
    dependency_map_page = SITE / "what-breaks.html"
    math_why_page = SITE / "the-math-why.html"
    if families_page.exists():
        require("Tutorial pressure carried by this family" in families_page.read_text(encoding="utf-8"), "families page lacks tutorial pressure section", errors)
    if themes_page.exists():
        require("Tutorial pressure in this theme" in themes_page.read_text(encoding="utf-8"), "themes page lacks tutorial pressure section", errors)
    if learning_path_page.exists():
        text = learning_path_page.read_text(encoding="utf-8")
        require("Cross-Video Learning Path" in text and "Reader task" in text, "learning path page lacks required route language", errors)
    if dependency_map_page.exists():
        text = dependency_map_page.read_text(encoding="utf-8")
        require("What Breaks If You Skip This" in text and "Repair" in text, "dependency map page lacks failure-and-repair language", errors)
    if math_why_page.exists():
        text = math_why_page.read_text(encoding="utf-8")
        require("The Mathematical Why" in text and "Worked example" in text and "Step-by-step calculation" in text and "The One Move" in text, "math why page lacks required companion language", errors)


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
