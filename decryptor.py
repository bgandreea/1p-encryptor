from utils import get_session_token, get_1password_field, decrypt_file
from constants import VAULT_ITEM_NAME, FIELD_ENCRYPTION_PASS, FIELD_OUTPUT_LOCATION, FIELD_DECRYPTED_OUTPUT_LOCATION

def run_decryptor():
    print("\U0001f513 Fetching session...")
    session_token = get_session_token()

    password = get_1password_field(VAULT_ITEM_NAME, FIELD_ENCRYPTION_PASS, session_token)
    encrypted_path = get_1password_field(VAULT_ITEM_NAME, FIELD_OUTPUT_LOCATION, session_token)
    decrypted_path = get_1password_field(VAULT_ITEM_NAME, FIELD_DECRYPTED_OUTPUT_LOCATION, session_token)

    print("\U0001f4a5 Decrypting file...")
    decrypt_file(password, encrypted_path, decrypted_path)

if __name__ == "__main__":
    run_decryptor()
