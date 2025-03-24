# La classe de base pour les scrapers.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

class BaseScrapper:
    def __init__(self, headless=True, web_driver="firefox"):
        options = Options() 
        if web_driver == "firefox":
        # configurer le driver firefox. 
            
            if headless:
                options.add_argument("--headless") # mode sans fenêtre 
            # options.add_argument("--width=1920") 
            # options.add_argument("--height=1080")  

            self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
            print(f"Mode headless activé ? {headless}")
        
        if web_driver == "chrome":
        # configurer le driver chrome. 
            options.headless = headless  # Mode sans interface graphique
            # options.add_argument("--window-size=1920,1080")

            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            print(f"Mode headless activé ? {headless}")
            
        
    def random_time(self, min_time=0.5, max_time=3):
        """
        Définit un temps d'attente aléatoire. On l'utilisera entre chaque requête pour ne pas se fair ban
        """
        pause = random.uniform(min_time, max_time)
        time.sleep(pause)
    
    def open_page(self, url):
        """
        Ouvre une page web.
        """
        
        self.driver.get(url)
        self.random_time()
    
    def get_page_source(self):
        """
        Retourne le code source de la page.
        """
        return self.driver.page_source
    
    def close_webdriver(self):
        """
        Ferme le navigateur.
        """
        self.driver.quit()
    
    def click_element(self, xpath):
        """clique sur un élément et ajoute une pause aléatoire"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))).click()
        self.random_time()
    
    def get_element_text(self, xpath):
        """Récupère le texte d'un élément et ajoute une pause aléatoire."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        text = element.text
        self.random_sleep()
        return text

    def accept_cookies(self):
        """Vérifie et clique sur le bouton 'Accepter les cookies' si présent."""    
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'cck-actions-button') and contains(text(), 'Accept all cookies')]"))).click()
            print("cookies acceptés")
        except Exception as e:
            print(f"pas de popup de cookies détectée : {e}")
        self.random_time()
