from PIL import Image, ImageEnhance, ImageFilter
import os

# Input and output directory paths
input_dir = './imgs'
output_dir = './editedimgs'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Supported image file extensions
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png')

for filename in os.listdir(input_dir):
    # Check if file is a supported image format
    if filename.lower().endswith(SUPPORTED_FORMATS):
        input_path = os.path.join(input_dir, filename)
        
        # Open image
        with Image.open(input_path) as img:
            # Get EXIF metadata
            exif_data = img._getexif()
            
            # Handle image orientation
            orientation = exif_data.get(0x0112) if exif_data else None
            if orientation in (3, 6, 8):
                rotation = {3: 180, 6: 270, 8: 90}
                img = img.rotate(rotation[orientation], expand=True)
            
            # Apply sharpening
            sharpened = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            
            # Enhance contrast
            contrast_enhancer = ImageEnhance.Contrast(sharpened)
            edited = contrast_enhancer.enhance(1.2)
            
            # Create output filename
            base_name, ext = os.path.splitext(filename)
            output_filename = f'{base_name}_edited{ext}'
            output_path = os.path.join(output_dir, output_filename)
            
            # Save edited image
            edited.save(output_path, exif=exif_data)

print("Image processing complete.")
