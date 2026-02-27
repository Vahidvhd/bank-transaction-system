# **Vault-Tec Bank**

## **Project Title & Overview**

## Bank Transaction System

### This project is a modular banking transaction system implemented in Python.

The system is designed using functional programming principles and ensures data integrity through deep copy mechanisms and automatic rollback on failure.

The main goal of this project is to simulate a simplified banking core system that supports:

Account creation

Secure money transfers

Batch transfers

Transaction history tracking

Persistent state storage using pickle

The system guarantees consistency by validating transactions before applying changes and restoring the previous state in case of errors

## Features

Functional-style design with modular structure

Safe transaction execution using a validation decorator

Automatic rollback on failure

Persistent data storage using pickle

Transaction logging with timestamps and system hash

Metadata tracking (created_at, last_modified, version)

Clean code structure (PEP8 compliant)

Modular architecture suitable for extension

## Project Structure

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

### system.py

Responsible for system lifecycle management:

init_system()

load_system()

save_system()

Handles pickle persistence and metadata updates.

### decorators.py

Contains:

validate_transaction decorator

This decorator:

Takes a deepcopy snapshot before execution

Executes the main function

On success → logs transaction + saves system

On error → restores previous state

### accounts.py

Contains core banking operations:

create_account()

transfer()

batch_transfer()

All critical operations are decorated with @validate_transaction.

### main.py

Demonstrates example usage of the system and how to call main functions.

## Installation & Running

### Clone the repository

git clone https://github.com/Vahidvhd/bank-transaction-system.git
cd bank-transaction-system

### Run the project

python main.py

If bank_data.pkl does not exist, the system automatically creates a new one.

No external dependencies are required beyond standard Python libraries

## Example Usage

### TODO: -->



## Team Contribution

###  Vahid – System Management & Persistence Layer

- Designed and implemented the core `bank_system` dictionary structure in `bank/system.py`.
- Implemented `init_system` to initialize a new system or load an existing one.
- Implemented `load_system` with proper error handling (`try/except`) to safely return `None` in case of missing or corrupted files.
- Implemented `save_system` using `pickle` for persistent storage.
- Used `deepcopy` during save operations to prevent unintended mutations.
- Managed system metadata including `created_at`, `last_modified`, and `version`.
- Ensured state persistence across multiple program executions.
- Maintained modular project structure compliance.

---

###  Saman – Transaction Validation & System Integrity

- Designed and implemented the `validate_transaction` decorator in `bank/decorators.py`.
- Implemented transactional safety using `deepcopy` snapshots before function execution.
- Developed rollback mechanism to restore system state on failure.
- Structured transaction logging according to the required specification:
  (`action`, `args`, `kwargs`, `timestamp`, `system_hash`, `success`).
- Generated system integrity hash after successful operations.
- Integrated automatic persistence via `save_system`.
- Ensured atomic and consistent behavior for `create_account`, `transfer`, and `batch_transfer`.
- Tested decorated functions to verify correct transactional behavior.

---

###  Mohammad Hasan – Account Management & Business Logic

- Designed and implemented account schema in `bank/accounts.py`.
- Implemented `create_account` with duplicate account ID validation.
- Added account opening transaction record during account creation.
- Implemented `transfer` function with:
  - Account existence validation  
  - Sufficient balance verification  
  - Positive amount enforcement  
- Implemented `batch_transfer` with multi-transaction handling.
- Used `deepcopy` for safe balance updates.
- Ensured per-account transaction history is properly recorded.
- Followed clean code principles and PEP8 standards.
