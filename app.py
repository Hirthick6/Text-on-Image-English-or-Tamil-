import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import base64

# Function to create an image with text overlay using PIL
def create_image_with_text(image, text, color):
    img = image.copy()
    draw = ImageDraw.Draw(img)

    font_size = int(min(img.width, img.height) / 20)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Wrap text
    avg_char_width = sum(font.getbbox(char)[2] for char in "abcdefghijklmnopqrstuvwxyz") / 26
    max_width = int(img.width * 0.8)
    wrapped_text = textwrap.fill(text, width=int(max_width / avg_char_width))

    # Calculate text position
    text_position = ((img.width - font.getsize(wrapped_text)[0]) / 2,
                     (img.height - font.getsize(wrapped_text)[1]) / 2)

    draw.text(text_position, wrapped_text, font=font, fill=color)
    return img

# Function to create and return PDF from image
def create_pdf(image_with_text):
    buffer = io.BytesIO()

    # Create PDF canvas
    pdf = canvas.Canvas(buffer, pagesize=letter)
    img_width, img_height = image_with_text.size

    # Maintain aspect ratio and adjust image size
    aspect_ratio = img_width / img_height
    pdf_width, pdf_height = letter
    new_height = pdf_height * 0.7
    new_width = new_height * aspect_ratio

    image_buffer = io.BytesIO()
    image_with_text.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    # Draw the image on the PDF
    pdf.drawImage(image_buffer, (pdf_width - new_width) / 2, 200, width=new_width, height=new_height)
    pdf.save()
    buffer.seek(0)

    return buffer

# Function to convert image to base64 for printing
def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode()

# Streamlit app
def main():
    st.title("Text on Image (Export Options)")

    # Input for text
    text_input = st.text_input("Enter the text", value="Hello Streamlit!")

    # File uploader for image
    uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    # Color picker for text color
    font_color = st.color_picker("Pick a text color", "#FFFFFF")

    if uploaded_image and text_input:
        # Process the image
        image = Image.open(uploaded_image)
        image_with_text = create_image_with_text(image, text_input, font_color)

        # Display the image with text overlay
        st.image(image_with_text, caption="Image with text overlay", use_column_width=True)

        # Export options
        st.subheader("Export Options")
        col1, col2, col3 = st.columns(3)

        # Download as Image button
        with col1:
            img_download = io.BytesIO()
            image_with_text.save(img_download, format="PNG")
            img_download.seek(0)
            st.download_button(
                label="Download as Image",
                data=img_download.getvalue(),
                file_name="image_with_text.png",
                mime="image/png"
            )

        # Download as PDF button
        with col2:
            pdf_buffer = create_pdf(image_with_text)
            st.download_button(
                label="Download as PDF",
                data=pdf_buffer,
                file_name="image_with_text.pdf",
                mime="application/pdf"
            )

        # Print button
        with col3:
            img_base64 = image_to_base64(image_with_text)
            print_html = f'<img src="data:image/png;base64,{img_base64}" style="width:100%">'
            st.markdown(f'<a href="data:text/html;base64,{base64.b64encode(print_html.encode()).decode()}" target="_blank"><button>Print Image</button></a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
