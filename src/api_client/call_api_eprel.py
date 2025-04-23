import requests
import os
import json
from time import sleep

# Ma liste d'id produit à récupérer dynamiquement depuis le scrapping 
product_ids = [2199799, 2199809, 2199832]

# Dossier de destination (pour l'instant en local mais futur DL)
output_folder = "src/api_client/data/raw"
# os.makedirs(output_folder, exist_ok=True)

base_url = "https://eprel.ec.europa.eu/api/products/waterheaters/"

for product_id in product_ids : 
    builded_url = f"{base_url}{product_id}"
    print(builded_url)

    try:
        response = requests.get(builded_url)

        if response.status_code == 200 :
            data = response.json()
            output_path = os.path.join(output_folder, f"{product_id}.json")
            print(output_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"json {product_id} enregistré")

        else:
            print(f"bug : {response.status_code}")

        sleep(2)

    except Exception as e:
        print(f"Try to call the api and then: {e}")
