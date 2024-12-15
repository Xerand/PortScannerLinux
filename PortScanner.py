#!/usr/bin/env python3

import pyfiglet
from rich.progress import Progress
from rich.table import Table
from rich.console import Console
import socket

def scan(target_ip, start_port, end_port, timeout):
    open_ports = []
    closed_ports = []
    
    # Crea un'istanza di Progress
    with Progress() as progress:
        # Crea una barra di progresso con un compito totale di 100
        task1 = progress.add_task("[red][+] Processing...", total=100)
        
        # Itera attraverso ogni porta nella gamma specificata da 'start_port' a 'end_port'
        for port in range(start_port, end_port+1):  
            # Crea un oggetto socket per la comunicazione di rete utilizzando IPv4 e TCP.
            
            # socket.AF_INET: Questo è un attributo che specifica la famiglia di indirizzi IPv4. 
            # In questo caso, AF_INET sta per Address Family IPv4. 
            # Indica che il socket sarà utilizzato per la comunicazione su una rete IPv4.

            # socket.SOCK_STREAM: Questo è un attributo che specifica il tipo di socket, 
            # in questo caso, SOCK_STREAM indica un socket di tipo stream. 
            # I socket di tipo stream sono orientati alla connessione e utilizzano il protocollo TCP. 
            # I socket di tipo stream forniscono una connessione affidabile, orientata al flusso di byte, 
            # che è adatta per le applicazioni in cui è importante che i dati vengano consegnati 
            # nell'ordine corretto e senza perdite
            
            # Quindi, l'istruzione socket.socket(socket.AF_INET, socket.SOCK_STREAM) sta creando 
            # un nuovo oggetto socket che utilizzerà la famiglia di indirizzi IPv4 e il protocollo TCP 
            # per la comunicazione orientata alla connessione. 
            # Questo tipo di socket è adatto per applicazioni in cui è necessario un flusso affidabile 
            # di dati tra il client e il server, come ad esempio nelle comunicazioni web o nelle 
            # connessioni di tipo client-server.
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Imposta un timeout di 1 secondo per la connessione.
            sock.settimeout(timeout)
            
            # Utilizza il metodo 'connect_ex' per tentare la connessione alla porta specificata sul target IP.
            result = sock.connect_ex((target_ip, port))
                        
            # Verifica se il risultato della connessione è 0, che indica una connessione riuscita.
            if result == 0:
                # Se la connessione è riuscita, aggiungi la porta alla lista 'open_ports' altrimenti alla lista 'closed_ports'.
                open_ports.append((port, 0))
            else:
                closed_ports.append((port, result))

            # Chiude il socket dopo il tentativo di connessione.
            sock.close()
            
            # Aggiorna la barra di progresso con un avanzamento incrementale
            progress.update(task1, advance=(100/((end_port+1)-start_port)))
    
    return open_ports + closed_ports


def make_tab(target_ip, ports_results):
    table = Table(title=f"Risultati per la scansione su {target_ip}")
    table.add_column("Porta", style="magenta")
    table.add_column("Stato", style="blue")
    
    for port in ports_results:
        if port[1] == 0:
            res = "open"
        else:
            res = str(port[1])
        table.add_row(str(port[0]), res)
    
    console = Console()
    console.print(table)
    
def main():
    pr = True
    while pr == True:
        target_ip = input("\n[-] Inserisci l'indirizzo IP da testare (x per uscire): ")
        if target_ip == "x":
            pr = False
        else:
            start_port = int(input("[-] Inserisci la porta iniziale del range: "))
            end_port = int(input("[-] Inserisci la porta finale del range: "))
            timeout = int(input("[-] Inserisci timeout: "))

            ports_results = scan(target_ip, start_port, end_port, timeout)

            print()
            make_tab(target_ip, ports_results)

banner = pyfiglet.figlet_format("Python Port Scanner")
print(banner)
print("[i] Tool per lo scan delle reti\n")

main()
