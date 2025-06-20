import os
import shutil
import subprocess

def kill_discord_processes():

    processes = [
        "Discord.exe",
        "DiscordCanary.exe",
        "DiscordPTB.exe",
        "DiscordDevelopment.exe"
    ]
    for proc in processes:
       
        subprocess.run(f'taskkill /F /IM {proc}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def disconnect_all_discords():
    
    kill_discord_processes()

    base_paths = [
        r'%APPDATA%\Discord',
        r'%APPDATA%\discordcanary',
        r'%APPDATA%\discordptb',
        r'%APPDATA%\discorddevelopment'
    ]

    for path in base_paths:
        full_path = os.path.expandvars(path)
        if os.path.exists(full_path):
            try:
                shutil.rmtree(full_path)
                print(f"Deleted {full_path}")
            except Exception as e:
                print(f"Failed to delete {full_path}: {e}")

if __name__ == "__main__":
    disconnect_all_discords()
