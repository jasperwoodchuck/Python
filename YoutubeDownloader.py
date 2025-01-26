import yt_dlp
import os
import re
import subprocess
import platform

def remove_invalid_characters(filename:str) -> str:
    if platform.system() != "Windows":
        return
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', "-", filename)


def webm_to_mp4(input: str, output: str) -> None:
    subprocess.run(
        ['ffmpeg', '-hide_banner',
         '-i', input,
         '-c:v', 'h264_nvenc',
         '-preset', 'fast',
         '-c:a', 'aac', output]
    )

    os.remove(input)


def download_youtube_video(
        video_url: str,
        download: bool = True
        ) -> dict:
    
    tempname = "temp_vid."
    ydl_opts = {
        'format': 'bestvideo[height=1080]+bestaudio/best',
        'outtmpl': tempname + "%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        params = ydl.extract_info(video_url, download=download)
        title = params.get('title', None)
        uploader_id = params.get('uploader_id', None)
        ext = params.get('ext', None)
    
    corrected_title = remove_invalid_characters(title)
    filename = f"{corrected_title} by {uploader_id}.mp4"
    webm_to_mp4(tempname + ext, filename)


urls = (
    "https://www.youtube.com/watch?v=",
    "https://www.youtube.com/watch?v=",
    "https://www.youtube.com/watch?v=",
    )

for url in urls:
    download_youtube_video(url)