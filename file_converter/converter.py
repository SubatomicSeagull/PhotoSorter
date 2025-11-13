from PIL import Image
from pillow_heif import register_heif_opener
import os
import subprocess
from datetime import datetime

def convert_heic_to_jpeg(source, dest):
    filename = os.path.basename(source)
    dirpath = os.path.dirname(source)
    print (f"\033[95mConverting {filename} to JPEG\033[0m")
    
    register_heif_opener()
    photo = Image.open(source)
    exif = photo.getexif()
    
    destination_path = os.path.join(dirpath, os.path.splitext(filename)[0] + '.jpg')
    
    photo.save(destination_path, "JPEG", quality=95, exif=exif, optimize=True)
    
# convert MOV and avi to MP4
def convert_to_mp4(source, dest, modified_date):
    filename = os.path.basename(source)
    
    command = [
        "ffmpeg",
        #"-hide_banner", "-loglevel", "error", "-nostats",
        "-fflags", "+genpts",
        "-i", source,
        "-metadata", f"creation_time={modified_date}",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-y",
        dest
    ]
    print(f"\033[95mConverting {filename} to MP4\033[0m")
    subprocess.run(command, check=True)