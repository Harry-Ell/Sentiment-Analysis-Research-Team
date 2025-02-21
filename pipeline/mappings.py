'''
Here is where we collect all of our functions which can map from the
options order book to a scalar. The data these expect is basically the 
same as expected, provided calls and puts will be treated as separate 
when they are passed into the function. 
'''
import numpy as np
import pandas as pd

class Mappings:
    """
    Collection of static methods for mapping an options order book to a scalar value.
    
    Please add your mappings as static methods here. Just copy the exact format, returning a 
    scalar value
    """

    @staticmethod
    def options_score_weighted_dte(df: pd.DataFrame) -> float:
        """
        Calculates score based on days until expiration, ratio of strike price to current stock price,
        and current trading price. Options closer to expiration are given more weight.
        
        Args:
            df (pd.DataFrame): DataFrame containing options data with columns 'lastPrice', 'ratio', 'dte'
            
        Returns:
            float: Scalar value representing market sentiment

        Explanation of the formula:
        - lastPrice: Higher option prices indicate higher demand, implying stronger sentiment
        - ratio: A higher strike to spot ratio for calls indicates more bullish sentiment
        - (365 - dte): Options closer to expiration / smaller dte are given more weight as they reflect
        more immediate sentiment
        """    
        score = df['lastPrice'] * df['ratio'] / (365 - df['dte'])
        return np.mean(score)

    @staticmethod
    def call_put_sentiment_comparison(calls_df: pd.DataFrame, puts_df: pd.DataFrame) -> float:
        """
        Compares call and put options sentiment to determine overall market direction.
        
        Args:
            calls_df (pd.DataFrame): DataFrame containing call options data
            puts_df (pd.DataFrame): DataFrame containing put options data
            
        Returns:
            float: Scalar value representing market sentiment (positive for bullish, negative for bearish)
        """
        mean_call_score = calls_df['lastPrice'] * calls_df['ratio'] / (365 - calls_df['dte']).mean()
        mean_put_score = puts_df['lastPrice'] * puts_df['ratio'] / (365 - puts_df['dte']).mean()
        difference = mean_call_score - mean_put_score
        
        # Return difference as sentiment indicator
        return difference
    



class MappingRegistry:
    """A registry for mapping functions, so they can be dynamically applied."""
    def __init__(self):
        self.mappings = {}

    def register_mapping(self, name: str, func):
        self.mappings[name] = func

    def apply_mapping(self, name: str, df: pd.DataFrame) -> pd.DataFrame:
        if name not in self.mappings:
            raise ValueError(f"Mapping '{name}' not found.")
        return self.mappings[name](df)
