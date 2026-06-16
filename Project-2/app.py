import os
import pickle
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Student Pass/Fail Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Load Model, Encoders & Accuracy
# ─────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    missing = []
    for fname in ["model.pkl", "encoders.pkl", "accuracy.pkl"]:
        if not os.path.exists(fname):
            missing.append(fname)
    if missing:
        return None, None, None, missing

    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("encoders.pkl", "rb") as f:
        encoders = pickle.load(f)
    with open("accuracy.pkl", "rb") as f:
        accuracy = pickle.load(f)
    return model, encoders, accuracy, []


model, encoders, model_accuracy, missing_files = load_artifacts()

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.title("🎓 Student Pass/Fail Prediction")
st.markdown(
    "An AI-powered app that predicts whether a student will **Pass** or **Fail** "
    "based on their **demographic background** using a trained **Decision Tree Classifier** — "
    "no exam scores required."
)
st.divider()

# ─────────────────────────────────────────────
# Missing files warning
# ─────────────────────────────────────────────
if missing_files:
    st.error(
        f"⚠️ The following required files are missing: **{', '.join(missing_files)}**\n\n"
        "Please run `python train_model.py` first to train the model and generate these files."
    )
    st.stop()

# ─────────────────────────────────────────────
# Sidebar — User Inputs
# ─────────────────────────────────────────────
st.sidebar.header("📋 Student Information")
st.sidebar.markdown("Fill in the student details below, then click **Predict**.")

gender = st.sidebar.selectbox(
    "Gender",
    options=list(encoders["gender"].classes_),
    help="Select the student's gender",
)

race_ethnicity = st.sidebar.selectbox(
    "Race / Ethnicity",
    options=list(encoders["race/ethnicity"].classes_),
    help="Select the student's race/ethnicity group",
)

parental_education = st.sidebar.selectbox(
    "Parental Level of Education",
    options=list(encoders["parental level of education"].classes_),
    help="Select the highest education level of the student's parent/guardian",
)

lunch = st.sidebar.selectbox(
    "Lunch Type",
    options=list(encoders["lunch"].classes_),
    help="Standard or free/reduced lunch",
)

test_prep = st.sidebar.selectbox(
    "Test Preparation Course",
    options=list(encoders["test preparation course"].classes_),
    help="Whether the student completed a test preparation course",
)

predict_btn = st.sidebar.button("🔮 Predict Result", type="primary", use_container_width=True)

# ─────────────────────────────────────────────
# Prediction Logic
# ─────────────────────────────────────────────
def encode_input():
    return {
        "gender": encoders["gender"].transform([gender])[0],
        "race/ethnicity": encoders["race/ethnicity"].transform([race_ethnicity])[0],
        "parental level of education": encoders["parental level of education"].transform([parental_education])[0],
        "lunch": encoders["lunch"].transform([lunch])[0],
        "test preparation course": encoders["test preparation course"].transform([test_prep])[0],
    }


col_pred, col_info = st.columns([1, 1], gap="large")

