from PIL import Image
from PIL.Image import Exif
import os
from datetime import datetime
import exifread
import piexif
from exif_reader.reader import read_simple_image_metadata, read_video_metadata
import subprocess


def update_image_dates(image_path, new_date):
    """
    Overwrites only the EXIF date-related fields:
      - DateTime (ImageIFD)
      - DateTimeOriginal (ExifIFD)
      - DateTimeDigitized (ExifIFD)
    using a date string in format 'YYYY:MM:DD HH:MM:SS'.
    """
    try:
        datetime.strptime(new_date, "%Y:%m:%d %H:%M:%S")
    except ValueError:
        raise ValueError("Date must be in 'YYYY:MM:DD HH:MM:SS' format")

    # Use exifread just to confirm the file is readable
    with open(image_path, "rb") as f:
        tags = exifread.process_file(f, details=False)
        if not tags:
            print("No EXIF found; will create minimal EXIF data.")

    # Build a minimal valid EXIF dictionary with only the date fields
    exif_dict = {
        "0th": {
            piexif.ImageIFD.DateTime: new_date.encode("ascii")
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: new_date.encode("ascii"),
            piexif.ExifIFD.DateTimeDigitized: new_date.encode("ascii"),
        },
        "1st": {},
        "GPS": {},
        "thumbnail": None,
    }

    # Write back to file
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)

    print(f"✔ Updated EXIF date fields for {os.path.basename(image_path)}")



def update_mp4_dates(file_path, new_date):
    """
    Updates MP4 metadata timestamps (creation_time and modify_time)
    using ffmpeg without re-encoding.
    
    new_date must be in format 'YYYY-MM-DD HH:MM:SS'
    """
    # Validate date
    try:
        datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Date must be in 'YYYY-MM-DD HH:MM:SS' format")

    # Convert to ISO 8601 format used by ffmpeg
    iso_date = new_date.replace(" ", "T")

    # Output temp file (ffmpeg can't modify in place)
    temp_file = file_path + ".tmp.mp4"

    # Build ffmpeg command
    cmd = [
        "ffmpeg",
        "-loglevel", "error",
        "-y",
        "-i", file_path,
        "-codec", "copy",
        "-metadata", f"creation_time={iso_date}",
        "-metadata", f"modify_time={iso_date}",
        temp_file
    ]

    subprocess.run(cmd, check=True)

    # Replace original file
    os.replace(temp_file, file_path)

    print(f"✔ Updated MP4 metadata dates for {os.path.basename(file_path)} to {new_date}")



filepath = ""
date = ""

update_mp4_dates(filepath, date)
read_video_metadata(filepath)
