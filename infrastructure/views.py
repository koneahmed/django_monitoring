from django.shortcuts import render
from .models import Environnement, Serveur, ServeurRole
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
import subprocess
import platform
import wmi
import pythoncom
# from ..utils import * 

def home(request):
    environnements = Environnement.objects.all()
    serveurs = Serveur.objects.all()
    
    wmi_user = "adminsaphirv3"
    wmi_password = "Operating0"

    # Transformez les objets en dictionnaires ou autres structures appropriées
    context = {
        'environnements': [
            {
                'id': env.id,
                'nom': env.nom,
                'departement': env.departement.nom,
            } for env in environnements
        ],
        'serveurs': [
            {
                'id': srv.id,
                'hostname': srv.hostname,
                'role': srv.hostname,
                'etat': check_server(srv.hostname, srv.IP),
                "roles": srv.roles.all(),
                "environnement": srv.environnement,
                "cpu": check_server_with_stats(srv.hostname, srv.IP, wmi_user, wmi_password).get("cpu"),
                "ram": check_server_with_stats(srv.hostname, srv.IP, wmi_user, wmi_password).get("ram"),
            } for srv in serveurs
        ]
    }
    # return render(request, 'default.html',{"environnements":environnements, "serveurs":serveurs})
    return render(request, 'home.html',context)

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
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        output = subprocess.check_output(['ping', param, '1', host], stderr=subprocess.STDOUT, universal_newlines=True)
        if "unreachable" in output.lower():
            return "Injoignable"
        else:
            return "Disponible"
    except subprocess.CalledProcessError:
        return "Injoignable"
    

def check_server(hostname, ip):
    if ip:
        status = ping(ip)
        print(f"Serveur {ip} est {status}.")
        return status
    elif hostname:
        status = ping(hostname)
        print(f"Serveur {hostname} est {status}.")
        return status
    else:
        print("Aucun des hôtes n'est disponible.")
        return "Injoignable"

    

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


def get_remote_cpu_ram_usage(host, user, password):
    try:
        pythoncom.CoInitialize()
        connection = wmi.WMI(host, user=user, password=password)
        
        processors = connection.Win32_Processor()
        print(f"Processors: {processors}")  # Debug print
        
        if processors:
            cpu_usage = sum(cpu.LoadPercentage for cpu in processors if cpu.LoadPercentage is not None) / len(processors)
        else:
            cpu_usage = None

        memory_info = connection.Win32_OperatingSystem()
        print(f"Memory Info: {memory_info}")  # Debug print
        
        if memory_info:
            memory_info = memory_info[0]
            print (memory_info)
            total_ram = float(memory_info.TotalVisibleMemorySize) if memory_info.TotalVisibleMemorySize is not None else None
            free_ram = float(memory_info.FreePhysicalMemory) if memory_info.FreePhysicalMemory is not None else None
            if total_ram and free_ram is not None:
                used_ram = ((total_ram - free_ram) / total_ram) * 100
            else:
                used_ram = None
        else:
            used_ram = None

        return {
            'cpu': f"{cpu_usage:.2f}" if cpu_usage is not None else None,
            'ram': f"{used_ram:.2f}" if used_ram is not None else None
        }
    except Exception as e:
        print(f"Erreur lors de la connexion à {host}: {e}")
        return {
            'cpu': None,
            'ram': None
        }
    finally:
        pythoncom.CoUninitialize()

        
def check_server_with_stats(hostname, ip, user, password):
    server_status = check_server(hostname, ip)
    
    if server_status == "Disponible":
        stats = get_remote_cpu_ram_usage(hostname, user, password)
        print(f"Serveur {hostname} - CPU: {stats['cpu']}%, RAM: {stats['ram']}%")
        return {
            "status": server_status,
            "cpu": stats['cpu'],
            "ram": stats['ram']
        }
    else:
        return {
            "status": server_status,
            "cpu": None,
            "ram": None
        }