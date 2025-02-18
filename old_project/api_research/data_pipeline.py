"""
Sentiment Anaylsis Data Pipeline

Handles the collection and processing of financial data for sentiment analysis.
Main components:
- API handlers for SEC EDGAR, Alpha Vantage and Yahoo Finance
- Sentiment anaylsis prcoessing
- Data Orchestration coordinates data collection and processing
"""

from typing import Dict, Any
from abc import ABC, abstractmethod
import requests
import time
from functools import lru_cache
import yfinance as yf

class BaseAPIHandler(ABC):
    """Abstract base class for API interactions. All API handlers inherit from this. Includes rate limiting""" 
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.retry_delay = 1

    @abstractmethod
    def fetch_data(self, ticker:str) -> Dict[str, Any]:
        pass

class SECEdgarHandler(BaseAPIHandler):
    """SEC EDGAR API integration. Integration with report_downloader2.py for document extraction."""
    def __init__(self):
        super().__init__()
        self.headers = {"User-Agent": "example@email.com"}

    def fetch_data(self, ticker: str) -> Dict[str, Any]:
        from report_downloader2 import extract_filings_text
        cik = self.get_cik(ticker)
        return {"sec_filings": extract_filings_text(cik, ticker, 5)}
    
class AlphaVantageHandler(BaseAPIHandler):
    """Handles Alpha Vantage API requests"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://www.alphavantage.co/query"

    def fetch_data(self, ticker: str) -> Dict[str, Any]:
        params = {
            "function": "NEWS_SENTIMENT",
            "ticker": ticker,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return {"news_data": response.json()}
    
class YahooFinanceHandler(BaseAPIHandler):
    """Handles Yahoo Finance data retrieval"""
    def fetch_data(self, ticker: str) -> Dict[str, Any]:
        stock = yf.Ticker(ticker)
        return {
            "market_data": {
                "info": stock.info,
                "earnings": stock.earnings,
            }
        }

class DataOrchestrator:
    """Coordinates data collection from multiple sources"""
    def __init__(self, alpha_vantage_key: str):
        self.handlers = {
            "sec_edgar": SECEdgarHandler(),
            "alpha_vantage": AlphaVantageHandler(alpha_vantage_key),
            "yahoo_finance": YahooFinanceHandler()
        }

    def collect_data(self, ticker: str) -> Dict[str, Any]:
        """
        Collects all data needed for sentiment analysis
        Returns structured data for LLM processing
        """
        collected_data = {}
        for source, handler in self.handlers.items():
            collected_data.update(handler.fetch_data(ticker))
        return collected_data


        