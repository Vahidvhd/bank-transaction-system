import secrets
import string
from copy import deepcopy
from datetime import datetime
from datetime import date
from operator import truediv
from uuid import uuid4
# from .decorators import validate_transaction
def collect_account_fields(system, key_1, key_2):
    result = []
    for acc in system.get("accounts", {}).values():
        section = acc.get(key_1)
        if isinstance(section, dict):
            value = section.get(key_2)
            if value is not None:
                result.append(value)
    return result

def create_expiration_date():
    now = datetime.now().date()
    expiration_date = now.replace(year=now.year + 5)
    return now.isoformat(), expiration_date.isoformat()

def accnumber_cvv_cartnumber_(prefix = "6037", length=16):
    length_1 = length - len(prefix)
    random_number =''
    random_number += ''.join(secrets.choice(string.digits)for _ in range(length_1))
    return prefix + random_number

def load_csv(file_name):
    accounts = []

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            account = line.strip()
            account = account.replace(" ", "")
            if account:
                accounts.append(account)

    if not accounts:
        raise ValueError("CSV file is empty or contains only empty lines.")

    return accounts
def resolve_account_number(system, identifier):

    identifier = str(identifier).strip().replace(" ", "")

    if not identifier:
        raise KeyError("Account/Card identifier is empty")

    accounts = system.get("accounts", {})

    if identifier in accounts:
        return identifier

    for account_id, account_data in accounts.items():
        cart_data = account_data.get("cart_data")

        if not isinstance(cart_data, dict):
            continue

        card_number = cart_data.get("cart_number")

        if card_number and str(card_number).strip().replace(" ", "") == identifier:

            if cart_data.get("status") == "Expired":
                raise ValueError("Card is expired")

            return account_id

    raise KeyError(f"Account or Card not found: {identifier}")
#@validate_transaction
def create_account(system, initial_balance, owner, account_type="Current"):
    national_ids = collect_account_fields(system, "owner", "national_id")
    if owner["national_id"] in national_ids:
        raise ValueError("Create Account is fail")
    if not isinstance(initial_balance, (int, float)):
        raise TypeError("Initial balance must be numeric")

    if initial_balance < 0:
        raise ValueError("Initial balance cannot be negative")

    if not isinstance(owner, dict):
        raise TypeError("Owner must be a dictionary")
    while True:
        account_number = accnumber_cvv_cartnumber_(prefix="", length=13)
        if account_number not in system["accounts"]:
            break

    current_time = datetime.now().isoformat()

    account_data = {
        "balance": float(initial_balance),
        "owner": deepcopy(owner),
        "created_at": current_time,
        "transactions": [],
        "status": "Active",
        "account_type": account_type
    }
    opening_transaction = {
        "id": str(uuid4()),
        "type": "Account Opening",
        "amount": float(initial_balance),
        "counterparty": "System",
        "time": current_time,
        "description": "Account opening with initial balance",
        "balance_after": float(initial_balance)
    }

    account_data["transactions"].append(opening_transaction)

    system["accounts"][account_number] = account_data

    return {
        "account_id": account_number,
        "balance": float(initial_balance),
        "status": "Account successfully created"
    }

