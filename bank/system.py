import os
import pickle
import copy
from datetime import datetime

DEFAULT_DATA_FILE = "bank_data.pkl"
DEFAULT_VERSION = "1.0.0"


def time_now():
    return datetime.now().isoformat(timespec="seconds")


def create_default_system():
    now = time_now()
    return {
        "accounts": {},
        "transaction_history": [],
        "data_file": DEFAULT_DATA_FILE,
        "metadata": {
            "created_at": now,
            "last_modified": now,
            "version": DEFAULT_VERSION
        }
    }


def load_system(data_file=DEFAULT_DATA_FILE):
    if not os.path.exists(data_file):
        return None
    try:
        with open(data_file, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None


def save_system(bank_system):
    bank_system["metadata"]["last_modified"] = time_now()
    snapshot = copy.deepcopy(bank_system)

    data_file = snapshot.get("data_file", DEFAULT_DATA_FILE)
    with open(data_file, "wb") as f:
        pickle.dump(snapshot, f)


def init_system():
    loaded = load_system(DEFAULT_DATA_FILE)
    if loaded is not None:
        return loaded
    return create_default_system()
