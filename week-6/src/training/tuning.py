import pandas as pd
import json
import os
import optuna

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC


print("Loading dataset...")

df = pd.read_csv("src/data/processed/features.csv")

print("Dataset shape:", df.shape)


# ----------------------------
# Features & Target
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
# Train Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ----------------------------
# Optuna Objective
# ----------------------------

def objective(trial):

    C = trial.suggest_float("C", 0.01, 100, log=True)
    gamma = trial.suggest_float("gamma", 0.0001, 1, log=True)
    kernel = trial.suggest_categorical("kernel", ["rbf", "poly", "sigmoid"])

    model = SVC(
        C=C,
        gamma=gamma,
        kernel=kernel,
        probability=True
    )

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="f1"
    )

    return scores.mean()


# ----------------------------
# Run Study
# ----------------------------

print("Starting hyperparameter tuning...")

study = optuna.create_study(direction="maximize")

study.optimize(objective, n_trials=30)

print("Tuning finished.")


# ----------------------------
# Best Parameters
# ----------------------------

best_params = study.best_params
best_score = study.best_value

print("Best parameters:", best_params)
print("Best CV F1:", best_score)


# ----------------------------
# Save Results
# ----------------------------

os.makedirs("src/tuning", exist_ok=True)

results = {
    "best_model": "SVM",
    "best_parameters": best_params,
    "best_f1_score": best_score
}

with open("src/tuning/results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Tuning results saved -> src/tuning/results.json")