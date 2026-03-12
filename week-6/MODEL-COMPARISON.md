# Model Comparison

## Overview

This project implements a machine learning pipeline to predict whether a movie will receive a **high IMDb rating**.
The dataset consists of information about the **Top 1000 IMDb movies**, including runtime, meta score, number of votes, gross revenue, and other metadata.

A classification target was created to identify **highly rated movies**. Multiple machine learning models were trained and compared using **5-fold cross-validation**.

---

# Dataset

* Total Samples: **969**
* Total Features After Processing: **4129**
* Features Used for Training: **5**
* Training Samples: **775**
* Test Samples: **194**

### Selected Features

The following features were used during model training:

* Runtime
* Meta_score
* No_of_Votes
* Gross
* movie_age

These features capture both **movie popularity and metadata signals**.

---

# Model Training Strategy

The following models were trained and evaluated:

1. Logistic Regression
2. Random Forest
3. Decision Tree
4. Support Vector Machine (SVM)

Each model was evaluated using:

* **5-fold Cross Validation**
* **F1 Score as the primary metric**

F1 score was chosen because it balances **precision and recall**, which is useful for classification problems.

---

# Cross Validation Results

| Model                        | Cross Validation F1 Score |
| ---------------------------- | ------------------------- |
| Logistic Regression          | 0.7049                    |
| Random Forest                | 0.7429                    |
| Decision Tree                | 0.6552                    |
| Support Vector Machine (SVM) | **0.7539**                |

### Best Model

The **Support Vector Machine (SVM)** achieved the highest cross-validation F1 score and was selected as the best model.

---

# Final Model Evaluation (Test Set)

After selecting the best model, evaluation was performed on the **held-out test dataset**.

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | 0.7113 |
| Precision | 0.7190 |
| Recall    | 0.7982 |
| F1 Score  | 0.7565 |
| ROC-AUC   | 0.7915 |

---

# Interpretation of Metrics

### Accuracy

Measures the overall percentage of correct predictions.

### Precision

Indicates how many predicted positive movies were actually high-rated movies.

### Recall

Measures how well the model identifies all high-rated movies.

### F1 Score

The combination of precision and recall.
Used as the primary evaluation metric.

### ROC-AUC

Measures the model’s ability to distinguish between high-rated and lower-rated movies.

---

# Best Model

The final trained model is:

**Support Vector Machine (SVM)**

Saved at:

```
src/models/best_model.pkl
```

---

# Saved Evaluation Metrics

Evaluation metrics are stored in:

```
src/evaluation/metrics.json
```

This file contains the final evaluation metrics for reproducibility and analysis.

---

# Conclusion

Among the evaluated models, **SVM performed the best**, achieving the highest F1 score during cross-validation and strong performance on the test set.

This pipeline demonstrates:

* Feature engineering
* Feature selection
* Cross-validation
* Model comparison
* Automated model selection
* Evaluation and metric tracking

The trained model can now be used for **predicting whether a movie will receive a high IMDb rating**.
