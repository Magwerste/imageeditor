from PIL import Image, ImageEnhance, ImageFilter
import os

input_dir = './imgs'
output_dir = './editedimgs'

#CREAT OUTPUT DIRECTORY -> IF IT DOESNT EXIST
os.makedirs(output_dir, exist_ok = True)

for filename in os.listdir(input_dir):
    #VERIFY FILE IS AN IMAGE
    if filename.endswith('.jpg') or filename.endswith('.png'):

        input_file = os.path.join(input_dir, filename)

        #OPEN IMAGE
        img = Image.open(f"{input_dir}/{filename}")

        #GET EXIF METADATA
        exif_data = img.getexif()

        #ORIENTATION/ROTATION
        orientation = exif_data.get(0x0112) if exif_data else None
        if orientation == 3:
            img = img.rotate(180, expand=True)

        elif orientation == 6:
            img = img.rotate(270, expand=True)
        
        elif orientation == 9:
            img = img.rotate(90, expand=True)
        

        #SHARPEN + PARAMETERS

        radius = 10  # Radius of the UnsharpMask filter
        percent = 110  # Percentage of sharpening (100 = no change, 200 = 2x sharpening)
        threshold = 3  # Threshold for sharpening (0-255, higher values reduce sharpening)
        edit = img.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))

        #CONTRAST
        factor = 1.15
        enchancer = ImageEnhance.Contrast(edit)
        edit = enchancer.enhance(factor)


        #CREATE OUTPUT FILENAME
        clean_name, ext = os.path.splitext(filename)
        output_filename = f'{clean_name}_edited{ext}'
        output_file = os.path.join(output_dir, output_filename)

        #SAVE
        edit.save(output_file)
    

    
