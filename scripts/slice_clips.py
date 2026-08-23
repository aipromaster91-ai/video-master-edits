#!/usr/bin/env python3
"""
slice_clips.py — Generic, JSON-driven clip slicer (for future daily projects).
=============================================================================

Unlike slice_yash_tara.py (hard-coded to the Yash/Tara schedule), this slicer
reads a clip schedule from JSON so you can re-point it at any Hero/Heroine
pair by editing one data file.

Usage
-----
    python3 scripts/slice_clips.py --schedule config/clips_schedule_yash_tara.json

Schedule JSON
-------------
{
  "sources": { "hero": "hero_yash.mp4", "heroine": "heroine_tara.mp4" },
  "output_dir": "downloaded_clips_yash_tara",
  "clips": [
     {"source": "hero",    "start": "00:00:15", "end": "00:00:20", "name": "Clip_01_Yash.mp4"},
     {"source": "heroine", "start": "00:00:20", "end": "00:00:25", "name": "Clip_02_Tara.mp4"}
  ]
}

Each clip is sliced with `-c copy` (instant) and native audio is dropped (-an).
"""
import argparse
import json
import os
import subprocess

LABEL_KEYS = ("source", "hero", "heroine", "label")


def resolve_source(clip, sources):
    for key in LABEL_KEYS:
        if key in clip and clip[key] in sources:
            return sources[clip[key]]
    # maybe the value is already a filename
    if "source" in clip and os.path.exists(clip["source"]):
        return clip["source"]
    raise SystemExit(f"❌ Cannot resolve source for clip: {clip}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schedule", default="config/clips_schedule_yash_tara.json")
    args = ap.parse_args()

    cfg = json.load(open(args.schedule))
    sources = cfg.get("sources", {})
    out_dir = cfg.get("output_dir", "clips")
    clips = cfg["clips"]
    os.makedirs(out_dir, exist_ok=True)

    print(f"🎬 Slicing {len(clips)} clips -> {out_dir}")
    for i, clip in enumerate(clips, 1):
        src = resolve_source(clip, sources)
        if not os.path.exists(src):
            raise SystemExit(f"❌ Missing source: {src}")
        out = os.path.join(out_dir, clip["name"])
        print(f"[{i}/{len(clips)}] {clip['name']} ({clip['start']} -> {clip['end']})")
        subprocess.run(
            ["ffmpeg", "-y", "-ss", clip["start"], "-to", clip["end"],
             "-i", src, "-an", "-c", "copy", "-avoid_negative_ts", "1", out],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("✅ Done.")


if __name__ == "__main__":
    main()
