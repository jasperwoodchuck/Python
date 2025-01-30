# Minecraft Sound & Texture Extractor + YouTube Video Downloader

This repository contains three Python scripts:
1. **[SoundsExtractor.py](Minecraft/SoundsExtractor.py)** - Extracts and converts Minecraft sounds.
2. **[TexturesExtractor.py](Minecraft/TexturesExtractor.py)** - Extracts and scales Minecraft textures.
3. **[YoutubeDownloader.py](YoutubeDownloader.py)** - Downloads YouTube videos and converts them to MP4.

### Prerequisites
- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) (for audio and video conversion)
- Required Python packages:
  
  `pip install pydub yt-dlp pillow`

### Extract Minecraft Sounds
`py SoundsExtracter.py`

Extracts Minecraft sounds and converts `.ogg` files to `.mp3`.

### Extract Minecraft Textures
`py TexturesExtracter.py`

Extracts Minecraft textures and scales them to 256x256 pixels.

### Download YouTube Videos
`py YoutubeDownloader.py`

Downloads and converts YouTube videos to MP4 (Using your GPU for faster performance).

## License
This project is licensed under the [MIT License](LICENSE.md).