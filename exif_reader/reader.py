# determin the file type and read the exif data return the earliest creation date either in the medatada or falling back on the file system modification date
from PIL import Image, ExifTags
import os
from datetime import datetime
from pymediainfo import MediaInfo
from pillow_heif import register_heif_opener

register_heif_opener()

def get_earliest_date(dates):
    parsed = []
    for d in dates:
        if not d:
            continue
        try:
            dt = datetime.strptime(d, "%Y:%m:%d %H:%M:%S")
            parsed.append((dt, d))
        except Exception:
            continue
    parsed.sort(key=lambda x: x[0])
    return parsed[0][1]

def get_file_creation_dates(photopath):
    dates = []
    dates.append(datetime.fromtimestamp(os.path.getmtime(photopath)).strftime("%Y:%m:%d %H:%M:%S"))
    dates.append(datetime.fromtimestamp(os.path.getctime(photopath)).strftime("%Y:%m:%d %H:%M:%S"))
    dates.append(datetime.fromtimestamp(os.path.getatime(photopath)).strftime("%Y:%m:%d %H:%M:%S"))
    return dates

def read_simple_image_metadata(photopath):
    try:
        photo = Image.open(photopath)
        exif = photo.getexif()
    except Exception as e:
        print(f"Failed to open image/exif: {e}, skipping")
        return

    data = {"DateTimeOriginal", "DateTime"}
    dates = get_file_creation_dates(photopath)
    for key, val in exif.items():
        tag = ExifTags.TAGS.get(key, key)
        if tag in data:
            dates.append(val)
    return get_earliest_date(dates)

def read_video_metadata(photopath):
    mediainfo = MediaInfo.parse(photopath)

    dates = get_file_creation_dates(photopath)
    data = {"file_last_modification_date", "encoded_date"}

    for track in mediainfo.tracks:
        info = track.to_data()
        for key, value in info.items():
            if key in data and value:
                dates.append(value)
    return get_earliest_date(dates)

def parse_type(photopath):
    
    imagetype = (os.path.splitext(photopath)[1][1:]).lower()
    
    match imagetype:
            
        case "mp4" | "avi" | "mkv" | "mov" | "vob" | "webm":
            print (f"Video: {photopath}: Type: {imagetype}, Date: {date}")
            return read_video_metadata(photopath)
            
        case "jpg" | "jpeg" | "png" | "tiff" | "tif" | "gif" | "bmp" | "webp" | "exr" | "heif" | "heic" | "raw" | "dng":
            date = read_simple_image_metadata(photopath)
            print (f"Image: {photopath}: Type: {imagetype}, Date: {date}")
            return date
        
        case "_":
            print(f"Type: Other ({imagetype})")