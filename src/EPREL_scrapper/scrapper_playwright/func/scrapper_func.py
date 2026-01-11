from playwright.sync_api import sync_playwright
import re
import os
import random
import time
import requests
import json


def parsing_waterheating_pages(xpath: str, page, list_url_to_grab):
    
    delay = random.uniform(1, 3)  # Entre 1 et 3 secondes
    # compteur de fiche produit disponible
    product_nbr = 0
    # Bouton pour cliquer sur "page suivante"
    next_page_button = page.locator("text=Suivant")
    nombre_de_page = 0

    while next_page_button.is_visible():
    # while nombre_de_page < 5:
        # Bouton pour cliquer sur "plus d'informations"
        # Attendre que les boutons se chargent
        informations_buttons = page.locator(xpath)
        try:
            informations_buttons.first.wait_for(state="visible", timeout=10000)
        except:
            print(f"Aucun bouton trouvé sur la page {nombre_de_page + 1}, arrêt du scrapping.")
            break

        buttons_nbr = informations_buttons.count()
        print(f"{buttons_nbr} bouttons trouvés sur la page {page.url}")

        for i in range(buttons_nbr):
            print(f"je clique sur le bouton {i+1} / {buttons_nbr}")
            if informations_buttons.nth(i).is_visible():
                informations_buttons.nth(i).click(timeout=60000)
                product_nbr += 1
                print(f"{product_nbr} ème produit en cours de parsing - page {nombre_de_page + 1}")
                time.sleep(delay)  # Pause aléatoire entre les clics
                try :
                    get_european_energy_label(page)
                except:
                    pass
                time.sleep(delay)
                try :
                    get_product_sheet(page)
                except :
                    pass
                time.sleep(delay)
                page.go_back(timeout=10000)
                time.sleep(delay)
                
            else:
                print(f"Le bouton {i + 1} est invisible ou non interactif, saut du clic.")

        nombre_de_page += 1
        print(f"page {nombre_de_page} terminée, passage à la page {nombre_de_page + 1}")

        # Clique sur "Suivant" et attendre le chargement
        try:
            next_page_button.click(timeout=10000)
            page.wait_for_load_state("load")
            time.sleep(1) 
        except:
            print("Impossible de cliquer sur 'Suivant', arrêt du scrapping.")
            break

def intercept_request(request, list_url_to_grab):
    
    referer = request.headers.get("referer", "")
    pattern = r"https://eprel\.ec\.europa\.eu/screen/product/waterheaters/\d+$"
    if referer and re.match(pattern, referer):
        if referer in list_url_to_grab:
            return
        else: 
            print(referer)
            list_url_to_grab.append(referer)

def get_european_energy_label(page):
    try:
        # Récupérer tous les éléments avec la classe ecl-link--standalone
        all_buttons = page.locator("a.ecl-link--standalone")
        buttons_count = all_buttons.count()
        
        target_button = None
        # on recherche le bouton avec le texte exact "Télécharger l'étiquette à imprimer"
        for i in range(buttons_count):
            button = all_buttons.nth(i)
            button_text = button.text_content().strip()
            
            # Normaliser l'apostrophe courbe (U+2019) en apostrophe droite (U+0027)
            normalized_text = button_text.replace("\u2019", "'")
            target_text = "Télécharger l'étiquette à imprimer"
            
            if normalized_text == target_text:
                target_button = button
                break
        
        if not target_button:
            print("Aucun bouton téléchargement d'étiquette trouvé")
            return
        
        target_button.wait_for(state="visible", timeout=10000)
        print("Bouton visible, clic en cours...")
        
        # Intercepter la nouvelle page/popup
        with page.context.expect_page() as new_page_info:
            target_button.click()
        
        new_page = new_page_info.value
        new_page.wait_for_load_state("load")
        
        pdf_url = new_page.url
        print(f"URL de l'étiquette : {pdf_url}")
        
        # Télécharger le PDF
        pdf_response = requests.get(pdf_url, timeout=10000)
        if pdf_response.status_code == 200:
            label_id_eprel = regex_for_id(pdf_url, "Label")
            if not label_id_eprel:
                label_id_eprel = "label_" + str(int(time.time()))
            
            # Créer le dossier s'il n'existe pas
            os.makedirs("src/EPREL_scrapper/data/european_energy_label", exist_ok=True)
            
            file_path = f"src/EPREL_scrapper/data/european_energy_label/{label_id_eprel}.pdf"
            try:
                with open(file_path, "xb") as f:  # "xb" échoue si le fichier existe
                    f.write(pdf_response.content)
                print(f"PDF {label_id_eprel} téléchargé")
            except FileExistsError:
                print(f"PDF {label_id_eprel} existe déjà, téléchargement ignoré")
        else:
            print(f"Erreur HTTP {pdf_response.status_code} lors du téléchargement")
        
        new_page.close()
            
    except Exception as e:
        print(f"Error downloading energy label: {e}")
 
