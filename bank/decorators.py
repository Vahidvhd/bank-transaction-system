from functools import wraps
from copy import deepcopy
from datetime import datetime
import hashlib
from bank.system import save_system

def validate_transaction(func):
    @wraps(func)
    def wrapper(system, *args, **kwargs):
        snapshot = deepcopy(system)

        try:
            result = func(system, *args, **kwargs)

            transaction_record = {
                # TODO:
            }

            system['transaction_history'].append(transaction_record)
            save_system(system)

            return result

        except Exception as e:
            system.clear()
            system.update(snapshot)
            raise e

    return wrapper





