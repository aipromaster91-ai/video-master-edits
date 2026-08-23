#!/usr/bin/env python3
"""
slice_aryan_kriti.py
--------------------
Slice the Aryan Khan & Kriti Sanon masters into 36 alternating clips
(downloaded_clips_aryan_kriti/). Native audio is dropped (-an) so the master
song is the only audio in the final render.
"""
import os
import subprocess
import shutil

hero_file = "hero_aryan.mp4"
heroine_file = "heroine_kriti.mp4"
output_dir = "downloaded_clips_aryan_kriti"
os.makedirs(output_dir, exist_ok=True)

clips_schedule = [
    {"source": hero_file, "start": "00:00:06", "end": "00:00:11", "name": "Clip_01_Aryan.mp4"},
    {"source": heroine_file, "start": "00:00:45", "end": "00:00:50", "name": "Clip_02_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:16", "end": "00:00:21", "name": "Clip_03_Aryan.mp4"},
    {"source": heroine_file, "start": "00:01:10", "end": "00:01:15", "name": "Clip_04_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:28", "end": "00:00:33", "name": "Clip_05_Aryan.mp4"},
    {"source": heroine_file, "start": "00:01:25", "end": "00:01:30", "name": "Clip_06_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:40", "end": "00:00:45", "name": "Clip_07_Aryan.mp4"},
    {"source": heroine_file, "start": "00:01:40", "end": "00:01:45", "name": "Clip_08_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:50", "end": "00:00:55", "name": "Clip_09_Aryan.mp4"},
    {"source": heroine_file, "start": "00:02:05", "end": "00:02:10", "name": "Clip_10_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:56", "end": "00:01:01", "name": "Clip_11_Aryan.mp4"},
    {"source": heroine_file, "start": "00:02:20", "end": "00:02:25", "name": "Clip_12_Kriti.mp4"},
    {"source": hero_file, "start": "00:01:01", "end": "00:01:06", "name": "Clip_13_Aryan.mp4"},
    {"source": heroine_file, "start": "00:02:35", "end": "00:02:40", "name": "Clip_14_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:20", "end": "00:00:25", "name": "Clip_15_Aryan.mp4"},
    {"source": heroine_file, "start": "00:02:50", "end": "00:02:55", "name": "Clip_16_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:35", "end": "00:00:40", "name": "Clip_17_Aryan.mp4"},
    {"source": heroine_file, "start": "00:03:05", "end": "00:03:10", "name": "Clip_18_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:45", "end": "00:00:50", "name": "Clip_19_Aryan.mp4"},
    {"source": heroine_file, "start": "00:03:20", "end": "00:03:25", "name": "Clip_20_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:52", "end": "00:00:57", "name": "Clip_21_Aryan.mp4"},
    {"source": heroine_file, "start": "00:03:30", "end": "00:03:35", "name": "Clip_22_Kriti.mp4"},
    {"source": hero_file, "start": "00:01:03", "end": "00:01:08", "name": "Clip_23_Aryan.mp4"},
    {"source": heroine_file, "start": "00:03:45", "end": "00:03:50", "name": "Clip_24_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:10", "end": "00:00:15", "name": "Clip_25_Aryan.mp4"},
    {"source": heroine_file, "start": "00:03:55", "end": "00:04:00", "name": "Clip_26_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:22", "end": "00:00:27", "name": "Clip_27_Aryan.mp4"},
    {"source": heroine_file, "start": "00:04:05", "end": "00:04:10", "name": "Clip_28_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:30", "end": "00:00:35", "name": "Clip_29_Aryan.mp4"},
    {"source": heroine_file, "start": "00:04:15", "end": "00:04:20", "name": "Clip_30_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:48", "end": "00:00:53", "name": "Clip_31_Aryan.mp4"},
    {"source": heroine_file, "start": "00:04:25", "end": "00:04:30", "name": "Clip_32_Kriti.mp4"},
    {"source": hero_file, "start": "00:00:58", "end": "00:01:03", "name": "Clip_33_Aryan.mp4"},
    {"source": heroine_file, "start": "00:04:35", "end": "00:04:40", "name": "Clip_34_Kriti.mp4"},
    {"source": hero_file, "start": "00:01:06", "end": "00:01:10", "name": "Clip_35_Aryan.mp4"},
    {"source": heroine_file, "start": "00:00:52", "end": "00:00:57", "name": "Clip_36_Kriti.mp4"},
]

print("🎬 Slicing 36 clips for Aryan Khan & Kriti Sanon...")
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
