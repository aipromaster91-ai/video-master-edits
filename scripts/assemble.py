#!/usr/bin/env python3
"""
assemble.py — Cinematic music-video assembler (ffmpeg-powered)
=============================================================

Turns a folder of pre-cut clips + one master audio track into a finished
4K / 24fps music video, automatically applying:

  1. Native-audio muting on every clip (master song is the ONLY audio).
  2. Per-clip speed ramps (slow-mo 0.5x / fast-mo 2x / ramps).
  3. Optional watermark removal by edge-cropping.
  4. Cinematic color grade (contrast / warmth / vignette / film grain).
  5. Seamless transitions (concat + edge-fade, or xfade whip/zoom).
  6. Master-audio mux with a 1.5s end fade-out.
  7. Upscale + 24fps + H.265 (or H.264) render, clamped to exactly 3:00.

This is the runnable, deterministic equivalent of the "Master All-In-One AI
Editing Prompt" (see docs/AI_EDITING_PROMPTS.md). For true AI inpainting /
optical-flow / Topaz-style upscaling you would feed the SAME clips + manifest
to a dedicated AI tool, but this script produces a real, shippable 4K MP4
fully automatically and for free.

Usage
-----
    python3 scripts/assemble.py --config config/project_example.json
    python3 scripts/assemble.py --config config/project_example.json \
        --master-audio master_song.mp3 --output final_yash_tara_4k.mp4

Config (JSON)
-------------
{
  "master_audio": "master_song.mp3",      # optional
  "clips": [ {"file":"Clip_01_Yash.mp4", "speed":1.0}, ... ],  # optional (auto-discovered)
  "settings": {
     "clips_dir": "downloaded_clips_yash_tara",
     "width": 3840, "height": 2160, "fps": 24, "fill": true,
     "fade": 0.25,                         # per-clip edge fade (concat mode)
     "transition_mode": "concat",          # "concat" | "xfade"
     "transition": "fade",                 # xfade transition name
     "transition_duration": 0.4,
     "watermark": {"enabled": false, "filter": "crop=iw:ih-80:0:40"},
     "grade": {
        "contrast": 1.18, "brightness": 0.02, "saturation": 1.22,
        "temperature": 5800, "vignette": "PI/5", "grain": 8
     },
     "output": {
        "filename": "final_yash_tara_4k.mp4",
        "duration": 180, "fade_out": 1.5,
        "codec": "libx265", "crf": 20, "preset": "medium",
        "pix_fmt": "yuv420p"
     }
  }
}
"""
import argparse
import json
import os
import re
import subprocess

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def to_seconds(t):
    if isinstance(t, (int, float)):
        return float(t)
    parts = [float(p) for p in str(t).split(":")]
    while len(parts) < 3:
        parts = [0.0] + parts
    h, m, s = parts
    return h * 3600 + m * 60 + s


def clip_source_duration(clip, default=5.0):
    if "duration" in clip:
        return float(clip["duration"])
    if "start" in clip and "end" in clip:
        return to_seconds(clip["end"]) - to_seconds(clip["start"])
    return default


def natural_sort_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def discover_clips(clips_dir):
    exts = (".mp4", ".mkv", ".mov", ".webm", ".m4v")
    files = [f for f in os.listdir(clips_dir) if f.lower().endswith(exts)]
    files.sort(key=natural_sort_key)
    return [{"file": f, "speed": 1.0} for f in files]


