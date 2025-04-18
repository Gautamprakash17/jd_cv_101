import os
from typing import List
from fastapi.responses import FileResponse
from utils.normalizer import normalize_phone
from fastapi import FastAPI, UploadFile, File
from utils.fetch_mail import fetch_resume_attachments
from utils.file_ops import load_existing_emails, append_candidate_to_excel
from utils.extractor import extract_pdf_text, extract_candidate_details, calculate_jd_cv_score
from pydantic import BaseModel
from utils.fetch_mail import fetch_resume_attachments
from fastapi import Form



app = FastAPI()
RESULT_FILE = "results/candidate_results.xlsx"
# ✅ Model to receive login info
class EmailCredentials(BaseModel):
    username: str
    password: str

# @app.post("/fetch-resumes")
# def fetch_resumes(credentials: EmailCredentials):
#     result = fetch_resume_attachments(credentials.username, credentials.password)
#     return {
#         "message": "✅ Resume fetch completed!",
#         "result": result
#     }
@app.post("/mail_download")
def fetch_resumes_form(username: str = Form(...), password: str = Form(...)):
    result = fetch_resume_attachments(username, password)
    return {
        "message": "✅ Resume fetch completed!",
        "result": result
    }
@app.post("/extract-mail")
async def extract_info(cv_file: UploadFile = File(...)):
    cv_text = extract_pdf_text(cv_file.file)
    details = extract_candidate_details(cv_text)
    details["Phone"] = normalize_phone(details.get("Phone", "")) 
    return details


@app.post("/only-score")
async def score_cv(jd_file: UploadFile = File(...), cv_file: UploadFile = File(...)):
    jd_text = extract_pdf_text(jd_file.file)
    cv_text = extract_pdf_text(cv_file.file)
    score = calculate_jd_cv_score(jd_text, cv_text)
    return {"score": score}


@app.post("/process-batch")
async def process_batch(jd_file: UploadFile = File(...), cv_files: list[UploadFile] = File(...)):
    jd_text = extract_pdf_text(jd_file.file)
    existing_emails, _ = load_existing_emails(RESULT_FILE)
    processed = skipped = 0

    for cv in cv_files:
        cv_text = extract_pdf_text(cv.file)
        details = extract_candidate_details(cv_text)
        email = details.get("Email", "").strip().lower()

        if email in existing_emails:
            skipped += 1
            continue

        score = calculate_jd_cv_score(jd_text, cv_text)
        phone = normalize_phone(details.get("Phone", ""))

        candidate = {
            "Candidate Name": details.get("Name", ""),
            "Phone": phone,
            "Email": email,
            "Entry Year": details.get("Entry Year", ""),
            "Passout Year": details.get("Passout Year", ""),
            "Branch Name": details.get("Branch", ""),
            "AI Relevant Projects (1-5)": details.get("AI Relevant Projects", ""),
            "AI Relevant Experience": details.get("AI Relevant Experience", ""),
            "Programming Languages": details.get("Programming Languages", ""),
            "Years Exp": details.get("Years of Experience", ""),
            "Certifications": details.get("Certifications", ""),
            "Soft Skills": details.get("Soft Skills", ""),
            "Company Exp": details.get("Previous Companies", ""),
            "Final Score": score
        }

        append_candidate_to_excel(candidate, RESULT_FILE)
        processed += 1

    return {
        "processed": processed,
        "skipped": skipped,
        "message": f"🎉 {processed} CVs processed. {skipped} skipped."
    }


@app.get("/download-excel")
async def download_excel():
    if os.path.exists(RESULT_FILE):
        return FileResponse(path=RESULT_FILE, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="candidate_results.xlsx")
    return {"error": "Excel file not found."}
