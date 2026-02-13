import socket 
from datetime import datetime, timedelta  


def port_scanner(target, ports):
    print("-" * 50)
    print(f"[*] Scanning Target: {target}")
    print (f"[*] scanning started at: {str(datetime.now())}")
    print("-" *50 )

    try:
        for port in ports:
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"[!] Error: {e}")
    except KeyboardInterrupt:
        print("[!] Scan cancelled by user")
     