import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from resume_reader import get_gemini_response  # Import the resume processing function

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following 
            keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, resume_analysis):
        print(job)
        print(resume_analysis)
        """
        This method generates a cold email based on the job description and the resume analysis.
        """
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

           ### RESUME ANALYSIS:
            {resume_analysis}
            
            ### INSTRUCTION:
            You are name mentioned in resume , a x year student in y university or college take the sentence if x and y are mentioned in resume  
            Write a cold email for the Fresher position or internship whatever mentioned in job description. 

            In the email:
            1. **Highlight** how your Projects ,academic background and strengths align with the job requirements.
            2. **Focus on the specific skills and experiences** that were identified from the resume analysis.
            3. **Do not include any information not present in the resume analysis.**
            4. **  can go to next line if there are too many words in a line
            
            Don't make email sound repetitive 
            
            Ensure the email is concise, professional, and directly addresses how you are a fit for the role based 
            on the job description and your resume analysis.
            
            
            **Note:** Do not include a preamble or introductory statements.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        # Combine the job description and resume analysis in the email generation
        res = chain_email.invoke({"job_description": str(job), "resume_analysis": resume_analysis})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
