import os
import logging


def get_mandatory_env_variable(env_variable_key: str):
    try:
        return os.environ[env_variable_key]
    except:
        error_message = f"Failed to get mandatory enviroment variable {env_variable_key}"
        logging.error(error_message)

        raise RuntimeError(error_message)

def decode_from_hex(input: str):
    return bytes.fromhex(input[2:])[0]