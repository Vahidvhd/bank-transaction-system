from bank.system import init_system, save_system
from bank.accounts import create_account, transfer, gen_acc_id
from bank.validators import validate_name_fname, validate_national_id, validate_password, validate_phone, validate_email
import getpass
import time
import random
import pyfiglet
from bank.verification.email_verification import send_email_gmail

def menu():
    user_menu = input('Select one option:\n1: Log in\n2: Create account\n\n\n0: Exit\n>>>: ').strip()
    return user_menu

def create_acc(system):
    print('***Create account***')

    name = validate_name_fname('Name: ')
    fname = validate_name_fname('Surname: ')
    national_id = validate_national_id('National id: ')
    password = validate_password('Password: ')
    phone = validate_phone('Phone: ')
    email = validate_email('Email: ')
    is_human = captcha_check()
    if not is_human:
        print("Captcha doesn't match, please try again")
        return

    owner_dict ={
    'name' : name,
    'fname' : fname,
    'national_id' : national_id,
    'password' : password,
    'contact' : {
        'phone' : phone,
        'email' : email,
        }
    }

    while True:
        init_amount = input('Enter initial deposit amount: ').strip()
        try:
            init_amount = float(init_amount)
            break
        except ValueError:
            print('Initial balance cannot contain any letters of special characters')
            continue
    
    account_id = gen_acc_id(system)

    try:
        result = create_account(system, account_id, init_amount, owner_dict)
        save_system(system)
        print(f"{result['status']}\nAccount number: {result['account_id']}\nBalance: {result['balance']}")
    except (TypeError , ValueError) as e:
        print('Error', e)

def log_in(system):  
    while True: 
        attempts =0
        while attempts < 3:
            acc_id = input('Account Number: ').strip()
            password = getpass.getpass('Password: 🔑 ').strip()
            user_acc = system.get('accounts',{}).get(acc_id)
            is_human = captcha_check()
            if not is_human:
                attempts += 1
                print(f"Captcha doesn't match, please try again ({3-attempts} left)")
                continue
            if not user_acc or user_acc['owner']['password'] != password:
                attempts += 1
                print(f'Invalid account number or password ({3-attempts} left)')
                continue
            else:
                print(f"Welcome {user_acc['owner']['name']}")
                return acc_id
        
        print('\nToo many failed attempts. Please wait 10 seconds.\n')
        for i in range(10, 0, -1):
            print(f"{i} ...")
            time.sleep(1)
        print('\nYou can try again now.\n')

def forgot_pass(system):
    while True:
        print("\n*** Forgot Password ***")
        forgot_menu= input("1: Get password by email\n\n2: Back\n>>>: ").strip()
        if forgot_menu == '1': 
            national_id = input('National id Number: ')
            email = input('Email: ')
            print('If the information you provided matches an existing account, we’ll send an email to the address you entered. Please also check your Spam/Junk folder.')
            for acc_id, acc_data in system.get('accounts', {}).items():
                owner = acc_data.get('owner', {})
                if owner.get('national_id')== national_id and owner.get('contact', {}).get('email') == email:
                    password = owner.get('password')
                    owner_name = owner.get('name')
                    owner_fname = owner.get('fname')
                    send_email_gmail(email, password, owner_name, owner_fname)
                    break
        elif forgot_menu == '2':
            return
        else:
            print('Invalid option')
            continue

def log_in_menu(system):
    print('***Log in***')
    login_menu = input('1: Log in with Account Number & Password\n2: Forgot Password\n\n\n3: Back\n>>>: ').strip()
    if login_menu == '1':
        log_in(system)
    elif login_menu == '2':
        forgot_pass(system)
    elif login_menu == '3':
        return
    else:
        print('Invalid option')

def captcha_check():
    chars = list('ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    code = "".join(random.choices(chars, k=5))
    print(pyfiglet.figlet_format(code, font="standard"))
    ans = input("Type CAPTCHA: ").strip()
    return ans == code

def main():
    system = init_system()
    print('System loaded/initialized')
    while True:
        user_choice = menu()
        if user_choice == '1':
            log_in_menu(system)
        elif user_choice == '2':
            create_acc(system)
        elif user_choice == '0':
            print('Exit (Not completed yet)')
            break
        else:
            print('Invalid option')
            continue

if __name__ == "__main__":
    main()