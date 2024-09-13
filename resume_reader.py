from dotenv import load_dotenv
import os
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
        # Read file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get mime type of uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
