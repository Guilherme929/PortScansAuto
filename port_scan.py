#!/usr/bin/env python3
import socket
import sys
import threading
import time
import requests


servicos = {
    20: 'ftp-data',
    21: 'ftp',
    22: 'ssh',
    23: 'telnet',
    25: 'smtp',
    53: 'dns',
    67: 'dhcp (servidor)',
    68: 'dhcp (cliente)',
    69: 'tftp',
    80: 'http',
    110: 'pop3',
    113: 'ident',
    119: 'nntp',
    123: 'ntp',
    135: 'msrpc',
    137: 'netbios-ns',
    138: 'netbios-dgm',
    139: 'netbios-ssn',
    143: 'imap',
    161: 'snmp',
    162: 'snmp-trap',
    179: 'bgp',
    389: 'ldap',
    443: 'https',
    445: 'microsoft-ds',
    465: 'smtps',
    514: 'syslog',
    515: 'printer',
    520: 'rip',
    587: 'smtp (submission)',
    631: 'ipp',
    636: 'ldaps',
    873: 'rsync',
    993: 'imaps',
    995: 'pop3s',
    1080: 'socks',
    1194: 'openvpn',
    1433: 'mssql',
    1434: 'mssql-monitor',
    1521: 'oracle',
    1723: 'pptp',
    1812: 'radius',
    1813: 'radius-acct',
    1883: 'mqtt',
    2049: 'nfs',
    2375: 'docker',
    2376: 'docker (ssl)',
    3306: 'mysql',
    3389: 'rdp',
    3690: 'svn',
    4000: 'icq',
    4045: 'nfs-lock',
    4444: 'metasploit',
    4657: 'laborator',
    5000: 'upnp',
    5432: 'postgresql',
    5632: 'pcanywhere',
    5900: 'vnc',
    5984: 'couchdb',
    6379: 'redis',
    6667: 'irc',
    7000: 'afs3-fileserver',
    8080: 'http-proxy',
    8081: 'webcache',
    8443: 'https-alt',
    8888: 'sun-answerbook',
    9050: 'tor',
    9200: 'elasticsearch',
    10000: 'webmin',
    11211: 'memcached',
    27017: 'mongodb',
    49152: 'reserved',
    2008: 'Desconhecido'
}

portas_abertas = []

def connect(ip, port, nome_arq):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1)
        response = client.connect_ex((ip, port))

        if response == 0:
            servico = servicos.get(port, 'desconhecido')
            portas_abertas.append((port, servico))
        
    except socket.timeout:
        pass
    except:
        pass


def worker(ip, port, nome_arq):
    connect(ip, port, nome_arq)

def verificando(ip):
        host = ip
        response = f'http://{host}'
        r = requests.get(response)

        version = r.headers['server']



def scan_agressivo(ip, nome_arq=None):
    print('Começando o scan...')
    threads = []
    for port in servicos:
        t = threading.Thread(target=worker, args=(ip, port, nome_arq))
        t.start()
        threads.append(t)
    
    # Aguardar todas as threads terminarem
    for t in threads:
        t.join()

    verificando(ip)

    host = ip
    response = f'http://{host}'
    r = requests.get(response)

    version = r.headers['server']

    # Ordenar as portas abertas e exibir
    portas_abertas.sort()
    for port, servico in portas_abertas:
        portas = (f'{port:<6} Porta aberta! Serviços: {servico:<10} Version: {version} ')
        print(portas)


        
        if nome_arq:
            with open(nome_arq, 'a') as arq:
                arq.write('{}\n'.format(portas))


def scan_nao_agressivo(ip, nome_arq=None):
    print('Começando o scan...')
    portas = list(servicos.keys())
    mid = len(portas) // 2
    portas1 = portas[:mid]
    portas2 = portas[mid:]

    def scan_portas(portas):
        for port in portas:
            connect(ip, port)

    # Criar e iniciar threads para as duas metades
    thread_1 = threading.Thread(target=scan_portas, args=(portas1,))
    thread_2 = threading.Thread(target=scan_portas, args=(portas2,))

    thread_1.start()
    thread_2.start()

    # Aguardar todas as threads terminarem
    thread_1.join()
    thread_2.join()

    # Ordenar as portas abertas e exibir
    portas_abertas.sort()
    for port, servico in portas_abertas:
        portas = f'{port:<6} Porta aberta! Serviços: {servico}'
        print(portas)
        return portas_abertas
    
    if nome_arq:
        with open(nome_arq, 'a') as arq:
            arq.write('{}\n'.format(portas))
    

def help():
    print('''
Esse PortScan fará uma varredura de porta e também identificará os serviços que estão rodando naquela porta.
Como usar a ferramenta:
    portscan <IP> - Você deve fornecer o IP alvo
    portscan -h ou --help - Exibe esta ajuda
    portscan -e arquivo.txt - Salva as portas e serviços em um arquivo
    portscan -nA - Realiza um scan não agressivo     

Esta ferramentas não pode conter os seguintes parâmetros, exemplo:
          "www", "https://", "http://" ...  
Somente o nome de domínio/ip!

A ferramenta pode não ser tão rapida, então por-favor, PACIÊNCIA!!!
''')

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        help()
        sys.exit(1)
    
    if (sys.argv[1]) in ('-h', '-help', '-H', 'help'):
        help()
        sys.exit()



    if any(proto in sys.argv[1] for proto in ('http://', 'www', 'https://')):
        help()
        sys.exit()
    
    
    ip = sys.argv[1]
    nome_do_arquivo = None



    if len(sys.argv) == 4 and sys.argv[2] in ('-e', '-E'):
        nome_do_arquivo = sys.argv[3]
    
    
    if len(sys.argv) == 2 and sys.argv[1] == '-nA':
        scan_nao_agressivo(ip, nome_do_arquivo)
    else:
        time_1 = time.time()
        scan_agressivo(ip, nome_do_arquivo)
        time_2 = time.time()
        print(f'\nTempo total: {time_2 - time_1:.2f} segundos!')
