import sqlite3
from datetime import datetime
import pandas as pd
from typing import Dict, Any
from abc import ABC, abstractmethod
import requests
import time
from functools import lru_cache

class DatabaseMananger:
    """
    Handles all database interactions with SQLite. Creates tables for fillings,
    news, and market data. 
    Manages connections and query execution
    Implements indexes for optimisation
    """
    def __init__(self, db_path="financial_data.db"):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """
        Initialize database structure:
        - filings: stores SEC document data
        - news: stores news articles and sentiment from articles
        - market_data: stores stock price data and volume info
        """
        with sqlite3.connect(self.db_path) as conn:
            # Filings table - stores SEC documents
            conn.execute("""
                CREATE TABLE IF NOT EXISTS filings (
                    id INTEGER PRIMARY KEY,
                    ticker TEXT,
                    filing_type TEXT,
                    filing_date DATE,
                    context TEXT,
                    sentiment_score FLOAT,
                    UNIQUE(ticker, filing_type, filing_date)
                )
            """)
            # News table - stores news articles
            conn.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY,
                    ticker TEXT,
                    publish_date DATE,
                    headline TEXT,
                    sentiment_score FLOAT
                )
            """)
            # Market data table - stores stock price data
            conn.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY,
                    ticker TEXT,
                    date DATE,
                    close_price FLOAT,
                    volume INTEGER
                )
            """)