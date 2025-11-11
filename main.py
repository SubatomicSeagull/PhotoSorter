import exif_reader
import file_converter
import os
from file_sorter import sorter


if __name__ == "__main__":
    source_dir = "C:\\Users\\jamie\\Desktop\\PhotoSorter\\photos\\"
    dest_dir = "C:\\Users\\jamie\\Desktop\\PhotoSorter\\sorted\\"
    
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                sorter.copy_file(source_dir, dest_dir, file_path)