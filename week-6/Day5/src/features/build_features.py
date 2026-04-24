import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

from feature_selector import combined_selection

print("Loading dataset...")

df = pd.read_csv("src/data/processed/final.csv")

print("Dataset shape:", df.shape)

# SEPARATE TARGET

rating = df["IMDB_Rating"]

X = df.drop("IMDB_Rating", axis=1)

# CLEAN RUNTIME

X["Runtime"] = X["Runtime"].str.replace(" min", "", regex=False)
X["Runtime"] = pd.to_numeric(X["Runtime"], errors="coerce")

# CLEAN GROSS

X["Gross"] = X["Gross"].astype(str).str.replace(",", "")
X["Gross"] = pd.to_numeric(X["Gross"], errors="coerce")

# HANDLE MISSING VALUES

X["Gross"] = X["Gross"].fillna(X["Gross"].median())
X["Meta_score"] = X["Meta_score"].fillna(X["Meta_score"].median())
X["Runtime"] = X["Runtime"].fillna(X["Runtime"].median())

X["Released_Year"] = pd.to_numeric(X["Released_Year"], errors="coerce")
X["Released_Year"] = X["Released_Year"].fillna(X["Released_Year"].median())

# FEATURE ENGINEERING 

print("Creating new features...")

X["movie_age"] = 2026 - X["Released_Year"]

X["log_votes"] = np.log1p(X["No_of_Votes"])
X["sqrt_votes"] = np.sqrt(X["No_of_Votes"].clip(lower=0))

X["votes_per_year"] = X["No_of_Votes"] / (X["movie_age"] + 1)

X["gross_per_vote"] = X["Gross"] / (X["No_of_Votes"] + 1)

X["runtime_squared"] = X["Runtime"] ** 2
X["log_runtime"] = np.log1p(X["Runtime"])

# TEXT FEATURES (TF-IDF)

print("Creating TF-IDF features...")

tfidf = TfidfVectorizer(
    max_features=50,
    stop_words="english",
    min_df=5
)

overview_matrix = tfidf.fit_transform(df["Overview"])

overview_df = pd.DataFrame(
    overview_matrix.toarray(),
    columns=tfidf.get_feature_names_out()
)

X = pd.concat([X.reset_index(drop=True), overview_df], axis=1)

# DROP UNUSED / HIGH CARDINALITY COLUMNS

drop_cols = [
    "Poster_Link",
    "Series_Title",
    "Overview",
    "Director",
    "Star1",
    "Star2",
    "Star3",
    "Star4"
]

X.drop(columns=drop_cols, inplace=True)

# ENCODE LOW-CARDINALITY CATEGORICALS

print("Encoding categorical variables...")

categorical_cols = [
    "Certificate",
    "Genre"
]

X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

# SCALE NUMERIC FEATURES

print("Scaling numeric features...")

scaler = StandardScaler()

numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns

X[numeric_cols] = scaler.fit_transform(X[numeric_cols])


# CREATE CLASSIFICATION TARGET

print("Creating classification target...")

median_rating = rating.median()

target = (rating >= median_rating).astype(int)


# TRAIN-TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    target,
    test_size=0.2,
    random_state=42
)

# FEATURE SELECTION

print("Selecting important features...")

selected_features, scores = combined_selection(
    X_train,
    y_train,
    top_k=30
)

# PLOT FEATURE IMPORTANCE

print("Plotting feature importance...")

top_scores = scores.sort_values(ascending=False).head(20)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_scores.values, y=top_scores.index)

plt.title("Top Feature Importance")
plt.tight_layout()
plt.show()


print("Saving feature list...")

with open("src/features/feature_list.json", "w") as f:
    json.dump(selected_features, f, indent=4)


print("Saving engineered dataset...")

X_selected = X[selected_features].copy()
X_selected["target"] = target

X_selected.to_csv("src/data/processed/features.csv", index=False)


print("Feature engineering pipeline completed.")