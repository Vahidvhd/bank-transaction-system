from bank.system import init_system
from bank.accounts import create_account, transfer

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

def main():
    system = init_system()
    print("System loaded/initialized ✅")
    demo(system)

if __name__ == "__main__":
    main()