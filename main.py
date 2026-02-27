from bank.system import init_system, save_system
from bank.accounts import create_account, transfer, batch_transfer
from bank.validators import validate_name_fname, validate_national_id, validate_password, validate_phone, validate_email
import getpass
import time
import random
import pyfiglet
from bank.verification.email_verification import send_email_gmail
import os

BANK_NAME = "VaulT - Tech Bank"
TAGLINE = "Secure • Fast • Reliable"

ANSI = {
    "reset": "\033[0m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
}
def show_logo():
    art = pyfiglet.figlet_format(BANK_NAME, font='small')

    print(ANSI["cyan"] + art + ANSI["reset"])
    print(ANSI["yellow"] + f"{TAGLINE.center(50)}" + ANSI["reset"])
    print(ANSI["cyan"] + ("═" * 50) + ANSI["reset"])


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_logo()

def pause(seconds= 2):
    time.sleep(seconds)

def menu():
    user_menu = input('Select one option:\n1: Log in\n2: Create account\n\n\n0: Exit\n>>>: ').strip()
    return user_menu

def create_acc(system):
    clear_terminal()
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
        pause()
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
            pause()
            continue
    
    try:
        result = create_account(system, init_amount, owner_dict)
        save_system(system)
        print(f"{result['status']}\nAccount number: {result['account_id']}\nBalance: {result['balance']}")
        pause(4)
    except (TypeError , ValueError) as e:
        print('Error', e)
        pause()

def log_in(system):  
    while True: 
        attempts =0
        while attempts < 3:
            clear_terminal()
            acc_id = input('Account Number: ').strip()
            password = getpass.getpass('Password: 🔑 ').strip()
            user_acc = system.get('accounts',{}).get(acc_id)
            is_human = captcha_check()
            if not is_human:
                attempts += 1
                print(f"Captcha doesn't match, please try again ({3-attempts} left)")
                pause()
                continue
            if not user_acc or user_acc['owner']['password'] != password:
                attempts += 1
                print(f'Invalid account number or password ({3-attempts} left)')
                pause()
                continue
            else:
                print(f"Welcome {user_acc['owner']['name']}")
                pause(1)
                log_in_menu(system, acc_id, user_acc)
                return
        
        print('\nToo many failed attempts. Please wait 10 seconds.\n')
        for i in range(10, 0, -1):
            print(f'{i} ...')
            time.sleep(1)
        print('\nYou can try again now.\n')
        pause(1)

def forgot_pass(system):
    while True:
        clear_terminal()
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
            input("\n\nPress Enter to continue...")
            return

        elif forgot_menu == '2':
            return
        else:
            print('Invalid option')
            pause()
            continue

def log_in_options(system):
    clear_terminal()
    print('***Log in***')
    login_menu = input('1: Log in with Account Number & Password\n2: Forgot Password\n\n\n0: Back\n>>>: ').strip()
    if login_menu == '1':
        log_in(system)
    elif login_menu == '2':
        forgot_pass(system)
    elif login_menu == '0':
        return
    else:
        print('Invalid option')
        pause()

def log_in_menu(system, acc_id, user_acc):
    while True:
        clear_terminal() 
        user_acc = system.get('accounts', {}).get(acc_id)

        if not user_acc:
            print('Account not found.')
            pause()
            return

        owner = user_acc.get('owner')
        name = owner.get('name')
        fname = owner.get('fname')
        balance = user_acc.get('balance', 0)
        national_id = user_acc.get('owner', {}).get('national_id')
        phone = user_acc.get('owner', {}).get('contact', {}).get('phone')
        email = user_acc.get('owner', {}).get('contact', {}).get('email')

        print("\n***Dashboard***\n")
        print(f'Welcome {name} {fname}                  Balance: {balance}')

        print("1: View your profile")
        print("2: Transfer")
        print("3: Batch transfer")
        print("\n\n0: Logout")
        choice = input(">>> ").strip()

        if choice == "1":
            show_user_info(name, fname, national_id, phone, email)  
        elif choice == "2":
            user_transfer(system, acc_id)
        elif choice == "3":
            user_batch_transfer(system, acc_id)
        elif choice == "0":
            print("Logged out.\n")
            pause(1)
            return
        else:
            print("Invalid option.")
            pause()


def show_user_info(name, fname, national_id, phone, email):
    clear_terminal() 
    print("\n***My info***\n\n")
    print(f'Name: {name}')
    print(f'Family Name: {fname}')
    print(f'National ID: {national_id}')
    print(f'Phone: {phone}')
    print(f'Email: {email}')
    user_choice = input('\n\n 0: Back')
    if user_choice == '0':
        return

def user_transfer(system, acc_id):
    clear_terminal()
    print("\n*** Transfer ***")
    to_acc = input("Destination (Account/Card number): ").strip()

    while True:
        amount_str = input("Amount: ").strip()
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Amount must be numeric.")
            pause()

    info = input("Description (optional): ").strip()

    try:
        result = transfer(system, acc_id, to_acc, amount, info)
        save_system(system)
        print("\n", result["status"])
        print("From balance:", result["from_balance"])
        print("To balance:", result["to_balance"])
        pause()
    except Exception as e:
        print("\nTransfer failed:", e)
        print()

    input("\nPress Enter to continue...")    

def user_batch_transfer(system, acc_id):
    clear_terminal()     
    print("\n*** Batch Transfer ***")
    file_name = input("CSV file path (one account/card per line): ").strip()

    while True:
        amount_str = input("Amount for each transfer: ").strip()
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Amount must be numeric.")
            pause()

    info = input("Description (optional): ").strip()

    try:
        result = batch_transfer(system, acc_id, amount, file_name, info)
        save_system(system)
        print("\n", result["status"])
        print("Total:", result["total_transfers"])
        print("Successful:", result["successful"])
        print("Failed:", result["failed"])
        if result["failed_accounts"]:
            print("Failed accounts:", result["failed_accounts"])
        pause()
    except Exception as e:
        print("\nBatch transfer failed:", e)
        pause()

    input("\nPress Enter to continue...")

def captcha_check():
    os.system('cls' if os.name == 'nt' else 'clear')
    chars = list('ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    code = "".join(random.choices(chars, k=5))
    print(pyfiglet.figlet_format(code, font="standard"))
    ans = input("Type CAPTCHA: ").strip()
    return ans == code

def main():
    system = init_system()
    print('System loaded/initialized')
    pause()
    while True:
        clear_terminal()
        user_choice = menu()
        if user_choice == '1':
            log_in_options(system)
        elif user_choice == '2':
            create_acc(system)
        elif user_choice == '0':
            print('Exiting system...')
            pause()
            save_system(system)
            print('Goodbye')
            pause(1)
            break
        else:
            print('Invalid option')
            pause()
            continue

if __name__ == "__main__":
    main()