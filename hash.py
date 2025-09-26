import subprocess
import os
import hashlib
import binascii

# Path to OpenSSL executable (adjust for your system)
OPENSSL_PATH = r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"

# File paths
input_file = "input.txt"
encrypted_file = "encrypted.bin"
decrypted_file = "decrypted.txt"
key_file = "aes_key.bin"
iv_file = "iv.bin"
hash_file = "input_hash.txt"

# Step 1: Generate key and IV using os.urandom
key = os.urandom(32)  # 32 bytes for AES-256
iv = os.urandom(16)   # 16 bytes for CBC IV
with open(key_file, "wb") as f:
    f.write(key)
print(f"[*] Generated AES-256 key: {key_file}")
with open(iv_file, "wb") as f:
    f.write(iv)
print(f"[*] Generated IV: {iv_file}")

# Step 2: Convert key and IV to hexadecimal
key_hex = binascii.hexlify(key).decode().strip()
iv_hex = binascii.hexlify(iv).decode().strip()
print(f"[*] Key (hex): {key_hex}")
print(f"[*] IV (hex): {iv_hex}")

# Step 3: Verify input file exists
if not os.path.exists(input_file):
    print(f"Error: Input file '{input_file}' does not exist.")
    exit(1)

# Step 4: Compute SHA-256 hash of input file
with open(input_file, "rb") as f:
    file_data = f.read()
hash_obj = hashlib.sha256(file_data)
file_hash = hash_obj.hexdigest()
with open(hash_file, "w") as f:
    f.write(file_hash)
print(f"[*] SHA-256 hash of '{input_file}': {file_hash}")

# Step 5: Encrypt the file using OpenSSL
command_encrypt = [
    OPENSSL_PATH, "enc", "-aes-256-cbc",
    "-in", input_file,
    "-out", encrypted_file,
    "-K", key_hex,
    "-iv", iv_hex
]
try:
    subprocess.run(command_encrypt, check=True, capture_output=True, text=True)
    print(f"[*] Encrypted '{input_file}' to '{encrypted_file}'")
except subprocess.CalledProcessError as e:
    print(f"[*] Encryption failed: {e.stderr}")
    exit(1)

# Step 6: Decrypt the file using OpenSSL
command_decrypt = [
    OPENSSL_PATH, "enc", "-aes-256-cbc", "-d",
    "-in", encrypted_file,
    "-out", decrypted_file,
    "-K", key_hex,
    "-iv", iv_hex
]
try:
    subprocess.run(command_decrypt, check=True, capture_output=True, text=True)
    print(f"[*] Decrypted '{encrypted_file}' to '{decrypted_file}'")
except subprocess.CalledProcessError as e:
    print(f"[*] Decryption failed: {e.stderr}")
    exit(1)

# Step 7: Verify hash of decrypted file
with open(decrypted_file, "rb") as f:
    decrypted_data = f.read()
decrypted_hash = hashlib.sha256(decrypted_data).hexdigest()
with open(hash_file, "r") as f:
    original_hash = f.read().strip()

if decrypted_hash == original_hash:
    print(f"[*] Hash verification successful: {decrypted_hash}")
else:
    print(f"[*] Hash verification failed!")
    print(f"Original hash: {original_hash}")
    print(f"Decrypted hash: {decrypted_hash}")