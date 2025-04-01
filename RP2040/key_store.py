import json
import os
from aes_encryptor import decrypt_aes_cbc, encrypt_aes_cbc

KEYS_FILE = "sd/keys.db"

class KeyStore:
    def __init__(self, master_key):
        self.master_key = master_key  # raw string (authenticated)
        self.db = self._load_db()

    def _load_db(self):
        # if KEYS_FILE not in os.listdir("/"):
        #     return {}

        try:
            with open(KEYS_FILE, "r") as f:
                encrypted = f.read().strip()
                decrypted = decrypt_aes_cbc(encrypted, self.master_key)
                return json.loads(decrypted)
        except Exception as e:
            print("⚠️ Failed to load key store:", e)
            return {}

    def get(self, site):
        return self.db.get(site)

    def add(self, site, username, password):
        self.db[site] = {"username": username, "password": password}
        self._save()

    def _save(self):
        try:
            plaintext = json.dumps(self.db)
            encrypted = encrypt_aes_cbc(plaintext, self.master_key)
            with open(KEYS_FILE, "w") as f:
                f.write(encrypted)
            print("💾 Vault saved successfully.")
        except Exception as e:
            print("❌ Failed to save vault:", e)
