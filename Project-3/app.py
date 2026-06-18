import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")   # Non-interactive backend for Streamlit

from data_preprocessing import preprocess
from recommendation import get_recommendations, find_similar_songs, get_genres

st.set_page_config(
    page_title="🎵 Spotify Song Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Global ── */
body { font-family: 'Segoe UI', sans-serif; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f0f1a 0%, #1a1a2e 100%);
    border-right: 1px solid #2d2d50;
}
[data-testid="stSidebar"] * { color: #e0e0f0 !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #1a1a2e;
    border: 1px solid #2d2d50;
    border-radius: 10px;
    padding: 12px;
}

/* ── Recommendation card ── */
.rec-card {
    background: linear-gradient(135deg, #1e1e3a, #16213e);
    border: 1px solid #0f3460;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    transition: transform 0.2s;
}
.rec-card:hover { transform: translateY(-2px); border-color: #1db954; }
.rec-title  { font-size: 1.05rem; font-weight: 700; color: #ffffff; }
.rec-artist { font-size: 0.88rem; color: #1db954; margin-top: 2px; }
.rec-meta   { font-size: 0.78rem; color: #a0a0c0; margin-top: 6px; }
.score-pill {
    display: inline-block;
    background: #1db954;
    color: #000;
    font-weight: 700;
    font-size: 0.78rem;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 8px;
}

/* ── Section headers ── */
h1, h2, h3 { color: #ffffff; }
.section-label {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #1db954;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="🎧 Loading Spotify dataset …")
def load_dataset():
    """Load and preprocess dataset once; cache for the session."""
    return preprocess("spotify_tracks.csv")


df = load_dataset()

if df is None:
    st.error(
        "⚠️ **Dataset not found.**  \n"
        "Please download `spotify_tracks.csv` from Kaggle and place it "
        "in the same folder as `app.py`.\n\n"
        "🔗 https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset"
    )
    st.stop()


with st.sidebar:
    st.title("🎵 Song Recommender")
    st.caption("Powered by Cosine Similarity & Content-Based Filtering")
    st.divider()

    st.markdown('<p class="section-label">Select Genres</p>', unsafe_allow_html=True)
    all_genres = get_genres(df)
    selected_genres = st.multiselect(
        label="Genres",
        options=all_genres,
        default=["pop"] if "pop" in all_genres else [all_genres[0]],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown('<p class="section-label">Mood & Audio Preferences</p>', unsafe_allow_html=True)

    energy = st.slider(
        "⚡ Energy",
        min_value=0.0, max_value=1.0, value=0.7, step=0.05,
        help="How intense and active the song feels (0 = calm, 1 = intense)",
    )
    danceability = st.slider(
        "💃 Danceability",
        min_value=0.0, max_value=1.0, value=0.7, step=0.05,
        help="How suitable the track is for dancing",
    )
    valence = st.slider(
        "😊 Valence (Happiness)",
        min_value=0.0, max_value=1.0, value=0.6, step=0.05,
        help="Musical positiveness — 0 = sad/angry, 1 = happy/euphoric",
    )
    acousticness = st.slider(
        "🎸 Acousticness",
        min_value=0.0, max_value=1.0, value=0.2, step=0.05,
        help="Likelihood the track is acoustic (no electronic production)",
    )
    popularity = st.slider(
        "🔥 Popularity",
        min_value=0, max_value=100, value=70, step=5,
        help="How popular the song is on Spotify (0–100)",
    )

    st.divider()

    # ── Advanced options ─────────────────────────────────────────
    with st.expander("Advanced Options"):
        speechiness = st.slider("🎤 Speechiness", 0.0, 1.0, 0.1, 0.05,
            help="Presence of spoken words in the track")
        instrumentalness = st.slider("🎹 Instrumentalness", 0.0, 1.0, 0.1, 0.05,
            help="Probability that the track has no vocals")
        liveness = st.slider("🎙️ Liveness", 0.0, 1.0, 0.2, 0.05,
            help="Detects presence of an audience (live recording feel)")
        tempo = st.slider("🥁 Tempo (BPM)", 60, 200, 120, 5,
            help="Speed of the song in beats per minute")
        top_n = st.number_input("Number of Recommendations", 5, 20, 10, 1)

    st.divider()
    get_recs_btn = st.button("🎯 Get Recommendations", use_container_width=True, type="primary")

st.markdown("## 🎵 AI Song Recommender")
st.caption("Content-Based Filtering · Cosine Similarity")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tracks", f"{len(df):,}")
col2.metric("Unique Genres", df["track_genre"].nunique())
col3.metric("Unique Artists", f"{df['artists'].nunique():,}")
col4.metric("Avg. Popularity", f"{df['popularity'].mean():.0f}")

st.divider()

tab_recs, tab_viz, tab_similar = st.tabs(
    ["🎯 Recommendations", "📊 Genre Visualizations", "🔍 Find Similar Songs"]
)

with tab_recs:
    if get_recs_btn or "recommendations" in st.session_state:

        if not selected_genres:
            st.warning("⚠️ Please select at least one genre from the sidebar.")
        else:
            with st.spinner("🔍 Finding your perfect songs …"):
                recommendations = get_recommendations(
                    df=df,
                    genres=selected_genres,
                    energy=energy,
                    danceability=danceability,
                    valence=valence,
                    popularity=float(popularity),
                    acousticness=acousticness,
                    speechiness=speechiness,
                    instrumentalness=instrumentalness,
                    liveness=liveness,
                    tempo=float(tempo),
                    top_n=int(top_n),
                )
                st.session_state["recommendations"] = recommendations

            if recommendations.empty:
                st.error("No songs found for the selected preferences. Try different genres.")
            else:
                st.success(f"✅ Found **{len(recommendations)}** recommendations for genres: {', '.join(selected_genres)}")

                for rank, (_, row) in enumerate(recommendations.iterrows(), start=1):
                    score_pct = int(row["similarity_score"] * 100)
                    bar_width = score_pct

                    st.markdown(f"""
                    <div class="rec-card">
                        <span style="color:#666;font-size:0.75rem">#{rank}</span>
                        <div class="rec-title">🎵 {row['track_name']}</div>
                        <div class="rec-artist">🎤 {row['artists']}</div>
                        <div class="rec-meta">
                            🎸 {row['track_genre']} &nbsp;|&nbsp;
                            ⚡ Energy: {row['energy']:.2f} &nbsp;|&nbsp;
                            💃 Dance: {row['danceability']:.2f} &nbsp;|&nbsp;
                            😊 Valence: {row['valence']:.2f} &nbsp;|&nbsp;
                            🔥 Pop: {int(row['popularity'])}
                        </div>
                        <div>
                            <span class="score-pill">Match: {score_pct}%</span>
                        </div>
                        <div style="background:#2d2d50;border-radius:4px;margin-top:8px;height:4px;">
                            <div style="background:#1db954;width:{bar_width}%;height:4px;border-radius:4px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()
                csv_data = recommendations.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Recommendations as CSV",
                    data=csv_data,
                    file_name="spotify_recommendations.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
    else:
        st.info("👈 Set your preferences in the sidebar and click **Get Recommendations**.")

        st.markdown("#### 📋 Sample Dataset Preview")
        st.dataframe(
            df[["track_name", "artists", "track_genre",
                "popularity", "danceability", "energy", "valence"]].head(8),
            use_container_width=True,
            hide_index=True,
        )


with tab_viz:
    st.markdown("### 📊 Genre Popularity & Audio Characteristics")

    top_genres_n = st.slider("Show top N genres", 5, 20, 10, key="viz_n")
    top_genres_df = (
        df.groupby("track_genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(top_genres_n)
        .reset_index()
    )

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    fig1.patch.set_facecolor("#0f0f1a")
    ax1.set_facecolor("#1a1a2e")

    bars = ax1.barh(
        top_genres_df["track_genre"],
        top_genres_df["popularity"],
        color="#1db954",
        edgecolor="none",
    )
    ax1.invert_yaxis()
    ax1.set_xlabel("Average Popularity", color="#a0a0c0")
    ax1.set_title("Top Genres by Avg. Popularity", color="#ffffff", pad=12)
    ax1.tick_params(colors="#a0a0c0")
    ax1.spines[:].set_color("#2d2d50")
    for bar, val in zip(bars, top_genres_df["popularity"]):
        ax1.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}", va="center", color="#ffffff", fontsize=8)

    st.pyplot(fig1, use_container_width=True)

    st.markdown("#### Energy vs Danceability")
    sample = df.sample(min(2000, len(df)), random_state=42)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    fig2.patch.set_facecolor("#0f0f1a")
    ax2.set_facecolor("#1a1a2e")
    scatter = ax2.scatter(
        sample["energy"], sample["danceability"],
        c=sample["valence"], cmap="RdYlGn",
        alpha=0.4, s=10, edgecolors="none"
    )
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label("Valence (happiness)", color="#a0a0c0")
    cbar.ax.yaxis.set_tick_params(color="#a0a0c0")
    ax2.set_xlabel("Energy", color="#a0a0c0")
    ax2.set_ylabel("Danceability", color="#a0a0c0")
    ax2.set_title("Energy vs Danceability (colour = Valence)", color="#ffffff", pad=10)
    ax2.tick_params(colors="#a0a0c0")
    ax2.spines[:].set_color("#2d2d50")
    st.pyplot(fig2, use_container_width=True)

    if selected_genres:
        st.markdown(f"#### Audio Feature Averages — {', '.join(selected_genres)}")
        genre_avg = (
            df[df["track_genre"].isin(selected_genres)]
            [["danceability", "energy", "valence", "acousticness", "speechiness"]]
            .mean()
        )
        fig3, ax3 = plt.subplots(figsize=(7, 3))
        fig3.patch.set_facecolor("#0f0f1a")
        ax3.set_facecolor("#1a1a2e")
        ax3.bar(genre_avg.index, genre_avg.values, color="#1db954", edgecolor="none")
        ax3.set_ylim(0, 1)
        ax3.set_ylabel("Average Value", color="#a0a0c0")
        ax3.set_title("Avg. Audio Features for Selected Genres", color="#ffffff")
        ax3.tick_params(colors="#a0a0c0", axis="x", rotation=15)
        ax3.tick_params(colors="#a0a0c0", axis="y")
        ax3.spines[:].set_color("#2d2d50")
        st.pyplot(fig3, use_container_width=True)

with tab_similar:
    st.markdown("### 🔍 Find Songs Similar to a Track You Love")
    st.caption("Enter any song name from the dataset to find the most similar tracks.")

    seed_track = st.text_input(
        "Track Name",
        placeholder="e.g.  Blinding Lights",
        label_visibility="collapsed",
    )
    n_similar = st.number_input("How many similar songs?", 3, 15, 5, key="n_sim")
    find_btn = st.button("🔍 Find Similar Songs", type="primary")

    if find_btn and seed_track.strip():
        with st.spinner("Searching …"):
            similar = find_similar_songs(df, seed_track.strip(), top_n=int(n_similar))

        if similar.empty:
            st.error(f"Track **'{seed_track}'** not found. Check the spelling and try again.")
        else:
            st.success(f"Songs similar to **{seed_track}**:")
            st.dataframe(
                similar.style.format({"similarity_score": "{:.2%}"}),
                use_container_width=True,
                hide_index=True,
            )

st.divider()
st.caption("🎵 Spotify AI Song Recommender · Built with ❤️ · Powered by Scikit-Learn & Streamlit")
 