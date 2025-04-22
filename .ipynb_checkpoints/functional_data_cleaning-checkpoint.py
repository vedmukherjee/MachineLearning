# functional_data_cleaning.py

import pandas as pd
from typing import List, Dict, Any, Tuple
import os

# --- Data Loading & Familiarization ---

def load_dataset(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at path: {filepath}")
    return pd.read_csv(filepath)

def get_dataset_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Pure function: Returns dataset structure info"""
    return {
        'num_rows': df.shape[0],
        'num_columns': df.shape[1],
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'nulls': df.isnull().sum().to_dict(),
    }

# --- Functional Cleaning & Preprocessing ---

def remove_incomplete_rows(df: pd.DataFrame, required_cols: List[str]) -> pd.DataFrame:
    """Filter out rows with nulls in required columns."""
    is_valid = lambda row: all(pd.notnull(row[col]) for col in required_cols)
    filtered_data = list(filter(is_valid, df.to_dict(orient='records')))
    return pd.DataFrame(filtered_data)

def normalize_text_columns(df: pd.DataFrame, text_cols: List[str]) -> pd.DataFrame:
    """Apply transformations using map and list comprehensions."""
    def normalize(text: str) -> str:
        return text.strip().lower() if isinstance(text, str) else text

    normalized_data = [
        {col: normalize(val) if col in text_cols else val for col, val in row.items()}
        for row in df.to_dict(orient='records')
    ]
    return pd.DataFrame(normalized_data)

# --- FP Refactoring Example ---

def remove_null_titles(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(filter(lambda row: pd.notnull(row['title']), df.to_dict(orient='records')))

# --- Mini Analysis ---

def get_top_categories(df: pd.DataFrame, col: str, top_n: int = 5) -> List[Tuple[str, int]]:
    """FP-style group count using value_counts and map"""
    return list(df[col].value_counts().head(top_n).items())

# --- Example Usage ---
if __name__ == "__main__":
    file_path = "/mnt/data/netflix_titles.csv"
    try:
        raw_df = load_dataset(file_path)

        info = get_dataset_info(raw_df)
        print("Dataset Info:", info)

        df_clean = remove_incomplete_rows(raw_df, required_cols=['title', 'type'])
        df_clean = normalize_text_columns(df_clean, text_cols=['title', 'type'])
        df_clean = remove_null_titles(df_clean)

        print("Top 5 Types:", get_top_categories(df_clean, 'type'))

    except FileNotFoundError as e:
        print(e)
        print("Please make sure the dataset file exists in the correct directory.")

