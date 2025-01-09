from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps
import os
import random

# Set the folder paths
input_folder = r'F:\goyee mission'  # Input folder where your images are
output_folder = r'F:\edited'  # Output folder to save the edited images
logo_path = r'F:\GCI Kutus\logo.jpg'  # Path to the logo image

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to handle orientation based on EXIF data
def open_image_with_correct_orientation(image_path):
    img = Image.open(image_path)
    try:
        img = ImageOps.exif_transpose(img)  # Correct orientation
    except (AttributeError, KeyError, IndexError):
        pass  # No EXIF data, so leave the image as is
    return img

# Function to apply classic adjustments to the image
def adjust_image(img):
    # Enhance brightness (increase for more brightness)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)  # Increase brightness by 20% for more vibrancy

    # Enhance contrast (slightly enhance to add depth)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)  # Increase contrast by 30% for stronger definition

    # Enhance saturation gently (to maintain classic tones)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.8)  # Reduce saturation by 20% for a timeless feel

    # Apply soft sharpening (to enhance details)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Add subtle noise to mimic film grain
    img = add_film_grain(img)

    # Apply a slight soft focus
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))  # Soft blur for a classic finish

    return img

# Function to add subtle film grain (noise)
def add_film_grain(img):
    width, height = img.size
    pixels = img.load()
    
    # Add random noise to pixels to mimic film grain
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            noise = random.randint(-10, 10)  # Random noise for a classic grainy effect
            pixels[i, j] = (
                min(255, max(0, r + noise)),
                min(255, max(0, g + noise)),
                min(255, max(0, b + noise))
            )
    
    return img

# Function to add a circular logo with a border and shadow to the image
def add_logo(img, logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    
    # Resize the logo to 7% of the image width
    logo_width = int(img.width * 0.07)  # Make the logo 7% of the image width
    logo_height = int(logo_width * logo.height / logo.width)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)  # Use LANCZOS for resampling
    
    # Create circular mask for the logo
    mask = Image.new("L", (logo_width, logo_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, logo_width, logo_height), fill=255)

    # Apply the mask to make the logo circular
    logo = Image.composite(logo, Image.new("RGBA", logo.size, (0, 0, 0, 0)), mask)

    # Add an orange circular border around the logo
    border_size = 8  # Smaller border size
    border_img = Image.new("RGBA", (logo_width + border_size * 2, logo_height + border_size * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(border_img)
    draw.ellipse((0, 0, logo_width + border_size * 2, logo_height + border_size * 2), fill=(255, 165, 0))  # Orange color
    border_img.paste(logo, (border_size, border_size), logo)

    # Create shadow effect for the logo with border
    shadow = Image.new("RGBA", (logo_width + border_size * 2 + 10, logo_height + border_size * 2 + 10), (0, 0, 0, 0))
    shadow.paste(border_img, (10, 10))  # Offset the shadow
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))  # Apply blur to the shadow for effect

    # Get the position (bottom-center) for the logo with shadow
    logo_position = (img.width // 2 - (logo_width + border_size * 2) // 2, img.height - (logo_height + border_size * 2) - 20)

    # Paste the shadow and then the logo on the image (with transparency)
    img.paste(shadow, logo_position, shadow)
    img.paste(border_img, logo_position, border_img)

    return img

# Iterate through all files in the input folder (process all images)
for filename in os.listdir(input_folder):
    print(f"Found file: {filename}")  # Debugging: check filenames
    
    if filename.endswith('.JPG'):  # Process only image files
        image_path = os.path.join(input_folder, filename)
        try:
            print(f"Processing image: {filename}")  # Debugging: check if the image is processed
            img = open_image_with_correct_orientation(image_path)  # Correct orientation
            
            # Ensure the image is in RGB format (to avoid issues with alpha channels)
            img = img.convert("RGB")
            
            # Apply classic adjustments to the image (brightness, contrast, etc.)
            img = adjust_image(img)
            
            # Add logo to the image (at bottom-center)
            img = add_logo(img, logo_path)
            
            # Save the edited image to the output folder with "_version1" suffix
            output_image_path = os.path.join(output_folder, filename.split('.')[0] + "_version1.JPG")
            img.save(output_image_path)
            print(f"Processed and saved: {filename.split('.')[0]}_version1.JPG")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")  # In case an error occurs during processing
    else:
        print(f"Skipping non-image file: {filename}")

print("Batch processing complete!")
