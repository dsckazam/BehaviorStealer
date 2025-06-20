import os
import platform
import subprocess
import sys

def kill_all_user_processes():
    system = platform.system()
    if system == "Windows":
        user = os.getlogin()
        subprocess.run(["taskkill", "/F", "/FI", f"USERNAME eq {user}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif system in ("Linux", "Darwin"):
        user = os.getlogin()
        subprocess.run(["pkill", "-u", user, "-9"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        sys.exit(1)

if __name__ == "__main__":
    kill_all_user_processes()
