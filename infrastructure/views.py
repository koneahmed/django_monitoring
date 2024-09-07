from django.shortcuts import render
from .models import Environnement, Serveur, ServeurRole
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
import subprocess
import platform

def home(request):
    environnements = Environnement.objects.all()
    serveurs = Serveur.objects.all()

    # Transformez les objets en dictionnaires ou autres structures appropriées
    # context = {
    #     'environnements': [
    #         {
    #             'id': env.id,
    #             'nom': env.nom,
    #             'departement': env.departement.nom, 
    #             # 'etat': env.etat,
    #             # 'couleur_fond': 'bg-green-100' if env.etat == 'Opérationnel' else 'bg-yellow-100' if env.etat == 'Maintenance' else 'bg-red-100',
    #             # 'couleur_texte': 'text-green-600' if env.etat == 'Opérationnel' else 'text-yellow-600' if env.etat == 'Maintenance' else 'text-red-600',
    #         } for env in environnements
    #     ],
    #     'serveurs': [
    #         {
    #             'id': srv.id,
    #             'hostname': srv.hostname,
    #             'role': srv.hostname,
    #             'etat': check_server(srv.hostname,srv.IP),
    #             "roles":    srv.roles.all(),
    #             "environnement":    srv.environnement,
                
    #             # 'cpu_usage': srv.cpu_usage,
    #             # 'ram_usage': srv.ram_usage,
    #             # 'couleur_icon': 'text-green-600' if srv.etat == 'En ligne' else 'text-yellow-600' if srv.etat == 'Charge élevée' else 'text-red-600',
    #             # 'couleur_texte': 'text-green-600' if srv.etat == 'En ligne' else 'text-yellow-600' if srv.etat == 'Charge élevée' else 'text-red-600',
    #         } for srv in serveurs
    #     ]
    # }
    return render(request, 'home.html',{"environnements":environnements, "serveurs":serveurs})

def environnement_list(request):
    environnements = Environnement.objects.annotate(
        #nombre_serveurs= 0, #Count('serveur'),
        #nombre_services=0 #Count('serveurs__roles')
    )
    return render(request, 'environments/index.html', {'environnements': environnements})

def environnement_details(request, id):
    environnement = get_object_or_404(Environnement, id=id)
    serveurs = environnement.serveurs.all()
    return render(request, 'environments/show.html', {
        'environnement': environnement,
        'serveurs': serveurs
    })

def serveur_details(request, id):
    serveur = get_object_or_404(Serveur, id=id)
    roles = serveur.roles.all()
    # services = serveur.services.all()
    return render(request, 'servers/show.html', {
        'serveur': serveur,
        'roles': roles,
        # "services": services
    })

def ping(host):
    """ Vérifie la disponibilité d'un hôte en utilisant la commande ping. """
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
        etat = True
    elif ip and ping(ip):
        print(f"Serveur {ip} est disponible.")
        etat = True
    else:
        print("Aucun des hôtes n'est disponible.")
        etat = False
    return etat
    
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