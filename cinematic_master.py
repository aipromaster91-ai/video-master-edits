#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 CINEMATIC MUSIC-VIDEO MASTER PIPELINE  (AUDIO-FREE BUILD)
================================================================================
Implements the "world-class music-video editor" spec from the project prompt,
EXCEPT the master audio track (added later by the user). Everything else is done:

  1. TIMELINE / DURATION ........ normalise every clip, trim final to N seconds
  2. WATERMARK / LOGO CLEANUP ... smart-crop to 16:9 + delogo on all 4 corners
  3. BEAT-STYLE SPEED RAMPING ... per-clip setpts rhythm (slow / normal / fast)
  4. SEAMLESS TRANSITIONS ....... chained xfade (whip-pan / zoom / flash / wipe)
  5. STUDIO COLOR GRADE ......... teal-orange filmic (eq + colorbalance + curves)
                                  + bloom + 35mm grain + vignette (uniform look)
  6. 4K MASTER EXPORT ........... spline upscale to 3840x2160, 24fps cinema,
                                  H.264 high-bitrate (HEVC option), muted audio

DAILY USAGE
-----------
You (the user) just send:
    - 2 source video files (hero + heroine), and
    - your clip schedule (the same `clips_schedule` list from your slice_*.py).

I convert that into:
    sources.json   -> {"hero": {"file": "hero_emraan.mp4", "url": "<YT url>"},
                       "heroine": {"file": "heroine_disha.mp4", "url": "<YT url>"}}
    schedule.json  -> [{"source":"hero","start":"00:00:18","end":"00:00:23"},
                       {"source":"heroine","start":"00:00:15","end":"00:00:20"}, ...]

then run:
    python3 cinematic_master.py --out "Mousam Barish Ka.mp4" --out-res 2160

CL = command line, fully overridable (resolution, transition length, target
length, speed pattern, grain, etc.). See --help.
================================================================================
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FFPROBE = os.environ.get("FFPROBE", "ffprobe")  # optional; we fall back to ffmpeg -i

# "Elite" xfade transitions cycled across the cut points -> whip-pan / zoom /
# flash / film-burn feel (no generic hard cuts).
TRANSITIONS = [
    "smoothleft", "smoothright", "smoothup", "smoothdown",  # whip pans
    "zoomin", "diagtl", "diagbr", "slideup", "slidedown",   # kinetic zooms
    "circleopen", "circleclose", "dissolve", "fadeblack",   # flash / burns
]

# Rhythm table simulating verse/chorus pacing. Index % len -> speed factor.
# <1.0 = optical-flow-style slow motion, >1.0 = speed-up.
RHYTHM = [0.75, 1.0, 1.25, 1.0, 0.8, 1.4, 1.0, 0.7]


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def run(cmd, check=True, capture=False):
    """Run a command, streaming or capturing output."""
    if isinstance(cmd, str):
        printable = cmd
        shell = True
    else:
        printable = " ".join(shlex.quote(c) for c in cmd)
        shell = False
    print("    $ " + printable, flush=True)
    return subprocess.run(
        cmd if shell else cmd,
        shell=shell,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def probe_duration(path):
    """Duration of a file via ffprobe if available, else ffmpeg -i parsing."""
    try:
        out = subprocess.run(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            check=True, text=True, capture_output=True)
        return float(out.stdout.strip())
    except Exception:
        out = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                             capture_output=True, text=True)
        import re
        m = re.search(r"Duration:\s(\d+):(\d+):(\d+\.\d+)", out.stderr)
        if not m:
            return 0.0
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def hms_to_seconds(t):
    parts = [float(p) for p in str(t).split(":")]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


