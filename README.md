# Automated Video Master Pipeline

Automated high-speed video processing pipeline for Hollywood/Bollywood music video slicing and mastering.
Automated video processing pipeline for creating 40 alternating solo clips per pair and publishing ZIP releases with GitHub Actions.

> Use this only with videos you own or have permission to download/process.

## Ready GitHub Action

Workflow file: `.github/workflows/process_all_pairs.yml`

How to run:

1. Open the repo on GitHub.
2. Go to **Actions**.
3. Select **Download, Slice & Release 7 Pairs x 40 Clips ZIPs**.
4. Click **Run workflow**.
5. Choose `pair_selection`:
   - `all` = generate all 7 ZIP files
   - any single pair = generate only that pair's ZIP
6. Set `release_tag`, for example `v1.0-40-solo-clips`.
7. Tick `confirm_rights`.
8. Run it.

The workflow downloads the configured source videos, slices exactly **40 clips per selected pair** (20 Hero + 20 Heroine, alternating), creates ZIP files, uploads them as workflow artifacts, and publishes them to the GitHub Release.

## Production Standard

- 40 alternating solo clips per pair: Hero, Heroine, Hero, Heroine ...
- 20 Hero clips + 20 Heroine clips
- 125% 4K smart crop filter: `scale=4800:2700:force_original_aspect_ratio=increase,crop=3840:2160,fps=24`
- Video-only clips: native audio stripped with `-an`
- Studio render settings: H.264, CRF 18, 24 FPS, 3840x2160
- Timestamp values from the PDF blueprint are normalized automatically, so values such as `00:63` become `00:01:03`.

## All 7 ZIP Output List

| # | Pair | Workflow ID | ZIP file | Output folder | Clips |
|---|------|-------------|----------|---------------|-------|
| 1 | Yash & Kiara Advani | `pair_01_yash_kiara` | `yash_kiara_solo_clips.zip` | `downloaded_clips_yash_kiara` | 40 |
| 2 | Yash & Huma Qureshi | `pair_02_yash_huma` | `yash_huma_solo_clips.zip` | `downloaded_clips_yash_huma` | 40 |
| 3 | Yash & Nayanthara | `pair_03_yash_nayanthara` | `yash_nayanthara_solo_clips.zip` | `downloaded_clips_yash_nayanthara` | 40 |
| 4 | Yash & Tara Sutaria | `pair_04_yash_tara` | `yash_tara_solo_clips.zip` | `downloaded_clips_yash_tara` | 40 |
| 5 | Shahid Kapoor & Alia Bhatt | `pair_05_shahid_alia` | `shahid_alia_solo_clips.zip` | `downloaded_clips_shahid_alia` | 40 |
| 6 | Ranveer Singh & Kriti Sanon | `pair_06_ranveer_kriti` | `ranveer_kriti_solo_clips.zip` | `downloaded_clips_ranveer_kriti` | 40 |
| 7 | Emraan Hashmi & Kriti Sanon | `pair_07_emraan_kriti` | `emraan_kriti_solo_clips.zip` | `downloaded_clips_emraan_kriti` | 40 |

## Source Videos Configured

### 1. Yash & Kiara Advani

- `yash_monster.mp4` — https://www.youtube.com/watch?v=R4He_Gcn7cA
- `yash_mehabooba.mp4` — https://www.youtube.com/watch?v=suk3mW0tDPA
- `kiara_shershaah.mp4` — https://www.youtube.com/watch?v=gvyUuxdRdR4
- `kiara_ranjha.mp4` — https://www.youtube.com/watch?v=V7LwfY5U5WI

### 2. Yash & Huma Qureshi

- `yash_monster.mp4` — https://www.youtube.com/watch?v=R4He_Gcn7cA
- `yash_mehabooba.mp4` — https://www.youtube.com/watch?v=suk3mW0tDPA
- `huma_badlapur.mp4` — https://www.youtube.com/watch?v=tLqhnrxLKoA

### 3. Yash & Nayanthara

- `yash_monster.mp4` — https://www.youtube.com/watch?v=R4He_Gcn7cA
- `yash_mehabooba.mp4` — https://www.youtube.com/watch?v=suk3mW0tDPA
- `nayan_jawan.mp4` — https://www.youtube.com/watch?v=VAdGW7QDJiU

### 4. Yash & Tara Sutaria

- `yash_monster.mp4` — https://www.youtube.com/watch?v=R4He_Gcn7cA
- `yash_mehabooba.mp4` — https://www.youtube.com/watch?v=suk3mW0tDPA
- `tara_marjaavaan.mp4` — https://www.youtube.com/watch?v=kpv4N55sJfs
- `tara_shaamat.mp4` — https://www.youtube.com/watch?v=Zf_n5TqA9_g

### 5. Shahid Kapoor & Alia Bhatt

- `shahid_kabir.mp4` — https://www.youtube.com/watch?v=Ps4aVpIESkc
- `shahid_tbmauj.mp4` — https://www.youtube.com/watch?v=XLqmL9cPN1E
- `alia_kesariya.mp4` — https://www.youtube.com/watch?v=BddP6PYo2gs
- `alia_tumkyamile.mp4` — https://www.youtube.com/watch?v=hacByYwJ_a4

### 6. Ranveer Singh & Kriti Sanon

- `ranveer_gully.mp4` — https://www.youtube.com/watch?v=jFGKJBPFdUA
- `ranveer_tumkyamile.mp4` — https://www.youtube.com/watch?v=hacByYwJ_a4
- `kriti_shehzada.mp4` — https://www.youtube.com/watch?v=bTw7tT82W2k
- `kriti_dopatti.mp4` — https://www.youtube.com/watch?v=lBvbNxiVmZA

### 7. Emraan Hashmi & Kriti Sanon

- `emraan_lutgaye.mp4` — https://www.youtube.com/watch?v=sCbbMZ-q4-I
- `emraan_kahani.mp4` — https://www.youtube.com/watch?v=f3FFOBrMmdg
- `kriti_shehzada.mp4` — https://www.youtube.com/watch?v=bTw7tT82W2k
- `kriti_dopatti.mp4` — https://www.youtube.com/watch?v=lBvbNxiVmZA

## Local Commands

List configured pairs:

```bash
python3 slice_solo.py --list-pairs
```

List pairs with every 40-clip timestamp:

```bash
python3 slice_solo.py --list-pairs --show-clips
```

Process all pairs locally:

```bash
python3 slice_solo.py --pair all
```

Process one pair locally:

```bash
python3 slice_solo.py --pair pair_04_yash_tara
```

## Features
- Alternating Hero & Heroine clips (5-second pacing)
- 1080p / 4K unified standard rendering
- Audio muting & seamless track synchronization
- GitHub Actions automated cloud processing

- 7 preconfigured pair selections
- 40 short solo clips per pair
- 4K smart crop output
- Muted video clips for editing workflows
- Automatic ZIP creation
- GitHub Release upload
- Workflow artifact upload backup
