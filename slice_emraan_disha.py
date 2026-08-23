#!/usr/bin/env python3
"""
slice_emraan_disha.py
---------------------
Slice the Emraan Hashmi & Disha Patani masters into 36 alternating clips
(downloaded_clips_emraan_disha/). Native audio is dropped (-an) so the master
song is the only audio in the final render.
"""
import os
import subprocess
import shutil

hero_file = "hero_emraan.mp4"
heroine_file = "heroine_disha.mp4"
output_dir = "downloaded_clips_emraan_disha"
os.makedirs(output_dir, exist_ok=True)

clips_schedule = [
    {"source": hero_file, "start": "00:00:18", "end": "00:00:23", "name": "Clip_01_Emraan.mp4"},
    {"source": heroine_file, "start": "00:00:15", "end": "00:00:20", "name": "Clip_02_Disha.mp4"},
    {"source": hero_file, "start": "00:00:45", "end": "00:00:50", "name": "Clip_03_Emraan.mp4"},
    {"source": heroine_file, "start": "00:00:35", "end": "00:00:40", "name": "Clip_04_Disha.mp4"},
    {"source": hero_file, "start": "00:01:05", "end": "00:01:10", "name": "Clip_05_Emraan.mp4"},
    {"source": heroine_file, "start": "00:00:55", "end": "00:01:00", "name": "Clip_06_Disha.mp4"},
    {"source": hero_file, "start": "00:01:22", "end": "00:01:27", "name": "Clip_07_Emraan.mp4"},
    {"source": heroine_file, "start": "00:01:12", "end": "00:01:17", "name": "Clip_08_Disha.mp4"},
    {"source": hero_file, "start": "00:01:45", "end": "00:01:50", "name": "Clip_09_Emraan.mp4"},
    {"source": heroine_file, "start": "00:01:30", "end": "00:01:35", "name": "Clip_10_Disha.mp4"},
    {"source": hero_file, "start": "00:02:05", "end": "00:02:10", "name": "Clip_11_Emraan.mp4"},
    {"source": heroine_file, "start": "00:01:50", "end": "00:01:55", "name": "Clip_12_Disha.mp4"},
    {"source": hero_file, "start": "00:02:25", "end": "00:02:30", "name": "Clip_13_Emraan.mp4"},
    {"source": heroine_file, "start": "00:02:10", "end": "00:02:15", "name": "Clip_14_Disha.mp4"},
    {"source": hero_file, "start": "00:02:40", "end": "00:02:45", "name": "Clip_15_Emraan.mp4"},
    {"source": heroine_file, "start": "00:02:30", "end": "00:02:35", "name": "Clip_16_Disha.mp4"},
    {"source": hero_file, "start": "00:03:00", "end": "00:03:05", "name": "Clip_17_Emraan.mp4"},
    {"source": heroine_file, "start": "00:02:45", "end": "00:02:50", "name": "Clip_18_Disha.mp4"},
    {"source": hero_file, "start": "00:03:15", "end": "00:03:20", "name": "Clip_19_Emraan.mp4"},
    {"source": heroine_file, "start": "00:03:05", "end": "00:03:10", "name": "Clip_20_Disha.mp4"},
    {"source": hero_file, "start": "00:03:35", "end": "00:03:40", "name": "Clip_21_Emraan.mp4"},
    {"source": heroine_file, "start": "00:03:25", "end": "00:03:30", "name": "Clip_22_Disha.mp4"},
    {"source": hero_file, "start": "00:03:48", "end": "00:03:53", "name": "Clip_23_Emraan.mp4"},
    {"source": heroine_file, "start": "00:03:40", "end": "00:03:45", "name": "Clip_24_Disha.mp4"},
    {"source": hero_file, "start": "00:04:00", "end": "00:04:05", "name": "Clip_25_Emraan.mp4"},
    {"source": heroine_file, "start": "00:03:55", "end": "00:04:00", "name": "Clip_26_Disha.mp4"},
    {"source": hero_file, "start": "00:04:15", "end": "00:04:20", "name": "Clip_27_Emraan.mp4"},
    {"source": heroine_file, "start": "00:04:05", "end": "00:04:10", "name": "Clip_28_Disha.mp4"},
    {"source": hero_file, "start": "00:04:25", "end": "00:04:30", "name": "Clip_29_Emraan.mp4"},
    {"source": heroine_file, "start": "00:04:15", "end": "00:04:20", "name": "Clip_30_Disha.mp4"},
    {"source": hero_file, "start": "00:04:35", "end": "00:04:40", "name": "Clip_31_Emraan.mp4"},
    {"source": heroine_file, "start": "00:04:25", "end": "00:04:30", "name": "Clip_32_Disha.mp4"},
    {"source": hero_file, "start": "00:04:45", "end": "00:04:50", "name": "Clip_33_Emraan.mp4"},
    {"source": heroine_file, "start": "00:04:30", "end": "00:04:35", "name": "Clip_34_Disha.mp4"},
    {"source": hero_file, "start": "00:04:50", "end": "00:04:55", "name": "Clip_35_Emraan.mp4"},
    {"source": heroine_file, "start": "00:04:35", "end": "00:04:40", "name": "Clip_36_Disha.mp4"},
]

print("🎬 Slicing 36 clips for Emraan & Disha Patani...")
for item in clips_schedule:
    if not os.path.exists(item["source"]):
        raise SystemExit(f"❌ Missing source file: {item['source']}")
    out_path = os.path.join(output_dir, item["name"])
    subprocess.run(
        ["ffmpeg", "-y", "-ss", item["start"], "-to", item["end"],
         "-i", item["source"], "-an", "-c", "copy", "-avoid_negative_ts", "1", out_path],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
    )
print("✅ Done! Clips saved in:", output_dir)
try:
    if shutil.which("xdg-open"):
        subprocess.run(["xdg-open", output_dir])
    elif shutil.which("explorer"):
        subprocess.run(["explorer", output_dir])
except Exception:
    pass
