import os
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter

# Settings
SIZE = 512
PROCESSED_FOLDER = "processed"

# Create processed folder if it doesn't exist
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def process_image(img):
    width, height = img.size
    if width < height:
        img = img.resize((SIZE, int(SIZE * (height/width))), resample=Image.LANCZOS)
    else:
        img = img.resize((int(SIZE * (width/height)), SIZE), resample=Image.LANCZOS)
    if img.size[0] != img.size[1]:
        if width > height:
            half_height = img.size[1] // 2
            img1 = img.crop((0, 0, img.size[0], half_height))
            img2 = img.crop((0, half_height, img.size[0], img.size[1]))
        else:
            half_width = img.size[0] // 2
            img1 = img.crop((0, 0, half_width, img.size[1]))
            img2 = img.crop((half_width, 0, img.size[0], img.size[1]))
        img1 = ImageOps.fit(img1, (SIZE, SIZE), centering=(0.5, 0.5))
        img2 = ImageOps.fit(img2, (SIZE, SIZE), centering=(0.5, 0.5))
        return img, img1, img2

def process_image_file(filename):
    img = Image.open(filename)
    img, img1, img2 = process_image(img)
    base_filename, file_suffix = os.path.splitext(filename)    
    base_filename = os.path.basename(base_filename)
    img.save(os.path.join(PROCESSED_FOLDER, filename))
    img1.save(os.path.join(PROCESSED_FOLDER, base_filename + '_1' + file_suffix))
    img2.save(os.path.join(PROCESSED_FOLDER, base_filename + '_2' + file_suffix))

def process_image_files(filenames):
    for filename in filenames:
        process_image_file(filename)

if len(sys.argv) == 2:
    process_image_file(sys.argv[1])
elif len(sys.argv) == 2:
    filenames = [f for f in os.listdir(sys.argv[1]) if f.endswith((".jpg", ".png", ".webp"))]
    process_image_files(filenames)
else:
    filenames = [f for f in os.listdir(".") if f.endswith((".jpg", ".png", ".webp"))]
    process_image_files(filenames)
