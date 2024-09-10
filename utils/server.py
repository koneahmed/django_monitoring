# serveur_module.py

import platform
import subprocess

def ping(host):
    """Vérifie la disponibilité d'un hôte en utilisant la commande ping."""
    # Détermine la commande ping en fonction du système d'exploitation
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    try:
        # Exécute la commande ping et vérifie si l'hôte répond
        output = subprocess.check_output(['ping', param, '1', host], stderr=subprocess.STDOUT, universal_newlines=True)
        return "disponible" in output.lower()
    except subprocess.CalledProcessError:
        return False
    

def check_server(hostname, ip):
    if hostname and ping(hostname):
        print(f"Serveur {hostname} est disponible.")
        return True
    elif ip and ping(ip):
        print(f"Serveur {ip} est disponible.")
        return True
    else:
        print("Aucun des hôtes n'est disponible.")
        return False
    

def check_servers(environnements):
    for env_name, details in environnements.items():
        hostname = details.get('hostname')
        ip = details.get('IP')
        domain = details.get('Domain')

        print(f"\nVérification pour {env_name}:")
        
        if hostname and ping(hostname):
            print(f"Serveur {hostname} est disponible.")
        elif ip and ping(ip):
            print(f"Serveur {ip} est disponible.")
        elif domain and ping(domain):
            print(f"Serveur {domain} est disponible.")
        else:
            print("Aucun des hôtes n'est disponible.")
