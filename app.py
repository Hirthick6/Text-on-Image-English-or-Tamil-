import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import textwrap

# Function to convert image to base64 string
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to add text to image
def add_text_to_image(image, text, font_color, font_size):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Load font (you may need to adjust the path)
    try:
        font = ImageFont.truetype("NotoSansTamil-Regular.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Wrap text
    chars_per_line = max(1, int(width / (font_size * 0.6)))
    wrapped_text = textwrap.fill(text, width=chars_per_line)
    
    # Calculate text position
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Draw text shadow
    shadow_color = "black"
    for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        draw.multiline_text((x + offset[0], y + offset[1]), wrapped_text, font=font, fill=shadow_color, align="center")
    
    # Draw main text
    draw.multiline_text((x, y), wrapped_text, font=font, fill=font_color, align="center")
    
    return image

# Function to generate HTML content
def generate_html(image_base64, text, color, width, height):
    # ... (keep the existing HTML generation code) ...

# Streamlit app
def main():
    st.set_page_config(page_title="Text on Image App", layout="wide")
    
    st.title("Text on Image (Mixed Tamil, English, and Numbers)")

    # Sidebar
    st.sidebar.title("About Me")
    st.sidebar.write("Done by Hirthick S")
    st.sidebar.write("Data Science Scholar")
    st.sidebar.title("Project Overview")
    st.sidebar.write("This project integrates mixed Tamil, English, and numeric text into images.")
    st.sidebar.title("Language Used")
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", width=50)
    st.sidebar.write("Python")

    # Main content
    text_input = st.text_input("Enter the text", value="")
    uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
    font_color = st.color_picker("Pick a text color", "#FFFFFF")  # Default is white

    if uploaded_image and text_input:
        image = Image.open(uploaded_image)
        width, height = image.size
        font_size = max(12, int(width / 20))  # Minimum font size of 12px
        
        # Create a copy of the image and add text
        image_with_text = image.copy()
        image_with_text = add_text_to_image(image_with_text, text_input, font_color, font_size)
        
        # Convert to base64 for display
        image_base64 = image_to_base64(image_with_text)
        html_content = generate_html(image_base64, text_input, font_color, width, height)

        # Display the HTML content
        st.components.v1.html(html_content, height=height, scrolling=True)

        # Convert image to bytes for download
        img_byte_arr = io.BytesIO()
        image_with_text.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Option to download the image
        st.download_button(
            label="Download Image",
            data=img_byte_arr,
            file_name="result.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
