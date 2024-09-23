import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import textwrap

# Function to create image with text overlay using PIL
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

    # Adjust image size and maintain aspect ratio
    aspect_ratio = img_width / img_height
    pdf_width, pdf_height = letter

    new_height = pdf_height * 0.7
    new_width = new_height * aspect_ratio

    image_buffer = io.BytesIO()
    image_with_text.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    # Draw image on PDF
    pdf.drawImage(image_buffer, (pdf_width - new_width) / 2, 200, 
                  width=new_width, height=new_height)
    
    pdf.save()
    buffer.seek(0)
    
    return buffer

# Streamlit app
def main():
    st.title("Text on Image (Download as PDF)")
    
    text_input = st.text_input("Enter the text", value="")
    uploaded_image = st.file_uploader("Choose an image...", 
                                      type=["png", "jpg", "jpeg"])
    font_color = st.color_picker("Pick a text color", "#FFFFFF")

    if uploaded_image and text_input:
        image = Image.open(uploaded_image)
        image_with_text = create_image_with_text(image, text_input, font_color)

        # Download PDF button
        if st.button("Download as PDF"):
            pdf_buffer = create_pdf(image_with_text)
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="image_with_text.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
