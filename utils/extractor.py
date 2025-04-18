import fitz
import json
import re
import openai
from openai import OpenAI

# ✅ OpenAI Setup
from openai import OpenAI

client = OpenAI(api_key="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")

# ✅ Extract text from PDF
def extract_pdf_text(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in pdf])


# ✅ Extract structured candidate details
def extract_candidate_details(cv_text):
    prompt = f"""
    Extract the following structured details from the candidate CV and return ONLY in pure JSON format (no text, no markdown):

    {{
        "Name": "",
        "Phone": "",
        "Email": "",
        "Degree": "",
        "Branch": "",
        "Entry Year": "",
        "Passout Year": "",
        "AI Relevant Projects": "",
        "AI Relevant Experience": "",
        "Programming Languages": "",
        "Certifications": "",
        "Years of Experience": "",
        "Previous Companies": "",
        "Soft Skills": ""
    }}

    Rules:
    - Fill only the relevant values, leave others as empty strings if not found.
    - "AI Relevant Experience" must ONLY contain total duration in AI/ML/Data Science/Data Analyst roles.
    - Return duration formats like: "6 months", "1 year", "1.5 years", "2 years", etc.
    - DO NOT include any company name, project name, job title, or description in that field.
    - If such details appear, ignore them and only estimate duration.
    - If no clear duration is found, return "0 months".

    Candidate CV:
    {cv_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        output = response.choices[0].message.content.strip()

        if output.startswith("```json"):
            output = output.strip("```json").strip("```").strip()

        details = json.loads(output)

        # Ensure all required fields are present
        required_fields = [
            "Name", "Phone", "Email", "Degree", "Branch", "Entry Year", "Passout Year",
            "AI Relevant Projects", "AI Relevant Experience", "Programming Languages",
            "Certifications", "Years of Experience", "Previous Companies", "Soft Skills"
        ]

        for field in required_fields:
            if field not in details:
                details[field] = ""

        ai_exp = details.get("AI Relevant Experience", "").lower()
        if not re.match(r'^\d+(\.\d+)?\s*(month|months|year|years)$', ai_exp):
            details["AI Relevant Experience"] = "0 months"

        return details

    except Exception as e:
        print(f"❌ OpenAI parsing error: {e}")
        return {field: "" for field in required_fields}


# ✅ JD-CV score matching
def calculate_jd_cv_score(jd_text, cv_text):
    prompt = f"""
    You are an intelligent job matching system.
    Based on the Job Description (JD) and Candidate CV below, return only a numeric compatibility score (0-100).
    JD: {jd_text}
    CV: {cv_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        result = response.choices[0].message.content.strip()
        match = re.fullmatch(r'\d+(\.\d+)?', result)
        return float(match.group()) if match else 0

    except Exception as e:
        print(f"❌ OpenAI scoring error: {e}")
        return 0
