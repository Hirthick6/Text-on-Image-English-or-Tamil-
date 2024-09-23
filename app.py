import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import textwrap
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import string

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

# Function to create image with text overlay using PIL
def create_image_with_text(image, text, color):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    
    # Use a default font (you may need to adjust this)
    font_size = int(min(img.width, img.height) / 20)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Wrap text
    avg_char_width = sum(font.getbbox(char)[2] for char in string.ascii_lowercase) / 26
    max_width = int(img.width * 0.8)
    wrapped_text = textwrap.fill(text, width=int(max_width / avg_char_width))
    
    # Calculate text position
    left, top, right, bottom = font.getbbox(wrapped_text)
    text_width = right - left
    text_height = bottom - top
    text_position = ((img.width - text_width) / 2, (img.height - text_height) / 2)
    
    # Draw text
    draw.text(text_position, wrapped_text, font=font, fill=color)
    
    return img

# Function to create PDF from image
def create_pdf(image):
    buffer = BytesIO()

    # Save PIL image to buffer as PNG
    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    # Create a PDF using reportlab and embed the image
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawImage(image_buffer, 100, 400, width=400, height=400)  # Adjust as per image size
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
        
        # Create image with text overlay
        image_with_text = create_image_with_text(image, text_input, font_color)
        
        # Export options
        st.subheader("Export Options")
        col1, col2, col3 = st.columns(3)
        
        # Download Image button
        with col1:
            img_download = BytesIO()
            image_with_text.save(img_download, format='PNG')
            st.download_button(
                label="Download Image",
                data=img_download.getvalue(),
                file_name="image_with_text.png",
                mime="image/png"
            )
        
        # Print button (opens in new tab for printing)
        with col2:
            img_print = BytesIO()
            image_with_text.save(img_print, format='PNG')
            img_print_base64 = base64.b64encode(img_print.getvalue()).decode()
            print_html = f'<img src="data:image/png;base64,{img_print_base64}" style="width:100%">'
            st.markdown(f'<a href="data:text/html;base64,{base64.b64encode(print_html.encode()).decode()}" target="_blank"><button>Print Image</button></a>', unsafe_allow_html=True)
        
        # Download PDF button
        with col3:
            pdf_buffer = create_pdf(image_with_text)
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="image_with_text.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
