
# 🧠 JD-CV Matching & Resume Processing API

A FastAPI-based backend to automate the entire flow of resume collection, extraction, JD matching, scoring, and candidate communication.

---

## 🚀 Features

✅ Fetch resumes from email inbox  
✅ Extract structured data from resumes using GPT  
✅ Match JD ↔ CV and assign a score (0–100)  
✅ Batch process resumes and save results to Excel  
✅ Download result Excel  
✅ Send shortlisted candidates their second-round test link via email  


---

## 🧩 Tech Stack

- Python 3.9+
- FastAPI 🚀
- IMAP & SMTP (GoDaddy Mail Integration)
- Pandas, PyMuPDF, phonenumbers
- Excel I/O with xlsxwriter
- dotenv for secret management

---

## 📂 API Endpoints

| Method | Endpoint             | Description                                    |
|--------|----------------------|------------------------------------------------|
| POST   | `/mail_download`     | Download resumes from inbox via form inputs   |
| POST   | `/extract-mail`      | Extract structured info from a single resume  |
| POST   | `/only-score`        | Score match between JD and CV                 |
| POST   | `/process-batch`     | Upload JD + multiple CVs and process all      |
| GET    | `/download-excel`    | Download result Excel sheet                   |
| POST   | `/send-intern-mails` | Send second-round test email to all candidates |

---

## 🔐 .env Setup

Create a `.env` file in the root folder:

