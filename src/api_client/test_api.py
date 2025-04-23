import requests
import json

url = "https://eprel.ec.europa.eu/api/products/waterheaters/2199809"

response = requests.get(url)

if response.status_code == 200:
    print("✅ API accessible sans authentification !")
    # print(response.json())
    print(json.dumps(response.json(), indent=2))
    # json.dumps
else:
    print(f"❌ Erreur {response.status_code}")
    print(response.text)  # Voir le détail de l'erreur