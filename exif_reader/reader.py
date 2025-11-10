# determin the file type and read the exif data and populate a metadata object with any information it can find
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
            dt = datetime.strptime(d, '%Y:%m:%d %H:%M:%S')
            parsed.append((dt, d))
        except Exception:
            continue
    parsed.sort(key=lambda x: x[0])
    return parsed[0][1]

def get_file_creation_dates(photopath):
    dates = []
    dates.append(datetime.fromtimestamp(os.path.getmtime(photopath)).strftime('%Y:%m:%d %H:%M:%S'))
    dates.append(datetime.fromtimestamp(os.path.getctime(photopath)).strftime('%Y:%m:%d %H:%M:%S'))
    dates.append(datetime.fromtimestamp(os.path.getatime(photopath)).strftime('%Y:%m:%d %H:%M:%S'))
    return dates

def read_simple_image_metadata(photopath):
    try:
        photo = Image.open(photopath)
        exif = photo.getexif()
    except Exception as e:
        print(f'Failed to open image/exif: {e}')
        return

    data = {'DateTimeOriginal', 'DateTime'}
    dates = get_file_creation_dates(photopath)
    for key, val in exif.items():
        tag = ExifTags.TAGS.get(key, key)
        if tag in data:
            dates.append(val)
    return get_earliest_date(dates)

def read_video_metadata(photopath):
    mediainfo = MediaInfo.parse(photopath)

    dates = get_file_creation_dates(photopath)
    data = {'file_last_modification_date', 'encoded_date'}

    for track in mediainfo.tracks:
        info = track.to_data()
        for key, value in info.items():
            if key in data and value:
                dates.append(value)
    return get_earliest_date(dates)

def parse_type(photopath):
    
    imagetype = (os.path.splitext(photopath)[1][1:]).lower()
    
    match imagetype:
        case 'jpg' | 'jpeg':
            print('Type: JPEG image')
            read_simple_image_metadata(photopath)
            # use DateTimeOrigianl, fallback on DateTime, fallback on date modified
            
        case 'png':
            print('Type: PNG image')
            read_simple_image_metadata(photopath)
            # use date modified
            
        case 'tiff' | 'tif':
            print('Type: TIFF image')
            read_simple_image_metadata(photopath)
            # use DateTime, fallback on date modified
            
        case 'gif':
            print('Type: GIF image')
            read_simple_image_metadata(photopath)
            # use date modified
            
        case 'bmp':
            print('Type: BMP image')
            read_simple_image_metadata(photopath)
            # use date modified
            
        case 'webp':
            print('Type: WEBP image')
            read_simple_image_metadata(photopath)
            # use date modified
            
        case "exr":
            read_simple_image_metadata(photopath)
            # use date modified
            
        case 'raw' | 'cr2' | 'nef' | 'arw' | 'dng':
            print('Type: RAW image')
            read_simple_image_metadata(photopath)
            # use DateTimeOriginal, fallback on DateTime, fallback on date modified
            
        case 'mp4' | 'avi' | "mkv":
            print('Type: Video file')
            read_video_metadata(photopath)
            # use file_last_modification_date, fallback on date modified
            
        case "mov":
            print('Type: MOV video')
            read_video_metadata(photopath)
            # use encoded date, fallback to file_last_modification_date, fallback on date modified
            
        case 'heic' | 'heif':
            print('Type: HEIC/HEIF image')
            read_simple_image_metadata(photopath)
            # use DateTimeOriginal, fallback on DateTime, fallback on date modified
            
        case "webm":
            print('Type: WEBM video')
            read_video_metadata(photopath)
            # use date modified
        
        case "vob":
            print('Type: VOB video')
            read_video_metadata(photopath)
            # use date modified
            
        case "_":
            print(f'Type: Other ({imagetype})')