def regex_for_id(url, inside_regex):
    """
    Extrait un identifiant au format KEYWORD_DIGITS de l'URL ou du texte donné.
    
    Args:
        url (str): L'URL ou le texte contenant l'ID
        inside_regex (str): Le préfixe à chercher (ex: "Label", "Fiche")
    
    Returns:
        str: L'identifiant trouvé (ex: "Label_69558", "Fiche_12345_EN") ou None
    """
    # Accepte un nombre variable de chiffres (au moins 1)
    pattern = fr'{inside_regex}_\d+'
    match = re.search(pattern, url)

    if match:
        return match.group()
    else:
        return None

def get_product_sheet(page):
    # Plus besoin de cliquer sur l'accordéon avec le nouveau site
    #  page.locator("//span[contains(@class, 'ecl-accordion__toggle-indicator') and  following-sibling::span[contains(text(), 'Fiche d’information sur le produit')]]").click()
    locator = page.locator("//span[contains(text(), 'Autres langues')]")
    locator.wait_for(state="visible")  # Attendre la visibilité
    locator.click()
    with page.expect_popup() as popup_info:
        télécharger_buton = page.locator("(//a[.//span[text()='Télécharger']])[7]")  # Remplace par le bon sélecteur
        télécharger_buton.click()
    time.sleep(2)
    pdf_page = popup_info.value  # Récupère la nouvelle page (liseuse PDF)
    pdf_page.wait_for_load_state("load")
    pdf_url = pdf_page.url
    print(f"URL fiche produit : {pdf_url}")
    product_sheet_id = regex_for_id(url=pdf_url, inside_regex="Fiche")
        # Vérifier que product_sheet_id n'est pas None
    if not product_sheet_id:
        product_sheet_id = "fiche_" + str(int(time.time()))
        print(f"⚠ ID non trouvé, utilisation de l'ID généré : {product_sheet_id}")

    if pdf_url:
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            file_path = f"src/EPREL_scrapper/data/product_sheet_document/{product_sheet_id}.pdf"
            try:
                with open(file_path, "xb") as f:
                    f.write(pdf_response.content)
                print(f"PDF fiche produit {product_sheet_id} a été téléchargé")
            except FileExistsError:
                print(f"PDF fiche produit {product_sheet_id} existe déjà, téléchargement ignoré")
        else:
            print("impossible de télécharger le PDF")
        pdf_page.close()
    else:
        print("pas de lien vers le PDF récupéré")

def save_url_list(list_url_to_grab):

    output_folder = "src/EPREL_scrapper/data"
    output_path = os.path.join(output_folder, "urls.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(list_url_to_grab, f, indent=2)

# uttilisé uniquement pour tester
def testing_parsing(xpath: str, page, list_url_to_grab):
    
    delay = random.uniform(1, 3)  # Entre 1 et 3 secondes
    # compteur de fiche produit disponible
    product_nbr = 0
    # Bouton pour cliquer sur "page suivante"
    next_page_button = page.locator("text=Suivant")

    # while next_page_button.is_visible():
    nombre_de_page = 0
    while nombre_de_page < 3:
         # Bouton pour cliquer sur "formations"
        informations_buttons = page.locator(xpath)
        buttons_nbr = informations_buttons.count()
        # current_url = page.url()
        print(f"{buttons_nbr} bouttons trouvés sur la page {page.url}")

        for i in range(buttons_nbr):
            print(f"je clique sur le bouton {i+1} / {buttons_nbr}")
            if informations_buttons.nth(i).is_visible():
                informations_buttons.nth(i).click(timeout=60000)
                product_nbr += 1
                print(f"Clic effectué sur le bouton {i + 1}")
                print(f"nombre de produit parsés : {product_nbr}")
                # délai aléatoire entre chaque clic
                time.sleep(delay)  # Pause aléatoire entre les clics
                get_european_energy_label(page)
                time.sleep(delay)
                get_product_sheet(page)
                time.sleep(delay)
                page.go_back(timeout=10000)

                # plus besoin de revenir à la page courante avec le code ci-dessous car le site a fixé le problème de perte de position lors du retour arrière
                # if nombre_de_page > 0 :
                #     for nombre in range(nombre_de_page):
                #         next_page_button.click(timeout=10000)
                time.sleep(delay)
                
            else:
                print(f"Le bouton {i + 1} est invisible ou non interactif, saut du clic.")
        nombre_de_page += 1
        for nombre in range(nombre_de_page):
            next_page_button.click(timeout=10000)