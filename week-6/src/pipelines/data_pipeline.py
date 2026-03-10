import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from sklearn.preprocessing import StandardScaler

# base directory (src folder)
BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


def load_data():
    print("Loading dataset...")

    file = list(RAW_DATA_DIR.glob("*.csv"))[0]

    df = pd.read_csv(file)

    print("Dataset shape:", df.shape)

    return df


def remove_duplicates(df):
    print("Removing duplicates...")

    before = df.shape[0]

    df = df.drop_duplicates()

    after = df.shape[0]

    print("Removed", before - after, "duplicates")

    return df


def handle_missing_values(df):
    print("Handling missing values...")

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    return df


def remove_outliers(df):
    print("Removing outliers using Z-score...")

    numeric_cols = df.select_dtypes(include=np.number).columns

    z_scores = np.abs(stats.zscore(df[numeric_cols]))

    df = df[(z_scores < 3).all(axis=1)]

    return df


def scale_features(df):
    print("Scaling numerical features...")

    scaler = StandardScaler()

    numeric_cols = df.select_dtypes(include=np.number).columns

    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df


def save_data(df):
    print("Saving processed dataset...")

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DATA_DIR / "final.csv"

    df.to_csv(output_file, index=False)

    print("Saved to:", output_file)


def run_pipeline():

    df = load_data()

    df = remove_duplicates(df)

    df = handle_missing_values(df)

    df = remove_outliers(df)

    df = scale_features(df)

    save_data(df)


if __name__ == "__main__":
    run_pipeline()