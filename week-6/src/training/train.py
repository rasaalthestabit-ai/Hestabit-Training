import pandas as pd
import json
import os
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

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
# Select features
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
# Train/Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)


# -----------------------------
# Models
# -----------------------------

models = {
    "logistic_regression": LogisticRegression(max_iter=2000),
    "random_forest": RandomForestClassifier(n_estimators=200),
    "decision_tree": DecisionTreeClassifier(),
    "svm": SVC(probability=True)
}


print("\nRunning 5-fold cross validation...\n")

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

    print(f"{name} CV F1: {scores.mean():.4f}")


# -----------------------------
# Select Best Model
# -----------------------------

best_model_name = max(cv_scores, key=cv_scores.get)

print("\nBest model:", best_model_name)

best_model = models[best_model_name]


# Train best model
best_model.fit(X_train, y_train)


# -----------------------------
# Evaluation
# -----------------------------

preds = best_model.predict(X_test)
probs = best_model.predict_proba(X_test)[:, 1]

metrics = {
    "accuracy": accuracy_score(y_test, preds),
    "precision": precision_score(y_test, preds),
    "recall": recall_score(y_test, preds),
    "f1_score": f1_score(y_test, preds),
    "roc_auc": roc_auc_score(y_test, probs)
}

print("\nEvaluation Metrics")

for k, v in metrics.items():
    print(k, ":", round(v, 4))


# -----------------------------
# Save Model
# -----------------------------

os.makedirs("src/models", exist_ok=True)

joblib.dump(best_model, "src/models/best_model.pkl")

print("\nBest model saved -> src/models/best_model.pkl")


# -----------------------------
# Save Metrics
# -----------------------------

os.makedirs("src/evaluation", exist_ok=True)

with open("src/evaluation/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Metrics saved -> src/evaluation/metrics.json")


# -----------------------------
# Confusion Matrix
# -----------------------------

cm = confusion_matrix(y_test, preds)

plt.figure(figsize=(6,5))

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

plt.title(f"Confusion Matrix ({best_model_name})")

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()

plt.show()

