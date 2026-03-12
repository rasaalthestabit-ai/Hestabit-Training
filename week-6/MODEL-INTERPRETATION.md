# Model Interpretation and Explainability

## Overview

This document analyzes the behavior and performance of the trained machine learning model used to predict whether a movie will receive a **high IMDb rating**.

The analysis focuses on:

* Hyperparameter tuning
* Model explainability using SHAP
* Feature importance
* Error analysis
* Bias–variance evaluation

The goal is to understand **why the model makes certain predictions** and identify areas where performance can improve.

---

# Model Used

From the model comparison phase, the **Support Vector Machine (SVM)** performed the best among the tested algorithms.

The models compared were:

* Logistic Regression
* Random Forest
* Decision Tree
* Support Vector Machine (SVM)

SVM achieved the **highest cross-validation F1 score**, making it the best candidate for further optimization.

---

# Hyperparameter Tuning

To improve the model performance, hyperparameter tuning was performed using **Optuna**.

Hyperparameters explored:

* **C** – regularization strength
* **gamma** – kernel influence
* **kernel** – SVM kernel type

The objective was to maximize the **F1 Score using 5-fold cross-validation**.

Example parameter search space:

* C: 0.01 → 100
* gamma: 0.0001 → 1
* kernel: rbf, poly, sigmoid

The tuning process ran multiple trials and selected the combination that produced the highest cross-validation performance.

The results of tuning are stored in:

```id="k5v4ht"
/src/tuning/results.json
```

Hyperparameter tuning helps the model achieve **better generalization and improved predictive performance**.

---

# Model Explainability

Machine learning models can behave like black boxes, making it difficult to understand why a prediction was made.

To interpret the model's behavior, explainability techniques were applied using **SHAP (SHapley Additive exPlanations)**.

SHAP is based on concepts from **Game Theory**, where each feature contributes to the final prediction similarly to how players contribute to a game's outcome.

SHAP helps answer questions such as:

* Which features influence predictions the most?
* How does each feature push predictions higher or lower?

---

# SHAP Summary Plot

A SHAP summary plot was generated to visualize the impact of each feature across all predictions.

The plot displays:

* Feature importance ranking
* Direction of feature influence
* Distribution of SHAP values

Features appearing higher in the plot contribute more strongly to model predictions.

Example insights observed:

* Higher **Meta Score** strongly increases the probability of predicting a highly rated movie.
* Higher **Number of Votes** generally increases the predicted rating probability.
* **Runtime** and **movie age** have smaller but noticeable effects.

This visualization provides a global view of how the model uses features to make predictions.

---

# Feature Importance

Feature importance was calculated using the **average absolute SHAP value** for each feature.

The most influential features typically included:

1. Meta Score
2. Number of Votes
3. Runtime
4. Movie Age
5. Gross Revenue

Interpretation:

* Movies with higher **Meta Scores** are more likely to receive higher IMDb ratings.
* Movies with more **user votes** tend to be more popular and therefore often receive higher ratings.
* **Movie age** can influence ratings because older classics often accumulate higher ratings over time.

These insights confirm that the model is relying on **meaningful movie metadata rather than random noise**.

---

# Error Analysis

To better understand the model’s weaknesses, prediction errors were analyzed.

Two types of errors occur in classification:

**False Positives**

The model predicts a movie will have a high rating, but the actual rating is lower.

**False Negatives**

The model predicts a lower rating, but the movie actually has a high rating.

An **error analysis heatmap** was generated to examine correlations between features and prediction mistakes.

This helps identify patterns such as:

* Movies with very few votes being misclassified
* Movies with missing or noisy metadata causing prediction errors
* Certain runtime ranges leading to incorrect predictions

Understanding these patterns helps guide **future feature engineering improvements**.

---

# Bias–Variance Analysis

Bias–variance analysis helps determine whether a model is:

* Too simple (high bias)
* Too complex (high variance)

The model evaluation results were compared:

| Metric              | Value |
| ------------------- | ----- |
| Cross Validation F1 | ~0.75 |
| Test F1 Score       | ~0.76 |

Because the cross-validation score and test score are close, the model shows **good generalization**.

This indicates:

* Low overfitting
* Stable learning behavior
* Balanced bias and variance

---

# Model Strengths

The model demonstrates several strengths:

* Stable performance across cross-validation folds
* Strong predictive power using a small number of features
* Meaningful feature influence based on real movie metadata
* Good balance between bias and variance

---

# Potential Improvements

Future improvements could include:

* Incorporating **more textual features** from movie descriptions
* Using **advanced embeddings** from movie overviews
* Testing additional models such as **Gradient Boosting or XGBoost**
* Expanding the dataset to include more movies

These improvements could further increase prediction accuracy.

---

# Conclusion

This project demonstrates a full machine learning workflow including:

* Feature engineering
* Model training
* Model comparison
* Hyperparameter tuning
* Explainable AI
* Error analysis

The **Support Vector Machine (SVM)** model provided the best overall performance.

Explainability techniques confirmed that the model relies on **meaningful movie metadata**, and error analysis provided insights for future improvements.

This analysis ensures that the model is not only accurate but also **interpretable and trustworthy**.
