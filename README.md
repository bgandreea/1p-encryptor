# 🔐 1Password Encryptor

Securely encrypt and decrypt files using AES-GCM with a password stored in your 1Password vault. This tool integrates with the 1Password CLI (`op`) to fetch secrets and manage session tokens automatically—including session caching.

## 📦 Features

- AES-GCM encryption with PBKDF2 key derivation
- Pulls credentials & paths securely from 1Password vault
- `.session_token` caching for non-interactive CLI usage
- Dual-mode support:
  - Use via PyCharm (green button)
  - Use via CLI with flags (`--encrypt`, `--decrypt`)
- Modular structure with clean separation of concerns

## 🧱 Project Structure

```
lp-encryptor/
├── cli.py                  # CLI entry point with argparse
├── constants.py            # Field names, shorthand, etc.
├── decryptor.py            # Decryption runner
├── encryptor.py            # Encryption runner
├── session.py              # Session management with caching
├── utils.py                # Shared crypto + 1Password utils
├── .session_token          # Cached session token (excluded from git)
└── .gitignore              # Ignores token, venv, IDE files, etc.
```

## 🚀 Requirements

- Python 3.8+
- [1Password CLI v2](https://developer.1password.com/docs/cli/)

Install dependencies:
```bash
pip install -r requirements.txt
```

> You may need to add the `op` CLI to your PATH on Windows.

## 🔑 1Password Setup

In your 1Password vault, create a new item (e.g. `EncryptionSecrets`) with these fields:

- `ENCRYPTION_PASS` – The password to derive the key
- `INPUT_LOCATION` – Absolute path to the input file
- `OUTPUT_LOCATION` – Path to save the encrypted result
- `DECRYPTED_OUTPUT_LOCATION` – Where to write the decrypted output

## 🧠 Session Token Management

This tool uses `.session_token` to cache your session between runs.

- You can generate it manually using:
  ```bash
  op signin --raw
  ```
- Paste the token into `.session_token` (no newlines)
- The script will auto-load it and skip validation (for full automation)

Add this to `.gitignore`:
```
.session_token
```

## ⚙️ Usage

### 🔹 Encrypt
```bash
python cli.py --encrypt
```

### 🔹 Decrypt
```bash
python cli.py --decrypt
```

### 🔹 Burn input (future support)
```bash
python cli.py --burn
```

## 🧪 Dev Mode (PyCharm)

1. Open `encryptor.py` or `decryptor.py`
2. Use the green run button (requires `.session_token`)
3. No prompts, no stalls—just clean encrypted output

## 📜 License

MIT License  
See `LICENSE` file for full terms.
