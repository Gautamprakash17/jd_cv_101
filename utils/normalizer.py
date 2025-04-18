import phonenumbers

def normalize_phone(phone):
    try:
        parsed = phonenumbers.parse(phone, "IN")
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except:
        pass
    return phone
