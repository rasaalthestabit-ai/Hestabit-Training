import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

print("Loading dataset...")

df = pd.read_csv("src/data/processed/features.csv")

features = [
    "Runtime",
    "Meta_score",
    "No_of_Votes",
    "Gross",
    "movie_age"
]

X = df[features]
y = df["target"]

print("Loading trained model...")

model = joblib.load("src/models/best_model.pkl")


X_sample = shap.sample(X, 100, random_state=42)

print("Running SHAP explainability...")

explainer = shap.Explainer(model.predict, X_sample)

shap_values = explainer(X_sample)


print("Generating SHAP summary plot...")

shap.plots.beeswarm(shap_values)

plt.show()

print("Generating feature importance chart...")

importance = np.abs(shap_values.values).mean(axis=0)

importance_df = pd.DataFrame({
    "feature": features,
    "importance": importance
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

plt.figure(figsize=(8,5))

sns.barplot(
    x="importance",
    y="feature",
    data=importance_df
)

plt.title("Feature Importance (SHAP)")
plt.tight_layout()
plt.show()

print("Running error analysis...")

preds = model.predict(X)

errors = preds != y

error_df = X.copy()
error_df["error"] = errors.astype(int)

corr = error_df.corr()

plt.figure(figsize=(8,6))

sns.heatmap(
    corr,
    cmap="coolwarm"
)

plt.title("Error Analysis Heatmap")
plt.tight_layout()
plt.show()