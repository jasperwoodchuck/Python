import os, sys, json
from pydub import AudioSegment
import shutil, platform


def get_mc_assets_path():
    if platform.system() == "Windows":
        return os.path.expandvars(r"%APPDATA%/.minecraft/assets")
    else:
        return os.path.expanduser(r"~/.minecraft/assets")


MC_ASSETS = get_mc_assets_path()


def get_latest_version():
    try:
        versions = os.listdir(os.path.join(MC_ASSETS, "indexes"))
        return versions[-1] if versions else None
    except FileNotFoundError:
        print("Error: Minecraft assets folder not found.")
        sys.exit(1)


MC_VERSION = get_latest_version()


if not MC_VERSION:
    print("Error: No Minecraft versions found.")
    sys.exit(1)

OUTPUT_PATH = os.path.normpath(os.getcwd())
MC_OBJECT_INDEX = os.path.join(MC_ASSETS, "indexes", MC_VERSION)
MC_OBJECTS_PATH = os.path.join(MC_ASSETS, "objects")
MC_SOUNDS = "minecraft/sounds/"


def load_index_file(index_file_path):
    try:
        with open(index_file_path, "r") as index_file:
            return json.load(index_file)
    except FileNotFoundError:
        print(f"Error: Index file '{index_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to parse the Minecraft index file.")
        sys.exit(1)


data = load_index_file(MC_OBJECT_INDEX)


def extract_sounds(data):
    sounds = {}
    for key, value in data["objects"].items():
        if key.startswith(MC_SOUNDS):
            sound_path = key[len(MC_SOUNDS) :]
            sound_hash = value["hash"]
            sounds[sound_path] = sound_hash
    return sounds


sounds = extract_sounds(data)

total_files = len(sounds)
if total_files == 0:
    print("No sound files found to extract.")
    sys.exit(0)


def process_sound_files(sounds, output_path):
    extracted_count = 0

    for sound_path, sound_hash in sounds.items():
        try:
            src_file = os.path.join(MC_OBJECTS_PATH, sound_hash[:2], sound_hash)
            dest_file = os.path.join(output_path, "sounds", sound_path)

            os.makedirs(os.path.dirname(dest_file), exist_ok=True)

            shutil.copyfile(src_file, dest_file)
            extracted_count += 1

            mp3_file = dest_file.replace(".ogg", ".mp3")
            audio = AudioSegment.from_ogg(dest_file)
            audio.export(mp3_file, format="mp3")

            print(f"[{extracted_count}/{total_files}] {sound_path[:-4]}.mp3")
            os.remove(dest_file)

        except FileNotFoundError:
            print(f"Warning: Source file '{src_file}' not found. Skipping...")
        except Exception as error:
            print(f"Error during processing '{src_file}': {error}")


def rename_files_to_paths(folder_path):
    sound_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg']

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in sound_extensions):
                file_path = os.path.join(root, filename)
                
                relative_path = os.path.relpath(file_path, folder_path)
                new_name = relative_path.replace(os.sep, "_")
                
                _, ext = os.path.splitext(filename)
                new_name = new_name.replace(ext, '') + ext

                new_file_path = os.path.join(root, new_name)

                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_path} -> {new_file_path}")


process_sound_files(sounds, OUTPUT_PATH)
rename_files_to_paths(OUTPUT_PATH)