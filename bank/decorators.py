from functools import wraps
from copy import deepcopy
from datetime import datetime
import hashlib
from .system import save_system


def validate_transaction(func):
    @wraps(func)
    def wrapper(system, *args, **kwargs):
        snapshot = deepcopy(system)

        try:
            result = func(system, *args, **kwargs)

            timestamp = datetime.now().isoformat()

            system_string = str(system).encode()
            system_hash = hashlib.md5(system_string).hexdigest()

            transaction_record = {
                'action': func.__name__,
                'args': args,
                'kwargs': kwargs,
                'timestamp': timestamp,
                'system_hash': system_hash,
                'success': True
            }

            system['transaction_history'].append(transaction_record)

            save_system(system)

            return result

        except Exception as e:
            system.clear()
            system.update(snapshot)
            raise e

    return wrapper