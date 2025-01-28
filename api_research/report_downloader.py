'''
Short script which will pull the annual or quaterly reports from SEC api. 

Very hacky fix to move the files from their first location to somewehre neater. 
The fucking downloader would not listen to the download path and just dropped 
it where ever it pleased.

Note, when you run this file, it expects your terminal to be in the location 
'Sentiment-Analysis-Research-Team\\api_research'. if its not and your terminal 
is one layer up in the file tree, it wont save in desired location. 

at risk of stating the obvious, just cd api_research
'''

import shutil
import os
from sec_edgar_downloader import Downloader

def main(ticker, filing_type, num_filings_to_download):
    '''
    this should only be three lines long. Almost all of this is just moving stuff across. 
    '''
    dl_path = f"../data/{ticker}"
    dl = Downloader(dl_path, 'fake.email@hotmail.co.uk')  # Specify where to save the reports
    _ = dl.get(filing_type, ticker , include_amends=True, limit = num_filings_to_download)


    # disobedient downloader will not place anything where i tell it to, so this 
    os.makedirs(dl_path, exist_ok=True)
    dl_path = f"../data/{ticker}"
    default_dl_path = os.path.join("sec-edgar-filings", ticker)

    # Move files to the location they were meant to go to in the first place
    if os.path.exists(default_dl_path):
        for filename in os.listdir(default_dl_path):
            shutil.move(os.path.join(default_dl_path, filename), dl_path + '/' + filing_type)

    shutil.rmtree("sec-edgar-filings")

if __name__ == "__main__":
    # Specify for which ticker, for which report type & how many you want 
    ticker = 'AAPL'
    filing_type = "10-K" # 10-K is annual report, 10-Q is quaterly  
    num_filings_to_download = 3
    main(ticker, filing_type, num_filings_to_download)
