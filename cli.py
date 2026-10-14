import argparse
from encryptor import run_encryptor
from decryptor import run_decryptor

parser = argparse.ArgumentParser(description="1p-encryptor CLI")
parser.add_argument("--encrypt", action="store_true", help="Encrypt the input file")
parser.add_argument("--decrypt", action="store_true", help="Decrypt the encrypted file")

args = parser.parse_args()

if args.encrypt:
    run_encryptor()

if args.decrypt:
    run_decryptor()