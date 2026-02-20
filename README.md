# bank-transaction-system
## A modular banking transaction system focused on functional design, transaction validation, and persistent state management.

<!-- ## Project Overview

### TODO:

## Project Structure Explanation

### TODO:

## How to Run the Project

### TODO:

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
