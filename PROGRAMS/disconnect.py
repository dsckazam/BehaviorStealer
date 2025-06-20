import os
import platform
import sys
import subprocess

def disconnect():
    system = platform.system()
    if system == "Windows":
        os.system("shutdown -l")
    elif system == "Linux":
        try:
            subprocess.run(["gnome-session-quit", "--logout", "--no-prompt"])
        except FileNotFoundError:
            os.system("pkill -KILL -u $USER")
    elif system == "Darwin":
        os.system('osascript -e \'tell application "System Events" to log out\'')
    else:
        sys.exit(1)

if __name__ == "__main__":
    disconnect()
