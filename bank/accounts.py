from copy import deepcopy
from datetime import datetime
from uuid import uuid4

#from bank.decorators import validate_transaction


#@validate_transaction
def create_account(system, account_id, initial_balance, owner, account_type="Current"):

    if account_id in system["accounts"]:
        raise ValueError("Account ID already exists")

    if not isinstance(initial_balance, (int, float)):
        raise TypeError("Initial balance must be numeric")

    if initial_balance < 0:
        raise ValueError("Initial balance cannot be negative")

    if not isinstance(owner, dict):
        raise TypeError("Owner must be a dictionary")

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

    system["accounts"][account_id] = account_data

    return {
        "account_id": account_id,
        "balance": float(initial_balance),
        "status": "Account successfully created"
    }

#@validate_transaction
def transfer(system, from_acc, to_acc, amount, description=""):

    if from_acc == to_acc:
        raise ValueError("Sender and receiver accounts must be different")

    if from_acc not in system["accounts"]:
        raise KeyError(f"Sender account not found: {from_acc}")

    if to_acc not in system["accounts"]:
        raise KeyError(f"Receiver account not found: {to_acc}")

    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be numeric")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    sender = system["accounts"][from_acc]
    receiver = system["accounts"][to_acc]

    if sender["balance"] < amount:
        raise ValueError("Insufficient balance")

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
