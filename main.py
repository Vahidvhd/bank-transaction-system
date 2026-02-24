from bank.system import init_system, save_system
from bank.accounts import create_account, transfer, gen_acc_id
from bank.validators import validate_name_fname, validate_national_id, validate_password, validate_phone, validate_email
import getpass
import time
import random
import pyfiglet
from bank.verification.email_verification import send_email_gmail
import os


def clear_terminal():
    os.system('cls')
    # print banner

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
                log_in_menu(system, acc_id, user_acc)
                return
        
        print('\nToo many failed attempts. Please wait 10 seconds.\n')
        for i in range(10, 0, -1):
            print(f'{i} ...')
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

def log_in_options(system):
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

def log_in_menu(system, acc_id, user_acc):
    while True:
        user_acc = system.get('accounts').get(acc_id)
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
            return
        else:
            print("Invalid option.")


def show_user_info(name, fname, national_id, phone, email):
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
    pass

def user_batch_transfer(system, acc_id):
    pass

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
            log_in_options(system)
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