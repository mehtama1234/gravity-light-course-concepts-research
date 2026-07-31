#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw-material" / "external-notes"
MANIFEST = RAW / "source-manifest.json"
PDF_DIR = RAW / "pdf"
TEXT_DIR = RAW / "text"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_manifest() -> list[dict[str, Any]]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def fetch(source: dict[str, Any]) -> Path:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    target = PDF_DIR / f"{source['id']}.pdf"
    if target.exists() and target.stat().st_size > 10_000:
        return target
    subprocess.run(
        ["curl", "-L", "--fail", "--retry", "3", "--output", str(target), source["url"]],
        cwd=ROOT,
        check=True,
    )
    return target


def extract_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            text = f"[text extraction failed on page {index}: {exc}]"
        pages.append(f"\n\n[[page {index}]]\n{text}")
    return "\n".join(pages).strip() + "\n"


def split_sections(text: str) -> dict[str, str]:
    headings = list(re.finditer(r"(?m)^(?:\d{1,2}\.?\s+)?Lecture\s+(\d{1,2})[:.\s].*$|^(?:\d{1,2})\s+([A-Z][A-Za-z].*)$", text))
    sections: dict[str, str] = {}
    for pos, match in enumerate(headings):
        lecture = match.group(1)
        if not lecture:
            heading = match.group(0).strip()
            first = heading.split(" ", 1)[0]
            lecture = first if first.isdigit() else ""
        if not lecture:
            continue
        start = match.start()
        end = headings[pos + 1].start() if pos + 1 < len(headings) else len(text)
        section = text[start:end].strip()
        if len(section.split()) >= 40:
            key = f"{int(lecture):02d}"
            if key not in sections or len(section) > len(sections[key]):
                sections[key] = section
    return sections


def main() -> int:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    for source in load_manifest():
        pdf = fetch(source)
        text = extract_pdf(pdf)
        text_path = TEXT_DIR / f"{source['id']}.txt"
        text_path.write_text(text, encoding="utf-8")
        sections = split_sections(text)
        for lecture, section in sections.items():
            section_path = TEXT_DIR / f"{source['id']}-lecture-{lecture}.txt"
            section_path.write_text(section + "\n", encoding="utf-8")
        records.append(
            {
                "id": source["id"],
                "title": source["title"],
                "url": source["url"],
                "pdf": str(pdf.relative_to(ROOT)),
                "text": str(text_path.relative_to(ROOT)),
                "lecture_sections": {
                    lecture: str((TEXT_DIR / f"{source['id']}-lecture-{lecture}.txt").relative_to(ROOT))
                    for lecture in sorted(sections)
                },
            }
        )
        print(f"{source['id']}: extracted {len(text.split())} words, {len(sections)} lecture sections")
    (RAW / "notes-index.json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
