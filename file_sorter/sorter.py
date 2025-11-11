import file_converter
import exif_reader
import os 
from datetime import datetime
import shutil

# iterate over every file and subdirectory in the given folder
# for each file, 
# 1. if its not a valid image file, continue
# 2. if its a heic or other special format, convert it to jpeg
# 3. copy the file to the new date format, creating any new date folders as needed

def copy_file(source, dest, photopath):
    date = exif_reader.Read(photopath)
    
    if date is None:
        print(f"{photopath} is probably not an image, skipping")
        return
    
    date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    
    year = date.strftime("%Y")
    month = date.strftime("%m") 
    month_name = date.strftime("%B")
    
    if os.path.splitext(photopath)[1].lower() in ['.heic', '.heif']:
        # convert heic to jpeg in the same folder
        file_converter.HEIC_to_JPEG(source, photopath)
        # update photopath to new jpeg file
        photopath = os.path.splitext(photopath)[0] + '.jpg'
        
    elif os.path.splitext(photopath)[1].lower() in ['.mov']:
        # convert mov to mp4 in the same folder
        file_converter.to_MP4(source, photopath, date)
        # update photopath to new mp4 file
        photopath = os.path.splitext(photopath)[0] + '.mp4'
    
    elif os.path.splitext(photopath)[1].lower() in ['.avi']:
        # convert avi to mp4 in the same folder
        file_converter.to_MP4(source, photopath, date)
        # update photopath to new mp4 file
        photopath = os.path.splitext(photopath)[0] + '.mp4'
    
    dest_path = (f"{dest}\\{year}\\{month}-{month_name}\\{os.path.basename(photopath)}")
    
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    shutil.copy2(photopath, dest_path)
    print(f"Copied {photopath} to {dest_path}")
    
    