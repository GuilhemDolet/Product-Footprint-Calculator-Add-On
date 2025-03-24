from EPREL_scrapper.scrapper.base_scrapper import BaseScrapper

class WaterHeaterScraper(BaseScrapper):
    # Quand on instancie WaterHeaterScraper, cela va appeler BaseScraper, qui va créer self.driver.
    def __init__(self, headless=True, web_driver="firefox"):
        super().__init__(headless, web_driver) 
    
    def go_to_water_heater_section(self, xpath):
        self.click_element(xpath)