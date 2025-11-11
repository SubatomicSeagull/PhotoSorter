from PIL import Image
from pillow_heif import register_heif_opener
import os
import subprocess
from datetime import datetime

def convert_heic_to_jpeg(source_dir, photopath):
    filename = os.path.basename(photopath)
    print (f"Converting {filename} to JPEG...")
    
    register_heif_opener()
    photo = Image.open(photopath)
    exif = photo.getexif()
    
    destination_path = os.path.join(source_dir, os.path.splitext(filename)[0] + '.jpg')
    
    photo.save(destination_path, "JPEG", quality=95, exif=exif, optimize=True)
    
# convert MOV and avi to MP4
def convert_to_mp4(source_dir, photopath, modified_date):
    filename = os.path.basename(photopath)
    destination_path = os.path.join(source_dir, os.path.splitext(filename)[0] + '.mp4')
    
    command = [
        "ffmpeg",
        "-hide_banner", "-loglevel", "error", "-nostats",
        "-fflags", "+genpts",
        "-i", photopath,
        "-metadata", f"creation_time={modified_date}",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-y",
        destination_path
    ]
    print(f"Converting {filename} to MP4...")
    subprocess.run(command, check=True)