from bank.system import init_system, save_system
from bank.accounts import create_account, transfer, gen_acc_id

def demo(system):
    print("Running demo...")

    create_account(system, "A1001", 1000, {"name": "Vahid"})
    create_account(system, "A1002", 500, {"name": "Saman"})

    print("Before transfer:")
    print("A1001:", system["accounts"]["A1001"]["balance"])
    print("A1002:", system["accounts"]["A1002"]["balance"])

    transfer(system, "A1001", "A1002", 200, "demo transfer")

    print("After transfer:")
    print("A1001:", system["accounts"]["A1001"]["balance"])
    print("A1002:", system["accounts"]["A1002"]["balance"])

    print("Demo finished ✅")

def menu():
    user_menu = input('Select one option:\n1: Log in\n2: Create account').strip()
    return user_menu

def create_acc(system):
    print('*** Create account***')

    owner_dict ={
    'Name' : input('Name: ').strip(),
    'Fname' : input('Surname: ').strip(),
    'National id' : input('National id: ').strip(),
    'Password' : input('Password: ').strip(),
    'Contact' : {
        'Phone' : input('Phone Number: ').strip(),
        'Email' : input('Email: ').strip(),
        }
    }
    while True:
        init_amout = input('Enter initial deposit amount: ').strip()
        try:
            init_amout = float(init_amout)
            break
        except ValueError:
            print('Initial balance cannot contain any letters of special characters')
            continue
    
    account_id = gen_acc_id(system)
    try:
        result = create_account(system, account_id, init_amout, owner_dict)
        save_system(system)
        print(f"{result['status']}\nAccount number: {result['account_id']}\nBalance: {result['balance']}")
    except (TypeError , ValueError) as e:
        print('Error', e)

def main():
    system = init_system()
    print("System loaded/initialized ✅")
    user_choice = menu()
    if user_choice == '1':
        demo(system)
    elif user_choice == '2':
        create_acc(system)


if __name__ == "__main__":
    main()