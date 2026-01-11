from playwright.sync_api import sync_playwright
from EPREL_scrapper.scrapper_playwright.func.scrapper_func import parsing_waterheating_pages, intercept_request, testing_parsing, save_url_list
import time

list_url_to_grab = []

with sync_playwright() as p:
    headless_option = False # headless=True pour mode caché
    browser = p.chromium.launch(headless=headless_option)
    print(f"Mode headless : {headless_option}") 
    
    # À chaque requête envoyée par la page, exécute la fonction intercept_request en lui passant automatiquement l'objet request."
    # On veut que la fonction get_url soit executé uniquement quand une requête est interceptée, en mode "automatique" ou événementiel
    # C'est playwright qui appelle la fonction lui même c'est pour ça qu'on écrit pas en dur get_url_by_request_to_api(request).
    page = browser.new_page()

    page.on("request", lambda request: intercept_request(request, list_url_to_grab))
    page.goto("https://eprel.ec.europa.eu/screen/product/waterheaters")
    # Gestion des cookies
    try:
        page.locator("text=Accept all cookies").click(timeout=15000)
    except:
        pass
    
    # FILTRAGE PAR CHAMP DE SAISIE 
    # Attendre que le champ se charge
    min_energy_input = page.locator("//input[@aria-label='waterHeatingAnnualEnergyGJMin']").nth(1)  # ou .second
    min_energy_input.wait_for(state="visible", timeout=10000)
    print("Champ de saisie trouvé")
    print(f"Valeur initiale : {min_energy_input.input_value()}")

    # Remplir le champ avec 8
    min_energy_input.clear()
    min_energy_input.fill("8")
    min_energy_input.press("Enter")
    print("Valeur définie à 8")

    time.sleep(2)
    # Attendre que les résultats se mettent à jour
    page.wait_for_load_state("load")
    time.sleep(2)
    print(f"Valeur après modification : {min_energy_input.input_value()}")
    

    parsing_waterheating_pages("//eui-card-header-right-content[@class='ecl-u-d-none ecl-u-d-m-block eui-card-header__right-content']/button[@class='ecl-button ecl-button--primary']", page, list_url_to_grab)

    browser.close()

save_url_list(list_url_to_grab)