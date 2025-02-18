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
    def first_ever_attempt(df: pd.DataFrame) -> float:
        """
        first map function we had. we dont expect this to be good
        """
        score = df['lastPrice'] * df['ratio'] / np.absolute(365 - df['dte'])
        return np.mean(score)

    @staticmethod
    def different_scaling(df: pd.DataFrame) -> float:
        """
        random other one
        """
        score = df['lastPrice'] * df['ratio'] * np.sqrt(df['dte'] / 365)
        return np.mean(score)
    



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
