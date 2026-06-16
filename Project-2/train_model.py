import os
import pickle
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. Load Dataset
# ─────────────────────────────────────────────
DATA_PATH = os.path.join("data", "StudentsPerformance.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"Dataset not found at '{DATA_PATH}'.\n"
        "Please download 'StudentsPerformance.csv' from:\n"
        "  https://www.kaggle.com/datasets/spscientist/students-performance-in-exams\n"
        "and place it in the 'data/' folder."
    )

df = pd.read_csv(DATA_PATH)
print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print(df.head(3))

# ─────────────────────────────────────────────
# 2. Create Target Column: Result
# ─────────────────────────────────────────────
df["average score"] = (
    df["math score"] + df["reading score"] + df["writing score"]
) / 3

df["Result"] = df["average score"].apply(lambda x: "Pass" if x >= 60 else "Fail")

print(f"\n📊 Result distribution:\n{df['Result'].value_counts()}")

# ─────────────────────────────────────────────
# 3. Encode Categorical Features
# ─────────────────────────────────────────────
categorical_cols = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]

encoders = {}
df_encoded = df.copy()

for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    encoders[col] = le
    print(f"  Encoded '{col}': {list(le.classes_)}")

# ─────────────────────────────────────────────
# 4. Features & Target
# ─────────────────────────────────────────────
feature_cols = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]

X = df_encoded[feature_cols]
y = df_encoded["Result"]

# ─────────────────────────────────────────────
# 5. Train / Test Split
# ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n🔀 Train size: {len(X_train)}  |  Test size: {len(X_test)}")

# ─────────────────────────────────────────────
# 6. Train Decision Tree Classifier
# ─────────────────────────────────────────────
model = DecisionTreeClassifier(random_state=42, max_depth=8, min_samples_split=5)
model.fit(X_train, y_train)
print("\n🌲 Decision Tree trained successfully.")

# ─────────────────────────────────────────────
# 7. Evaluate Model
# ─────────────────────────────────────────────
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Model Accuracy: {accuracy * 100:.2f}%")
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# ─────────────────────────────────────────────
# 8. Save Model & Encoders
# ─────────────────────────────────────────────
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("💾 model.pkl saved.")

with open("encoders.pkl", "wb") as f:
    pickle.dump(encoders, f)
print("💾 encoders.pkl saved.")

with open("accuracy.pkl", "wb") as f:
    pickle.dump(round(accuracy * 100, 2), f)
print("💾 accuracy.pkl saved.")

# ─────────────────────────────────────────────
# 9. Generate Visualizations
# ─────────────────────────────────────────────
os.makedirs("screenshots", exist_ok=True)

# --- Pass vs Fail Distribution ---
fig, ax = plt.subplots(figsize=(7, 5))
counts = df["Result"].value_counts()
colors = ["#4CAF50", "#F44336"]
ax.bar(counts.index, counts.values, color=colors, edgecolor="black", width=0.5)
ax.set_title("Pass vs Fail Distribution", fontsize=15, fontweight="bold")
ax.set_xlabel("Result", fontsize=12)
ax.set_ylabel("Number of Students", fontsize=12)
for i, (label, val) in enumerate(counts.items()):
    ax.text(i, val + 5, str(val), ha="center", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("screenshots/pass_fail_distribution.png", dpi=150)
plt.close()
print("📸 screenshots/pass_fail_distribution.png saved.")

# --- Feature Distribution by Result ---
cat_cols = ["gender", "lunch", "test preparation course"]
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, col in zip(axes, cat_cols):
    ct = df.groupby([col, "Result"]).size().unstack(fill_value=0)
    ct.plot(kind="bar", ax=ax, color=["#F44336", "#4CAF50"], edgecolor="black", rot=15)
    ax.set_title(col.title(), fontsize=12, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Count")
    ax.legend(title="Result")
plt.suptitle("Pass/Fail Rate by Demographic Feature", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("screenshots/feature_distribution.png", dpi=150)
plt.close()
print("📸 screenshots/feature_distribution.png saved.")

# --- Confusion Matrix ---
cm = confusion_matrix(y_test, y_pred, labels=["Fail", "Pass"])
fig, ax = plt.subplots(figsize=(6, 5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Fail", "Pass"])
disp.plot(ax=ax, colorbar=True, cmap="Blues")
ax.set_title("Confusion Matrix", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig("screenshots/confusion_matrix.png", dpi=150)
plt.close()
print("📸 screenshots/confusion_matrix.png saved.")

print("\n✅ Training complete! All files saved.")
print(f"   Final Accuracy: {accuracy * 100:.2f}%")
