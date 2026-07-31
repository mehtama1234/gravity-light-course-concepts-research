#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw-material" / "youtube"
MANIFEST = RAW / "course-manifests" / "gravity-light-central-lecture-course.json"
SLUG = "gravity-light-central-lecture-course"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, check=check)


def dump_json(cmd: list[str]) -> dict[str, Any]:
    return json.loads(subprocess.check_output(cmd, cwd=ROOT, text=True))


def paths() -> dict[str, Path]:
    base = RAW / "transcripts" / SLUG
    out = {
        "base": base,
        "raw": base / "raw-vtt",
        "clean": base / "clean",
        "cues": base / "cues",
        "meta": RAW / "metadata" / SLUG,
        "playlists": RAW / "playlists",
    }
    for path in out.values():
        path.mkdir(parents=True, exist_ok=True)
    return out


def capture_playlist_manifest(manifest: dict[str, Any]) -> None:
    data = dump_json(
        ["yt-dlp", "--flat-playlist", "--dump-single-json", manifest["playlist_url"]]
    )
    data.pop("epoch", None)
    (paths()["playlists"] / f"{SLUG}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def download_video(index: int, video_id: str) -> None:
    p = paths()
    output_tpl = str(p["raw"] / f"{index:03d}-%(id)s-%(title).120B.%(ext)s")
    result = run(
        [
            "yt-dlp",
            "--skip-download",
            "--write-info-json",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            "en,en-US,en-orig",
            "--sub-format",
            "vtt",
            "--sleep-requests",
            "1",
            "--sleep-interval",
            "1",
            "-o",
            output_tpl,
            video_url(video_id),
        ],
        check=False,
    )
    for info in p["raw"].glob(f"{index:03d}-{video_id}-*.info.json"):
        target = p["meta"] / info.name
        if target.exists():
            target.unlink()
        info.replace(target)
    print(f"{index:03d} {video_id} rc={result.returncode}")


def parse_timestamp(value: str) -> float:
    hours, minutes, rest = value.split(":")
    seconds = float(rest)
    return int(hours) * 3600 + int(minutes) * 60 + seconds


def clean_line(line: str) -> str:
    line = re.sub(r"<[^>]+>", "", line)
    line = (
        line.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )
    return re.sub(r"\s+", " ", line).strip()


def parse_vtt(path: Path) -> tuple[str, list[dict[str, Any]]]:
    cues: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    text_lines: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or line.startswith(("Kind:", "Language:")):
            continue
        if "-->" in line:
            start, end = [part.strip().split(" ")[0] for part in line.split("-->", 1)]
            current = {
                "start": start,
                "end": end,
                "start_seconds": parse_timestamp(start),
                "end_seconds": parse_timestamp(end),
                "text": [],
            }
            cues.append(current)
            continue
        if re.match(r"^\d+$", line):
            continue
        cleaned = clean_line(line)
        if not cleaned:
            continue
        if current is not None:
            if not current["text"] or current["text"][-1] != cleaned:
                current["text"].append(cleaned)
        text_lines.append(cleaned)

    compact_cues: list[dict[str, Any]] = []
    for cue in cues:
        joined = " ".join(cue["text"]).strip()
        if not joined:
            continue
        compact_cues.append({**cue, "text": joined})

    deduped: list[str] = []
    for line in text_lines:
        if not deduped or deduped[-1] != line:
            deduped.append(line)
    return "\n".join(deduped).strip() + "\n", compact_cues


def choose_vtt(index: int, video_id: str) -> Path | None:
    candidates = sorted(paths()["raw"].glob(f"{index:03d}-{video_id}-*.vtt"))
    if not candidates:
        return None
    ranks = []
    for item in candidates:
        name = item.name
        if name.endswith(".en-US.vtt"):
            rank = 0
        elif name.endswith(".en.vtt"):
            rank = 1
        elif name.endswith(".en-orig.vtt"):
            rank = 2
        else:
            rank = 9
        ranks.append((rank, item))
    return sorted(ranks, key=lambda pair: (pair[0], pair[1].name))[0][1]


def rebuild_index() -> None:
    manifest = load_manifest()
    p = paths()
    records = []
    for video in manifest["videos"]:
        index = video["index"]
        video_id = video["id"]
        vtt = choose_vtt(index, video_id)
        if vtt is None:
            records.append(
                {
                    "id": video_id,
                    "index": index,
                    "expected_title": video["title"],
                    "title": video["title"],
                    "url": video_url(video_id),
                    "transcript_status": "missing",
                    "word_count": 0,
                    "cue_count": 0,
                }
            )
            continue
        clean_text, cues = parse_vtt(vtt)
        clean_path = p["clean"] / f"{index:03d}-{video_id}.txt"
        cue_path = p["cues"] / f"{index:03d}-{video_id}.json"
        clean_path.write_text(clean_text, encoding="utf-8")
        cue_path.write_text(json.dumps(cues, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        meta_files = sorted(p["meta"].glob(f"{index:03d}-{video_id}-*.info.json"))
        metadata = json.loads(meta_files[0].read_text(encoding="utf-8")) if meta_files else {}
        records.append(
            {
                "id": video_id,
                "index": index,
                "expected_title": video["title"],
                "title": metadata.get("title", video["title"]),
                "url": video_url(video_id),
                "duration": metadata.get("duration"),
                "channel": metadata.get("channel"),
                "clean_txt": str(clean_path.relative_to(ROOT)),
                "cue_json": str(cue_path.relative_to(ROOT)),
                "raw_vtt": str(vtt.relative_to(ROOT)),
                "word_count": len(clean_text.split()),
                "cue_count": len(cues),
                "transcript_status": "available",
            }
        )
    (RAW / "transcript-index.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    summary = {
        "slug": SLUG,
        "title": manifest["title"],
        "videos": len(manifest["videos"]),
        "available_transcripts": sum(r["transcript_status"] == "available" for r in records),
        "total_words": sum(r.get("word_count", 0) for r in records),
        "total_cues": sum(r.get("cue_count", 0) for r in records),
    }
    (RAW / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"indexed {summary['available_transcripts']}/{summary['videos']} transcripts, "
        f"{summary['total_words']} words"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()
    manifest = load_manifest()
    if not args.summary_only:
        capture_playlist_manifest(manifest)
        for video in manifest["videos"]:
            download_video(video["index"], video["id"])
    rebuild_index()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
