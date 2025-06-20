import os
import sys
import winreg

path = os.path.abspath(sys.argv[0])
key = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    0, winreg.KEY_SET_VALUE
)
winreg.SetValueEx(key, "StartupEntry", 0, winreg.REG_SZ, path)
winreg.CloseKey(key)
