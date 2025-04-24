# Product-Footprint-Calculator-Add-On

## Work in progress :

### If you want to test the scrapper localy : 

- clone the repo
- Install Poetry (if not already installed):
- run poetry init at the root of the project
- run poetry install : install the dependencies listed in pyproject.toml (including Playwright): 
- poetry run playwright install (not automatized yet) : Playwright needs to download the necessary browser binaries for automation.
- and run EPREL_com.py
    - if you are at the root level : poetry run python src/EPREL_scrapper/scrapper_playwright/EPREL_com.py