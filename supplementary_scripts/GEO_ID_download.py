import requests
from bs4 import BeautifulSoup

def fetch_geo_accession_ids(query):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "gds",
        "term": query,
        "retmode": "xml",
        "retmax": 20000     # sets maximum amount of results to be returned
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "xml")
    ids = [id_tag.text for id_tag in soup.find_all("Id")]
    
    # Convert IDs to the correct GEO accession format
    geo_accession_ids = []
    for id in ids:
        if id.startswith('200'):
            geo_accession_ids.append(f'GSE{id[3:]}')  # Convert 200XXXXX to GSEXXXXX
        elif id.startswith('30'):
            geo_accession_ids.append(f'GSM{id[2:]}')  # Convert 30XXXXXXX to GSMXXXXXXX
        else:
            geo_accession_ids.append(id)  # Keep any other IDs as they are
    
    return geo_accession_ids

def save_accession_ids(ids, filename):
    with open(filename, "w") as file:
        for geo_id in ids:
            file.write(f"'{geo_id}',")  

if __name__ == "__main__":
    query = '(((organoid[Description]) AND Homo sapiens[Organism]) AND ("2019"[Publication Date] : "3000"[Publication Date])) NOT cancer'
    geo_ids = fetch_geo_accession_ids(query)
    save_accession_ids(geo_ids, "geo_ids.txt")
    print(f"Saved {len(geo_ids)} GEO accession IDs to geo_ids.txt")
