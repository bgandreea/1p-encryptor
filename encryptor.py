from utils import get_session_token, get_1password_field, encrypt_file
from constants import VAULT_ITEM_NAME, FIELD_ENCRYPTION_PASS, FIELD_INPUT_LOCATION, FIELD_OUTPUT_LOCATION

def run_encryptor():
    print("\U0001f512 Fetching session...")
    session_token = get_session_token()

    password = get_1password_field(VAULT_ITEM_NAME, FIELD_ENCRYPTION_PASS, session_token)
    input_path = get_1password_field(VAULT_ITEM_NAME, FIELD_INPUT_LOCATION, session_token)
    output_path = get_1password_field(VAULT_ITEM_NAME, FIELD_OUTPUT_LOCATION, session_token)

    print("\U0001f680 Encrypting file...")
    encrypt_file(password, input_path, output_path)

if __name__ == "__main__":
    run_encryptor()
