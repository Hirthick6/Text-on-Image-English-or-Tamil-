import streamlit as st
from PIL import Image
from io import BytesIO
from html2image import Html2Image
import base64
import os

# Sidebar details
st.sidebar.title("About Me")
st.sidebar.write("Done by Hirthick S")
st.sidebar.write("Data Science Scholar")

st.sidebar.title("Project Overview")
st.sidebar.write("This project integrates mixed Tamil, English, and numeric text into images.")

st.sidebar.title("Language Used")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", width=50)
st.sidebar.write("Python")

# Function to convert image to base64 string
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Function to generate HTML content with the image and text
def generate_html(image_base64, text, color):
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;700&display=swap" rel="stylesheet">

        <style>
            body, html {{
                height: 100%;
                margin: 0;
            }}
            .bg {{
                background-image: url('{image_base64}');
                height: 100%;
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: 'Noto Sans Tamil', sans-serif;
            }}
            h2 {{
                color: {color};
                font-size: 5vw;
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="bg">
            <h2>{text}</h2>
        </div>
    </body>
    </html>
    """
    return html_content

# Streamlit app
def main():
    st.title("Text on Image (Mixed Tamil, English, and Numbers)")

    # Set Chromium path based on environment
    chromium_path = "C:/Users/user/AppData/Local/Chromium/Application/chrome.exe"
    if os.path.exists(chromium_path):
        hti = Html2Image(browser_executable=chromium_path)
    else:
        hti = Html2Image()  # Use default Chromium if path is not found

    # Image upload
    text_input = st.text_input("Enter the text", value="")
    uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    # Font color picker
    font_color = st.color_picker("Pick a text color", "#FFFFFF")  # Default is white

    if uploaded_image and text_input:
        # Load the image with Pillow
        image = Image.open(uploaded_image)

        # Convert image to base64 string
        image_base64 = image_to_base64(image)

        # Generate the HTML content with image, text, and font color
        html_content = generate_html(image_base64, text_input, font_color)

        # Render the HTML to an image using Html2Image
        hti.screenshot(html_str=html_content, save_as='output_image.png', size=(image.width, image.height))

        # Display the resulting image
        st.image('output_image.png', caption="Generated Image with Text", use_column_width=True)

        # Option to download the generated image
        with open('output_image.png', "rb") as file:
            st.download_button(
                label="Download Image",
                data=file,
                file_name="result.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