#@validate_transaction
def transfer(system, from_acc, to_acc, amount, description=""):
    from_acc = resolve_account_number(system, from_acc)
    to_acc = resolve_account_number(system, to_acc)
    if from_acc == to_acc:
        raise ValueError("Sender and receiver accounts must be different")


    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be numeric")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    sender = system["accounts"][from_acc]
    receiver = system["accounts"][to_acc]

    if sender["balance"] < amount:
        raise ValueError("Insufficient balance")

    system_backup = deepcopy(system)

    try:
        sender = deepcopy(sender)
        receiver = deepcopy(receiver)

        now = datetime.now().isoformat()
        tx_id = str(uuid4())

        sender_new_balance = float(sender["balance"]) - float(amount)
        receiver_new_balance = float(receiver["balance"]) + float(amount)

        sender["balance"] = sender_new_balance
        receiver["balance"] = receiver_new_balance

        sender_tx = {
            "id": tx_id,
            "type": "Transfer Out",
            "amount": float(amount),
            "counterparty": to_acc,
            "time": now,
            "description": description or f"Transfer to {to_acc}",
            "balance_after": sender_new_balance,
        }

        receiver_tx = {
            "id": tx_id,
            "type": "Transfer In",
            "amount": float(amount),
            "counterparty": from_acc,
            "time": now,
            "description": description or f"Transfer from {from_acc}",
            "balance_after": receiver_new_balance,
        }

        sender.setdefault("transactions", [])
        receiver.setdefault("transactions", [])

        sender["transactions"].append(sender_tx)
        receiver["transactions"].append(receiver_tx)

        system["accounts"][from_acc] = sender
        system["accounts"][to_acc] = receiver

        return {
            "from": from_acc,
            "to": to_acc,
            "amount": float(amount),
            "from_balance": sender_new_balance,
            "to_balance": receiver_new_balance,
            "status": "Transfer successful",
        }

    except Exception as e:
        system.clear()
        system.update(system_backup)

        return {
            "from": from_acc,
            "to": to_acc,
            "amount": amount,
            "status": "Transfer failed - no changes applied",
            "error": str(e),
        }

def batch_transfer(system, from_acc, amount, file_name, description=""):
    from_acc = resolve_account_number(system, from_acc)
    transfers = load_csv(file_name)

    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be numeric")
    if amount <= 0:
        raise ValueError("Amount must be positive")

    total_amount = float(amount) * len(transfers)
    sender_balance = float(system["accounts"][from_acc]["balance"])
    if sender_balance < total_amount:
        raise ValueError("Insufficient balance for batch transfer")

    results = []
    success_count = 0
    failed_accounts = []

    for to_acc in transfers:
        try:
            result = transfer(system, from_acc, to_acc, amount, description=description)
        except Exception as e:
            result = {
                "from": from_acc,
                "to": to_acc,
                "amount": float(amount),
                "status": "Transfer failed",
                "error": str(e),
            }

        if result.get("status") == "Transfer successful":
            success_count += 1
        else:
            failed_accounts.append(to_acc)

        results.append(result)

    return {
        "from": from_acc,
        "total_transfers": len(results),
        "successful": success_count,
        "failed": len(failed_accounts),
        "failed_accounts": failed_accounts,
        "details": results,
        "status": "Batch completed"
    }

def create_cart(system, account_number):
    person_data = deepcopy(system["accounts"][account_number])
    card_numbers = set(collect_account_fields(system, "cart_data", "cart_number"))
    cart_data = person_data.setdefault("cart_data", {})
    while True:
        cart_number = accnumber_cvv_cartnumber_()
        if cart_number not in card_numbers:
            cart_data["cart_number"] = cart_number
            cart_data["cvv"] = accnumber_cvv_cartnumber_(prefix='', length=3)
            cart_data["status"] = "Active"
            break
    expiration_date = create_expiration_date()
    cart_data["create_date"] = expiration_date[0]
    cart_data["expiration_date"] = expiration_date[1]
    system["accounts"][account_number] = person_data

    return {
            "account_id": account_number,
            "card_number": cart_data["cart_number"],
            "status": "Card successfully created"
    }

def deactivate_expired_cards(system):
    today = date.today()
    updated_accounts = []

    for acc_id, acc in system.get("accounts", {}).items():
        cart_data = acc.get("cart_data")
        if not isinstance(cart_data, dict):
            continue

        exp_str = cart_data.get("expiration_date")
        if not exp_str:
            continue

        exp_date = date.fromisoformat(exp_str)

        if today > exp_date:
            cart_data["status"] = "Expired"
            updated_accounts.append(acc_id)

    return updated_accounts

