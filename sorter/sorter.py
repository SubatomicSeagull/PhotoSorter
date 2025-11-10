# iterate over every file and subdirectory in the given folder
# for each file, 
# 1. if its not a valid image file, continue
# 2. if its a heic or other special format, convert it to jpeg
# 3. create an empty metadata object and populate it with exif data
# 4. copy the file to the new date format, creating any new date folders as needed