import pandas as pd

print("Checking data drift...")

train_data = pd.read_csv("src/data/processed/features.csv")
logs = pd.read_csv("src/logs/prediction_logs.csv")

if logs.empty:
    print("No prediction logs yet.")
    exit()

# Extract input JSON
logs["input"] = logs["input"].apply(eval)
pred_df = pd.json_normalize(logs["input"])

features = ["Runtime", "Meta_score", "No_of_Votes", "Gross", "movie_age"]

print("\nFeature Drift Report:\n")

for col in features:
    train_mean = train_data[col].mean()
    pred_mean = pred_df[col].mean()

    drift = abs(train_mean - pred_mean)

    print(f"{col}: Train={train_mean:.2f}, Live={pred_mean:.2f}, Drift={drift:.2f}")