import pandas as pd
import json
import os
import optuna

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


print("Loading dataset...")

df = pd.read_csv("src/data/processed/features.csv")

print("Dataset shape:", df.shape)


# ----------------------------
# Load Best Model from train.py
# ----------------------------

with open("src/tuning/best_model.json", "r") as f:
    data = json.load(f)

best_model_name = data["best_model"]

print("Tuning model:", best_model_name)


# ----------------------------
# Features
# ----------------------------

features = [
    "Runtime",
    "Meta_score",
    "No_of_Votes",
    "Gross",
    "movie_age"
]

X = df[features]
y = df["target"]


# ----------------------------
# Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ----------------------------
# Objective Function
# ----------------------------

def objective(trial):

    if best_model_name == "logistic_regression":
        C = trial.suggest_float("C", 0.01, 10, log=True)

        model = Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(C=C, max_iter=2000))
        ])

    elif best_model_name == "random_forest":
        model = RandomForestClassifier(
            n_estimators=trial.suggest_int("n_estimators", 100, 300),
            max_depth=trial.suggest_int("max_depth", 3, 20),
            random_state=42
        )

    elif best_model_name == "xgboost":
        model = XGBClassifier(
            n_estimators=trial.suggest_int("n_estimators", 100, 300),
            max_depth=trial.suggest_int("max_depth", 3, 10),
            learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3),
            eval_metric='logloss',
            random_state=42
        )

    elif best_model_name == "lightgbm":
        model = LGBMClassifier(
            n_estimators=trial.suggest_int("n_estimators", 100, 300),
            learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3),
            random_state=42
        )

    elif best_model_name == "neural_network":
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("model", MLPClassifier(
                hidden_layer_sizes=trial.suggest_categorical(
                    "hidden_layer_sizes",
                    [(64,), (128, 64), (128, 64, 32)]
                ),
                max_iter=300,
                random_state=42
            ))
        ])

    else:
        raise ValueError("Unknown model")

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="f1"
    )

    return scores.mean()


# ----------------------------
# Run Optuna
# ----------------------------

print("\nStarting tuning...")

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

print("Tuning completed.")


# ----------------------------
# Save Results
# ----------------------------

results = {
    "best_model": best_model_name,
    "best_parameters": study.best_params,
    "best_f1_score": study.best_value
}

os.makedirs("src/tuning", exist_ok=True)

with open("src/tuning/results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Results saved -> src/tuning/results.json")