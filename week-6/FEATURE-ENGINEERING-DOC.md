# Feature Engineering Pipeline Documentation

## Overview

This document describes the feature engineering pipeline implemented for the IMDb Top 1000 Movies dataset. The objective of this pipeline is to transform raw movie metadata into meaningful machine learning features that can be used for predictive modeling.

The pipeline performs the following tasks:

* Data cleaning and preprocessing
* Feature transformation
* Text feature extraction
* Categorical feature encoding
* Feature scaling
* Feature selection
* Feature importance visualization

The final output of the pipeline includes selected features saved in `feature_list.json`.

---

# Dataset Description

The dataset contains information about the top 1000 movies on IMDb.

Important columns include:

| Feature       | Description                          |
| ------------- | ------------------------------------ |
| Poster_Link   | Link to movie poster                 |
| Series_Title  | Name of the movie                    |
| Released_Year | Year the movie was released          |
| Certificate   | Movie certification (U, A, PG, etc.) |
| Runtime       | Duration of the movie                |
| Genre         | Genre of the movie                   |
| IMDB_Rating   | IMDb rating (target variable)        |
| Overview      | Plot summary                         |
| Meta_score    | Metacritic score                     |
| Director      | Director of the movie                |
| Star1–Star4   | Main actors                          |
| No_of_Votes   | Total IMDb votes                     |
| Gross         | Movie gross revenue                  |

The target variable used for modeling is:

```
IMDB_Rating
```

---

# Feature Engineering Pipeline

The feature engineering pipeline is implemented in:

```
src/features/build_features.py
```

Feature selection logic is implemented in:

```
src/features/feature_selector.py
```

---

# Data Cleaning

Several preprocessing steps were applied to ensure data quality.

### Runtime Cleaning

Runtime values originally appear as strings such as:

```
130 min
142 min
```

These were converted into numeric values.

### Gross Revenue Cleaning

Gross revenue values contain commas:

```
46,836,394
```

These were cleaned and converted to numeric values.

### Released Year Conversion

The `Released_Year` column sometimes contains non-numeric values. These were converted to numeric format using:

```
pd.to_numeric(errors="coerce")
```

Missing values were replaced with the column median.

---

# Feature Transformations

Several new features were engineered to improve model performance.

### Movie Age

```
movie_age = current_year - Released_Year
```

This captures how old a movie is.

### Log Transformed Votes

```
log_votes = log(No_of_Votes)
```

This helps reduce skewness in vote distribution.

### Square Root of Votes

```
sqrt_votes = sqrt(No_of_Votes)
```

Useful for stabilizing variance.

### Votes Squared

```
votes_squared = No_of_Votes^2
```

Captures nonlinear relationships.

### Votes Per Year

```
votes_per_year = No_of_Votes / movie_age
```

Shows popularity relative to movie age.

### Rating-Votes Interaction

```
rating_votes_interaction = IMDB_Rating * No_of_Votes
```

Captures interaction between popularity and rating.

### Meta Rating Interaction

```
meta_rating_interaction = Meta_score * IMDB_Rating
```

Combines critic scores with IMDb rating.

### Gross Per Vote

```
gross_per_vote = Gross / No_of_Votes
```

Measures financial performance relative to popularity.

### Runtime Transformations

Additional runtime features were created:

```
runtime_squared
log_runtime
```

---

# Text Feature Extraction

Movie plot summaries (`Overview`) were converted into numerical features using TF-IDF.

TF-IDF (Term Frequency–Inverse Document Frequency) captures the importance of words in movie descriptions.

The pipeline extracts the top 100 most informative words.

```
TfidfVectorizer(max_features=100)
```

These features help capture movie themes and story elements.

---

# Categorical Feature Encoding

Categorical variables such as:

```
Certificate
Genre
Director
Star1
Star2
Star3
Star4
```

were converted into numerical form using **One-Hot Encoding**.

```
pd.get_dummies()
```

This allows machine learning models to interpret categorical data.

---

# Feature Scaling

All numerical features were standardized using:

```
StandardScaler
```

This ensures that features have:

* Mean = 0
* Standard deviation = 1

Scaling prevents features with large magnitudes from dominating the model.

---

# Train-Test Split

The dataset was split into training and testing sets using:

```
train_test_split(test_size=0.2, random_state=42)
```

This produces:

```
X_train
X_test
y_train
y_test
```

80% of the data is used for training and 20% for testing.

---

# Feature Selection

Feature selection was performed using **Mutual Information**.

Mutual Information measures how much information each feature provides about the target variable.

The top 30 most informative features were selected.

This process helps:

* Reduce overfitting
* Improve model performance
* Remove irrelevant features

---

# Feature Importance Visualization

A feature importance plot was generated using:

```
Seaborn barplot
```

This visualization shows the most influential features contributing to the prediction of IMDb ratings.

---

# Output Files

The pipeline generates the following outputs:

```
src/features/feature_list.json
```

This file contains the selected features used for model training.

Example:

```
[
 "No_of_Votes",
 "log_votes",
 "votes_per_year",
 "Meta_score",
 "gross_per_vote"
]
```

---

# Pipeline Summary

The feature engineering pipeline performs the following steps:

1. Load cleaned dataset
2. Clean and transform numeric fields
3. Generate new engineered features
4. Extract text features using TF-IDF
5. Encode categorical variables
6. Normalize numerical features
7. Split dataset into training and testing sets
8. Perform feature selection
9. Save selected feature list

This pipeline prepares the dataset for machine learning model training.

---

# Conclusion

Feature engineering plays a critical role in improving machine learning performance. By transforming raw movie metadata into meaningful numerical representations, the pipeline enables models to better understand patterns influencing IMDb ratings.

The resulting feature set provides a robust foundation for the next stage of the machine learning pipeline: **model training and evaluation**.
