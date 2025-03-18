import sys
import os

# XOR key size (16 bytes)
KEY_SIZE = 15

# Generate a random XOR key
key = os.urandom(KEY_SIZE)

try:
    with open(sys.argv[1], "rb") as f:
        plaintext = f.read()
except IndexError:
    print(f"Usage: {sys.argv[0]} <raw payload file>")
    sys.exit(1)
except FileNotFoundError:
    print("Error: File not found!")
    sys.exit(1)

# XOR encode shellcode
ciphertext = bytearray(len(plaintext))
for i in range(len(plaintext)):
    ciphertext[i] = plaintext[i] ^ key[i % KEY_SIZE]

# Print XOR key
print('unsigned char xorKey[] = { ' + ', '.join(f'0x{byte:02x}' for byte in key) + ' };')

# Print encoded shellcode
print('unsigned char encodedShellcode[] = { ' + ', '.join(f'0x{byte:02x}' for byte in ciphertext) + ' };')
