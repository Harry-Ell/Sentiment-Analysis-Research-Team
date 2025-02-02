import os
import requests
from bs4 import BeautifulSoup

def extract_filings_text(cik, TICKER, MAX_FILES, filing_types=["10-K", "10-Q"], output_dir="data"): 
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
    ticker_dir = os.path.join(output_dir, TICKER)
    os.makedirs(ticker_dir, exist_ok=True)
    
    successes = 0
    first_file_path = None
    # Process filings
    for i, form_type in enumerate(filing_types_list):
        if successes >= MAX_FILES:
            print('Fetch complete')
            return first_file_path
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
                output_file = os.path.join(ticker_dir, f"{form_type}_{accession_numbers[i].replace('/', '-')}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(clean_text)
                
                print(f"Saved: {output_file}")
                
                if first_file_path is None:
                    first_file_path = output_file

    return first_file_path

if __name__ == "__main__":
    cik = "0000320193"  # Apple Inc.'s CIK
    first_file_path = extract_filings_text(cik, 'AAPL', 5)
    print(f"First file path: {first_file_path}")