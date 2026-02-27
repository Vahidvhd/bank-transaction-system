<img width="626" height="366" alt="logo" src="https://github.com/user-attachments/assets/784694ec-07c9-46ca-b011-bdcb96130c4e" />


# **Vault-Tech Bank**

## **Project Title & Overview**

## Bank Transaction System

### This project is a modular banking transaction system implemented in Python.

The system is designed using functional programming principles and ensures data integrity through deep copy mechanisms and automatic rollback on failure.

The main goal of this project is to simulate a simplified banking core system that supports:

•	Account creation

•	Secure money transfers

•	Batch transfers

•	Transaction history tracking

•	Persistent state storage using pickle

The system guarantees consistency by validating transactions before applying changes and restoring the previous state in case of errors

## Features

•	Functional-style design with modular structure

•	Safe transaction execution using a validation decorator

•	Automatic rollback on failure

•	Persistent data storage using pickle

•	Transaction logging with timestamps and system hash

•	Metadata tracking (created_at, last_modified, version)

•	Clean code structure (PEP8 compliant)

•	Modular architecture suitable for extension

## Project Structure
```plaintext
bank-transaction-system/
│
├── bank/
│   ├── __init__.py
│   ├── system.py
│   ├── decorators.py
│   ├── accounts.py
│   ├── verification/
│        ├── __init__.py
│        ├── email_verification.py
│        ├── logo.jpg
├── main.py
├── README.md
├── .gitignore
└── License
```
### system.py

Responsible for system lifecycle management:

•	init_system()

•	load_system()

•	save_system()

Handles pickle persistence and metadata updates.

### decorators.py

Contains:

•	validate_transaction decorator

This decorator:

•	Takes a deepcopy snapshot before execution

•	Executes the main function

•	On success → logs transaction + saves system

•	On error → restores previous state

### accounts.py

Contains core banking operations:

•	create_account()

•	transfer()

•	batch_transfer()

All critical operations are decorated with @validate_transaction.

### main.py

Demonstrates example usage of the system and how to call main functions.

## Installation & Running

### Clone the repository
```python
git clone https://github.com/Vahidvhd/bank-transaction-system.git
cd bank-transaction-system
```
### Run the project
```python
python main.py
```
If bank_data.pkl does not exist, the system automatically creates a new one.

No external dependencies are required beyond standard Python libraries

## Example Usage
```python
from bank.system import init_system
from bank.accounts import create_account, transfer

system = init_system()

create_account(
    system,
    "ACC001",
    1000000,
    {
        "name": "Ali Rezaei",
        "type": "Personal",
        "national_id": "0012345678",
        "contact": {
            "email": "ali@email.com",
            "phone": "09123456789"
        }
    }
)

transfer(system, "ACC001", "ACC002", 500000, description="Loan repayment")
```
## Data Structure Examples
### Bank System Structure
```python
bank_system = {
    'accounts': {},
    'transaction_history': [],
    'data_file': 'bank_data.pkl',
    'metadata': {
        'created_at': 'ISO timestamp',
        'last_modified': 'ISO timestamp',
        'version': '1.0.0'
    }
}
```
### Transaction History Entry
```python
{
    'action': 'transfer',
    'args': ('ACC001', 'ACC002', 500000),
    'kwargs': {'description': 'Loan repayment'},
    'timestamp': 'ISO timestamp',
    'system_hash': 'hash_value',
    'success': True
}
```
### Account Structure
```python
{
    'ACC001': {
        'balance': 1000000.0,
        'owner': {...},
        'created_at': 'ISO timestamp',
        'transactions': [...],
        'status': 'Active',
        'account_type': 'Current'
    }
}
```
## Team Contribution

###  Vahid Vahedi – System Management & Persistence Layer

•	System architecture design

•	Implementation of init_system, load_system, and save_system

•	Pickle-based persistence mechanism

•	Metadata management (created_at, last_modified, version control)

•	Ensuring state consistency across sessions


###  Saman Zhiani – Transaction Validation & System Integrity

•	Implementation of @validate_transaction decorator

•	Transaction history logging system

•	Automatic rollback mechanism on failure

•	Exception handling and error propagation strategy

•	Ensuring atomic transaction behavior (commit on success, restore on error)



###  Mohammad-Hasan Anisi – Account Management & Business Logic

•	Implementation of core account operations (create_account, transfer, batch_transfer)

•	Business logic validation (duplicate account check, balance validation, positive amount validation)

•	Balance updates using deepcopy for safe state manipulation

•	Account-level transaction recording
