import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from utils import clean_txt
from resume_reader import input_image_setup, get_gemini_response  # Import the resume reader functions

# Streamlit app creation function
def create_streamlit_app(llm, clean_txt):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    # Sidebar with a title and description
    with st.sidebar:
        st.title("📧 Personalized Cold Email     Generator")
        st.markdown("""
            **Welcome!** This tool helps you create cold emails from job descriptions on career pages. 
            Simply enter the URL of the career page and upload your resume, 
            and we will extract relevant jobs and generate a cold email.
        """)
        st.info("Please ensure the URL is publicly accessible.")

    # Main content layout
    st.header("Generate a Cold Email")
    st.write("Fill in the details below to get started.")

    # Form layout to input URL and upload the resume
    with st.form(key="url_form"):
        url_input = st.text_input("🔗 Enter a Job Posting URL", placeholder="https://example.com/careers")
        uploaded_file = st.file_uploader("📄 Upload your Resume (image or pdf) (pdf, jpg, jpeg, png)", type=["pdf","jpg", "jpeg", "png"])
        submit_button = st.form_submit_button(label="🚀 Extract Jobs and Generate Email")

    if submit_button:
        if not uploaded_file:
            st.error("Please upload a resume image.")
        else:
            try:
                st.info("Fetching data from the provided URL and analyzing resume...")

                # Load and clean job description data
                loader = WebBaseLoader([url_input])
                data = clean_txt(loader.load().pop().page_content)

                # Load and analyze resume image
                image_data = input_image_setup(uploaded_file)
                input_prompt = """
                               You are an expert in analyzing resumes.
                               You will receive input images as a person's resume & 
                               you will have to answer questions based on the input image.
                               """
                resume_response = get_gemini_response(input_prompt, image_data, "Analyze this resume")

                # Display extracted jobs
                jobs = llm.extract_jobs(data)

                st.subheader("Extracted Job Postings")
                for index, job in enumerate(jobs, start=1):
                    st.markdown(f"**Job {index}: {job.get('role', 'Unknown Role')}**")
                    st.write(f"**Experience:** {job.get('experience', 'Not provided')}")
                    st.write(f"**Skills:** {', '.join(job.get('skills', []) if job.get('skills') else [])}")
                    st.write(f"**Description:** {job.get('description', 'No description available')}")

                    # Generate cold email using the job description and resume analysis
                    email = llm.write_mail(job, resume_response)

                    # Show the generated email
                    st.subheader(f"Generated Cold Email for Job {index}")
                    st.code(email, language='markdown')

                    # Add download button for email
                    st.download_button(label=f"📥 Download Email for Job {index}",
                                       data=email,
                                       file_name=f"cold_email_{index}.txt")

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Main function to run the app
if __name__ == "__main__":
    chain = Chain()
    create_streamlit_app(chain, clean_txt)
