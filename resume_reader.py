from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from PIL import Image
import google.generativeai as genai  # Ensure this is imported

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key is missing")

genai.configure(api_key=api_key)


# Function to get a response from the Gemini model
def get_gemini_response(input_prompt, image, extra_input):
    try:
        # Load the model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate response using the image (resume) and input prompt
        response = model.generate_content([input_prompt, image[0], extra_input])

        if response and response.text:  # Ensure valid response
            return response.text
        else:
            return "Failed to analyze the resume."

    except Exception as e:
        return f"Error analyzing resume: {e}"


# Function to process the uploaded image (resume)
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            # Handle PDF files: Extract text or convert pages to images
            pdf_reader = PdfReader(uploaded_file)
            bytes_data = b""
            
            # Extract the raw bytes data from the PDF (could be converted to text/images as needed)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                # Option 1: Extract text (if you're dealing with textual PDFs)
                bytes_data += page.extract_text().encode()

            pdf_parts = [
                {
                    "mime_type": file_type,  # MIME type for PDF
                    "data": bytes_data
                }
            ]
            return pdf_parts

        elif file_type in ["image/jpeg", "image/png", "image/jpg"]:
            # Handle image files: Convert them to raw bytes and return
            bytes_data = uploaded_file.getvalue()

            image_parts = [
                {
                    "mime_type": file_type,  # Get mime type of uploaded file (e.g., image/jpeg)
                    "data": bytes_data
                }
            ]
            return image_parts

        else:
            raise ValueError("Unsupported file type. Please upload a PDF or an image file.")
    else:
        raise FileNotFoundError("No file uploaded")
