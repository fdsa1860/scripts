
import os
import shutil
import sys
import time
from tqdm import tqdm
from datetime import datetime
from PIL import Image
import subprocess
import json


def get_capture_date(file_path):
    capture_date = None
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    video_extensions = (".mp4", ".avi", ".mov", ".wmv", ".flv", ".mpg")
    if file_path.lower().endswith(image_extensions):
        with Image.open(file_path) as img:
            exif_data = img.getexif()
            if exif_data:
                capture_date = exif_data.get(36867)
                if capture_date:
                    return datetime.strptime(capture_date, '%Y:%m:%d %H:%M:%S').strftime('%Y')
    elif file_path.lower().endswith(video_extensions):
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', file_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = json.loads(result.stdout)
        if 'format' in output and 'tags' in output['format'] and 'creation_time' in output['format']['tags']:
            capture_date = output['format']['tags']['creation_time']
            if capture_date:
                return datetime.strptime(capture_date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y')

    if capture_date is None:
        creation_time = os.path.getctime(file_path)
        modification_time = os.path.getmtime(file_path)
        earliest_time = min(creation_time, modification_time)
        return datetime.fromtimestamp(earliest_time).strftime('%Y')


def copy_media(src_folder, dest_folder):
    # Get the list of all files in the source folder and its subdirectories
    files = []
    for dirpath, dirnames, filenames in os.walk(src_folder):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    # Filter out files starting with "."
    files = [file for file in files if not os.path.basename(file).startswith(".")]
    # Filter out non-image and non-video files
    media_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".mp4", ".avi", ".mov", ".wmv", ".flv"]
    files = [file for file in files if any(file.lower().endswith(ext) for ext in media_extensions)]
    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)
    # Move the files to the destination folder
    for file in tqdm(files):
        src_path = file
        creation_year = get_capture_date(file) 
        year_folder = os.path.join(dest_folder, creation_year)
        os.makedirs(year_folder, exist_ok=True)
        dest_path = os.path.join(year_folder, os.path.basename(file))
        shutil.copy2(src_path, dest_path)

if __name__ == "__main__":
    # Get the command line arguments
    if len(sys.argv) != 3:
        print("Number of arguments " + str(len(sys.argv)) + " is not 3")
        print("Arg[0] = " + str(sys.argv[0]))
        print("Arg[1] = " + str(sys.argv[1]))
        print("Usage: python copy_media.py <src_folder> <dest_folder>")
        sys.exit(1)
    src_folder = sys.argv[1]
    dest_folder = sys.argv[2]
    # Run the function
    copy_media(src_folder, dest_folder)
