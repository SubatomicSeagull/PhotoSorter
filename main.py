<<<<<<< HEAD
import exif_reader
import heic_converter


def __main__():
    exif_reader.Read("C:\\Users\\jamie\\Desktop\\PhotoSorter\\photos\\20130716_102004.jpg")


=======
from PIL import Image, ExifTags
import os
from datetime import datetime
from pymediainfo import MediaInfo
import pathlib
import sys


photopath = "C:\\Users\\jamie\\Desktop\\PhotoSorter\\photos\\kidspicutres (43).JPG"

imagetype = (os.path.splitext(photopath)[1][1:]).lower()

# Use Python 3.10+ match-case if available; otherwise fall back to if/elif

match imagetype:
    case 'jpg' | 'jpeg':
        print('Type: JPEG image')
    case 'png':
        print('Type: PNG image')
    case 'tiff' | 'tif':
        print('Type: TIFF image')
    case 'gif':
        print('Type: GIF image')
    case 'bmp':
        print('Type: BMP image')
    case 'raw' | 'cr2' | 'nef' | 'arw' | 'dng':
        print('Type: RAW image')
    case 'mp4' | 'mov' | 'avi':
        print('Type: Video file')
    case 'heic' | 'heif':
        print('Type: HEIC/HEIF image')
    case 'webp':
        print('Type: WEBP image')
    case "webm":
        print('Type: WEBM video')
    case "vob":
        print('Type: VOB video')
    case "exr":
        print('Type: EXR image')
    case "_":
        print(f'Type: Other ({imagetype})')
            
photo = Image.open(photopath)
exif = photo.getexif()
datemodified = datetime.fromtimestamp(os.path.getmtime(photopath)).strftime('%Y:%m:%d %H:%M:%S')
datecreated = datetime.fromtimestamp(os.path.getctime(photopath)).strftime('%Y:%m:%d %H:%M:%S')
dateaccessed = datetime.fromtimestamp(os.path.getatime(photopath)).strftime('%Y:%m:%d %H:%M:%S')
print(f'Date Modified:{datemodified}')
print(f'Date Created:{datecreated}')
print(f'Date Accessed:{dateaccessed}')
for key, val in exif.items():
    if key in ExifTags.TAGS:
        print(f'{ExifTags.TAGS[key]}:{val}')
    else:
        print(f'{key}:{val}')

#jpg
>>>>>>> 4a5e1a3 (depends + image filter)
