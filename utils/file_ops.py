import os
import pandas as pd
from datetime import datetime

def load_existing_emails(file_path):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return set(df["Email"].dropna().astype(str).str.lower()), df
    return set(), pd.DataFrame()

def append_candidate_to_excel(candidate, file_path):
    df = pd.DataFrame([candidate])
    
    # Merge with existing if present
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        df = pd.concat([existing_df, df], ignore_index=True)

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Candidates")
        
        # Format Phone column as text
        if "Phone" in df.columns:
            phone_col = df.columns.get_loc("Phone")
            workbook = writer.book
            worksheet = writer.sheets["Candidates"]
            worksheet.set_column(phone_col, phone_col, 20, workbook.add_format({'num_format': '@'}))

    print(f"✅ Candidate {candidate.get('Candidate Name', 'Unknown')} appended to {file_path}")
