import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from dotenv import load_dotenv

load_dotenv()

REST_COUNTRIES_API_URL = "https://restcountries.com/v3.1"
MAX_ROWS = 251

def get_paginated_countries(page):
    url = f"{REST_COUNTRIES_API_URL}/all?per_page={MAX_ROWS}&page={page}"
    response = requests.get(url)
    return response.json()

def save_as_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)

def save_as_parquet(data, filename):
    df = pd.DataFrame(data)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, filename)

def save_as_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    countries = []
    page = 1

    while len(countries) < MAX_ROWS:
        page_countries = get_paginated_countries(page)
        countries += page_countries
        page += 1

    # Salvar cada página em um arquivo diferente
    for i, page_countries in enumerate([countries[i:i+MAX_ROWS] for i in range(0, len(countries), MAX_ROWS)]):
        save_as_json(page_countries, f"countries_page_{i+1}.json")
        save_as_parquet(page_countries, f"countries_page_{i+1}.parquet")
        save_as_csv(page_countries, f"countries_page_{i+1}.csv")
