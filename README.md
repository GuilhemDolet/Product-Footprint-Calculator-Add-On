# Product-Footprint-Calculator-Add-On

## Work in progress :

### If you want to test the scrapper localy : 

### 1/ SCRAPPING :
- clone the repo
- Install Poetry (if not already installed):
- run poetry init at the root of the project
- run poetry install : install the dependencies listed in pyproject.toml (including Playwright): 
- poetry run playwright install (not automatized yet) : Playwright needs to download the necessary browser binaries for automation.
- and run EPREL_com.py
    - if you are at the root level : poetry run python src/EPREL_scrapper/scrapper_playwright/EPREL_com.py

### 2/ CALL API
- after that you can run call_api_eprel.py
- data will be collected into the file api_client/data/raw

### 3/ Flaten operation
- in order to load json informations into a SQL database (through a datalake before), you can create a NDJSON file, with one line for one JSON.
- it helps a little bit to clean  the raw data too
- run the build_ndjson.py script



## Architecture 
```bash
Product-Footprint-Calculator-Add-On/
├── poetry.lock
├── pyproject.toml
├── README.md
├── test.py
├── infrastructure/
├── src/
│   ├── api_client/
│   │   ├── build_ndjson.py
│   │   ├── call_api_eprel.py
│   │   ├── test_api.py
│   │   ├── data/
│   │   │   ├── bronze/
│   │   │   │   └── eprel_waterheaters.ndjson
│   │   │   ├── raw/
│   │   │   ├── european_energy_label/
│   │   │   └── product_sheet_document/
│   │   └── func/
│   │       ├── flatten_json.py
│   │ 
│   ├── EPREL_scrapper/
│   │   ├── data/
│   │   │   ├── urls.json
│   │   │   ├── european_energy_label/
│   │   │   └── product_sheet_document/
|   │   ├── scrapper_playwright/
|   │   │   ├── EPREL_com.py
|   │   │   ├── test_scrapper.py
|   │   │   └── func/
│   └── utils/

```
