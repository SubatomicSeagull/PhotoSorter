from PIL import Image
from pillow_heif import register_heif_opener
import os

def convert_heic_to_jpeg(source_dir, photopath):
    filename = os.path.basename(photopath)
    print (f"Converting {filename} to JPEG...")
    
    register_heif_opener()
    photo = Image.open(photopath)
    exif = photo.getexif()
    
    destination_path = os.path.join(source_dir, os.path.splitext(filename)[0] + '.jpg')
    
    photo.save(destination_path, "JPEG", quality=95, exif=exif, optimize=True)
    print(f"Saved converted image to {destination_path}")

# convert MOV to MP4
def convert_mov_to_mp4(source_dir, photopath):
    pass

def convert_avi_to_mp4(source_dir, photopath):
    pass