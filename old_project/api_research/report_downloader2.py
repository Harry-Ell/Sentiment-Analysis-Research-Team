'''
this should be a cleaner way to get the company reports rather than opening a pdf as a .txt 
file which the old approach was basically doing. 


This will save nicer versions of the company reports to the data folder. 
'''


import os
import requests
from bs4 import BeautifulSoup

def extract_filings_text(cik, TICKER, MAX_FILES,  filing_types=["10-K", "10-Q"], output_dir="data"): 
    # SEC API URL
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    headers = {"User-Agent": "avanti.westcoast@fake.co.uk"}
    

    response = requests.get(url, headers=headers)
    data = response.json()
    
    # from this we can pull recent filings (quaterly and annually) 
    recent_filings = data.get("filings", {}).get("recent", {})
    accession_numbers = recent_filings.get("accessionNumber", [])
    filing_types_list = recent_filings.get("form", [])
    filing_urls = recent_filings.get("primaryDocument", [])
    
    # more file path wizardry
    os.makedirs(output_dir, exist_ok=True)
    successes = 0
    # Process filings
    for i, form_type in enumerate(filing_types_list):
        if successes >= MAX_FILES:
            print('Fetch complete')
            return None
        elif form_type in filing_types:
                successes += 1 
                # Construct the filing URL
                filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_numbers[i].replace('-', '')}/{filing_urls[i]}"
                
                # fetch html version of the doc 
                filing_response = requests.get(filing_url, headers=headers)
                soup = BeautifulSoup(filing_response.text, "html.parser")
                text_content = []
                
                # Extract all text from section header areas, this may leave out some useful bits though, not tested throughly 
                for tag in soup.find_all(["p", "div", "h1", "h2", "h3", "h4"]):
                    text = tag.get_text(strip=True)
                    if text:  
                        text_content.append(text)
                
                # Clean and save 
                clean_text = "\n".join(text_content)
                output_file = os.path.join(output_dir, f"{TICKER}/{form_type}_{accession_numbers[i].replace('/', '-')}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(clean_text)
                
                print(f"Saved: {output_file}")

# a downside is you have to find the cik number for the company. lifes a bitch
if __name__ == "__main__":
    cik = "0000320193"  # Apple Inc.'s CIK
    extract_filings_text(cik, 'AAPL', 5)
