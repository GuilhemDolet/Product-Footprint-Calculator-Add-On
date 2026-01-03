from playwright.sync_api import sync_playwright
import re
import os
import random
import time
import requests
import json

def run_playwright_scrapper(main_url):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True pour mode caché
        page = browser.new_page()
        page.goto(main_url)
        return browser, page

def parsing_waterheating_pages(xpath: str, page, list_url_to_grab):
    
    delay = random.uniform(1, 3)  # Entre 1 et 3 secondes
    # compteur de fiche produit disponible
    product_nbr = 0
    # Bouton pour cliquer sur "page suivante"
    next_page_button = page.locator("text=Suivante")

    # while next_page_button.is_visible():
    nombre_de_page = 0
    while nombre_de_page < 5:
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
                print(f"nombre de produit trouvés : {product_nbr}")
                # délai aléatoire entre chaque clic
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
                if nombre_de_page > 0 :
                    for nombre in range(nombre_de_page):
                        next_page_button.click(timeout=10000)
                time.sleep(delay)
                
            else:
                print(f"Le bouton {i + 1} est invisible ou non interactif, saut du clic.")
        nombre_de_page += 1
        for nombre in range(nombre_de_page):
            next_page_button.click(timeout=10000)

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
        
        print(f"Nombre de boutons trouvés : {buttons_count}")
        
        target_button = None
        
        for i in range(buttons_count):
            button = all_buttons.nth(i)
            button_text = button.text_content().strip()
            
            # Normaliser l'apostrophe courbe (U+2019) en apostrophe droite (U+0027)
            normalized_text = button_text.replace("\u2019", "'")
            target_text = "Télécharger l'étiquette à imprimer"
            
            if normalized_text == target_text:
                print(f"✓ Bouton trouvé à l'index {i}")
                target_button = button
                break
        
        if not target_button:
            print("✗ Aucun bouton trouvé")
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
            with open(file_path, "wb") as f:
                f.write(pdf_response.content)
            print(f"Energy label PDF {label_id_eprel} downloaded successfully")
        else:
            print(f"Erreur HTTP {pdf_response.status_code} lors du téléchargement")
        
        new_page.close()
            
    except Exception as e:
        print(f"Error downloading energy label: {e}")
 
def regex_for_id(url, inside_regex):

    pattern = fr'{inside_regex}_\d{{7}}'
    match = re.search(pattern, url)

    if match:
        return match.group()
    else:
        return None


def get_product_sheet(page):
    page.locator("//span[contains(@class, 'ecl-accordion__toggle-indicator') and  following-sibling::span[contains(text(), 'Fiche d’information sur le produit')]]").click()
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
    product_sheet_id = regex_for_id(url=pdf_url, inside_regex="Fiche")

    if pdf_url:
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            file_path = f"src/EPREL_scrapper/data/product_sheet_document/{product_sheet_id}.pdf"
            with open(file_path, "wb") as f:
                f.write(pdf_response.content)
            print(f"PDF {product_sheet_id} a été téléchargé")
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
                # time.sleep(delay)
                # get_product_sheet(page)
                # time.sleep(delay)
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