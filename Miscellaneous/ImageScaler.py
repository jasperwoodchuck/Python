from PIL.Image import Resampling
from PIL import Image as IMG
import os

def scale_textures(path: str) -> None:
    base_path = os.path.join(path)
    for root, _dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                img = IMG.open(file_path)
                breath, height = img.size

                multiplier = 1024 / max(breath, height)
                size = (int(breath * multiplier), int(height * multiplier))

                img_resized = img.resize(size, resample=Resampling.NEAREST)
                img_resized.save(file_path)
                print(f"[Resized] {file_path} -> {size}")
            except Exception as e:
                print(f"[Skipped] {file_path} ({e})")

if __name__ == "__main__":
    path = r"<insert path here>"
    scale_textures(path)