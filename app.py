import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import base64
import io

# Function to convert image to base64 string
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to add text to image
def add_text_to_image(image, text, font_color):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Use a font size proportional to the image size
    font_size = int(min(width, height) / 10)
    
    # Use default font
    font = ImageFont.load_default()
    
    # Get text size
    text_width, text_height = draw.textsize(text, font=font)
    
    # Calculate position to center the text
    position = ((width - text_width) / 2, (height - text_height) / 2)
    
    # Draw text outline
    outline_color = "black"
    for adj in range(-3, 4):
        draw.text((position[0]+adj, position[1]), text, font=font, fill=outline_color)
        draw.text((position[0], position[1]+adj), text, font=font, fill=outline_color)
    
    # Draw main text
    draw.text(position, text, font=font, fill=font_color)
    
    return image

# Function to generate HTML content
def generate_html(image_base64, width, height):
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
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
        </style>
    </head>
    <body>
        <div class="container">
            <img class="image" src="data:image/png;base64,{image_base64}" alt="Result Image">
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

    if uploaded_image and text_input:
        image = Image.open(uploaded_image)
        width, height = image.size
        
        # Add text to image
        result_image = add_text_to_image(image.copy(), text_input, font_color)
        
        # Convert result image to base64
        result_image_base64 = image_to_base64(result_image)
        
        # Generate and display HTML
        html_content = generate_html(result_image_base64, width, height)
        st.components.v1.html(html_content, height=height, scrolling=True)

        # Option to download the result image
        buffered = io.BytesIO()
        result_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{img_str}" download="result_image.png">Download Result Image</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Option to download the HTML
        st.download_button(
            label="Download HTML",
            data=html_content,
            file_name="result.html",
            mime="text/html"
        )

if __name__ == "__main__":
    main()
