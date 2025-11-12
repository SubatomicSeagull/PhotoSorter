# determin the file type and read the exif data return the earliest creation date either in the medatada or falling back on the file system modification date
from PIL import Image, ExifTags
import os
from datetime import datetime
from pymediainfo import MediaInfo
from pillow_heif import register_heif_opener
import exifread

register_heif_opener()

def get_earliest_date1(dates):
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

def get_earliest_date(dates):
    formats = [
        "%Y:%m:%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S %Z"
    ]
    
    parsed = []
    
    for date in dates:
        if date is None:
            continue

        for line in formats:
            # skip dates that are probably invalid i.e 01/01/1970

            try:
                if datetime.strptime(date, line).month != 1 and datetime.strptime(date, line).day != 1 and datetime.strptime(date, line).hour != 0 and datetime.strptime(date, line).minute != 0 and datetime.strptime(date, line).second != 0:
                    parsed.append((datetime.strptime(date, line)))
                    break
            except Exception:
                continue

    lowest = min(parsed)
    return lowest

def get_file_creation_dates(photopath):
    dates = []
    dates.append(datetime.fromtimestamp(os.path.getmtime(photopath)).strftime("%Y:%m:%d %H:%M:%S"))
    dates.append(datetime.fromtimestamp(os.path.getctime(photopath)).strftime("%Y:%m:%d %H:%M:%S"))
    dates.append(datetime.fromtimestamp(os.path.getatime(photopath)).strftime("%Y:%m:%d %H:%M:%S"))
    return dates

def read_simple_image_metadata(photopath):
    
    dates = get_file_creation_dates(photopath)
    
    with open(photopath, 'rb') as f:
        tags = exifread.process_file(f)
        
    print("======METADATA FOR IMAGE========")
    for tag in tags:
        print(f"{tag}: {tags[tag]}")
        if tag in ["EXIF DateTimeOriginal", "Image DateTime"]:
            dates.append(str(tags[tag]))
    print("================================")
    
    print(f"======================\nDATES FOUND: {dates}\n======================")
    print(f"USING DATE: {get_earliest_date(dates)}")
    return get_earliest_date(dates)


def read_video_metadata(photopath):
    mediainfo = MediaInfo.parse(photopath)

    dates = get_file_creation_dates(photopath)
    data = {"file_last_modification_date", "encoded_date"}


    print("======METADATA FOR VIDEO========")
    for track in mediainfo.tracks:
        info = track.to_data()
        for key, value in info.items():
            if key in data and value:
                dates.append(value)
                print(f"{key}: {value}")
    print("================================")
    print(f"======================\nDATES FOUND: {dates}\n======================")
    print(f"USING DATE: {get_earliest_date(dates)}")
    
    return get_earliest_date(dates)

def parse_type(photopath):
    
    imagetype = (os.path.splitext(photopath)[1][1:]).lower()
    
    match imagetype:
            
        case "mp4" | "avi" | "mkv" | "mov" | "vob" | "webm"| "3gp":
            return read_video_metadata(photopath)
            
        case "jpg" | "jpeg" | "png" | "tiff" | "tif" | "gif" | "bmp" | "webp" | "exr" | "heif" | "heic" | "raw" | "dng":
            return read_simple_image_metadata(photopath)
        
        case "_":
            return None