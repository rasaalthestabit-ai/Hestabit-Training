"""
Module for transforming and preparing sales data for analysis.

This module provides functions to normalize and scale the sales data, 
making it more suitable for analysis and modeling.
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from typing import Optional

def normalize_sales_data(data: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Normalize the sales data using Min-Max Scaler.

    Args:
    - data (pd.DataFrame): The sales data to be normalized.

    Returns:
    - pd.DataFrame: The normalized sales data.
    """
    try:
        # Initialize Min-Max Scaler
        scaler = MinMaxScaler()
        
        # Fit and transform the data
        normalized_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
        
        return normalized_data
    
    except Exception as e:
        # Handle any exceptions during normalization
        print(f"Error normalizing sales data: {str(e)}")
        return None

def scale_sales_data(data: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Scale the sales data using Standard Scaler.

    Args:
    - data (pd.DataFrame): The sales data to be scaled.

    Returns:
    - pd.DataFrame: The scaled sales data.
    """
    try:
        # Initialize Standard Scaler
        scaler = StandardScaler()
        
        # Fit and transform the data
        scaled_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
        
        return scaled_data
    
    except Exception as e:
        # Handle any exceptions during scaling
        print(f"Error scaling sales data: {str(e)}")
        return None

def transform_sales_data(data: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Transform the sales data by normalizing and scaling it.

    Args:
    - data (pd.DataFrame): The sales data to be transformed.

    Returns:
    - pd.DataFrame: The transformed sales data.
    """
    try:
        # Normalize the data
        normalized_data = normalize_sales_data(data)
        
        # Scale the normalized data
        scaled_data = scale_sales_data(normalized_data)
        
        return scaled_data
    
    except Exception as e:
        # Handle any exceptions during transformation
        print(f"Error transforming sales data: {str(e)}")
        return None

if __name__ == "__main__":
    # Load the sales data
    from load_the_sales_csv_file_into_the_system import load_sales_data
    data = load_sales_data("sales.csv")
    
    # Transform the sales data
    transformed_data = transform_sales_data(data)
    
    # Print the transformed data
    print(transformed_data.head())