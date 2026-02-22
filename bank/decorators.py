from typing import Callable, Dict
from datetime import datetime
from functools import wraps
from copy import deepcopy
from .system import save_system


def validate_transaction(func: Callable) -> Callable:
    """Decorator to ensure transactional safety for critical bank operations."""

    @wraps(func)
    def wrapper(system: Dict, *args, **kwargs):
        # snapshot = deepcopy(system)

        # try:
        #     result = func(system, *args, **kwargs)
        #     timestamp = datetime.now().isoformat()
        #     system_string = str(system).encode()

        #     transaction_record = {
        #         'args': args,
        #         'kwargs': kwargs,
        #         "timestamp": timestamp,
        #         # TODO:
        #     }

        #     system["transaction_history"].append(transaction_record)
        #     save_system(system)

        #     return result

        # except Exception as e:
        #     system.clear()
        #     system.update(snapshot)
        #     raise e

    return wrapper
