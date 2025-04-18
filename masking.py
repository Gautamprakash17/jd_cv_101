import pandas as pd

def smart_partial_mask_email(email):
    if not email or "@" not in email:
        return email
    try:
        username, domain = email.split("@")
        uname_len = len(username)
        if uname_len <= 2:
            return username[0] + "***@" + domain
        elif uname_len <= 4:
            return username[0] + "***" + username[-1] + "@" + domain
        elif uname_len <= 7:
            first = username[:2]
            last = username[-1:]
            masked = "*" * (uname_len - len(first) - len(last))
            return f"{first}{masked}{last}@{domain}"
        else:
            first = username[:3]
            last = username[-4:]
            masked = "*" * (uname_len - len(first) - len(last))
            return f"{first}{masked}{last}@{domain}"
    except:
        return "***@***.com"

# Load data
df = pd.read_excel("Tech Task Submission  (Responses).xlsx", sheet_name="Form Responses 1")

# Select relevant columns only
df_selected = df[['1. Full Name :', '2. Email Address']].copy()

# Apply email masking
df_selected['2. Email Address'] = df_selected['2. Email Address'].apply(smart_partial_mask_email)

# Save to CSV
output_path = "masked_output_name_email.csv"
df_selected.to_csv(output_path, index=False)

output_path
