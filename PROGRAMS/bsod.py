import ctypes
import sys

def trigger_bsod():
    
    ntdll = ctypes.WinDLL("ntdll")
    
    
    NtRaiseHardError = ntdll.NtRaiseHardError
    NtRaiseHardError.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong), ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]
    NtRaiseHardError.restype = ctypes.c_ulong

  
    STATUS_SEVERITY_ERROR = 0xC0000000
    STATUS_UNSUCCESSFUL = 0xC0000001

    response = ctypes.c_ulong()
    
    
    NtRaiseHardError(
        STATUS_UNSUCCESSFUL, 
        0, 
        0, 
        None, 
        6,  
        ctypes.byref(response)
    )

if __name__ == "__main__":
    print("")
    try:
        trigger_bsod()
    except Exception as e:
        print(f"")
        sys.exit(1)
