#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import io
from pathlib import Path

from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[1]


def decode_audio_window(path: Path, start: float, end: float, sampling_rate: int = 16000):
    import av
    import numpy as np

    resampler = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=sampling_rate)
    raw_buffer = io.BytesIO()
    dtype = None

    with av.open(str(path), mode="r", metadata_errors="ignore") as container:
        container.seek(int(start * av.time_base), any_frame=False, backward=True)
        for frame in container.decode(audio=0):
            frame_time = float(frame.time or 0.0)
            if frame_time > end:
                break
            if frame_time + float(frame.samples / frame.sample_rate) < start:
                continue
            frame.pts = None
            for resampled in resampler.resample(frame):
                array = resampled.to_ndarray()
                dtype = array.dtype
                raw_buffer.write(array)
        for resampled in resampler.resample(None):
            array = resampled.to_ndarray()
            dtype = array.dtype
            raw_buffer.write(array)

    del resampler
    gc.collect()
    audio = np.frombuffer(raw_buffer.getbuffer(), dtype=dtype)
    return audio.astype(np.float32) / 32768.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio")
    parser.add_argument("--lecture", required=True)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--duration", type=float, default=600.0)
    parser.add_argument("--model", default="tiny.en")
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--output-dir", default=".cache/transcripts")
    args = parser.parse_args()

    start = args.start
    end = start + args.duration
    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{args.lecture}-{int(start):05d}-{int(end):05d}.{args.model}.txt"

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    audio = decode_audio_window(ROOT / args.audio, start, end)
    segments, info = model.transcribe(
        audio,
        language="en",
        beam_size=1,
        vad_filter=False,
        condition_on_previous_text=False,
        max_new_tokens=args.max_new_tokens,
    )

    with output.open("w", encoding="utf-8") as handle:
        handle.write(f"lecture={args.lecture}\n")
        handle.write(f"audio={args.audio}\n")
        handle.write(f"model={args.model}\n")
        handle.write(f"clip={start:.2f},{end:.2f}\n")
        handle.write(f"language={info.language} probability={info.language_probability}\n\n")
        for segment in segments:
            handle.write(f"[{segment.start:.2f} --> {segment.end:.2f}] {segment.text.strip()}\n")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
