# AI Editing Prompts (copy-paste ready)

These are the prompts you pasted for feeding an **external AI video editor**
(Runway, Kaiber, CapCut PC, DaVinci + AI plugins, Topaz, etc.). They describe
the *creative intent*. The repo's `scripts/assemble.py` already does an ffmpeg
version of all of this automatically — but if you want the maximum "AI" quality
(inpainting, true optical-flow, Topaz upscale), hand the same 36 clips + master
audio + one of these prompts to that tool.

---

## Option 1 — Master All-In-One AI Editing Prompt

```
Act as a world-class Hollywood/Bollywood post-production music video editor, colorist,
and VFX supervisor. Execute a fully automated, synchronized, studio-grade music video
edit using the provided 36 video clips and 1 master audio track based on the following
strict technical directives:

1. TIMELINE & DURATION CONTROL:
- Import master audio track and strictly trim the timeline to exactly 03:00 minutes
  (180 seconds). Apply a smooth 1.5-second audio fade-out at the 03:00 mark.
- Completely MUTE all embedded/native audio across all 36 source video clips. The
  master song must be the only audible track (100% volume, master-limited at -0.1 dB).

2. FOOTAGE CLEANUP & WATERMARK REMOVAL:
- Scan all 36 clips for on-screen watermarks, logos, text overlays, and timestamps
  (especially in the bottom/top corners).
- Automatically apply smart crop (maintaining 16:9 cinematic aspect ratio) or
  content-aware fill/inpainting to completely eliminate every watermark without
  distorting the primary subject.

3. BEAT SYNCHRONIZATION & SPEED RAMPING:
- Analyze the master audio track for BPM, waveform transients, verse-chorus
  transitions, drum drops, and melody shifts.
- Distribute and sequence the 36 clips across the 180-second duration dynamically:
  * Slow, emotional sections / Melodic verses: Use 0.5x to 0.7x smooth optical-flow
    slow motion.
  * Fast beats, drum fills, drops, and high-energy choruses: Use speed ramping
    (1.5x to 3.0x fast-motion transitioning into sudden slow-motion impact on key
    beats).
  * Cut on the snare/kick drum transients for high-impact rhythm.

4. SEAMLESS CINEMATIC TRANSITIONS:
- Avoid generic default transitions. Apply elite commercial/studio transitions:
  * Dynamic motion blur whip pans and directional zooms.
  * Seamless match cuts based on subject motion direction.
  * Subtle organic light leaks, film burns, and flash frames precisely on beat drops.

5. HOLLYWOOD/BOLLYWOOD STUDIO COLOR GRADING & LOOK:
- Match the visual tone across all 36 clips for color uniformity and high-budget
  production value.
- Apply high-end film emulation (Kodak 2383 / ARRI Alexa look):
  * Rich, deep cinematic contrast with soft rolled-off highlights.
  * Vibrant yet natural skin tones with warm golden hour/teal-orange color separation.
  * Subtle anamorphic lens glow, atmospheric bloom on highlights, and fine 35mm
    film grain.

6. FINAL MASTER EXPORT & UPSCALE:
- Upscale and render final composition to Ultra HD 4K / 8K DCI Master.
- Frame Rate: 24 fps (True Cinema Standard) with realistic motion blur
  (Shutter angle 180°).
- Output format: ProRes 422HQ or H.265 (HEVC), 10-bit color depth, Maximum Bitrate
  Render.
```

---

## Option 2 — Step-by-Step AI Prompts

### Step 1: Ingest, Audio Trim & Watermark Cleanup
```
Task: Source Cleanup and Ingest
1. Set project timeline to exactly 03:00 minutes. Cut the master song at 03:00 with
   a natural fade-out.
2. Mute native audio tracks on all 36 imported clips.
3. Detect and remove/crop all logos, watermarks, and burned-in captions on all 36
   clips using AI inpainting or smart framing to 16:9 widescreen.
```

### Step 2: Beat Mapping & Dynamic Speed Ramping
```
Task: AI Rhythm Editing & Speed Dynamics
1. Detect all beats, drops, and energy curves from the audio track.
2. Sequence all 36 clips to match the song structure:
   - Apply Optical Flow Slow-Motion (50% speed) during melodic/intro sections.
   - Apply dynamic Speed Ramps (200% acceleration into 40% slow-mo) on beat drops
     and bass impacts.
   - Align every cut point precisely with audio transients (downbeats/snares).
```

### Step 3: Studio Transitions & VFX
```
Task: Visual Transitions
1. Apply professional music video transitions: Seamless directional whip pans, zoom
   bursts, kinetic motion blurs, and organic film burns.
2. Ensure transitions trigger exactly on downbeats for maximum visual impact.
```

### Step 4: Cinematic Studio Color Grade & 4K/8K Upscale
```
Task: Color Grading & Master Render
1. Apply a high-end Bollywood/Hollywood cinematic LUT (warm highlights, rich shadow
   contrast, protected skin tones, subtle film glow).
2. Upscale output to 4K/8K resolution with AI detail enhancement, denoising, and
   24fps cinematic motion blur.
```
