import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import textwrap
import requests

# Function to convert image to base64 string
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to download and load a font
def load_font(font_url, font_size):
    response = requests.get(font_url)
    font = ImageFont.truetype(io.BytesIO(response.content), font_size)
    return font

# Function to add text to image
def add_text_to_image(image, text, font_color):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Calculate font size and load font
    font_size = max(12, int(width / 20))
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosanstamil/NotoSansTamil%5Bwdth%2Cwght%5D.ttf"
    font = load_font(font_url, font_size)
    
    # Estimate characters per line and wrap text
    chars_per_line = max(1, int(width / (font_size * 0.6)))
    wrapped_text = textwrap.fill(text, width=chars_per_line)
    
    # Get text size and position
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((width - text_width) / 2, (height - text_height) / 2)
    
    # Draw text outline
    outline_color = "black"
    for adj in range(-2, 3):
        draw.multiline_text((position[0]+adj, position[1]), wrapped_text, font=font, fill=outline_color, align="center")
        draw.multiline_text((position[0], position[1]+adj), wrapped_text, font=font, fill=outline_color, align="center")
    
    # Draw main text
    draw.multiline_text(position, wrapped_text, font=font, fill=font_color, align="center")
    
    return image

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
        
        # Create image with text overlay
        result_image = add_text_to_image(image.copy(), text_input, font_color)
        
        # Display the result
        st.image(result_image, caption="Result Image", use_column_width=True)

        # Option to download the result image
        buffered = io.BytesIO()
        result_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        st.download_button(
            label="Download Image",
            data=buffered.getvalue(),
            file_name="result_image.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
