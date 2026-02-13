import socket 
from datetime import datetime


def port_scanner(target, ports):
    print("-" * 50)
    print(f"[*] Scanning Target: {target}")
    print (f"[*] scanning started at: {str(datetime.now())}")
    print("-" *50 )

    try:
        for port in ports:
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            
            result =  s.connect_ex((target, port))
            
            if result == 0:
                print(f"[+] port {port}: OPEN")
                
            s.close()
            
    except KeyboardInterrupt:
        print("\n [-] Exiting Program...")
    except socket.gairror:
        print("\n [-] Hostname Could Not Be Resolved")
    except socket.error:
        print("\n [-] server not responding. ")
        
if __name__ == "__main__":
    target_ip = input("[+] Enter Target IP: ").strip()
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]
    
    port_scanner(target_ip, common_ports)
            

            
            
