from bank.system import init_system, save_system
from bank.accounts import create_account, transfer, gen_acc_id
from bank.validators import validate_name_fname, validate_national_id, validate_password, validate_phone, validate_email


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
    attemps =0
    while attemps < 3:
        acc_id = input('Account Number: ').strip()
        password = input('Password: ').strip()
        user_acc = system.get('accounts',{}).get(acc_id)
        if not user_acc or user_acc['owner']['password'] != password:
            attemps += 1
            print(f'Invalid account number or password ({3-attemps} left)')
        else:
            print(f"Welcome {user_acc['owner']['name']}")
            return acc_id
    print("Too many failed attempts. Returning to main menu.") # # TODO: Add lockout timer after 3 failed attempts
    return None
def log_in_menu(system):
    print('***Log in***')
    login_menu = input('1: Log in with Account Number & Password\n2: Forgot Password\n\n\n3: Back\n>>>: ').strip()
    if login_menu == '1':
        log_in(system)
    elif login_menu == '2':
        # TODO: implement forgot password feature
        pass
    elif login_menu == '3':
        return
    else:
        print('Invalid option')

def main():
    system = init_system()
    print("System loaded/initialized ✅")
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