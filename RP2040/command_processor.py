from aes_encryptor import encrypt_aes_cbc, decrypt_aes_cbc
from auth_manager import register_master_key, authenticate
from key_store import KeyStore
import digitalio
import board
import time

class CommandProcessor:
    def __init__(self, hid_output):
        self.hid = hid_output
        self.authenticated = False
        self.master_key = None
        self.vault = None

    def execute(self, command):
        command = command.strip()
        print(f"Executing command: '{command}'")

        if command.startswith("encrypt "):
            if not self.authenticated:
                print("🔒 Auth required before sending credentials.")
                return
            _, msg = command.split(" ", 1)
            encrypted = encrypt_aes_cbc(msg, key_string=self.master_key)
            print("🔐 Encrypted (base64):", encrypted)

        elif command.startswith("decrypt "):
            if not self.authenticated:
                print("🔒 Auth required before sending credentials.")
                return
            _, b64 = command.split(" ", 1)
            decrypted = decrypt_aes_cbc(b64, key_string=self.master_key)
            print("🔓 Decrypted:", decrypted)
            self.hid.type_text(decrypted, delay=0.2)

        elif command.startswith("auth "):
            _, auth = command.split(" ", 1)
            if auth is None:
                print("🔐 Usage: auth <masterkey>")
            elif authenticate(auth):
                print("✅ Authentication successful!")
                self.authenticated = True
                self.master_key = auth
                self.vault = KeyStore(self.master_key)
                
        elif command.startswith("register "):
            _, new_key = command.split(" ", 1)
            if new_key is None:
                print("🔐 Usage: register <masterkey>")
            elif register_master_key(new_key):
                print("✅ Registration successful!")
                self.master_key = new_key
        # elif command.startswith("encrypt_save "):
        #     _, msg = command.split(" ", 1)
        #     encrypted = encrypt_aes_cbc(msg, key_string=self.master_key)
        #     try:
        #         with open("sd/messages.txt", "a") as f:
        #             f.write(encrypted + "\n")
        #         print("💾 Encrypted message saved to /messages.txt")
        #     except Exception as e:
        #         print("❌ Failed to save:", e)
        elif command.lower() == "show_messages":
            try:
                with open("sd/messages.txt", "r") as f:
                    lines = f.readlines()
                print("📝 Encrypted Messages:")
                for line in lines:
                    print("-", line.strip())
            except Exception:
                print("📂 No messages saved yet.")
        elif command.startswith("get "):
            if not self.authenticated:
                print("🔒 Auth required before sending credentials.")
                return
            _, domain = command.split(" ", 1)
            creds = self.vault.get(domain)
            print(f"🔑 Credentials for {domain}: {creds}")
            if creds:
                time.sleep(1)
                self.hid.type_text(creds["username"])
                self.hid.key_strokes("TAB")
                self.hid.type_text(creds["password"])
                self.hid.key_strokes("ENTER")
        elif command.lower() == "hello":
            self.hid.type_text("Hello people!!!", delay=0.2)
        elif command.lower() == "greet":
            self.hid.type_text("Hi there! How can I help?")
        elif command.lower() == "bye":
            self.hid.type_text("Goodbye!")
        elif command.lower() == "help":
            self.hid.type_text("Available: hello, greet, bye, encrypt <msg>, decrypt <base64>")
        else:
            print(f"Unknown command: '{command}'")
