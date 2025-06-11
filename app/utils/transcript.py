import subprocess
import os
from pathlib import Path
import re

def extract_video_id(url: str) -> str:
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return url


def clean_vtt_line(line: str) -> str:
    # <00:00:00.000> 또는 <c> ... </c> 같은 태그 제거
    line = re.sub(r"<[^>]+>", "", line)
    return line.strip()

def get_transcript(url: str) -> list[str]:
    video_id = extract_video_id(url)
    print(f"📥 Downloading subtitle for video ID: {video_id}")

    command = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", "en",
        "--skip-download",
        "--output", f"{video_id}.%(ext)s",
        url
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("❌ yt-dlp 실행 중 오류 발생:")
        print(e.stderr.decode())
        return []

    vtt_file = Path(f"{video_id}.en.vtt")
    if not vtt_file.exists():
        print("❌ 자막 파일이 생성되지 않았습니다.")
        return []

    lines = []
    for line in vtt_file.read_text(encoding='utf-8').splitlines():
        if line and not line.startswith(('WEBVTT', '00:', '-->', 'NOTE')):
            cleaned = clean_vtt_line(line)
            if cleaned:
                lines.append(cleaned)

    print("📜 Parsed transcript lines:", lines[:5])
    return lines