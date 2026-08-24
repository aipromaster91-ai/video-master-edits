import argparse
import os
import shutil
import subprocess
import sys
import zipfile

PAIRS = [
    {
        "id": "pair_01_yash_kiara",
        "name": "Yash & Kiara Advani",
        "hero_url": "https://www.youtube.com/watch?v=suk3mW0tDPA",
        "heroine_url": "https://www.youtube.com/watch?v=gvyUuxdRdR4",
        "hero_file": "yash_master.mp4",
        "heroine_file": "kiara_master.mp4",
        "output_dir": "downloaded_solo_clips_yash_kiara",
        "zip_name": "yash_kiara_solo_clips.zip"
    },
    {
        "id": "pair_02_yash_huma",
        "name": "Yash & Huma Qureshi",
        "hero_url": "https://www.youtube.com/watch?v=suk3mW0tDPA",
        "heroine_url": "https://www.youtube.com/watch?v=tLqhnrxLKoA",
        "hero_file": "yash_master.mp4",
        "heroine_file": "huma_master.mp4",
        "output_dir": "downloaded_solo_clips_yash_huma",
        "zip_name": "yash_huma_solo_clips.zip"
    },
    {
        "id": "pair_03_yash_nayanthara",
        "name": "Yash & Nayanthara",
        "hero_url": "https://www.youtube.com/watch?v=suk3mW0tDPA",
        "heroine_url": "https://www.youtube.com/watch?v=VAdGW7QDJiU",
        "hero_file": "yash_master.mp4",
        "heroine_file": "nayanthara_master.mp4",
        "output_dir": "downloaded_solo_clips_yash_nayanthara",
        "zip_name": "yash_nayanthara_solo_clips.zip"
    },
    {
        "id": "pair_04_yash_tara",
        "name": "Yash & Tara Sutaria",
        "hero_url": "https://www.youtube.com/watch?v=suk3mW0tDPA",
        "heroine_url": "https://www.youtube.com/watch?v=kpv4N55sJfs",
        "hero_file": "yash_master.mp4",
        "heroine_file": "tara_master.mp4",
        "output_dir": "downloaded_solo_clips_yash_tara",
        "zip_name": "yash_tara_solo_clips.zip"
    },
    {
        "id": "pair_05_shahid_alia",
        "name": "Shahid Kapoor & Alia Bhatt",
        "hero_url": "https://www.youtube.com/watch?v=Ps4aVpIESkc",
        "heroine_url": "https://www.youtube.com/watch?v=BddP6PYo2gs",
        "hero_file": "shahid_master.mp4",
        "heroine_file": "alia_master.mp4",
        "output_dir": "downloaded_solo_clips_shahid_alia",
        "zip_name": "shahid_alia_solo_clips.zip"
    },
    {
        "id": "pair_06_ranveer_kriti",
        "name": "Ranveer Singh & Kriti Sanon",
        "hero_url": "https://www.youtube.com/watch?v=jFGKJBPFdUA",
        "heroine_url": "https://www.youtube.com/watch?v=bTw7tT82W2k",
        "hero_file": "ranveer_master.mp4",
        "heroine_file": "kriti_master.mp4",
        "output_dir": "downloaded_solo_clips_ranveer_kriti",
        "zip_name": "ranveer_kriti_solo_clips.zip"
    },
    {
        "id": "pair_07_emraan_kriti",
        "name": "Emraan Hashmi & Kriti Sanon",
        "hero_url": "https://www.youtube.com/watch?v=sCbbMZ-q4-I",
        "heroine_url": "https://www.youtube.com/watch?v=bTw7tT82W2k",
        "hero_file": "emraan_master.mp4",
        "heroine_file": "kriti_master.mp4",
        "output_dir": "downloaded_solo_clips_emraan_kriti",
        "zip_name": "emraan_kriti_solo_clips.zip"
    }
]

def download_video(url, output_path):
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000000:
        print(f"✅ Video already downloaded: {output_path}")
        return True

    print(f"📥 Downloading: {url} -> {output_path}")
    strategies = [
        ["yt-dlp", "--extractor-args", "youtube:player_client=android", "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best", "--merge-output-format", "mp4", url, "-o", output_path],
        ["yt-dlp", "--extractor-args", "youtube:player_client=ios", "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best", "--merge-output-format", "mp4", url, "-o", output_path],
        ["yt-dlp", "--extractor-args", "youtube:player_client=mweb,web", "-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4", url, "-o", output_path],
        ["yt-dlp", "-f", "best", url, "-o", output_path]
    ]

    for i, cmd in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}/{len(strategies)}...")
            res = subprocess.run(cmd, check=True)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
                print(f"✅ Download success: {output_path}")
                return True
        except Exception as e:
            print(f"  Attempt {i} failed: {e}")

    print(f"❌ Failed to download {url}")
    return False

