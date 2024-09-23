import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import textwrap
import numpy as np
from scipy import ndimage

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

# Function to remove brackets
def remove_brackets(img):
    # Convert to numpy array
    img_array = np.array(img)
    
    # Define the color of the brackets (you may need to adjust this)
    bracket_color = [0, 0, 0]  # Black
    
    # Create a mask for the brackets
    mask = np.all(img_array == bracket_color, axis=-1)
    
    # Dilate the mask to capture the full brackets
    mask = ndimage.binary_dilation(mask, iterations=2)
    
    # Fill the bracket areas with the background color
    bg_color = img_array[0, 0]  # Assuming top-left pixel is background
    img_array[mask] = bg_color
    
    # Convert back to PIL Image
    result = Image.fromarray(img_array)
    
    return result

# Function to generate HTML content
def generate_html(image_base64, text, color, width, height):
    font_size = max(12, int(width / 20))  # Minimum font size of 12px
    chars_per_line = max(1, int(width / (font_size * 0.6)))
    wrapped_text = textwrap.fill(text, width=chars_per_line)
    
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body, html {{
                height: 100%;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                position: relative;
                display: inline-block;
                width: {width}px;
                height: {height}px;
            }}
            .image {{
                width: 100%;
                height: 100%;
                object-fit: contain;
            }}
            .text {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: {color};
                font-family: 'Noto Sans Tamil', sans-serif;
                font-size: {font_size}px;
                text-align: center;
                text-shadow: 
                    -2px -2px 0 #000,
                    2px -2px 0 #000,
                    -2px 2px 0 #000,
                    2px 2px 0 #000;
                white-space: pre-wrap;
                max-width: 90%;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img class="image" src="data:image/png;base64,{image_base64}" alt="Uploaded Image">
            <div class="text">{wrapped_text}</div>
        </div>
    </body>
    </html>
    """
    return html_content

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
    remove_brackets_option = st.checkbox("Remove brackets from behind text")

    if uploaded_image:
        image = Image.open(uploaded_image)
        
        if remove_brackets_option:
            image = remove_brackets(image)
        
        if text_input:
            width, height = image.size
            font_size = max(12, int(width / 20))  # Minimum font size of 12px
            
            # Create a copy of the image and add text
            image_with_text = image.copy()
            image_with_text = add_text_to_image(image_with_text, text_input, font_color, font_size)
        else:
            image_with_text = image
        
        # Convert to base64 for display
        image_base64 = image_to_base64(image_with_text)
        html_content = generate_html(image_base64, text_input, font_color, image.width, image.height)

        # Display the HTML content
        st.components.v1.html(html_content, height=image.height, scrolling=True)

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
