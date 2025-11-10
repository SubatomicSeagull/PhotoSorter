from PIL import Image
from pillow_heif import register_heif_opener

def convert_heic_to_jpeg(photopath):
    register_heif_opener()
    photo = Image.open(photopath)
    exif = photo.getexif()
    photo.save("C:\\Users\\jamie\\Desktop\\PhotoSorter\\photos\\test_converted.jpg", "JPEG", quality=95, exif=exif, optimize=True)