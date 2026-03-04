import os
import json
import PyPDF2
from google import genai  # Use the new SDK
from dotenv import load_dotenv

load_dotenv()

# Initialize the new Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_resume(resume_text, job_description):
    # Gemini 2.5 Flash is the stable, cost-effective choice for 2026
    model_id = "gemini-2.5-flash"
    
    prompt = f"""
    Analyze the following resume against the job description.
    Return ONLY a valid JSON object with these keys:
    "match_score": (0-100),
    "matching_skills": (list),
    "missing_skills": (list),
    "summary": (string),
    "recommendations": (list)

    Resume: {resume_text}
    JD: {job_description}
    """
    
    try:
        # The new SDK call structure
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        
        # Clean and parse JSON
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        return {"error": f"API Error: {str(e)}", "match_score": 0}