with col_pred:
    st.subheader("🔮 Prediction Result")

    if predict_btn:
        input_data = encode_input()
        input_df = pd.DataFrame([input_data])

        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        class_labels = model.classes_
        prob_dict = dict(zip(class_labels, probabilities))
        confidence = max(probabilities) * 100

        if prediction == "Pass":
            st.success(f"### ✅ Prediction: **PASS**")
            st.balloons()
        else:
            st.error(f"### ❌ Prediction: **FAIL**")

        st.metric(label="Confidence Score", value=f"{confidence:.2f}%")
        st.metric(label="Model Accuracy", value=f"{model_accuracy:.2f}%")

        st.markdown("**Probability Breakdown:**")
        prob_df = pd.DataFrame(
            {"Result": list(prob_dict.keys()), "Probability": [f"{v*100:.2f}%" for v in prob_dict.values()]}
        )
        st.dataframe(prob_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("**Input Summary:**")
        summary = {
            "Gender": gender,
            "Race/Ethnicity": race_ethnicity,
            "Parental Education": parental_education,
            "Lunch": lunch,
            "Test Prep": test_prep,
        }
        st.dataframe(
            pd.DataFrame(summary.items(), columns=["Feature", "Value"]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("👈 Fill in the student details in the sidebar and click **Predict Result**.")
        st.metric(label="Model Accuracy", value=f"{model_accuracy:.2f}%")

with col_info:
    st.subheader("📖 How It Works")
    st.markdown(
        """
        1. **Input** — Select the student's 5 demographic features in the sidebar.
        2. **Encoding** — Categorical features are encoded using saved `LabelEncoders`.
        3. **Prediction** — The trained **Decision Tree Classifier** predicts the result.
        4. **Result** — The app displays:
           - ✅ **Pass** (predicted from background features)
           - ❌ **Fail** (predicted from background features)
           - 📊 **Confidence Score** (probability of the predicted class)
           - 🎯 **Model Accuracy** (performance on the test set)

        > **Note:** The model learns patterns from demographic data only —
        > gender, race/ethnicity, parental education, lunch type, and
        > test preparation course. No exam scores are used as input.
        """
    )

# ─────────────────────────────────────────────
# Visualizations Section
# ─────────────────────────────────────────────
st.divider()
st.header("📊 Data Visualizations")

DATA_PATH = os.path.join("data", "StudentsPerformance.csv")
viz_tabs = st.tabs(["📈 Pass vs Fail", "📊 Feature Distribution", "🧮 Confusion Matrix"])

# ── Tab 1: Pass vs Fail Distribution ──
with viz_tabs[0]:
    st.subheader("Pass vs Fail Distribution")
    img_path = os.path.join("screenshots", "pass_fail_distribution.png")
    if os.path.exists(img_path):
        st.image(img_path, width="stretch")
    elif os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df["average score"] = (df["math score"] + df["reading score"] + df["writing score"]) / 3
        df["Result"] = df["average score"].apply(lambda x: "Pass" if x >= 60 else "Fail")
        counts = df["Result"].value_counts()
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(counts.index, counts.values, color=["#4CAF50", "#F44336"], edgecolor="black", width=0.5)
        ax.set_title("Pass vs Fail Distribution", fontsize=15, fontweight="bold")
        ax.set_xlabel("Result"); ax.set_ylabel("Number of Students")
        for i, (label, val) in enumerate(counts.items()):
            ax.text(i, val + 5, str(val), ha="center", fontsize=12, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.warning("Run `python train_model.py` to generate visualizations.")

# ── Tab 2: Feature Distribution by Result ──
with viz_tabs[1]:
    st.subheader("Pass/Fail Rate by Demographic Feature")
    img_path = os.path.join("screenshots", "feature_distribution.png")
    if os.path.exists(img_path):
        st.image(img_path, width="stretch")
    elif os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df["average score"] = (df["math score"] + df["reading score"] + df["writing score"]) / 3
        df["Result"] = df["average score"].apply(lambda x: "Pass" if x >= 60 else "Fail")
        cat_cols = ["gender", "lunch", "test preparation course"]
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        for ax, col in zip(axes, cat_cols):
            ct = df.groupby([col, "Result"]).size().unstack(fill_value=0)
            ct.plot(kind="bar", ax=ax, color=["#F44336", "#4CAF50"], edgecolor="black", rot=15)
            ax.set_title(col.title(), fontsize=12, fontweight="bold")
            ax.set_xlabel(""); ax.set_ylabel("Count")
            ax.legend(title="Result")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.warning("Run `python train_model.py` to generate visualizations.")

# ── Tab 3: Confusion Matrix ──
with viz_tabs[2]:
    st.subheader("Confusion Matrix (Model Performance)")
    img_path = os.path.join("screenshots", "confusion_matrix.png")
    if os.path.exists(img_path):
        st.image(img_path, width="stretch")
    else:
        st.warning("Run `python train_model.py` to generate the confusion matrix.")

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center; color:gray; font-size:13px;'>"
    "Student Pass/Fail Prediction | Built with Streamlit & scikit-learn | "
    "Dataset: <a href='https://www.kaggle.com/datasets/spscientist/students-performance-in-exams' target='_blank'>Kaggle</a>"
    "</div>",
    unsafe_allow_html=True,
)
