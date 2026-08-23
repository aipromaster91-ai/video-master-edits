#!/usr/bin/env python3
"""
slice_yash_tara.py
------------------
Slice the two master videos (Hero Yash + Heroine Tara Sutaria) into 36 short
clips that alternate Hero -> Heroine -> Hero ... as required.

  * Each clip is at most 5 seconds long.
  * Native audio is DROPPED here (-an) so the master song is the only audio
    in the final render (handled by scripts/assemble.py).
  * Uses `-c copy` (stream copy) so slicing is near-instant; the heavy
    re-encode happens once, in the assembler.

Input  (place in repo root before running):
    hero_yash.mp4
    heroine_tara.mp4

Output:
    downloaded_clips_yash_tara/Clip_01_Yash.mp4 ... Clip_36_Tara.mp4
"""
import os
import subprocess
import webbrowser
import shutil

hero_file = "hero_yash.mp4"
heroine_file = "heroine_tara.mp4"
output_dir = "downloaded_clips_yash_tara"
os.makedirs(output_dir, exist_ok=True)

clips_schedule = [
    {"source": hero_file, "start": "00:00:15", "end": "00:00:20", "name": "Clip_01_Yash.mp4"},
    {"source": heroine_file, "start": "00:00:20", "end": "00:00:25", "name": "Clip_02_Tara.mp4"},
    {"source": hero_file, "start": "00:00:35", "end": "00:00:40", "name": "Clip_03_Yash.mp4"},
    {"source": heroine_file, "start": "00:00:35", "end": "00:00:40", "name": "Clip_04_Tara.mp4"},
    {"source": hero_file, "start": "00:00:55", "end": "00:01:00", "name": "Clip_05_Yash.mp4"},
    {"source": heroine_file, "start": "00:00:50", "end": "00:00:55", "name": "Clip_06_Tara.mp4"},
    {"source": hero_file, "start": "00:01:15", "end": "00:01:20", "name": "Clip_07_Yash.mp4"},
    {"source": heroine_file, "start": "00:01:05", "end": "00:01:10", "name": "Clip_08_Tara.mp4"},
    {"source": hero_file, "start": "00:01:35", "end": "00:01:40", "name": "Clip_09_Yash.mp4"},
    {"source": heroine_file, "start": "00:01:20", "end": "00:01:25", "name": "Clip_10_Tara.mp4"},
    {"source": hero_file, "start": "00:01:45", "end": "00:01:50", "name": "Clip_11_Yash.mp4"},
    {"source": heroine_file, "start": "00:01:35", "end": "00:01:40", "name": "Clip_12_Tara.mp4"},
    {"source": hero_file, "start": "00:02:00", "end": "00:02:05", "name": "Clip_13_Yash.mp4"},
    {"source": heroine_file, "start": "00:01:50", "end": "00:01:55", "name": "Clip_14_Tara.mp4"},
    {"source": hero_file, "start": "00:02:10", "end": "00:02:15", "name": "Clip_15_Yash.mp4"},
    {"source": heroine_file, "start": "00:02:05", "end": "00:02:10", "name": "Clip_16_Tara.mp4"},
    {"source": hero_file, "start": "00:02:25", "end": "00:02:30", "name": "Clip_17_Yash.mp4"},
    {"source": heroine_file, "start": "00:02:20", "end": "00:02:25", "name": "Clip_18_Tara.mp4"},
    {"source": hero_file, "start": "00:02:35", "end": "00:02:40", "name": "Clip_19_Yash.mp4"},
    {"source": heroine_file, "start": "00:02:35", "end": "00:02:40", "name": "Clip_20_Tara.mp4"},
    {"source": hero_file, "start": "00:02:50", "end": "00:02:55", "name": "Clip_21_Yash.mp4"},
    {"source": heroine_file, "start": "00:02:50", "end": "00:02:55", "name": "Clip_22_Tara.mp4"},
    {"source": hero_file, "start": "00:03:05", "end": "00:03:10", "name": "Clip_23_Yash.mp4"},
    {"source": heroine_file, "start": "00:03:05", "end": "00:03:10", "name": "Clip_24_Tara.mp4"},
    {"source": hero_file, "start": "00:03:15", "end": "00:03:20", "name": "Clip_25_Yash.mp4"},
    {"source": heroine_file, "start": "00:03:20", "end": "00:03:25", "name": "Clip_26_Tara.mp4"},
    {"source": hero_file, "start": "00:03:25", "end": "00:03:30", "name": "Clip_27_Yash.mp4"},
    {"source": heroine_file, "start": "00:03:30", "end": "00:03:35", "name": "Clip_28_Tara.mp4"},
    {"source": hero_file, "start": "00:03:30", "end": "00:03:35", "name": "Clip_29_Yash.mp4"},
    {"source": heroine_file, "start": "00:03:40", "end": "00:03:45", "name": "Clip_30_Tara.mp4"},
    {"source": hero_file, "start": "00:03:40", "end": "00:03:45", "name": "Clip_31_Yash.mp4"},
    {"source": heroine_file, "start": "00:03:48", "end": "00:03:53", "name": "Clip_32_Tara.mp4"},
    {"source": hero_file, "start": "00:03:45", "end": "00:03:50", "name": "Clip_33_Yash.mp4"},
    {"source": heroine_file, "start": "00:03:55", "end": "00:04:00", "name": "Clip_34_Tara.mp4"},
    {"source": hero_file, "start": "00:03:50", "end": "00:03:55", "name": "Clip_35_Yash.mp4"},
    {"source": heroine_file, "start": "00:04:00", "end": "00:04:05", "name": "Clip_36_Tara.mp4"}
]

print("🎬 Slicing 36 clips for Yash & Tara Sutaria...")
for idx, item in enumerate(clips_schedule, 1):
    if not os.path.exists(item["source"]):
        raise SystemExit(f"❌ Missing source file: {item['source']}")
    out_path = os.path.join(output_dir, item["name"])
    print(f"[{idx}/36] {item['name']} ({item['start']} -> {item['end']})")
    subprocess.run(
        ["ffmpeg", "-y", "-ss", item["start"], "-to", item["end"],
         "-i", item["source"], "-an", "-c", "copy", "-avoid_negative_ts", "1", out_path],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
    )

print("✅ Done! Clips saved in:", output_dir)
# Open the folder cross-platform (best effort)
try:
    if shutil.which("xdg-open"):
        subprocess.run(["xdg-open", output_dir])
    elif shutil.which("explorer"):
        subprocess.run(["explorer", output_dir])
    else:
        webbrowser.open(output_dir)
except Exception:
    pass
