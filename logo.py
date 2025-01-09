from PIL import Image, ImageDraw, ImageFont
import os

def create_3d_sunday_service_poster(output_path):
    # Create a blank image for the poster with white background
    img = Image.new('RGBA', (800, 1200), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Add background color (white or transparent)
    background_color = (255, 255, 255)
    img.paste(background_color, (0, 0, 800, 1200))

    # Title with 3D text effect
    title = "Sunday Service"
    try:
        font_title = ImageFont.truetype("arial.ttf", 80)
    except IOError:
        font_title = ImageFont.load_default()

    # Calculate the title size and draw with shadow effect (3D look)
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    title_position = (400 - title_width // 2, 100)

    # Shadow Effect (Offset text for 3D look)
    shadow_offset = 5
    draw.text((title_position[0] + shadow_offset, title_position[1] + shadow_offset), title, font=font_title, fill=(100, 100, 100))  # Gray shadow

    # Actual text with bright color
    draw.text(title_position, title, font=font_title, fill=(255, 223, 0))  # Gold color for title

    # Tagline: "A Time of Worship and Fellowship"
    tagline = "A Time of Worship and Fellowship"
    try:
        font_tagline = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font_tagline = ImageFont.load_default()

    tagline_bbox = draw.textbbox((0, 0), tagline, font=font_tagline)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_height = tagline_bbox[3] - tagline_bbox[1]
    tagline_position = (400 - tagline_width // 2, 250)
    draw.text(tagline_position, tagline, font=font_tagline, fill=(255, 255, 255))  # White text for tagline

    # Service Details (Date, Time, Location)
    details = """
    Date: Sunday, 12th February 2025
    Time: 10:00 AM
    Location: Grace Chapel International - Kutus
    """
    try:
        font_details = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font_details = ImageFont.load_default()

    details_bbox = draw.textbbox((0, 0), details, font=font_details)
    details_width = details_bbox[2] - details_bbox[0]
    details_height = details_bbox[3] - details_bbox[1]
    details_position = (400 - details_width // 2, 400)
    draw.text(details_position, details, font=font_details, fill=(255, 255, 255))

    # Add a simple cross icon or other symbols related to faith (like light rays)
    cross_color = (255, 223, 0)
    draw.line((400, 500, 400, 700), fill=cross_color, width=10)  # Vertical line of the cross
    draw.line((350, 600, 450, 600), fill=cross_color, width=10)  # Horizontal line of the cross

    # Call to Action: Join Us! (in bold)
    call_to_action = "Join Us This Sunday!"
    try:
        font_cta = ImageFont.truetype("arial.ttf", 50)
    except IOError:
        font_cta = ImageFont.load_default()

    cta_bbox = draw.textbbox((0, 0), call_to_action, font=font_cta)
    cta_width = cta_bbox[2] - cta_bbox[0]
    cta_height = cta_bbox[3] - cta_bbox[1]
    cta_position = (400 - cta_width // 2, 850)
    draw.text(cta_position, call_to_action, font=font_cta, fill=(255, 223, 0))  # Gold color

    # Add a Bible Verse at the bottom
    bible_verse = "John 4:24 - 'God is Spirit, and his worshipers must worship in the Spirit and in truth.'"
    try:
        font_bible_verse = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font_bible_verse = ImageFont.load_default()

    verse_bbox = draw.textbbox((0, 0), bible_verse, font=font_bible_verse)
    verse_width = verse_bbox[2] - verse_bbox[0]
    verse_height = verse_bbox[3] - verse_bbox[1]
    verse_position = (400 - verse_width // 2, 1100)
    draw.text(verse_position, bible_verse, font=font_bible_verse, fill=(255, 255, 255))

    # Add Speaker Info (optional)
    speaker_info = "Speaker: Pastor John Doe"
    try:
        font_speaker = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font_speaker = ImageFont.load_default()

    speaker_bbox = draw.textbbox((0, 0), speaker_info, font=font_speaker)
    speaker_width = speaker_bbox[2] - speaker_bbox[0]
    speaker_height = speaker_bbox[3] - speaker_bbox[1]
    speaker_position = (400 - speaker_width // 2, 950)
    draw.text(speaker_position, speaker_info, font=font_speaker, fill=(255, 255, 255))

    # Save the poster image
    img.save(output_path)

# Folder to save the poster
output_folder = r'F:\GCI Kutus'

# Create the Sunday Service Poster and save it
create_3d_sunday_service_poster(os.path.join(output_folder, "sunday_service_poster_3d.png"))

print("3D Sunday Service Poster created and saved!")
