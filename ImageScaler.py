from PIL.Image import Resampling
from PIL import Image as IMG
import os

def scale_textures(path: str) -> None:
    base_path = os.path.join(path)
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                img = IMG.open(file_path)
                if not img.size == (18, 18):
                    continue

                img_resized = img.resize((256, 256), resample=Resampling.NEAREST)
                img_resized.save(file_path)
                print(file_path)
            except:
                ...

if __name__ == "__main__":
    path = r"<insert path here>"
    scale_textures(path)