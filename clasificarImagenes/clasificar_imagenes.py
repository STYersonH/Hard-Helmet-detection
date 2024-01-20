from clasificar import clasificar_imagen

import os

def process_images(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Filter the list to include only .png and .jpg files
    image_files = [f for f in files if f.endswith('.png') or f.endswith('.jpg')]

    # Process each image file
    for i, image_file in enumerate(image_files):
        clasificar_imagen(os.path.join(directory, image_file), i)


process_images('./')
