# Model Interpretation and Explainability

## Overview

This document analyzes the behavior and performance of the trained machine learning model used to predict whether a movie will receive a **high IMDb rating**.

The analysis focuses on:

* Model selection and comparison
* Feature importance and explainability
* Error analysis
* Bias–variance evaluation

The goal is to understand **why the model makes certain predictions** and identify areas where performance can improve.

---

# Model Used

From the model comparison phase, the **Random Forest Classifier** performed the best among the tested algorithms.

The models compared were:

* Logistic Regression
* Random Forest
* LightGBM
* Neural Network (MLP Classifier)

Random Forest achieved the **highest cross-validation F1 score**, making it the best candidate for final deployment and further analysis.

---

# Model Selection Summary

| Model               | CV F1 Score |
| ------------------- | ----------- |
| Logistic Regression | 0.7049      |
| Random Forest       | **0.7445**  |
| LightGBM            | 0.7331      |
| Neural Network      | 0.7342      |

---

# Hyperparameter Tuning

After selecting the best model, hyperparameter tuning was performed using **Optuna** to further improve performance.

For Random Forest, the following hyperparameters are typically optimized:

* **n_estimators** – number of trees
* **max_depth** – maximum depth of trees
* **min_samples_split** – minimum samples required to split
* **min_samples_leaf** – minimum samples in leaf nodes

The objective was to maximize the **F1 Score using 5-fold cross-validation**.

The tuning results are stored in:

```id="tune1"
src/tuning/results.json
```

This step helps improve **model generalization and robustness**.

---

# Model Explainability

Unlike SVM, **Random Forest provides built-in interpretability** through feature importance scores.

To further enhance interpretability, **SHAP (SHapley Additive exPlanations)** can be used.

SHAP is based on **game theory**, where each feature contributes to the prediction outcome.

It helps answer:

* Which features influence predictions the most?
* How does each feature affect the prediction (positively or negatively)?

---

# Feature Importance

Feature importance is computed using tree-based importance scores.

### Key Influential Features:

1. Meta Score
2. Number of Votes
3. Gross Revenue
4. Runtime
5. Movie Age

### Interpretation:

* **Meta Score** → Strongest indicator of high IMDb rating
* **Number of Votes** → Reflects popularity and reliability of rating
* **Gross Revenue** → Indicates commercial success
* **Runtime & Movie Age** → Provide contextual signals

These features confirm that the model is using **meaningful real-world signals**.

---

# SHAP Explainability

If SHAP is used, it provides:

* Global feature importance ranking
* Local explanations for individual predictions
* Visualization of feature impact distribution

Example insights:

* Higher **Meta Score** increases probability of high rating
* Higher **Votes** strongly push predictions toward positive class
* Lower values may reduce confidence

---

# Final Model Evaluation

The selected Random Forest model was evaluated on the test dataset:

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | 0.7577 |
| Precision | 0.7818 |
| Recall    | 0.7890 |
| F1 Score  | 0.7854 |
| ROC-AUC   | 0.8227 |

---

# Error Analysis

To understand model limitations, prediction errors were analyzed.

### Types of Errors:

**False Positives**

* Model predicts high rating, but actual rating is low

**False Negatives**

* Model predicts low rating, but actual rating is high

### Observations:

* Movies with **low vote counts** may be misclassified
* Noisy or missing metadata can affect predictions
* Some edge cases in **mid-range meta scores** cause confusion

This analysis helps guide **future improvements in feature engineering**.

---

# Bias–Variance Analysis

| Metric              | Value  |
| ------------------- | ------ |
| Cross Validation F1 | 0.7445 |
| Test F1 Score       | 0.7854 |

### Interpretation:

* Test score is slightly higher than CV score → good generalization
* No significant overfitting observed
* Model maintains stability across datasets

This indicates a **balanced bias–variance tradeoff**.

---

# Model Strengths

The model demonstrates:

* Strong performance across cross-validation
* Good generalization on unseen data
* Interpretability via feature importance
* Robustness using ensemble learning (Random Forest)

---

# Conclusion

This project demonstrates a complete and production-ready machine learning workflow:

* Model comparison across multiple algorithms
* Automated best model selection
* Hyperparameter tuning using Optuna
* Feature importance and explainability
* Error analysis and performance evaluation

The **Random Forest Classifier** emerged as the best-performing model, achieving strong results across both cross-validation and test datasets.

Explainability analysis confirms that the model relies on **meaningful movie metadata**, ensuring that predictions are both **accurate and interpretable**.

This makes the system suitable for **real-world deployment via API**, with logging and monitoring capabilities already integrated.