# --------------------------------------------------------------------------- #
# Per-clip filter chain
# --------------------------------------------------------------------------- #
def build_clip_chain(clip, idx, settings):
    """Return a filter string that turns input [idx:v] into [cv{idx}]."""
    speed = float(clip.get("speed", 1.0))
    wm = settings.get("watermark") or {}
    W = settings["width"]
    H = settings["height"]
    fps = settings.get("fps", 24)
    fill = settings.get("fill", True)
    grade = settings.get("grade", {})
    fade = float(settings.get("fade", 0.0))

    f = []
    # 1. speed ramp (video only — clip audio is dropped)
    if abs(speed - 1.0) > 1e-3:
        f.append(f"setpts=PTS/{speed}")
    # 2. watermark removal
    if wm.get("enabled"):
        f.append(wm["filter"])
    # 3. normalize / upscale to target resolution
    if fill:
        f.append(f"scale={W}:{H}:force_original_aspect_ratio=increase")
        f.append(f"crop={W}:{H}")
    else:
        f.append(f"scale={W}:{H}:force_original_aspect_ratio=decrease")
        f.append(f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2")
    f.append("setsar=1")
    f.append(f"fps={fps}")
    f.append("format=yuv420p")
    # 4. cinematic color grade
    f.append("eq=contrast={c}:brightness={b}:saturation={s}".format(
        c=grade.get("contrast", 1.0),
        b=grade.get("brightness", 0.0),
        s=grade.get("saturation", 1.0)))
    if "temperature" in grade:
        f.append(f"colortemperature=temperature={grade['temperature']}")
    if grade.get("vignette"):
        f.append(f"vignette={grade['vignette']}")
    if grade.get("grain", 0) > 0:
        f.append(f"noise=alls={int(grade['grain'])}:allf=t")
    # 5. per-clip edge fades (smoothness in concat mode)
    disp = clip_source_duration(clip) / speed
    if fade > 0:
        f.append(f"fade=t=in:st=0:d={fade}")
        f.append(f"fade=t=out:st={max(disp - fade, 0):.3f}:d={fade}")
    return ",".join(f)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Cinematic music-video assembler")
    ap.add_argument("--config", default="config/project_example.json")
    ap.add_argument("--clips-dir", default=None, help="override clips folder")
    ap.add_argument("--master-audio", default=None, help="override master audio")
    ap.add_argument("--output", default=None, help="override output filename")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    settings = cfg.get("settings", {})
    if args.clips_dir:
        settings["clips_dir"] = args.clips_dir
    clips_dir = settings.get("clips_dir", "downloaded_clips_yash_tara")
    clips = cfg.get("clips") or discover_clips(clips_dir)
    master_audio = args.master_audio or cfg.get("master_audio")
    out = args.output or settings.get("output", {}).get("filename", "final_video.mp4")
    mode = settings.get("transition_mode", "concat")
    trans = settings.get("transition", "fade")
    trans_dur = float(settings.get("transition_duration", 0.4))

    if not clips:
        raise SystemExit(f"❌ No clips found in {clips_dir}")

    # Build per-clip filter chains: input [i:v] -> [cv{i}]
    chains = []
    for i, clip in enumerate(clips):
        path = os.path.join(clips_dir, clip["file"])
        if not os.path.exists(path):
            raise SystemExit(f"❌ Missing clip: {path}")
        chains.append((i, path, f"[{i}:v]{build_clip_chain(clip, i, settings)}[cv{i}]"))

    fc_parts = [c[2] for c in chains]
    n = len(clips)
    disp_durs = [clip_source_duration(c) / float(c.get("speed", 1.0)) for c in clips]

    if mode == "xfade":
        cur = "cv0"
        for i in range(1, n):
            offset = sum(disp_durs[:i]) - (i - 1) * trans_dur
            fc_parts.append(
                f"[{cur}][cv{i}]xfade=transition={trans}:"
                f"duration={trans_dur}:offset={offset:.3f}[x{i}]")
            cur = f"x{i}"
        video_out = cur
    else:  # concat
        labels = "".join(f"[cv{i}]" for i in range(n))
        fc_parts.append(f"{labels}concat=n={n}:v=1:a=0[outv]")
        video_out = "outv"

    inputs = [c[1] for c in chains]

    # Master audio mux + end fade + exact-duration stretch
    target = float(settings.get("output", {}).get("duration", 180))
    audio_active = bool(master_audio and os.path.exists(master_audio))
    if audio_active:
        inputs.append(master_audio)
        a_idx = len(inputs) - 1
        fade_out = float(settings.get("output", {}).get("fade_out", 1.5))
        a_chain = (f"[{a_idx}:a]loudnorm=I=-16:TP=-1.5:LRA=11,"
                   f"afade=t=out:st={max(target - fade_out, 0):.3f}:d={fade_out}[aout]")
        fc_parts.append(a_chain)
        # Stretch/shrink the video so it lands EXACTLY on the song length
        vlen = (sum(disp_durs) - (n - 1) * trans_dur) if mode == "xfade" else sum(disp_durs)
        if abs(vlen - target) > 0.2:
            stretch = target / vlen
            fc_parts.append(f"[{video_out}]setpts=PTS*{stretch:.6f}[vfin]")
            video_out = "vfin"

    maps = ["-map", f"[{video_out}]"]
    if audio_active:
        maps += ["-map", "[aout]"]

    fc = ";".join(fc_parts)

    out_set = settings.get("output", {})
    W, H = settings["width"], settings["height"]
    fps = settings.get("fps", 24)
    codec = out_set.get("codec", "libx265")
    crf = out_set.get("crf", 20)
    preset = out_set.get("preset", "medium")
    pix = out_set.get("pix_fmt", "yuv420p")

    cmd = ["ffmpeg", "-y"]
    for p in inputs:
        cmd += ["-i", p]
    cmd += ["-filter_complex", fc]
    cmd += maps
    cmd += ["-c:v", codec, "-crf", str(crf), "-preset", preset,
            "-r", str(fps), "-pix_fmt", pix,
            "-tag:v", "hvc1" if codec == "libx265" else "avc1",
            "-movflags", "+faststart"]
    if master_audio:
        cmd += ["-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]
    cmd += ["-t", str(target), out]

    if args.dry_run:
        print("FILTER_COMPLEX:\n" + fc + "\n")
        print("CMD:\n" + " ".join(cmd))
        return

    print(f"🎥 Rendering {out}  ({W}x{H} @ {fps}fps, {codec}, "
          f"{len(clips)} clips, mode={mode})")
    subprocess.run(cmd, check=True)
    print("✅ Done ->", out)


if __name__ == "__main__":
    main()
