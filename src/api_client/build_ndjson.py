from api_client.func.flatten_json import flat_my_json
import os
import json

raw_folder = "src/api_client/data/raw"
output_ndjson_folder = "src/api_client/data/bronze/eprel_waterheaters.ndjson"

fields_to_keep = [
    "eprelRegistrationNumber",
    "country",
    "city",
    "postalCode",
    "serviceName",
    "webSiteURL",
    "email",
    "thermostatSettings",
    "energyClass",
    "onMarketStartDate",
    "declaredLoadProfileWaterHeatingAnnualEnergyGJ",
    "complexType",
    "isDeclaredLoadProfile",
    "waterHeatingAnnualElectricityCons",
    "waterHeatingEfficiency",
    "type",
    "waterHeatingAnnualEnergyGJ",
    "modelIdentifier",
    "supplierOrTrademark",
    "declaredLoadProfileType"
]

os.makedirs(os.path.dirname(output_ndjson_folder), exist_ok=True)

with open(output_ndjson_folder, "w", encoding="utf-8") as ndjson_file:
    for filename in os.listdir(raw_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(raw_folder, filename) # le chemin de mon json source

            with open(file_path, "r", encoding="utf-8") as json_file:
                try:
                    data = json.load(json_file)
                    cleaned_data = flat_my_json(data) # création d'une liste avec les valeurs de la liste fields_to_keep et on va chercher les valeurs correspondantes.
                    json.dump(cleaned_data, ndjson_file)
                    ndjson_file.write("\n")
                except json.JSONDecodeError as json_error:
                    print(f"erreur survenu lors du nettoyage du json : {json_error}")
                