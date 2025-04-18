# utils/email_sender.py

import pandas as pd
import os, time, logging
from datetime import datetime
from email.utils import make_msgid, formatdate
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

logging.basicConfig(filename='email_errors.log', level=logging.ERROR)

def send_second_round_emails(preview: bool = False):
    test_link = "https://forms.gle/ZH1UYhrvUHyv72h26"
    sheet_name = "Form Responses 1"
    xlsx_file = "AI Intern Test (Responses).xlsx"

    df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
    emails = df['Email Address'].dropna().unique()

    subject = "Elint AI Internship – Second Round Assessment Invitation"

    success_emails = []
    failed_emails = []

    for recipient_email in emails:
        recipient_email = str(recipient_email).strip()

        if not recipient_email or "@" not in recipient_email:
            continue

        body_html = f"""\
        <html>
            <body>
                <p>Dear Candidate,</p>
                <p>Thank you for completing the first round of our recruitment process.</p>
                <p>You have been shortlisted for the second round of assessment.</p>
                <p><b>Test Details:</b></p>
                <ul>
                    <li><b>Round:</b> Second Round</li>
                    <li><b>Format:</b> Online Assessment (Google Form)</li>
                    <li><b>Link:</b> <a href="{test_link}">{test_link}</a></li>
                </ul>
                <p>Please ensure you complete the assessment as soon as possible.</p>
                <p>Best regards,<br><b>Jyotsna Choubey</b><br>HR – Elint AI</p>
            </body>
        </html>
        """

        plain_text_body = f"""Dear Candidate,

Thank you for completing the first round of our recruitment process.
You have been shortlisted for the second round of assessment.

Test Details:
- Round: Second Round
- Format: Online Assessment (Google Form)
- Link: {test_link}

Please complete it as soon as possible.

Best regards,
Jyotsna Choubey
HR – Elint AI
{datetime.now().strftime('%d %b %Y')}
"""

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"Jyotsna Choubey <{EMAIL_USER}>"
        msg["To"] = recipient_email
        msg["Cc"] = "sj@elintai.in"
        msg["Reply-To"] = EMAIL_USER
        msg["Message-ID"] = make_msgid()
        msg["Date"] = formatdate(localtime=True)
        msg.set_content(plain_text_body)
        msg.add_alternative(body_html, subtype='html')

        all_recipients = [recipient_email, "sj@elintai.in"]

        if preview:
            print(f"🔍 Preview Email to {recipient_email}:\n{body_html}\n")
            continue

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg, to_addrs=all_recipients)

            success_emails.append(recipient_email)
            time.sleep(2)

        except Exception as e:
            failed_emails.append(recipient_email)
            logging.error(f"{datetime.now()}: Error sending to {recipient_email}: {e}")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not preview:
        with open("sent_second_round.log", "a", encoding="utf-8") as archive:
            archive.write(f"\n[{timestamp}] Sent:\n")
            for email in success_emails:
                archive.write(f"- {email}\n")

        if failed_emails:
            with open("failed_second_round.log", "a", encoding="utf-8") as fail_log:
                fail_log.write(f"\n[{timestamp}] Failed:\n")
                for email in failed_emails:
                    fail_log.write(f"- {email}\n")

    return {
        "sent": len(success_emails),
        "failed": len(failed_emails),
        "preview_mode": preview
    }
