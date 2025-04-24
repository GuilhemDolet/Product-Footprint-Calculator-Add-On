import requests
import os
import json
from time import sleep

# Ma liste d'id produit à récupérer dynamiquement depuis le scrapping 
product_ids = []
base_url = "https://eprel.ec.europa.eu/api/products/waterheaters/"

# Dossier de destination (pour l'instant en local mais futur DL)
output_folder = "src/api_client/data/raw"
# os.makedirs(output_folder, exist_ok=True)

with open("src/EPREL_scrapper/data/urls.json", "r") as f:
    urls = json.load(f)

for url in urls : 
    product_id = url[-7:]
    builded_url = f"{base_url}{product_id}"

    try:

        response = requests.get(builded_url)
        print("ok")
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