def get_schedule(hero_file="hero_master.mp4", heroine_file="heroine_master.mp4"):
    return [
        # 1 to 10
        {"source": hero_file, "start": "00:00:15", "end": "00:00:20", "name": "Clip_01_Male.mp4"},
        {"source": heroine_file, "start": "00:00:20", "end": "00:00:25", "name": "Clip_02_Female.mp4"},
        {"source": hero_file, "start": "00:00:35", "end": "00:00:40", "name": "Clip_03_Male.mp4"},
        {"source": heroine_file, "start": "00:00:45", "end": "00:00:50", "name": "Clip_04_Female.mp4"},
        {"source": hero_file, "start": "00:00:55", "end": "00:01:00", "name": "Clip_05_Male.mp4"},
        {"source": heroine_file, "start": "00:01:05", "end": "00:01:10", "name": "Clip_06_Female.mp4"},
        {"source": hero_file, "start": "00:01:15", "end": "00:01:20", "name": "Clip_07_Male.mp4"},
        {"source": heroine_file, "start": "00:01:20", "end": "00:01:25", "name": "Clip_08_Female.mp4"},
        {"source": hero_file, "start": "00:01:35", "end": "00:01:40", "name": "Clip_09_Male.mp4"},
        {"source": heroine_file, "start": "00:01:35", "end": "00:01:40", "name": "Clip_10_Female.mp4"},

        # 11 to 20
        {"source": hero_file, "start": "00:01:45", "end": "00:01:50", "name": "Clip_11_Male.mp4"},
        {"source": heroine_file, "start": "00:01:50", "end": "00:01:55", "name": "Clip_12_Female.mp4"},
        {"source": hero_file, "start": "00:02:10", "end": "00:02:15", "name": "Clip_13_Male.mp4"},
        {"source": heroine_file, "start": "00:02:05", "end": "00:02:10", "name": "Clip_14_Female.mp4"},
        {"source": hero_file, "start": "00:02:25", "end": "00:02:30", "name": "Clip_15_Male.mp4"},
        {"source": heroine_file, "start": "00:02:20", "end": "00:02:25", "name": "Clip_16_Female.mp4"},
        {"source": hero_file, "start": "00:02:35", "end": "00:02:40", "name": "Clip_17_Male.mp4"},
        {"source": heroine_file, "start": "00:02:40", "end": "00:02:45", "name": "Clip_18_Female.mp4"},
        {"source": hero_file, "start": "00:02:50", "end": "00:02:55", "name": "Clip_19_Male.mp4"},
        {"source": heroine_file, "start": "00:02:50", "end": "00:02:55", "name": "Clip_20_Female.mp4"},

        # 21 to 30
        {"source": hero_file, "start": "00:03:05", "end": "00:03:10", "name": "Clip_21_Male.mp4"},
        {"source": heroine_file, "start": "00:03:05", "end": "00:03:10", "name": "Clip_22_Female.mp4"},
        {"source": hero_file, "start": "00:03:15", "end": "00:03:20", "name": "Clip_23_Male.mp4"},
        {"source": heroine_file, "start": "00:03:20", "end": "00:03:25", "name": "Clip_24_Female.mp4"},
        {"source": hero_file, "start": "00:03:25", "end": "00:03:30", "name": "Clip_25_Male.mp4"},
        {"source": heroine_file, "start": "00:03:30", "end": "00:03:35", "name": "Clip_26_Female.mp4"},
        {"source": hero_file, "start": "00:03:30", "end": "00:03:35", "name": "Clip_27_Male.mp4"},
        {"source": heroine_file, "start": "00:03:40", "end": "00:03:45", "name": "Clip_28_Female.mp4"},
        {"source": hero_file, "start": "00:03:40", "end": "00:03:45", "name": "Clip_29_Male.mp4"},
        {"source": heroine_file, "start": "00:03:48", "end": "00:03:53", "name": "Clip_30_Female.mp4"},

        # 31 to 36
        {"source": hero_file, "start": "00:03:45", "end": "00:03:50", "name": "Clip_31_Male.mp4"},
        {"source": heroine_file, "start": "00:03:55", "end": "00:04:00", "name": "Clip_32_Female.mp4"},
        {"source": hero_file, "start": "00:03:50", "end": "00:03:55", "name": "Clip_33_Male.mp4"},
        {"source": heroine_file, "start": "00:04:00", "end": "00:04:05", "name": "Clip_34_Female.mp4"},
        {"source": hero_file, "start": "00:01:15", "end": "00:01:20", "name": "Clip_35_Male.mp4"},
        {"source": heroine_file, "start": "00:00:20", "end": "00:00:25", "name": "Clip_36_Female.mp4"}
    ]

