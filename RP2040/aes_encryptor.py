import aesio
import os
import binascii

BLOCK_SIZE = 16

def pad(data):
    """Apply PKCS#7 padding."""
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len

def unpad(padded_data):
    """Remove PKCS#7 padding."""
    pad_len = padded_data[-1]
    if pad_len > BLOCK_SIZE or pad_len == 0:
        raise ValueError("Invalid padding")
    return padded_data[:-pad_len]

def encrypt_aes_cbc(plaintext, key_string):
    key = key_string.encode("utf-8")
    key = (key + b"\x00" * BLOCK_SIZE)[:BLOCK_SIZE]

    iv = os.urandom(BLOCK_SIZE)
    padded = pad(plaintext.encode("utf-8"))
    encrypted = bytearray(len(padded))

    cipher = aesio.AES(key, aesio.MODE_CBC, IV=iv)
    cipher.encrypt_into(padded, encrypted)

    result = iv + encrypted
    return binascii.b2a_base64(result).decode("utf-8").strip()


def decrypt_aes_cbc(base64_input, key_string):
    key = key_string.encode("utf-8")
    key = (key + b"\x00" * BLOCK_SIZE)[:BLOCK_SIZE]

    try:
        encrypted_data = binascii.a2b_base64(base64_input)
    except Exception:
        return "[ERROR] Invalid base64"

    if len(encrypted_data) < BLOCK_SIZE:
        return "[ERROR] Data too short"

    iv = encrypted_data[:BLOCK_SIZE]
    ciphertext = encrypted_data[BLOCK_SIZE:]
    decrypted = bytearray(len(ciphertext))

    cipher = aesio.AES(key, aesio.MODE_CBC, IV=iv)
    cipher.decrypt_into(ciphertext, decrypted)

    try:
        unpadded = unpad(decrypted)
        return unpadded.decode("utf-8")
    except Exception:
        return "[ERROR] Invalid padding or decoding"
