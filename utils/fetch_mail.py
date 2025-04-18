# utils/fetch_mail.py

import imaplib
import email
from email.header import decode_header
import os

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx"]

def fetch_resume_attachments(email_user: str, email_pass: str):
    IMAP_SERVER = "imap.secureserver.net"

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    os.makedirs("attachments", exist_ok=True)

    downloaded = 0
    for i in email_ids:
        res, msg_data = mail.fetch(i, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                for part in msg.walk():
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            decoded_filename, encoding = decode_header(filename)[0]
                            if isinstance(decoded_filename, bytes):
                                decoded_filename = decoded_filename.decode(encoding or "utf-8", errors="ignore")
                            if any(decoded_filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
                                filepath = os.path.join("attachments", decoded_filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                downloaded += 1

    mail.logout()
    return {
        "unread_emails_found": len(email_ids),
        "attachments_downloaded": downloaded
    }
