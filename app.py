import streamlit as st
from PIL import Image
import base64
import io
import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Function to convert image to base64 string
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to generate HTML content
def generate_html(image_base64, text, color, width, height):
    # Calculate font size based on image width
    font_size = max(12, int(width / 20))  # Minimum font size of 12px
    
    # Estimate characters per line
    chars_per_line = max(1, int(width / (font_size * 0.6)))  # Assuming average char width is 0.6 times font size
    
    # Wrap text
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

# Function to create PDF
def create_pdf(image, text, color):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Register Tamil font
    pdfmetrics.registerFont(TTFont('NotoSansTamil', 'NotoSansTamil-Regular.ttf'))
    
    # Add image
    img_width, img_height = image.size
    aspect = img_height / float(img_width)
    max_width = 500
    width = min(img_width, max_width)
    height = width * aspect
    c.drawImage(image, 50, letter[1] - 50 - height, width=width, height=height)
    
    # Add text
    c.setFont('NotoSansTamil', 12)
    c.setFillColor(color)
    text_object = c.beginText(50, letter[1] - 60 - height)
    for line in textwrap.wrap(text, width=60):
        text_object.textLine(line)
    c.drawText(text_object)
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

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
        image_base64 = image_to_base64(image)
        html_content = generate_html(image_base64, text_input, font_color, width, height)

        # Display the HTML content
        st.components.v1.html(html_content, height=height, scrolling=True)

        # Option to download as PDF
        pdf_buffer = create_pdf(image, text_input, font_color)
        st.download_button(
            label="Download as PDF",
            data=pdf_buffer,
            file_name="result.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
