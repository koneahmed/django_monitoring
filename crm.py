import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration
crm_url = "http://gsecrmc1dev/HTDEV2016/api/data/v8.2/"
username = "adminsaphirv3"
password = "Operating0"
solution_id = "78eb28df-86eb-ee11-80e1-0050568e67ef"  # Remplacez par l'ID de votre solution

def get_solution_content(solution_id):
    # Endpoint pour récupérer le contenu de la solution
    endpoint = f"{crm_url}solutions({solution_id})"
    
    # En-têtes de la requête
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }
    
    # Faire la requête GET
    response = requests.get(endpoint, headers=headers, auth=HTTPBasicAuth(username, password))
    
    # Vérifier le statut de la réponse
    if response.status_code == 200:
        solution_details = response.json()
        print("Détails de la solution récupérés avec succès.")
        print(json.dumps(solution_details, indent=4))  # Affiche les détails de la solution
    else:
        print(f"Erreur lors de la récupération de la solution: {response.status_code} - {response.text}")

def main():
    get_solution_content(solution_id)

if __name__ == "__main__":
    main()