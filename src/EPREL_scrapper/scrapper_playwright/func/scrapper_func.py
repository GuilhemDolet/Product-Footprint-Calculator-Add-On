from playwright.sync_api import sync_playwright
import re
import random
import time
import requests

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

    while next_page_button.is_visible():
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
                get_european_energy_label(page)
                time.sleep(delay)
                get_product_sheet(page)
                time.sleep(delay)
                page.go_back(timeout=10000)
                time.sleep(delay)
            else:
                print(f"Le bouton {i + 1} est invisible ou non interactif, saut du clic.")

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

    # URL de base du site
    base_url = "https://eprel.ec.europa.eu"

    # Récupérer l'URL de l'image depuis la balise <img>
    img_src = page.get_attribute("img[alt='Label']", "src")
    # Récupérer le Label_XXXXXXX de l'image pour le passer en nom du fichier à stocker et pour garder son ID
    label_id_eprel = regex_for_id(img_src, "Label")

    if img_src:
        img_url = f"{base_url}{img_src}"  # Construire l'URL complète
        # Télécharger l'image
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            file_path = f"src/EPREL_scrapper/data/european_energy_label/{label_id_eprel}.svg"
            with open(file_path, "wb") as f: #image récupérée en vectoriel .svg 
                f.write(img_response.content)
            print("Image téléchargée avec succès")
        else:
            print("Erreur lors du téléchargement de l'image :", img_response.status_code)
    else:
        print("Impossible de récupérer l'URL de l'image.")
 
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