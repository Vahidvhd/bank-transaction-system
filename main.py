from bank.system import init_system
from bank.accounts import create_account, transfer

def demo(system):
    """Run a minimal demo so the project 'runs' out of the box."""
    print("Running demo...")

    create_account(system, "A1001", 1000, "Vahid")
    create_account(system, "A1002", 500, "Saman")
    transfer(system, "A1001", "A1002", 200, "demo transfer")

    print("Demo finished ✅")

def main():
    system = init_system()
    print("System loaded/initialized ✅")

    demo(system)

if __name__ == "__main__":
    main()
