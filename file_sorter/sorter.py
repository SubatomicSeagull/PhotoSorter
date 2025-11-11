import file_converter
import exif_reader
import os 
from datetime import datetime
import shutil

def copy_file(source, dest):
    date = exif_reader.Read(source)
    
    if date is None:
        print(f"\033[91m{source} is probably not an image, skipping\033[0m")
        return

    date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")

    year = date.strftime("%Y")
    month = date.strftime("%m") 
    month_name = date.strftime("%B")
    
    if os.path.splitext(source)[1].lower() in [".heic", ".heif"]:

        dest_path = (f"{dest}\\{year}\\{month}-{month_name}\\{os.path.splitext(os.path.basename(source))[0] + ".mp4"}")
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))
        file_converter.HEIC_to_JPEG(source, dest_path)

        
    elif os.path.splitext(source)[1].lower() in [".mov", ".avi", ".mkv"]:

        dest_path = (f"{dest}\\{year}\\{month}-{month_name}\\{os.path.splitext(os.path.basename(source))[0] + ".mp4"}")
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))
        file_converter.to_MP4(source, dest_path, date)
    
    else:
        dest_path = (f"{dest}\\{year}\\{month}-{month_name}\\{os.path.basename(source)}")
        
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))
            
        shutil.copy2(source, dest_path)
        
    print(f"Copied {source} to {dest_path}")