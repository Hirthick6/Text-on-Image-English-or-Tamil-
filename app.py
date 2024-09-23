import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# Sidebar details
st.sidebar.title("About Me")
st.sidebar.write("Done by Hirthick S")
st.sidebar.write("Data Science Scholar")

st.sidebar.title("Project Overview")
st.sidebar.write("This project integrates mixed Tamil, English, and numeric text into images.")

st.sidebar.title("Language Used")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", width=50)
st.sidebar.write("Python")

# Function to load a font
@st.cache_resource
def load_font():
    font_url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansTamil/NotoSansTamil-Regular.ttf"
    response = requests.get(font_url)
    font = ImageFont.truetype(io.BytesIO(response.content), size=50)
    return font

# Function to add text to image
def add_text_to_image(image, text, font, text_color):
    draw = ImageDraw.Draw(image)
    
    # Get text size
    left, top, right, bottom = font.getbbox(text)
    text_width = right - left
    text_height = bottom - top
    
    # Calculate position to center the text
    position = ((image.width - text_width) / 2, (image.height - text_height) / 2)
    
    # Draw text outline
    outline_color = "black"
    for adj in range(-3, 4):
        draw.text((position[0]+adj, position[1]), text, font=font, fill=outline_color)
        draw.text((position[0], position[1]+adj), text, font=font, fill=outline_color)
    
    # Draw main text
    draw.text(position, text, font=font, fill=text_color)
    
    return image

# Streamlit app
def main():
    st.title("Text on Image (Mixed Tamil, English, and Numbers)")

    # Load font
    font = load_font()

    # Image upload
    text_input = st.text_input("Enter the text", value="")
    uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    # Font color picker
    font_color = st.color_picker("Pick a text color", "#FFFFFF")  # Default is white

    if uploaded_image and text_input:
        # Load the image with Pillow
        image = Image.open(uploaded_image).convert("RGBA")

        # Add text to image
        result_image = add_text_to_image(image, text_input, font, font_color)

        # Display the resulting image
        st.image(result_image, caption="Generated Image with Text", use_column_width=True)

        # Option to download the generated image
        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Download Image",
            data=byte_im,
            file_name="result.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