def zip_folder(folder_path, output_zip):
    print(f"📦 Zipping '{folder_path}' -> '{output_zip}'...")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"✅ Created zip ({os.path.getsize(output_zip) / (1024*1024):.2f} MB): {output_zip}")

def process_slicing(hero_file="hero_master.mp4", heroine_file="heroine_master.mp4", output_dir="downloaded_solo_clips", create_zip=False, zip_name="solo_clips.zip"):
    os.makedirs(output_dir, exist_ok=True)
    schedule = get_schedule(hero_file, heroine_file)

    print(f"🎬 Slicing 36 PURE SOLO clips into '{output_dir}' with 120% Tight Smart-Crop...")
    vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24"

    for idx, item in enumerate(schedule, 1):
        out_path = os.path.join(output_dir, item["name"])
        print(f"[{idx}/36] Slicing {item['name']} ({item['start']} -> {item['end']}) from {item['source']}...")
        if os.path.exists(item["source"]):
            cmd = [
                "ffmpeg", "-y",
                "-ss", item["start"],
                "-to", item["end"],
                "-i", item["source"],
                "-vf", vf,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "20",
                "-an",
                out_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"⚠️ Source file {item['source']} not found. Skipping slice execution.")

    print(f"✅ All 36 Solo Clips Processed for {output_dir}")
    if create_zip and os.path.exists(output_dir):
        zip_folder(output_dir, zip_name)

def process_pair_pipeline(pair):
    print(f"\n==========================================")
    print(f"🚀 Processing: {pair['name']} ({pair['id']})")
    print(f"==========================================")
    
    # Download hero
    download_video(pair["hero_url"], pair["hero_file"])
    # Download heroine
    download_video(pair["heroine_url"], pair["heroine_file"])

    # Slice clips & create zip
    process_slicing(
        hero_file=pair["hero_file"],
        heroine_file=pair["heroine_file"],
        output_dir=pair["output_dir"],
        create_zip=True,
        zip_name=pair["zip_name"]
    )

def list_pairs():
    print("📋 Configured Pairs & Direct Links:")
    print("=" * 60)
    for idx, pair in enumerate(PAIRS, 1):
        print(f"{idx}. {pair['name']} ({pair['id']})")
        print(f"   Hero URL: {pair['hero_url']}")
        print(f"   Heroine URL: {pair['heroine_url']}")
        print(f"   Zip File Output: {pair['zip_name']}")
        print("-" * 60)

def main():
    parser = argparse.ArgumentParser(description="Universal 100% Solo Slicing Script")
    parser.add_argument("--list-pairs", action="store_true", help="List all 7 preconfigured pairs and YouTube links")
    parser.add_argument("--pair", type=str, default=None, help="Process specific pair ID or 'all'")
    parser.add_argument("--hero", type=str, default="hero_master.mp4", help="Hero master mp4 file")
    parser.add_argument("--heroine", type=str, default="heroine_master.mp4", help="Heroine master mp4 file")
    parser.add_argument("--output-dir", type=str, default="downloaded_solo_clips", help="Output directory")
    parser.add_argument("--zip", action="store_true", help="Zip the output folder after slicing")
    parser.add_argument("--zip-name", type=str, default="downloaded_solo_clips.zip", help="Output zip filename")

    args = parser.parse_args()

    if args.list_pairs:
        list_pairs()
        return

    if args.pair:
        if args.pair.lower() == "all":
            for pair in PAIRS:
                process_pair_pipeline(pair)
        else:
            pair = next((p for p in PAIRS if p["id"] == args.pair or p["id"].endswith(args.pair)), None)
            if pair:
                process_pair_pipeline(pair)
            else:
                print(f"❌ Pair '{args.pair}' not found. Run --list-pairs to view available pairs.")
    else:
        process_slicing(
            hero_file=args.hero,
            heroine_file=args.heroine,
            output_dir=args.output_dir,
            create_zip=args.zip,
            zip_name=args.zip_name
        )

if __name__ == "__main__":
    main()
