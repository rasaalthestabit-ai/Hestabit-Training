import pandas as pd
from sklearn.feature_selection import mutual_info_regression
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression


def mutual_information_selection(X, y, top_k=30):

    mi = mutual_info_regression(X, y)

    mi_scores = pd.Series(mi, index=X.columns)

    mi_scores = mi_scores.sort_values(ascending=False)

    selected_features = mi_scores.head(top_k).index.tolist()

    return selected_features, mi_scores


def rfe_selection(X, y, top_k=20):

    model = LinearRegression()

    rfe = RFE(model, n_features_to_select=top_k)

    rfe.fit(X, y)

    selected_features = X.columns[rfe.support_].tolist()

    return selected_features