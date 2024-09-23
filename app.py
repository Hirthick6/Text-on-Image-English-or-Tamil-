import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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

# Function to capture screenshot using Selenium
def capture_screenshot(html_content, output_path, width, height):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.set_window_size(width, height)
    
    # Save HTML content to a temporary file
    with open("temp.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Open the temporary HTML file
    driver.get("file://" + os.path.abspath("temp.html"))
    
    # Capture screenshot
    driver.save_screenshot(output_path)
    
    driver.quit()
    os.remove("temp.html")

# Streamlit app
def main():
    st.title("Text on Image (Mixed Tamil, English, and Numbers)")

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

        # Capture screenshot using Selenium
        output_path = 'output_image.png'
        capture_screenshot(html_content, output_path, image.width, image.height)

        # Display the resulting image
        st.image(output_path, caption="Generated Image with Text", use_column_width=True)

        # Option to download the generated image
        with open(output_path, "rb") as file:
            st.download_button(
                label="Download Image",
                data=file,
                file_name="result.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
