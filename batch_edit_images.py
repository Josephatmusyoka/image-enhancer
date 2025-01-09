import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os

# Set the folder paths
input_folder = r'F:\goyee mission'  # Input folder where your images are
output_folder = r'F:\edited'  # Output folder to save the edited images
logo_path = r'F:\GCI Kutus\logo.jpg'  # Path to your logo image

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the logo
logo = Image.open(logo_path)

# Convert the logo to RGBA (for transparency handling)
logo = logo.convert("RGBA")

# Add a function to resize the logo based on the image size (without scaling)
def resize_logo(logo, img_width, img_height):
    # Resize the logo based on the smaller dimension (width or height) of the image
    scale_factor = 0.15  # Logo will take up 15% of the smaller dimension (adjustable)
    
    # Get original logo dimensions
    logo_width, logo_height = logo.size
    
    # Resize the logo according to the scale factor based on the image's size
    logo_width_resized = int(img_width * scale_factor)
    logo_height_resized = int(logo_height * scale_factor)
    
    # Resize the logo proportionally
    logo_resized = logo.resize((logo_width_resized, logo_height_resized))
    
    # Create a circular mask for the logo (without removing its background)
    mask = Image.new("L", logo_resized.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, logo_resized.width, logo_resized.height), fill=255)  # Draw a white circle

    # Apply the circular mask to the logo
    logo_resized.putalpha(mask)
    
    return logo_resized

# Create a circular border around the logo
def add_logo_border(logo_resized):
    border_color = (173, 216, 230)  # Light Blue border (can change to orange or yellow)
    border_width = 10  # Width of the border
    
    # Create a new image for the border
    bordered_logo = Image.new("RGBA", (logo_resized.width + 2 * border_width, logo_resized.height + 2 * border_width), (0, 0, 0, 0))  # Transparent background
    border_draw = ImageDraw.Draw(bordered_logo)
    
    # Draw the circular border
    border_draw.ellipse((0, 0, bordered_logo.width, bordered_logo.height), outline=border_color, width=border_width)
    
    # Paste the logo onto the image with the border
    bordered_logo.paste(logo_resized, (border_width, border_width), logo_resized)
    
    return bordered_logo

# Add shadow effect to the logo
def add_shadow_to_logo(bordered_logo):
    shadow_offset = 10  # Shadow displacement (offset)
    shadow_color = (255, 140, 0, 100)  # Orange shadow with transparency
    
    shadow = Image.new("RGBA", bordered_logo.size, (0, 0, 0, 0))  # Transparent background
    shadow.paste(bordered_logo, (shadow_offset, shadow_offset))  # Apply shadow offset
    
    # Blur the shadow to make it soft
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    
    # Combine the shadow and bordered logo
    final_logo = Image.alpha_composite(shadow, bordered_logo)
    
    return final_logo

def adjust_brightness_contrast(img):
    """Adjust the brightness and contrast of the image automatically."""
    # Convert image to grayscale for brightness/contrast analysis
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    min_gray = np.min(gray)
    max_gray = np.max(gray)
    
    # Adjust brightness (if image is too dark or too bright)
    if min_gray < 50:
        # Increase brightness if the image is too dark
        brightness_factor = 1.2
    elif max_gray > 200:
        # Decrease brightness if the image is too bright
        brightness_factor = 0.8
    else:
        brightness_factor = 1  # No adjustment if brightness is fine
    
    # Enhance contrast: we can do a histogram stretch
    contrast = cv2.convertScaleAbs(img, alpha=1.3, beta=0)  # alpha for contrast
    
    return contrast

def reduce_noise(img):
    """Remove noise from the image using OpenCV."""
    # Use Non-Local Means Denoising algorithm (good for color images)
    denoised_img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)  # Reduced noise parameters
    return denoised_img

def adjust_hue(img):
    """Automatically adjust the hue of the image to make colors appear more natural."""
    # Convert to HSV color space for easier hue adjustments
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # Adjust hue (shift by 10 for minor correction)
    h = cv2.add(h, 10)
    
    # Merge the adjusted hue back
    adjusted_hue_img = cv2.merge([h, s, v])
    
    # Convert back to BGR
    img_with_adjusted_hue = cv2.cvtColor(adjusted_hue_img, cv2.COLOR_HSV2BGR)
    
    return img_with_adjusted_hue

def process_image(image_path):
    """Process each image: reduce noise, adjust lighting, contrast, and hue."""
    img = cv2.imread(image_path)

    # Step 1: Reduce Noise
    img = reduce_noise(img)

    # Step 2: Adjust Brightness and Contrast
    img = adjust_brightness_contrast(img)

    # Step 3: Adjust Hue (if needed)
    img = adjust_hue(img)
    
    return img

def save_processed_image(output_path, img):
    """Save the processed image to the output folder."""
    # Convert image from BGR to RGB for saving using Pillow
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    pil_img.save(output_path)

# Counter for the first five images
processed_files = 0

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):  # Process image files
        if processed_files >= 5:  # Stop after processing 5 images
            break
        
        image_path = os.path.join(input_folder, filename)
        try:
            print(f"Processing image: {filename}")
            
            # Step 1: Process the image (reduce noise, adjust brightness/contrast, hue)
            processed_img = process_image(image_path)

            # Step 2: Convert processed image to Pillow format for logo overlay
            processed_img_pil = Image.fromarray(processed_img)

            # Step 3: Resize the logo based on the image size
            img_width, img_height = processed_img_pil.size
            resized_logo = resize_logo(logo, img_width, img_height)

            # Step 4: Add border to the resized logo
            bordered_logo = add_logo_border(resized_logo)

            # Step 5: Add shadow to the logo
            final_logo = add_shadow_to_logo(bordered_logo)

            # Step 6: Calculate position for the logo (bottom center)
            logo_width, logo_height = final_logo.size
            x_position = (img_width - logo_width) // 2  # Center the logo horizontally
            y_position = img_height - logo_height  # Place logo at the bottom

            # Paste the logo onto the image with transparency (using the alpha channel)
            processed_img_pil.paste(final_logo, (x_position, y_position), final_logo)

            # Step 7: Save the processed image to the output folder
            output_image_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_processed{os.path.splitext(filename)[1]}")
            save_processed_image(output_image_path, np.array(processed_img_pil))
            
            processed_files += 1
            print(f"Processed and saved: {filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")  # In case an error occurs during processing
    else:
        print(f"Skipping non-image file: {filename}")

print("Batch processing complete!")
