# Cinematic Music-Video Master Pipeline

Fully automated, **studio-grade** music-video editing engine. Give it **2 source
videos + a 36-clip schedule**, and it returns a **4K filmic master** (cropped,
watermark-cleaned, speed-ramped, beat-style transitions, teal-orange graded,
film-grained, 24fps) — **with NO audio** (the song is added later).

This implements the full "world-class music-video editor" spec, **except the
audio step** which you handle yourself.

---

## What the engine does (per the spec)

| Spec step | How it's done |
|---|---|
| 1. Timeline / duration | every clip normalised; final trimmed to N s (default 180) |
| 2. Watermark / logo removal | smart-crop to 16:9 + `delogo` on all 4 corners |
| 3. Beat-style speed ramping | per-clip `setpts` rhythm table (slow / normal / fast) |
| 4. Seamless transitions | chained `xfade` (whip-pan / zoom / flash / wipe — no hard cuts) |
| 5. Studio color grade | uniform teal-orange filmic (eq + colorbalance + curves) + bloom + 35mm grain + vignette |
| 6. 4K master export | spline upscale to 3840×2160, 24fps cinema, H.264 / HEVC, muted |

> Audio is intentionally **omitted** (your instruction). Output is video-only.

---

## Daily workflow (what you send → what you get)

Each day you send me:

1. **2 YouTube links** (hero + heroine), and which is which.
2. **The clip schedule** — just paste your `slice_*.py` (the `clips_schedule`
   list). I auto-convert it to `schedule.json`. Rules: exactly **alternating**
   hero/heroine, **no clip longer than 5 s**.
3. **The final file name** (e.g. `Mousam Barish Ka.mp4`).
4. Optional: resolution (default 4K), codec.

I then:
- write `sources.json` (the 2 links) and `schedule.json` (the 36 clips),
- commit + push,
- trigger the **Cinematic Music Video Master** workflow on GitHub Actions
  (GitHub's runners have open internet, so the YouTube download + 4K render
  happen there),
- hand you the **direct download link** from the GitHub Release.

After each video is delivered, the 36 intermediate clips are discarded and the
next video starts clean.

---

## Run it yourself (optional)

From the **Actions** tab → *Cinematic Music Video Master* → *Run workflow*:

```
final_name    = Mousam Barish Ka.mp4
resolution    = 2160        # 4K
codec         = h264
target_seconds= 180         # 3:00
```

Or locally (if you already have the 2 source files):

```bash
python3 cinematic_master.py --out "Mousam Barish Ka.mp4" --out-res 2160
```

Useful overrides: `--transition 0.45 --flat-speed 0 --grain 9 --teal-orange 0.08
--bloom 0.30 --crf 18 --codec hevc`.

---

## Files

- `cinematic_master.py` — the editing engine (audio-free).
- `schedule.json` — today's 36 clips (`source` = `hero` / `heroine`, `start`, `end`).
- `sources.json` — today's 2 sources (`file` + YouTube `url` per role).
- `.github/workflows/process_music_video.yml` — the GitHub Actions automation.
- `master_slicer.py` — original basic slicer (kept for reference).
