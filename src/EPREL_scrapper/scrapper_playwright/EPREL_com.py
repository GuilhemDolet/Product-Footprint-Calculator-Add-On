from playwright.sync_api import sync_playwright
from EPREL_scrapper.scrapper_playwright.func.scrapper_func import parsing_waterheating_pages, intercept_request, testing_parsing, save_url_list

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
    # informations_buttons = page.locator("//eui-block-content/div/app-search-result-item/article/div[1]/div/div/div[3]/div/button")
    
    testing_parsing("//eui-block-content/div/app-search-result-item/article/div[1]/div/div/div[3]/div/button", page, list_url_to_grab)

    browser.close()

# print("URLs collectées :", list_url_to_grab, len(list_url_to_grab))
save_url_list(list_url_to_grab)