# --------------------------------------------------------------------------- #
# per-clip normalisation (geometry + watermark + speed + fps) -- LIGHT pass
# --------------------------------------------------------------------------- #
def render_intermediate(src_file, start, end, idx, workdir, args):
    """
    Extract [start,end] from src_file and produce a normalised intermediate:
      - scaled + centre-cropped to INTERNAL res (16:9)
      - delogo on all 4 corners (watermark / channel-logo removal)
      - per-clip speed factor applied (rhythm)
      - constant 24 fps, yuv420p, NO audio
    """
    w, h = args.internal_w, args.internal_h
    kw, kh = int(w * args.delogo_w_frac), int(h * args.delogo_h_frac)

    speed = args.flat_speed if args.flat_speed else RHYTHM[idx % len(RHYTHM)]

    # delogo boxes for the four corners (must stay strictly inside the frame:
    # delogo interpolates from a 1px border around the rect, so leave 1px margin)
    delogos = ",".join([
        f"delogo=x=1:y=1:w={kw}:h={kh}:show=0",
        f"delogo=x={w - kw - 1}:y=1:w={kw}:h={kh}:show=0",
        f"delogo=x=1:y={h - kh - 1}:w={kw}:h={kh}:show=0",
        f"delogo=x={w - kw - 1}:y={h - kh - 1}:w={kw}:h={kh}:show=0",
    ])

    vf = (
        f"scale={w}:{h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{h},setsar=1,"
        f"{delogos},"
        f"setpts=PTS/{speed},"
        f"fps={args.fps},"
        f"format=yuv420p"
    )

    out = os.path.join(workdir, f"clip_{idx:02d}.mp4")
    cmd = [
        FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
        "-ss", str(hms_to_seconds(start)),
        "-to", str(hms_to_seconds(end)),
        "-i", src_file,
        "-an",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-pix_fmt", "yuv420p",
        out,
    ]
    run(cmd)
    # analytical duration (post-speed) -> exact value for the xfade offsets
    seg = hms_to_seconds(end) - hms_to_seconds(start)
    dur = seg / speed
    print(f"    clip {idx:02d}: speed={speed}x  ->  {dur:.2f}s")
    return out, dur


