# Model Comparison

## Overview

This project implements a machine learning pipeline to predict whether a movie will receive a **high IMDb rating**.
The dataset consists of information about the **Top 1000 IMDb movies**, including runtime, meta score, number of votes, gross revenue, and other metadata.

A classification target was created to identify **highly rated movies**. Multiple machine learning models were trained and compared using **5-fold cross-validation**, followed by **automatic best model selection and hyperparameter tuning**.

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
3. LightGBM
4. Neural Network (MLP Classifier)

Each model was evaluated using:

* **5-fold Cross Validation**
* **F1 Score as the primary metric**

F1 score was chosen because it balances **precision and recall**, which is useful for classification problems.

---

# Cross Validation Results

| Model               | Cross Validation F1 Score |
| ------------------- | ------------------------- |
| Logistic Regression | 0.7049                    |
| Random Forest       | **0.7445**                |
| LightGBM            | 0.7331                    |
| Neural Network      | 0.7342                    |

---

# Best Model Selection

The **Random Forest model** achieved the highest cross-validation F1 score and was selected as the best model.

The best model configuration is saved at:

```
src/tuning/best_model.json
```

---

# Final Model Evaluation (Test Set)

After selecting the best model, evaluation was performed on the **held-out test dataset**.

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | 0.7577 |
| Precision | 0.7818 |
| Recall    | 0.7890 |
| F1 Score  | 0.7854 |
| ROC-AUC   | 0.8227 |

---

# Interpretation of Metrics

### Accuracy

Measures the overall percentage of correct predictions.

### Precision

Indicates how many predicted positive movies were actually high-rated movies.

### Recall

Measures how well the model identifies all high-rated movies.

### F1 Score

The harmonic mean of precision and recall.
Used as the primary evaluation metric.

### ROC-AUC

Measures the model’s ability to distinguish between high-rated and lower-rated movies across different thresholds.

---

# Best Model

The final selected model is:

**Random Forest Classifier**

This model demonstrated the best balance between precision and recall and achieved the highest F1 score during cross-validation.

---

# Model Storage

The trained model is stored at:

```
src/models/best_model.pkl
```

The best model metadata (name and selection details) is stored at:

```
src/tuning/best_model.json
```

---

# Saved Evaluation Metrics

Evaluation metrics are stored in:

```
src/evaluation/metrics.json
```

This ensures **reproducibility and consistent tracking of model performance**.

---

# Pipeline Enhancements

This updated pipeline includes:

* Multiple model comparison
* Automated best model selection
* Hyperparameter tuning (Optuna)
* Model versioning support
* API deployment readiness
* Prediction logging and monitoring

---

# Conclusion

Among all evaluated models, the **Random Forest classifier performed the best**, achieving the highest F1 score during cross-validation and strong performance on the test set.

This pipeline demonstrates a **production-ready ML workflow**, including:

* Feature engineering
* Feature selection
* Cross-validation
* Model comparison
* Automated model selection
* Hyperparameter tuning
* Evaluation tracking
* Deployment readiness

The trained model can now be used for **predicting whether a movie will receive a high IMDb rating**, and is fully integrated into an API-based serving system.
