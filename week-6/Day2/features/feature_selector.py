import pandas as pd
import numpy as np

from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

# MUTUAL INFORMATION

def mutual_information_selection(X, y, top_k=30):

    print("Running Mutual Information (classification)...")

    mi = mutual_info_classif(X, y, discrete_features="auto")

    mi_scores = pd.Series(mi, index=X.columns)

    mi_scores = mi_scores.sort_values(ascending=False)

    selected_features = mi_scores.head(top_k).index.tolist()

    return selected_features, mi_scores

# TREE-BASED FEATURE IMPORTANCE

def tree_based_selection(X, y, top_k=30):

    print("Running Tree-based feature selection...")

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X, y)

    importances = pd.Series(
        model.feature_importances_,
        index=X.columns
    )

    importances = importances.sort_values(ascending=False)

    selected_features = importances.head(top_k).index.tolist()

    return selected_features, importances


def rfe_selection(X, y, top_k=20):

    print("Running RFE...")

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    rfe = RFE(model, n_features_to_select=top_k)

    rfe.fit(X, y)

    selected_features = X.columns[rfe.support_].tolist()

    return selected_features


def combined_selection(X, y, top_k=30):

    mi_features, mi_scores = mutual_information_selection(X, y, top_k=top_k*2)
    tree_features, tree_scores = tree_based_selection(X, y, top_k=top_k*2)

    combined = list(set(mi_features + tree_features))
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X[combined], y)

    final_scores = pd.Series(
        model.feature_importances_,
        index=combined
    ).sort_values(ascending=False)

    selected_features = final_scores.head(top_k).index.tolist()

    return selected_features, final_scores