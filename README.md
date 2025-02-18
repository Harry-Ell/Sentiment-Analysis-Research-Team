# Sentiment-Analysis-Research-Team
Repository for sentiment analysis research project undertaken as part of the Quant team in LUIFS Ghosal Fund. 


# Repository Overview
[change once you have altered this]

## Features
- User API for sentiment analysis based on input Tickers
- Analysis of predictive power of sentiment changes on stock price

## Project Structure

- `datasets`: datasets related to testing of sentiment, in this case is option price data, with the files labelled by the fractional changes in price.  
- `pipeline/DataFetcher.py`: script to populate the data folder with all the relevant options order book snapshots
- `pipeline/mappings.py`: script containing a class which can be imported which has a variety of functions within which are used to map an order book to a scalar. All should follow same structure. 
- `pipeline/populate_fits.py`: class/ function which can loop through the available functions in `mappings`, apply them to every dataset in `dataset` and produce a csv of tuples which is saved in `fitted_function_values`.
- `pipeline/GP_Regressor.py`: function which can fit a gp regressor to any of the datasets we have mapped to in `fitted_function_values`. 

## Limitations

- None of this has actually been done yet 

<!--## License

MIT License-->