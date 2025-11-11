import os
import time
from file_sorter import sorter

if __name__ == "__main__":
    start_time = time.time()
    with open("config.txt", "r") as f:
        source_dir = f.readline().split("=", 1)[1].strip()
        dest_dir = f.readline().split("=", 1)[1].strip()

    print(f"Copying files from \nSOURCE - {source_dir} to \nDESTINATION - {dest_dir}\n\nLOG:")

    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                sorter.copy_file(file_path, dest_dir)

    elapsed = time.time() - start_time
    print(f"\nCompleted in {elapsed:.2f} seconds.")
    input("Press Enter to exit...")