"""
recommendation.py
-----------------
Content-Based Recommendation Engine using Cosine Similarity.

How it works (in plain English):
  1. The user provides preferences: genre(s) + slider values for
     energy, danceability, valence, and popularity.
  2. We build a "user vector" — a single row of numbers that
     represents the user's ideal song.
  3. We filter the dataset to songs matching the chosen genre(s).
  4. We calculate how similar each song's feature vector is to the
     user vector using COSINE SIMILARITY.
  5. We return the top-N songs with the highest similarity scores.

Author: DecodeLabs Internship Project
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from data_preprocessing import FEATURE_COLUMNS, preprocess


# ─────────────────────────────────────────────
# NORMALIZED FEATURE COLUMN NAMES
# e.g., "energy" → "energy_norm"
# ─────────────────────────────────────────────
NORM_FEATURE_COLUMNS = [f"{col}_norm" for col in FEATURE_COLUMNS]


# ─────────────────────────────────────────────
# 1. BUILD USER PREFERENCE VECTOR
# ─────────────────────────────────────────────

def build_user_vector(
    energy: float = 0.5,
    danceability: float = 0.5,
    valence: float = 0.5,
    popularity: float = 50.0,
    acousticness: float = 0.5,
    speechiness: float = 0.1,
    instrumentalness: float = 0.1,
    liveness: float = 0.2,
    tempo: float = 120.0,
) -> np.ndarray:
    """
    Translate user slider inputs into a numeric feature vector.

    The vector must match the same column ORDER as FEATURE_COLUMNS:
      [danceability, energy, valence, acousticness, speechiness,
       instrumentalness, liveness, tempo, popularity]

    All slider values from the UI arrive pre-normalized to [0, 1]
    EXCEPT popularity (0–100) and tempo (0–250); we normalize those
    here to match the training data scale.

    Args:
        energy           : 0.0 – 1.0
        danceability     : 0.0 – 1.0
        valence          : 0.0 – 1.0
        popularity       : 0 – 100  (raw; normalized here)
        acousticness     : 0.0 – 1.0
        speechiness      : 0.0 – 1.0
        instrumentalness : 0.0 – 1.0
        liveness         : 0.0 – 1.0
        tempo            : 0 – 250  (raw; normalized here)

    Returns:
        1-D NumPy array of shape (9,)
    """
    # Normalize popularity (0–100) → (0–1)
    popularity_norm = popularity / 100.0

    # Normalize tempo (0–250 BPM) → (0–1)
    tempo_norm = tempo / 250.0

    # Order MUST match FEATURE_COLUMNS list exactly
    vector = np.array([
        danceability,
        energy,
        valence,
        acousticness,
        speechiness,
        instrumentalness,
        liveness,
        tempo_norm,
        popularity_norm,
    ], dtype=float)

    return vector.reshape(1, -1)   # shape (1, 9) for cosine_similarity


# ─────────────────────────────────────────────
# 2. FILTER BY GENRE
# ─────────────────────────────────────────────

def filter_by_genre(df: pd.DataFrame, genres: list) -> pd.DataFrame:
    """
    Keep only rows whose track_genre is in the selected list.

    Args:
        df     : Preprocessed full DataFrame.
        genres : List of genre strings chosen by the user.

    Returns:
        Filtered DataFrame. If no songs match, returns empty DF.
    """
    if not genres:
        return df   # No filter if user selects nothing

    filtered = df[df["track_genre"].isin(genres)].copy()
    print(f"🎵 Genre filter: {len(filtered):,} songs match {genres}")
    return filtered


# ─────────────────────────────────────────────
# 3. CALCULATE COSINE SIMILARITY
# ─────────────────────────────────────────────

def calculate_similarity(
    filtered_df: pd.DataFrame,
    user_vector: np.ndarray,
) -> pd.DataFrame:
    """
    Compute Cosine Similarity between every song in filtered_df
    and the user preference vector.

    Cosine Similarity Formula:
        similarity = (A · B) / (||A|| × ||B||)

    where A = song feature vector, B = user preference vector.

    - Result is 1.0  → perfectly aligned with user preferences.
    - Result is 0.0  → completely different from user preferences.

    Args:
        filtered_df : Genre-filtered DataFrame with *_norm columns.
        user_vector : Shape (1, 9) NumPy array from build_user_vector().

    Returns:
        DataFrame with a new 'similarity_score' column (0.0 – 1.0).
    """
    if filtered_df.empty:
        return filtered_df

    # Extract the song feature matrix — shape (N songs, 9 features)
    song_matrix = filtered_df[NORM_FEATURE_COLUMNS].values

    # cosine_similarity returns shape (N, 1); flatten to (N,)
    scores = cosine_similarity(song_matrix, user_vector).flatten()

    result = filtered_df.copy()
    result["similarity_score"] = scores
    return result


# ─────────────────────────────────────────────
# 4. GET TOP-N RECOMMENDATIONS
# ─────────────────────────────────────────────

def get_recommendations(
    df: pd.DataFrame,
    genres: list,
    energy: float = 0.5,
    danceability: float = 0.5,
    valence: float = 0.5,
    popularity: float = 50.0,
    acousticness: float = 0.5,
    speechiness: float = 0.1,
    instrumentalness: float = 0.1,
    liveness: float = 0.2,
    tempo: float = 120.0,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Full recommendation pipeline:
      filter → build user vector → score → sort → return top-N.

    Args:
        df           : Preprocessed full DataFrame.
        genres       : List of selected genres.
        energy       : User energy preference (0–1).
        danceability : User danceability preference (0–1).
        valence      : User valence preference (0–1).
        popularity   : User popularity preference (0–100).
        acousticness : User acousticness preference (0–1).
        speechiness  : User speechiness preference (0–1).
        instrumentalness : User instrumentalness preference (0–1).
        liveness     : User liveness preference (0–1).
        tempo        : User tempo preference in BPM (0–250).
        top_n        : Number of recommendations to return.

    Returns:
        DataFrame of top-N recommended songs with display columns
        and 'similarity_score'.
    """
    # Step 1 — Filter by genre
    filtered = filter_by_genre(df, genres)

    if filtered.empty:
        print("⚠️  No songs found for selected genres.")
        return pd.DataFrame()

    # Step 2 — Build user preference vector
    user_vec = build_user_vector(
        energy=energy,
        danceability=danceability,
        valence=valence,
        popularity=popularity,
        acousticness=acousticness,
        speechiness=speechiness,
        instrumentalness=instrumentalness,
        liveness=liveness,
        tempo=tempo,
    )

    # Step 3 — Score every song
    scored = calculate_similarity(filtered, user_vec)

    # Step 4 — Sort descending by similarity score
    top = (
        scored
        .sort_values("similarity_score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # Step 5 — Return only the columns needed for display
    display_cols = [
        "track_name", "artists", "track_genre",
        "popularity", "danceability", "energy",
        "valence", "tempo", "similarity_score",
    ]
    # Keep only columns that exist (safety check)
    display_cols = [c for c in display_cols if c in top.columns]
    return top[display_cols]


# ─────────────────────────────────────────────
# 5. FIND SIMILAR SONGS (Bonus feature)
# ─────────────────────────────────────────────

def find_similar_songs(
    df: pd.DataFrame,
    track_name: str,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    Given a track name, find the most similar songs across
    the entire dataset (regardless of genre).

    This is a "more like this" feature often seen on streaming apps.

    Args:
        df         : Preprocessed full DataFrame.
        track_name : Exact name of the seed track.
        top_n      : Number of similar songs to return.

    Returns:
        DataFrame of similar songs (excluding the seed song itself).
    """
    seed_rows = df[df["track_name"].str.lower() == track_name.lower()]

    if seed_rows.empty:
        print(f"⚠️  Track '{track_name}' not found in dataset.")
        return pd.DataFrame()

    # Use the first matching row as the reference vector
    seed_vector = seed_rows.iloc[0][NORM_FEATURE_COLUMNS].values.reshape(1, -1)

    # Score all songs against the seed track
    song_matrix = df[NORM_FEATURE_COLUMNS].values
    scores = cosine_similarity(song_matrix, seed_vector).flatten()

    result = df.copy()
    result["similarity_score"] = scores

    # Exclude the seed song itself and return top-N
    similar = (
        result[result["track_name"].str.lower() != track_name.lower()]
        .sort_values("similarity_score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    display_cols = ["track_name", "artists", "track_genre", "similarity_score"]
    return similar[[c for c in display_cols if c in similar.columns]]


# ─────────────────────────────────────────────
# 6. GENRE LIST HELPER
# ─────────────────────────────────────────────

def get_genres(df: pd.DataFrame) -> list:
    """
    Return a sorted list of all unique genres in the dataset.

    Args:
        df: Preprocessed DataFrame.

    Returns:
        Sorted list of genre strings.
    """
    return sorted(df["track_genre"].dropna().unique().tolist())


# ─────────────────────────────────────────────
# Quick smoke-test when run directly
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading data …")
    df = preprocess()

    if df is not None:
        print(f"\nAvailable genres (first 10): {get_genres(df)[:10]}")

        print("\n🔍 Sample recommendation — pop + high energy:")
        recs = get_recommendations(
            df,
            genres=["pop"],
            energy=0.9,
            danceability=0.8,
            valence=0.7,
            popularity=70,
            top_n=5,
        )
        print(recs.to_string(index=False))
