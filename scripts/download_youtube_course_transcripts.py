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
DEFAULT_MANIFEST = RAW / "course-manifests" / "gravity-light-central-lecture-course.json"
DEFAULT_SLUG = "gravity-light-central-lecture-course"


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, check=check)


def dump_json(cmd: list[str]) -> dict[str, Any]:
    return json.loads(subprocess.check_output(cmd, cwd=ROOT, text=True))


def paths(slug: str) -> dict[str, Path]:
    base = RAW / "transcripts" / slug
    out = {
        "base": base,
        "raw": base / "raw-vtt",
        "clean": base / "clean",
        "cues": base / "cues",
        "meta": RAW / "metadata" / slug,
        "playlists": RAW / "playlists",
    }
    for path in out.values():
        path.mkdir(parents=True, exist_ok=True)
    return out


def capture_playlist_manifest(manifest: dict[str, Any], slug: str) -> None:
    source_url = manifest.get("playlist_url") or manifest.get("channel_url")
    if not source_url:
        return
    data = dump_json(
        ["yt-dlp", "--flat-playlist", "--dump-single-json", source_url]
    )
    data.pop("epoch", None)
    (paths(slug)["playlists"] / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def video_index(video: dict[str, Any]) -> int:
    return int(video.get("index", video.get("archive_index")))


def download_video(index: int, video_id: str, slug: str) -> None:
    p = paths(slug)
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


def choose_vtt(index: int, video_id: str, slug: str) -> Path | None:
    candidates = sorted(paths(slug)["raw"].glob(f"{index:03d}-{video_id}-*.vtt"))
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


def rebuild_index(manifest: dict[str, Any], slug: str, index_output: Path, summary_output: Path, video_type: str | None = None) -> None:
    p = paths(slug)
    records = []
    videos = [
        video
        for video in manifest["videos"]
        if video_type is None or video.get("type") == video_type
    ]
    for video in videos:
        index = video_index(video)
        video_id = video["id"]
        vtt = choose_vtt(index, video_id, slug)
        if vtt is None:
            records.append(
                {
                    "id": video_id,
                    "index": index,
                    "archive_index": video.get("archive_index", index),
                    "type": video.get("type", "central-lecture"),
                    "type_index": video.get("type_index", index),
                    "related_central_lectures": video.get("related_central_lectures", []),
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
                "archive_index": video.get("archive_index", index),
                "type": video.get("type", "central-lecture"),
                "type_index": video.get("type_index", index),
                "related_central_lectures": video.get("related_central_lectures", []),
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
    index_output.write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    summary = {
        "slug": slug,
        "title": manifest["title"],
        "videos": len(videos),
        "available_transcripts": sum(r["transcript_status"] == "available" for r in records),
        "total_words": sum(r.get("word_count", 0) for r in records),
        "total_cues": sum(r.get("cue_count", 0) for r in records),
    }
    summary_output.write_text(
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
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--slug", default=DEFAULT_SLUG)
    parser.add_argument("--index-output", default=str(RAW / "transcript-index.json"))
    parser.add_argument("--summary-output", default=str(RAW / "summary.json"))
    parser.add_argument("--video-type", choices=["central-lecture", "tutorial", "evening-lecture"])
    args = parser.parse_args()
    manifest = load_manifest(ROOT / args.manifest if not Path(args.manifest).is_absolute() else Path(args.manifest))
    index_output = ROOT / args.index_output if not Path(args.index_output).is_absolute() else Path(args.index_output)
    summary_output = ROOT / args.summary_output if not Path(args.summary_output).is_absolute() else Path(args.summary_output)
    index_output.parent.mkdir(parents=True, exist_ok=True)
    summary_output.parent.mkdir(parents=True, exist_ok=True)
    if not args.summary_only:
        capture_playlist_manifest(manifest, args.slug)
        for video in manifest["videos"]:
            if args.video_type is not None and video.get("type") != args.video_type:
                continue
            download_video(video_index(video), video["id"], args.slug)
    rebuild_index(manifest, args.slug, index_output, summary_output, args.video_type)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