# --------------------------------------------------------------------------- #
# master merge: chained xfade + uniform grade + bloom + grain + 4K upscale
# --------------------------------------------------------------------------- #
def render_master(intermediates, durs, args, out_path):
    n = len(intermediates)
    T = min(args.transition, min(durs) * 0.5) if durs else args.transition

    inputs = []
    for p in intermediates:
        inputs += ["-i", p]

    # ---- build chained xfade graph ----
    fc, cur_label = [], "[0:v]"
    cur_len = durs[0]
    for i in range(1, n):
        offset = max(0.0, cur_len - T)
        trans = TRANSITIONS[(i - 1) % len(TRANSITIONS)]
        out_lbl = f"[x{i}]"
        fc.append(
            f"{cur_label}[{i}:v]xfade=transition={trans}:"
            f"duration={T:.3f}:offset={offset:.3f}{out_lbl}"
        )
        cur_label = out_lbl
        cur_len = offset + durs[i]

    merged = cur_label  # label of fully-merged stream

    # ---- uniform cinematic grade + bloom + grain + vignette + 4K upscale ----
    ow, oh = args.out_w, args.out_h
    grade = (
        f"scale={ow}:{oh}:flags=lanczos,"
        f"unsharp=5:5:0.6:5:5:0.2,"                          # detail after upscale
        f"eq=contrast={args.contrast}:saturation={args.saturation}:gamma={args.gamma},"
        f"colorbalance="
        f"rs={-args.teal_orange}:gs=0.02:bs={args.teal_orange}:"    # teal shadows
        f"rh={args.teal_orange}:gh=0.02:bh={-args.teal_orange},"   # orange highs
        f"curves=master='0/0 0.25/0.20 0.5/0.52 0.75/0.83 1/1'"
    )
    bloom = args.bloom
    grain = args.grain
    # upscale + uniform cinematic grade, THEN bloom (split+blur+screen-blend),
    # temporal 35mm grain, and vignette.
    polish = (
        f"{merged}{grade}[graded];"
        f"[graded]split=2[base][glow];"
        f"[glow]gblur=sigma={args.bloom_sigma}[glow];"
        f"[base][glow]blend=all_mode=screen:all_opacity={bloom}[blended];"
        f"[blended]noise=alls={grain}:allf=t+0,"
        f"vignette=PI/{args.vignette},format=yuv420p[vout]"
    )
    fc.append(polish)
    filter_complex = ";".join(fc)

    encoder = ["-c:v", "libx265" if args.codec == "hevc" else "libx264"]
    extra = []
    if args.codec == "hevc":
        extra += ["-preset", "medium", "-x265-params",
                  "log-level=error:colorprim=bt709:transfer=bt709:colormatrix=bt709",
                  "-crf", str(args.crf), "-tag:v", "hvc1", "-pix_fmt", "yuv420p"]
    else:
        extra += ["-preset", args.preset, "-crf", str(args.crf), "-pix_fmt", "yuv420p"]

    cmd = [
        FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-an",
        "-r", str(args.fps),
        *(["-t", str(args.target)] if args.target else []),
        *encoder, *extra,
        "-movflags", "+faststart",
        out_path,
    ]
    run(cmd)
    print(f"\n    MASTER rendered: {out_path}  ({probe_duration(out_path):.2f}s, "
          f"{ow}x{oh}, {args.codec})")


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Cinematic music-video master (audio-free)")
    ap.add_argument("--sources", default="sources.json")
    ap.add_argument("--schedule", default="schedule.json")
    ap.add_argument("--out", required=True, help="output file, e.g. 'Mousam Barish Ka.mp4'")
    # resolution
    ap.add_argument("--internal", default="1080", choices=["720", "1080", "1440"],
                    help="working resolution for xfade merge")
    ap.add_argument("--out-res", default="2160", choices=["1080", "1440", "2160", "4320"],
                    help="final master resolution (2160=4K, 4320=8K)")
    ap.add_argument("--fps", type=int, default=24)
    # rhythm / transitions
    ap.add_argument("--transition", type=float, default=0.45,
                    help="xfade duration (s)")
    ap.add_argument("--flat-speed", type=float, default=0.0,
                    help="if >0, override rhythm with a single speed factor")
    ap.add_argument("--target", type=float, default=180.0,
                    help="trim final to N seconds (0 = no trim)")
    # grade / look
    ap.add_argument("--contrast", type=float, default=1.14)
    ap.add_argument("--saturation", type=float, default=1.18)
    ap.add_argument("--gamma", type=float, default=0.97)
    ap.add_argument("--teal-orange", type=float, default=0.08)
    ap.add_argument("--bloom", type=float, default=0.30)
    ap.add_argument("--bloom-sigma", type=float, default=14.0)
    ap.add_argument("--grain", type=float, default=9.0)
    ap.add_argument("--vignette", type=float, default=4.5)
    ap.add_argument("--delogo-w-frac", type=float, default=0.17)
    ap.add_argument("--delogo-h-frac", type=float, default=0.13)
    # encode
    ap.add_argument("--codec", default="h264", choices=["h264", "hevc"])
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--workdir", default=None)
    args = ap.parse_args()

    res_h = {"720": (1280, 720), "1080": (1920, 1080), "1440": (2560, 1440)}
    out_h = {"1080": (1920, 1080), "1440": (2560, 1440),
             "2160": (3840, 2160), "4320": (7680, 4320)}
    args.internal_w, args.internal_h = res_h[args.internal]
    args.out_w, args.out_h = out_h[args.out_res]

    with open(args.sources) as f:
        sources = json.load(f)
    with open(args.schedule) as f:
        schedule = json.load(f)

    print(f" cinematic_master -> {len(schedule)} clips, "
          f"internal {args.internal_w}x{args.internal_h}, "
          f"master {args.out_w}x{args.out_h}, codec={args.codec}\n")

    workdir = args.workdir or tempfile.mkdtemp(prefix="cine_")
    os.makedirs(workdir, exist_ok=True)
    print(f" workdir: {workdir}")

    # 1) normalise each clip
    print("\n[1/2] Normalising clips (crop + delogo + speed + 24fps, muted)...")
    inter, durs = [], []
    for i, item in enumerate(schedule):
        src = sources[item["source"]]["file"]
        if not os.path.exists(src):
            sys.exit(f"  !! source file missing: {src}")
        p, d = render_intermediate(src, item["start"], item["end"], i, workdir, args)
        inter.append(p)
        durs.append(d)

    # 2) merge + grade + 4K
    print("\n[2/2] Master merge (xfade transitions + filmic grade + 4K)...")
    render_master(inter, durs, args, args.out)

    # 3) cleanup intermediates
    if args.workdir is None:
        import shutil
        shutil.rmtree(workdir, ignore_errors=True)

    print(f"\n DONE -> {args.out}")


if __name__ == "__main__":
    main()
