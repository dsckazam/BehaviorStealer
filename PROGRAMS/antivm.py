import uuid
from tkinter import messagebox
import os
import socket
import subprocess
import psutil

blacklisted_users = [
    'wdagutilityaccount', 'abby', 'hmarc', 'patex', 'rdhj0cnfevzx', 'keecfmwgj', 'frank',
    '8nl0colnq5bq', 'lisa', 'john', 'george', 'pxmduopvyx', '8vizsm', 'w0fjuovmccp5a',
    'lmvwjj9b', 'pqonjhvwexss', '3u2v9m8', 'julia', 'heuerzl', 'fred', 'server',
    'bvjchrpnsxn', 'harry johnson', 'sqgfof3g', 'lucas', 'mike', 'patex', 'h7dk1xpr',
    'louise', 'user01', 'test', 'rgzcbuyrznreg', 'bruno', 'administrator',
    'sandbox', 'user', 'sysadmin', 'malware', 'analyst', 'debug'
]

blacklisted_pc_names = [
    'bee7370c-8c0c-4', 'desktop-nakffmt', 'win-5e07cos9alr', 'b30f0242-1c6a-4',
    'desktop-vrsqlag', 'q9iatrkprh', 'xc64zb', 'desktop-d019gdm', 'desktop-wi8clet',
    'server1', 'lisa-pc', 'john-pc', 'desktop-b0t93d6', 'desktop-1pykp29',
    'desktop-1y2433r', 'wileypc', 'work', '6c4e733f-c2d9-4', 'ralphs-pc',
    'desktop-wg3myjs', 'desktop-7xc6gez', 'desktop-5ov9s0o', 'qarzhrdbpj',
    'oreleepc', 'archibaldpc', 'julia-pc', 'd1bnjkfvlh', 'nettypc', 'desktop-bugio',
    'desktop-cbgpfee', 'server-pc', 'tiqiyla9tw5m', 'desktop-kalvino', 'compname_4047',
    'desktop-19olltd', 'desktop-de369se', 'ea8c2e2a-d017-4', 'aidanpc', 'lucas-pc',
    'marci-pc', 'acepc', 'mike-pc', 'desktop-iapkn1p', 'desktop-ntu7vuo', 'louise-pc',
    't00917', 'test42', 'desktop-et51ajo', 'desktop-test', 'sandbox', 'winvm'
]

blacklisted_uuids = [
    '00000000-0000-0000-0000-000000000000', '11111111-2222-3333-4444-555555555555',
    '03000200-0400-0500-0006-000700080009', '6F3CA5EC-BEC9-4A4D-8274-11168F640058',
    'ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548', '4C4C4544-0050-3710-8058-CAC04F59344A',
    '49434D53-0200-9036-2500-36902500F022', '777D84B3-88D1-451C-93E4-D235177420A7',
    '49434D53-0200-9036-2500-369025000C65', '00000000-0000-0000-0000-AC1F6BD048FE',
    '49434D53-0200-9036-2500-369025003AF0', '8B4E8278-525C-7343-B825-280AEBCD3BCB',
    'FF577B79-782E-0A4D-8568-B35A9B7EB76B', '08C1E400-3C56-11EA-8000-3CECEF43FEDE',
    '00000000-0000-0000-0000-50E5493391EF', 'BB64E044-87BA-C847-BC0A-C797D1A16A50',
    '3F284CA4-8BDF-489B-A273-41B44D668F6D', 'A15A930C-8251-9645-AF63-E45AD728C20C',
    '67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3', 'C7D23342-A5D4-68A1-59AC-CF40F735B363'
]

blacklisted_processes = [
    'vmtoolsd.exe', 'vmwaretray.exe', 'vmwareuser.exe', 'vboxservice.exe', 'vboxtray.exe',
    'xenservice.exe', 'qemu-ga.exe', 'wireshark.exe', 'processhacker.exe', 'procexp.exe',
    'ida.exe', 'ollydbg.exe', 'x64dbg.exe', 'fiddler.exe', 'tcpview.exe', 'vmacthlp.exe'
]

blacklisted_services = [
    'vmmouse', 'vmhgfs', 'vboxguest', 'vboxmouse', 'vboxservice', 'vboxvideo',
    'vmvss', 'vmx86', 'vmware', 'vmsrvc', 'xenevtchn'
]

def check_blacklisted():
    username = os.getlogin().lower()
    hostname = socket.gethostname().lower()
    pc_uuid = str(uuid.UUID(int=uuid.getnode())).upper()

    if username in blacklisted_users:
        return True
    if hostname in blacklisted_pc_names:
        return True
    if pc_uuid in blacklisted_uuids:
        return True

    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in blacklisted_processes:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    services = subprocess.getoutput("sc query type= service state= all")
    for bad_service in blacklisted_services:
        if bad_service.lower() in services.lower():
            return True

    return False

if check_blacklisted():
    messagebox.showerror("Error", "Virtual Machine or Sandbox detected.")
    exit()
