def flat_my_json(data):
    """
    Transforme une structure JSON imbriquée en un dictionnaire aplati avec des clés spécifiques.

    Cette fonction extrait des informations spécifiques d'une structure JSON potentiellement complexe
    et les organise dans un dictionnaire à plat. Elle gère les cas où certaines clés ou sous-clés
    peuvent être absentes en utilisant des valeurs par défaut.

    Args:
        data (dict): Le dictionnaire JSON d'entrée contenant les données à aplatir.

    Returns:
        dict: Un dictionnaire contenant les données aplaties avec les clés suivantes :
            - eprelRegistrationNumber : Numéro d'enregistrement EPREL.
            - country : Pays (extrait de "contactDetails").
            - city : Ville (extrait de "contactDetails").
            - postalCode : Code postal (extrait de "contactDetails").
            - serviceName : Nom du service (extrait de "contactDetails").
            - webSiteURL : URL du site web (extrait de "contactDetails").
            - email : Adresse email (extrait de "contactDetails").
            - thermostatSettings : Paramètres du thermostat (extrait de "languageSpecifics").
            - energyClass : Classe énergétique.
            - onMarketStartDate : Date de début de mise sur le marché.
            - declaredLoadProfileWaterHeatingAnnualEnergyGJ : Profil de charge déclaré pour le chauffage de l'eau (en GJ).
            - complexType : Type complexe.
            - isDeclaredLoadProfile : Indique si le profil de charge est déclaré (extrait de "loadProfiles").
            - waterHeatingAnnualElectricityCons : Consommation annuelle d'électricité pour le chauffage de l'eau (extrait de "loadProfiles").
            - waterHeatingEfficiency : Efficacité du chauffage de l'eau (extrait de "loadProfiles").
            - type : Type de profil de charge (extrait de "loadProfiles").
            - waterHeatingAnnualEnergyGJ : Énergie annuelle pour le chauffage de l'eau (en GJ, extrait de "loadProfiles").
            - modelIdentifier : Identifiant du modèle.
            - supplierOrTrademark : Fournisseur ou marque déposée.
            - declaredLoadProfileType : Type de profil de charge déclaré.
    """
    return {
        "eprelRegistrationNumber": data.get("eprelRegistrationNumber"),
        "country": data.get("contactDetails", {}).get("country"),
        "city": data.get("contactDetails", {}).get("city"),
        "postalCode": data.get("contactDetails", {}).get("postalCode"),
        "serviceName": data.get("contactDetails", {}).get("serviceName"),
        "webSiteURL": data.get("contactDetails", {}).get("webSiteURL"),
        "email": data.get("contactDetails", {}).get("email"),
        "thermostatSettings": (data.get("languageSpecifics") or [{}])[0].get("thermostatSettings"),
        "energyClass": data.get("energyClass"),
        "onMarketStartDate": data.get("onMarketStartDate"),
        "declaredLoadProfileWaterHeatingAnnualEnergyGJ": data.get("declaredLoadProfileWaterHeatingAnnualEnergyGJ"),
        "complexType": data.get("complexType"),
        "isDeclaredLoadProfile": (data.get("loadProfiles") or [{}])[0].get("isDeclaredLoadProfile"),
        "waterHeatingAnnualElectricityCons": (data.get("loadProfiles") or [{}])[0].get("waterHeatingAnnualElectricityCons"),
        "waterHeatingEfficiency": (data.get("loadProfiles") or [{}])[0].get("waterHeatingEfficiency"),
        "type": (data.get("loadProfiles") or [{}])[0].get("type"),
        "waterHeatingAnnualEnergyGJ": (data.get("loadProfiles") or [{}])[0].get("waterHeatingAnnualEnergyGJ"),
        "modelIdentifier": data.get("modelIdentifier"),
        "supplierOrTrademark": data.get("supplierOrTrademark"),
        "declaredLoadProfileType": data.get("declaredLoadProfileType"),
    }