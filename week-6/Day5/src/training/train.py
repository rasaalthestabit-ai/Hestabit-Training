import pandas as pd
import json
import os
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

import seaborn as sns
import matplotlib.pyplot as plt


print("Loading dataset...")

df = pd.read_csv("src/data/processed/features.csv")

print("Dataset shape:", df.shape)


# -----------------------------
# Features
# -----------------------------

features = [
    "Runtime",
    "Meta_score",
    "No_of_Votes",
    "Gross",
    "movie_age"
]

X = df[features]
y = df["target"]


# -----------------------------
# Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------
# Models
# -----------------------------

models = {
    "logistic_regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=2000))
    ]),

    "random_forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),

    "xgboost": XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    ),

    "lightgbm": LGBMClassifier(
        n_estimators=200,
        learning_rate=0.1,
        random_state=42
    ),

    "neural_network": Pipeline([
        ("scaler", StandardScaler()),
        ("model", MLPClassifier(
            hidden_layer_sizes=(128, 64),
            max_iter=300,
            random_state=42
        ))
    ])
}


# -----------------------------
# Cross Validation
# -----------------------------

print("\nRunning CV...\n")

cv_scores = {}

for name, model in models.items():

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="f1"
    )

    cv_scores[name] = scores.mean()

    print(f"{name}: {scores.mean():.4f}")


# -----------------------------
# Select Best Model
# -----------------------------

best_model_name = max(cv_scores, key=cv_scores.get)

print("\nBest model:", best_model_name)


# ✅ Save best model name for tuning
os.makedirs("src/tuning", exist_ok=True)

with open("src/tuning/best_model.json", "w") as f:
    json.dump({"best_model": best_model_name}, f, indent=4)

print("Best model saved -> src/tuning/best_model.json")


# -----------------------------
# Train Best Model
# -----------------------------

best_model = models[best_model_name]

best_model.fit(X_train, y_train)


# -----------------------------
# Evaluation
# -----------------------------

preds = best_model.predict(X_test)

if hasattr(best_model, "predict_proba"):
    probs = best_model.predict_proba(X_test)[:, 1]
else:
    probs = None

metrics = {
    "accuracy": accuracy_score(y_test, preds),
    "precision": precision_score(y_test, preds),
    "recall": recall_score(y_test, preds),
    "f1_score": f1_score(y_test, preds),
}

if probs is not None:
    metrics["roc_auc"] = roc_auc_score(y_test, probs)


print("\nEvaluation Metrics")

for k, v in metrics.items():
    print(k, ":", round(v, 4))


# -----------------------------
# Save Model
# -----------------------------

os.makedirs("src/models", exist_ok=True)

joblib.dump(best_model, "src/models/best_model.pkl")

print("\nModel saved -> src/models/best_model.pkl")


# -----------------------------
# Save Metrics
# -----------------------------

os.makedirs("src/evaluation", exist_ok=True)

with open("src/evaluation/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)


# -----------------------------
# Confusion Matrix
# -----------------------------

cm = confusion_matrix(y_test, preds)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

plt.title(f"Confusion Matrix ({best_model_name})")

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()
plt.show()