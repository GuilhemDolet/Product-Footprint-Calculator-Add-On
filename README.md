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
<pre lang="markdown"> ```mermaid graph TD root[Product-Footprint-Calculator-Add-On/] root --> poetry[poetry.lock] root --> pyproject[pyproject.toml] root --> readme[README.md] root --> test[test.py] root --> infrastructure[infrastructure/] root --> src[src/] src --> api_client[api_client/] src --> eprel_scrapper[EPREL_scrapper/] src --> utils[utils/] api_client --> build[build_ndjson.py] api_client --> call[call_api_eprel.py] api_client --> testapi[test_api.py] api_client --> func1[func/] api_client --> data1[data/] func1 --> flatten[flatten_json.py] data1 --> bronze[bronze/] data1 --> raw[raw/] data1 --> label1[european_energy_label/] data1 --> sheet1[product_sheet_document/] bronze --> eprel[eprel_waterheaters.ndjson] eprel_scrapper --> data2[data/] eprel_scrapper --> scrapper[scrapper_playwright/] data2 --> urls[urls.json] data2 --> label2[european_energy_label/] data2 --> sheet2[product_sheet_document/] scrapper --> com[EPREL_com.py] scrapper --> testscrap[test_scrapper.py] scrapper --> func2[func/] ``` </pre>