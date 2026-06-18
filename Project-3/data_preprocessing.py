import pandas as pd
import numpy as np


def load_data(filepath: str = "spotify_tracks.csv") -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        print("   Download the dataset from: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    initial_rows = len(df)

    key_columns = [
        "track_name", "artists", "track_genre",
        "popularity", "danceability", "energy",
        "valence", "tempo", "acousticness",
        "speechiness", "instrumentalness", "liveness"
    ]

    df = df.dropna(subset=key_columns)

    df = df.drop_duplicates(subset=["track_name", "artists"])

    df = df.reset_index(drop=True)

    removed = initial_rows - len(df)
    print(f"🧹 Cleaned dataset: removed {removed:,} rows  |  {len(df):,} rows remaining")
    return df

FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "valence",
    "acousticness",
    "speechiness",
    "instrumentalness",
    "liveness",
    "tempo",
    "popularity",
]


def normalize_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in FEATURE_COLUMNS:
        col_min = df[col].min()
        col_max = df[col].max()

        if col_max - col_min == 0:
            df[f"{col}_norm"] = 0.0
        else:
            df[f"{col}_norm"] = (df[col] - col_min) / (col_max - col_min)

    print("✅ Features normalized to [0, 1]")
    return df

def basic_eda(df: pd.DataFrame) -> None:
    print("\n📊 Basic EDA")
    print("─" * 40)
    print(f"Total tracks   : {len(df):,}")
    print(f"Unique genres  : {df['track_genre'].nunique()}")
    print(f"Unique artists : {df['artists'].nunique():,}")
    print(f"\nTop 5 genres by track count:")
    print(df["track_genre"].value_counts().head())
    print(f"\nFeature statistics:")
    print(df[FEATURE_COLUMNS].describe().round(3))


def preprocess(filepath: str = "spotify_tracks.csv") -> pd.DataFrame:
    df = load_data(filepath)
    if df is None:
        return None

    df = clean_data(df)
    df = normalize_features(df)
    return df

if __name__ == "__main__":
    df = preprocess()
    if df is not None:
        basic_eda(df)
