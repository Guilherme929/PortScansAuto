import time
import os
import socket
from colorama import init, Fore, Style
import threading
import requests

init()

def verificar_url(url):
    try:
        code = requests.get(url)
        if code.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def verificar_porta(IP, PORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1)
        code = client.connect_ex((IP, PORT))
        if code == 0:
            print(f'{Fore.GREEN}Porta {PORT} aberta!{Style.RESET_ALL}')
        client.close()
    except:
        pass

def conect(IP, start_port=1, end_port=65535, thread_count=100):
    portas = range(start_port, end_port + 1)
    threads = []

    for PORT in portas:
        thread = threading.Thread(target=verificar_porta, args=(IP, PORT))
        threads.append(thread)
        thread.start()

        if len(threads) >= thread_count:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

def main(url, start_port, end_port):
    if verificar_url(url):
        host = url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        conect(host, start_port, end_port)
    else:
        print("URL inválido")

def sair():
    for sair in range(3, 0, -1):
        print(f'{sair}')
        time.sleep(1)
    os.system('clear')

def help():
    print("""
- [01] Essa opção irá scanear portas enviando pacotes "TCP", as portas que retornarem resposta serão printadas na tela.
- [00] Essa opção sairá do programa.
""")

if __name__ == '__main__':
    os.system('clear')
    print(f'''
        {Fore.GREEN}
        {Fore.CYAN} +--^----------,--------,-----,--------^-,
        |  {Fore.RED}|||||||||   --------      |         O
        {Fore.CYAN} +---------------------------^----------|
        {Fore.CYAN} \_,---------,---------,--------------'
        / {Fore.RED}XXXXXX{Fore.CYAN} /'|       / /'    
        / {Fore.RED}XXXXXX{Fore.CYAN} /   \ ___/ /'
        / {Fore.RED}XXXXXX{Fore.CYAN} / _______ /                
        / {Fore.RED}XXXXXX{Fore.CYAN} /
        / {Fore.RED}XXXXXX{Fore.CYAN} /
        (________( {Fore.MAGENTA}https://github.com/Guilherme929/Port_scans_auto.git{Fore.CYAN}
        ____________________________
        |                          |
        |[01] - Scanear            |
        |[00] - Exit               |
        |                          |
        | -help                    |
        |__________________________|
    ''')

    while True:
        try:
            escolha = input('\nEscolha uma opção: ')

            if escolha in ('Scanear', '1', 'scanear'):
                url = input('Digite o URL-alvo: ')
                start_port = int(input('Digite a porta inicial: '))
                end_port = int(input('Digite a porta final: '))
                start_time = time.time()
                main(url, start_port, end_port)
                end_time = time.time()
                print(f'\nVarredura concluída em {end_time - start_time:.2f} segundos.')
            elif escolha in ('Exit', 'exit', '0'):
                sair()
                break
            elif escolha in ('-help', '-h', 'h'):
                help()
            else:
                print('Opção inválida!')
        except (KeyboardInterrupt, ValueError, EOFError, KeyError, ChildProcessError) as error:
            print(f'\n\nTente novamente! {error}')
            continue
