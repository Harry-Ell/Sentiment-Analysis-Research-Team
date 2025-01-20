## Web scraping approach
## A simple toy test to plot sentiment against stock price - can be used to verify correlation after further processing
## Neutrals could be removed?

## Imports
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from pattern.en import sentiment

# Set up the url for the ticker on finviz
finviz_url = 'https://finviz.com/quote.ashx?t='
ticker = 'CBT'
url = finviz_url + ticker

# Build a request object to scrape Finviz
req = Request(url=url, headers={'user-agent' : 'quant'}) # any user agent name
response = urlopen(req)
html = BeautifulSoup(response, 'html')

# A table containing timestamps, titles and links
news_table = html.find(id='news-table')

# An object to store timestamp, link and title
parsed_data = []

news_rows = news_table.findAll('tr')
for index, row in enumerate(news_rows):
    title = row.a.get_text()
    timestamp = row.td.text
    timestamp = timestamp.strip().split(' ')
    if len(timestamp) == 1:
        time = timestamp[0]
        date = parsed_data[-1][0]
        # TODO: get date from previous row
    else:
        time = timestamp[1]
        date = timestamp[0]

    parsed_data.append([date, time, title])

df = pd.DataFrame(parsed_data, columns=['date', 'time', 'title'])

# Calulate sentiment scores using VADER library
vader = SentimentIntensityAnalyzer()
compound_score_lambda = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(compound_score_lambda)

# Calculate sentiment scores using the pattern library
# pattern_sentiment_lambda = lambda title: sentiment(title)[0]  # Extract polarity from the tuple
# df['pattern_sentiment'] = df['title'].apply(pattern_sentiment_lambda)

df['date'] = pd.to_datetime(df.date).dt.date # sort

# Stock data retrieval
stock_data = yf.download(ticker, start=df['date'].min(), end=df['date'].max())
stock_data['date'] = stock_data.index.date # add date column
stock_data['date'] = pd.to_datetime(stock_data.date).dt.date

# Join together for visualisation - purple represents stock price and blue is the sentiment scores of the titles
# Calculate mean sentiment scores
mean_df = df.groupby('date')['compound'].mean().reset_index()

# Merge mean sentiment scores with stock data
stock_data = stock_data[['date', 'Close']]  # Keep only relevant columns
joined_df = pd.merge(mean_df, stock_data, on='date', how='inner')  # Join on 'date'

# mean_df.plot(kind='bar')

fig, ax1 = plt.subplots(figsize=(10, 8))
ax1.plot(joined_df['date'], joined_df['compound'], color='lightblue', marker='o', label='Compound Sentiment Score')
#ax1.bar(joined_df['date'], joined_df['pattern_sentiment'], color='orange', label='Pattern Sentiment Score', alpha=0.7)

ax2 = ax1.twinx()
ax2.plot(joined_df['date'], joined_df['Close'], color='purple', marker='o', label='Stock Price')
plt.show()