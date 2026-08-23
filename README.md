# Video Master Edits 🎬

Automated, GitHub-Actions + ffmpeg pipeline that turns two master videos
(Hero + Heroine) into a finished **4K / 24fps cinematic music video** — sliced
into 36 alternating clips, graded, transitioned, and synced to one master song.

> **You don't need to share a GitHub token.** This Arena sandbox already has
> GitHub access via the `gh` CLI (`gh auth status`). Just give me the video
> links + the clip schedule and I'll run the pipeline and hand you the final
> video. (Never paste personal access tokens in chat — they're credentials.)

---

## What's in the box

| File | Purpose |
|------|---------|
| `.github/workflows/download_4k.yml` | One-click 4K downloader → publishes the full master to **Releases** (up to 2 GB/file). |
| `.github/workflows/process_music_video.yml` | Full pipeline: download Hero+Heroine (+optional master audio) → slice → render → publish. |
| `slice_yash_tara.py` | Slices the Yash/Tara masters into 36 alternating clips (`downloaded_clips_yash_tara/`). |
| `scripts/slice_clips.py` | Generic, JSON-driven slicer for any future Hero/Heroine pair. |
| `scripts/assemble.py` | **The cinematic assembler** — mute, speed-ramp, grade, transition, upscale, mux master audio → 4K MP4. |
| `config/project_example.json` | Assemble manifest (36 clips + grade + output settings). |
| `config/clips_schedule_yash_tara.json` | The 36-clip schedule as data (for `slice_clips.py`). |
| `docs/AI_EDITING_PROMPTS.md` | The "Master All-In-One AI Editing Prompt" + step-by-step prompts (for external AI tools). |

---

## Daily workflow (how we'll use it)

1. **You give me** the two YouTube links (Hero + Heroine) and, optionally, the
   master-song link, plus the **clip schedule** (which timestamps → which clip,
   like the `clips_schedule` list in `slice_yash_tara.py`).
2. **I run** (in this sandbox, which has ~fast egress + ffmpeg):
   - `yt-dlp` to grab the two masters,
   - `python3 slice_yash_tara.py` to cut 36 clips,
   - `python3 scripts/assemble.py --config config/project_example.json --master-audio master_song.mp3`
     to render the final 4K video.
3. **You get** `final_yash_tara_4k.mp4` (or whatever the config names it).

If you'd rather do the heavy download in GitHub's cloud, just run
**`download_4k.yml`** (Actions → Run workflow) to drop the 4K master into
Releases, then hand me the link.

---

## Run it yourself (local)

```bash
# 0. needs ffmpeg + yt-dlp
sudo apt install ffmpeg -y && pip install yt-dlp

# 1. grab the two masters (replace URLs)
yt-dlp -f "bv*+ba/best" --merge-output-format mp4 "<HERO_URL>"   -o hero_yash.mp4
yt-dlp -f "bv*+ba/best" --merge-output-format mp4 "<HEROINE_URL>" -o heroine_tara.mp4
yt-dlp -x --audio-format mp3 "<SONG_URL>" -o master_song.mp3     # optional

# 2. slice 36 clips
python3 slice_yash_tara.py

# 3. assemble the 4K master
python3 scripts/assemble.py --config config/project_example.json --master-audio master_song.mp3
```

---

## Tuning the look (`config/project_example.json`)

- **`settings.grade`** — contrast / brightness / saturation / `temperature`
  (Kelvin; lower = warmer) / `vignette` (`PI/5`) / `grain` (film grain amount).
- **`settings.fade`** — per-clip edge fade for smooth cuts (concat mode).
- **`settings.transition_mode`** — `"concat"` (exact 3:00, no time lost) or
  `"xfade"` (cinematic cross-dissolve/whip/zoom; auto-stretched to 3:00).
- **`clips[].speed`** — per-clip speed ramp (e.g. `0.6` slow-mo, `1.8` fast-mo,
  `3.0` impact). Alternating speeds = beat-synced energy.
- **`settings.watermark`** — `{"enabled": true, "filter": "crop=iw:ih-80:0:40"}`
  to shave watermark bars off the edges.
- **`settings.output`** — `codec` (`libx265`/`libx264`), `width`/`height`
  (`3840x2160` for 4K), `crf`, `preset`, `duration` (180s), `fade_out` (1.5s).

> **Note on "AI" effects:** `assemble.py` approximates the prompt with ffmpeg
> (eq/colortemperature/vignette/noise filters, setpts speed-ramps, xfade). For
> true AI inpainting, optical-flow, and Topaz-style upscaling, use the prompts in
> `docs/AI_EDITING_PROMPTS.md` with a dedicated AI editor — the clips + config
> here are already in the right shape to feed it.

---

## GitHub Actions notes

- Releases allow **up to 2 GB per file** — plenty for a 4K master.
- The `process_music_video.yml` runner is 2 vCPU / 7 GB; 4K H.265 of 3 min is
  doable but takes a few minutes. For max speed, render locally (this sandbox)
  and only use Actions for the 1 Gbps 4K *download*.
- `permissions: contents: write` is required so the workflow can publish Releases.

## Responsible use

Downloading YouTube content may be bound by YouTube's Terms of Service and the
content's copyright. Use this pipeline only for material you have the rights to
download, edit, and redistribute (your own footage, licensed stock, or where
fair use / the platform permits).
