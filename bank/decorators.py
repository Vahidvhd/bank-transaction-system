from typing import Callable, Dict
from datetime import datetime
from functools import wraps
from copy import deepcopy
import hashlib
from .system import save_system


def validate_transaction(func: Callable) -> Callable:
    """Decorator to ensure transactional safety for critical bank operations."""

    @wraps(func)
    def wrapper(system: Dict, *args, **kwargs):
        snapshot = deepcopy(system)

        try:
            result = func(system, *args, **kwargs)

            timestamp = datetime.now().isoformat()
            system_string = str(system).encode()
            system_hash = hashlib.sha256(system_string).hexdigest()

            transaction_record = {
                "action": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "action_time": timestamp,
                "system_hash": system_hash,
                "success": True,
            }

            system["transaction_history"].append(transaction_record)
            save_system(system)

            return result

        except Exception as e:
            system["transaction_history"].append(
                {
                    "action": func.__name__,
                    "args": args,
                    "kwargs": kwargs,
                    "timestamp": datetime.now().isoformat(),
                    "system_hash": None,
                    "success": False,
                }
            )

            system.clear()
            system.update(snapshot)
            raise e

    return wrapper
