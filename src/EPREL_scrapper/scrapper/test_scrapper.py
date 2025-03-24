import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from EPREL_scrapper.scrapper.base_scrapper import BaseScrapper
from EPREL_scrapper.scrapper.water_heater_scrapper import WaterHeaterScraper

scraper = WaterHeaterScraper(headless=False, web_driver="firefox")
scraper.open_page("https://eprel.ec.europa.eu/screen/home")
#Libérer la popup des cookies si elle s'affiche
scraper.accept_cookies()
# Il faut cliquer sur le bouton
scraper.go_to_water_heater_section("//eui-card[contains(@class, 'eui-card')][.//eui-card-header-title[contains(text(), 'Chauffe-eau')]]")
