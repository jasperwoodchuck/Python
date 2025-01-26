from PIL.Image import Resampling
from PIL import Image as IMG
import os, zipfile

def extract_textures() -> None:
    APPDATA = os.getenv("APPDATA")
    APPdirs = os.path.join(APPDATA, ".minecraft", "versions")

    folders = os.listdir(APPdirs)[:-2]

    for i, folder in enumerate(folders):
        print(f"{i} -> {folder}")

    version = folders[int(input("Select Version (index): "))]

    jarfile = f"{version}.jar"
    APPpath = os.path.join(APPdirs, version, jarfile)
    textures_path = "assets/minecraft/textures"

    with zipfile.ZipFile(APPpath, "r") as jar:
        for info in jar.infolist():
            if info.filename.startswith(textures_path):
                if info.filename.endswith(".png"):
                    file_path = jar.extract(info, version)
                    textures_to_pngsequence(file_path)
                    print(file_path)

    scale_textures(version)

def textures_to_pngsequence(image_path: str) -> None:
    nimage = IMG.open(image_path)
    breath = nimage.width
    height = nimage.height

    if breath == 16 and height > 16 and height % 16 == 0:
        ntiles = height // 16
        output = os.path.splitext(image_path)[0]
        os.makedirs(output, exist_ok=True)

        for count in range(ntiles):
            upper = count * 16 
            lower = upper + 16
            ntile = nimage.crop((0, upper, breath, lower))
            ntile_path = os.path.join(
                output,
                f'{os.path.basename(image_path)[:-4]}_{count}.png'
                )
            try:
                ntile.save(ntile_path)
                print(f"{ntile_path}")
            except FileNotFoundError:
                ... 

        os.remove(image_path)

def scale_textures(version: str) -> None:
    base_path = os.path.join(version)
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                img = IMG.open(file_path)
                if not img.size == (16, 16):
                    continue

                img_resized = img.resize(
                    (256, 256), resample=Resampling.NEAREST
                    )
                img_resized.save(file_path)
                print(file_path)
            except:
                ...
                    
if __name__ == "__main__":
    extract_textures()
