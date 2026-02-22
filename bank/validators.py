def validate_name_fname(prompt):
    while True:
        name = input(prompt).strip()
        if name.replace(' ','').isalpha() and 3 <=len(name) <= 30:
            return name
        print(' Name must contain only letters and be at least 3 characters.')
        

def validate_national_id(prompt):
    while True:
        nid = input(prompt).strip()
        if nid.isdigit() and len(nid) == 10:
            return nid
        print('National ID must be exactly 10 digits.')

def validate_password(prompt):
    while True:
        password = input(prompt + ': 🔑 ').strip()
        re_password = input('Confirm password: 🔑 ').strip()

        if len(password) < 8:
            print('Password must be at least 8 characters.')
            continue

        has_letter = any(ch.isalpha() for ch in password)
        has_upper = any(ch.isupper() for ch in password)
        has_digit = any(ch.isdigit() for ch in password)
        has_special = any(not ch.isalnum() for ch in password)

        if not has_letter:
            print('Password must contain at least one letter.')
            continue
        if not has_upper:
            print('Password must contain at least one uppercase letter.')
            continue
        if not has_digit:
            print('Password must contain at least one number.')
            continue
        if not has_special:
            print('Password must contain at least one special character.')
            continue
        if password != re_password:
            print('Passwords do not match.')
            continue

        return password


def validate_phone(prompt):
    while True:
        phone = input(prompt).strip()
        if phone.isdigit() and len(phone) == 11 and phone.startswith('09'):
            return phone
        print('Phone must be 11 digits and start with 09XXXXXXXXX.')

def validate_email(prompt):
    while True:
        email = input(prompt).strip()
        if ' ' in email:
            print("Email must not contain spaces.")
            continue
        if email.count('@') == 1 and email.count('.com') ==1 and email.endswith('.com'):
            return email
        print('Email must contain one @ and end with .com')