import os
import adafruit_hashlib as hashlib
import binascii
import json

AUTH_FILE = "sd/auth.json"
SALT_SIZE = 16  # 128-bit salt

def is_registered():
    return AUTH_FILE in os.listdir("/")

def generate_salt():
    return os.urandom(SALT_SIZE)

def hash_password(password: str, salt: bytes) -> str:
    combined = salt + password.encode("utf-8")
    hashed = hashlib.sha256(combined).digest()
    return binascii.hexlify(hashed).decode("utf-8")

def save_credentials(salt: bytes, hashed_password: str):
    data = {
        "salt": binascii.hexlify(salt).decode("utf-8"),
        "hash": hashed_password
    }
    # with open(AUTH_FILE, "w") as f:
    #     f.write(json.dumps(data))
    print(f"💾 Credentials saved securely.{data}")

def register_master_key(password: str) -> bool:
    if is_registered():
        print("⚠️ Master key already registered.")
        return False

    salt = generate_salt()
    hashed = hash_password(password, salt)
    save_credentials(salt, hashed)
    print("✅ Master key registered securely.")
    return True

def authenticate(password: str) -> bool:
    # if not is_registered():
    #     print("❌ No master key registered.")
    #     return False

    try:
        with open(AUTH_FILE, "r") as f:
            data = json.load(f)
            print(f"🔐 Loaded data: {data}")
            salt = binascii.unhexlify(data["salt"])
            stored_hash = data["hash"]
    except Exception as e:
        print("❌ Error reading auth file:", e)
        return False

    test_hash = hash_password(password, salt)
    return test_hash == stored_hash
