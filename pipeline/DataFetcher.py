'''
At last, we have options data. 

This probably will need to be modified as time goes on, and you guys will not be 
able to run it as you dont have a wrds account. This is just here for interest of 
anyone/ because it may help in building your functions for mapping to scalars.  
'''

import pandas as pd
import yfinance as yf
import wrds

class DataFetcher:
    '''
    Class to populate the folder datasets with a variety of order books, 
    with the name of each file being the ratio of the change of 1yr after.
    '''

    def __init__(
            self,
            ticker_universe:list[str]
    ):
        self.tickers = ticker_universe
        self.dates = ['2023-01-01', '2022-01-01', '2021-01-01', '2020-01-01', '2019-01-01', '2018-01-01']

    def _translate_tickers(self, connection) -> list[int]:
        '''
        On this api, querys are only done via sec id. This function will take in tickers and 
        change them to these sec IDs for you. save them as a variable in self when this is 
        called in main.
        ''' 

        query = f"""
        SELECT DISTINCT op.secid, crsp.permno
        FROM wrdsapps_link_crsp_optionm.opcrsphist op
        JOIN crsp.stocknames crsp ON op.permno = crsp.permno
        WHERE crsp.ticker IN {self.tickers}
        """

        data = connection.raw_sql(query)
        return data['secid'].tolist()


    def _single_call(self, ratio, spot, sec_id:int, date:str, connection)-> pd.DataFrame:
        '''
        this is the function that will give us a single order book snapshot for a given stock
        
        output will be saved as a csv file which is in data/v{price_ratio}
        '''
        year = date[0:4]
        # another sql query
        query = f"""
        (
            SELECT *
            FROM optionm.opprcd{year}
            WHERE secid = {sec_id} AND cp_flag = 'C'
            LIMIT 5000
        )
        UNION ALL
        (
            SELECT *
            FROM optionm.opprcd{year}
            WHERE secid = {sec_id} AND cp_flag = 'P'
            LIMIT 5000
        )
        """

        df = connection.raw_sql(query)
        # data has some strange rescaling
        df['strike_price'] = df['strike_price']/1000
        df['date'] = pd.to_datetime(df['date'])
        df['exdate'] = pd.to_datetime(df['exdate'])

        # Compute the difference in days and store in a new column 'dte'
        df['dte'] = (df['exdate'] - df['date']).dt.days
        df['ratio'] = (df['strike_price'] / spot).apply(lambda x: float(f"{x:.5g}"))

        trimmed_df = df[['secid', 'cp_flag', 'ratio', 'best_bid', 'dte']]
        trimmed_df.columns = ['sec_id', 'call_or_put', 'ratio', 'lastPrice', 'dte']
        trimmed_df.to_csv(f'datasets/v{ratio:.5g}.csv', index=False)



    def _labeller(self, ticker:int, date:str)->float:
        '''here we will pull data from yfinance to get the fractional change in price one year
        on from the latest day of option trading. '''
        ticker_symbol = ticker
        date_of_interest = date
        ticker = yf.Ticker(ticker_symbol)

        start_date = pd.to_datetime(date_of_interest)
        end_date = start_date + pd.Timedelta(days=5) # give a 5 day window to dodge any weekends 
        
        data_1 = ticker.history(start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
        data_2 = ticker.history(start=(start_date+pd.DateOffset(years=1)).strftime("%Y-%m-%d"), end=(end_date+pd.DateOffset(years=1)).strftime("%Y-%m-%d"))

        try:
            start_price = data_1['Close'].iloc[0]
            end_price = data_2['Close'].iloc[0]
            return end_price / start_price, start_price 
        except Exception as e:
            print(e)
            return None

    def main(self):
        '''main function for entry to script.
        
        logical flow idea for now: 
        open connection
        define collection of times to pull data from 
        for each, make a dataframe with columns: ticker, secid, date, option_score, fractional_change_in1yr
        save this to current directory
        '''
    
        db = wrds.Connection()
        self.sec_ids = self._translate_tickers(db)
        
        for date in self.dates:
            for ticker, secid in zip(self.tickers, self.sec_ids):
                ratio, spot = self._labeller(ticker, date)
                # now call the data and fill the table
                self._single_call(ratio, spot, secid, date, db)


fetcher = DataFetcher(ticker_universe=('TSLA', 'NVDA'))
fetcher.main()