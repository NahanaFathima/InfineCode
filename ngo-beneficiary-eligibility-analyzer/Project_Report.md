# 📄 Project Report
## NGO Beneficiary Eligibility Analyzer
### AI + Python — Task 2

---

## 1. Introduction

### 1.1 Project Background
Non-Governmental Organizations (NGOs) play a vital role in supporting underprivileged communities by providing educational scholarships, food assistance, medical aid, and skill development programs. However, manually reviewing hundreds of applicants to determine eligibility is time-consuming, inconsistent, and prone to human error.

### 1.2 Problem Statement
How can NGOs quickly and accurately identify which applicants qualify for support programs, without spending hours manually reviewing each case?

### 1.3 Solution
This project builds an AI-powered Beneficiary Eligibility Analyzer — a complete end-to-end system that takes applicant information as input and automatically predicts whether the person is eligible for NGO support, along with a confidence score.

---

## 2. Objectives

- Create a realistic beneficiary dataset
- Apply data preprocessing techniques
- Train a machine learning classification model
- Build a REST API to expose the model
- Create an interactive web UI for NGO staff
- Evaluate model performance with standard metrics

---

## 3. Dataset

### 3.1 Dataset Description
A synthetic dataset of 200 applicants was generated with the following features:

| Feature | Type | Example Values |
|---|---|---|
| applicant_name | Text | Ravi Kumar, Fatima Banu |
| age | Integer | 18 – 60 |
| family_income | Integer | ₹50,000 – ₹5,00,000 |
| family_members | Integer | 1 – 10 |
| employment_status | Categorical | Employed, Unemployed, Self-Employed, Student |
| education_level | Categorical | No Education, Primary, Secondary, Undergraduate, Postgraduate |
| disability_status | Categorical | Yes, No |
| eligibility_status | Categorical (Target) | Eligible, Not Eligible |

### 3.2 Eligibility Rules
An applicant is marked **Eligible** if ANY of the following conditions are true:
- Family Income < ₹1,50,000
- Employment Status = "Unemployed"
- Disability Status = "Yes"

### 3.3 Dataset Statistics
| Metric | Value |
|---|---|
| Total Records | 200 |
| Eligible Applicants | 157 (78.5%) |
| Not Eligible Applicants | 43 (21.5%) |
| Average Family Income | ₹2,57,615 |
| Features Used for Training | 6 |

---

## 4. Data Preprocessing

### 4.1 Why Preprocessing?
Machine learning models only understand numbers. Raw data contains text values like "Unemployed" or "Yes" which must be converted to numbers before training.

### 4.2 Steps Performed

**Step 1 — Missing Value Check**
All 200 records were checked for missing values. No missing values were found in the dataset.

**Step 2 — Drop Irrelevant Column**
The `applicant_name` column was dropped as names have no predictive value for eligibility.

**Step 3 — Label Encoding**
All categorical columns were converted to numeric values:

| Column | Encoding |
|---|---|
| employment_status | Employed=0, Self-Employed=1, Student=2, Unemployed=3 |
| education_level | No Education=0, Postgraduate=1, Primary=2, Secondary=3, Undergraduate=4 |
| disability_status | No=0, Yes=1 |
| eligibility_status | Eligible=0, Not Eligible=1 |

**Step 4 — Feature/Target Split**
- Features (X): age, family_income, family_members, employment_status, education_level, disability_status
- Target (y): eligibility_status

---

## 5. Machine Learning

### 5.1 Train-Test Split
The dataset was split into:
- Training set: 160 records (80%)
- Testing set: 40 records (20%)

This ensures the model is evaluated on data it has never seen during training — giving a fair measure of real-world performance.

### 5.2 Models Trained

**Model 1: Decision Tree Classifier**
A Decision Tree learns by asking a series of yes/no questions about the features and building a tree of decisions. It is simple, interpretable, and fast.

**Model 2: Random Forest Classifier**
A Random Forest is an ensemble of 100 Decision Trees. Each tree votes on the prediction and the majority wins. This reduces overfitting and improves accuracy compared to a single tree.

### 5.3 Why Random Forest was Selected
Random Forest was selected as the best model because:
- It combines multiple trees to reduce errors
- It handles class imbalance better
- It provides confidence scores (probability outputs)
- It is more robust on real-world noisy data

---

## 6. Model Evaluation

### 6.1 Results

| Metric | Decision Tree | Random Forest |
|---|---|---|
| Accuracy | 100% | 100% |
| Precision | 100% | 100% |
| Recall | 100% | 100% |

### 6.2 Confusion Matrix (Random Forest)

```
                  Predicted
                  Eligible   Not Eligible
Actual Eligible      30            0
Actual Not Eligible   0           10
```

Zero misclassifications on all 40 test cases.

### 6.3 Why 100% Accuracy?
The dataset was generated with clean, consistent rules (no noise or exceptions). The model easily learned these deterministic patterns. In real-world NGO data with human error and edge cases, accuracy would typically be 85–95%.

### 6.4 Metric Definitions

**Accuracy** — Out of all predictions, what percentage were correct?
Formula: (TP + TN) / Total

**Precision** — Of all "Eligible" predictions, how many were truly Eligible?
Avoids wasting resources on ineligible applicants.

**Recall** — Of all truly Eligible people, how many did we correctly identify?
Most important for NGOs — we don't want to miss someone who needs help.

---

## 7. API Development

### 7.1 Framework
FastAPI was used to build the REST API because it is fast, modern, and automatically generates interactive documentation.

### 7.2 Endpoints Implemented

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /beneficiaries | Retrieve all records |
| GET | /beneficiaries/{id} | Retrieve one record |
| POST | /beneficiaries | Add new record |
| PUT | /beneficiaries/{id} | Update a record |
| DELETE | /beneficiaries/{id} | Delete a record |
| POST | /train | Retrain the model |
| POST | /predict | Predict eligibility |
| GET | /analytics | Summary statistics |

### 7.3 Data Validation
Pydantic models were used to validate all incoming request data. Invalid inputs are automatically rejected with descriptive error messages.

---

## 8. User Interface

### 8.1 Framework
Streamlit was used to build an interactive web UI with a professional dark theme.

### 8.2 Pages

| Page | Description |
|---|---|
| Home | Overview with live statistics and support programs |
| Check Eligibility | Form-based prediction with confidence score |
| Analytics Dashboard | Charts and metrics |
| Visualizations | 4 pre-generated data charts |
| View Dataset | Searchable and filterable dataset table |

### 8.3 UI Features
- Dark gradient background (purple/navy theme)
- Glowing metric cards with color coding
- Gradient result cards (green for Eligible, red for Not Eligible)
- Animated confidence progress bar
- Live stats in sidebar
- Search and filter on dataset page

---

## 9. Data Visualizations

Four charts were generated to understand the dataset:

| Chart | Type | Insight |
|---|---|---|
| Eligibility Distribution | Pie Chart | 78.5% Eligible, 21.5% Not Eligible |
| Income Distribution | Histogram | Income spread across ₹50K–₹5L |
| Education Distribution | Bar Chart | Fairly even distribution across levels |
| Income vs Eligibility | Box Plot | Eligible group has lower median income |

---

## 10. Prediction Workflow

```
User Input (age, income, members, employment, education, disability)
        ↓
Label Encoding (text → numbers using saved encoders)
        ↓
Feature Array Creation (same column order as training)
        ↓
Random Forest Model Prediction
        ↓
Decode Prediction (number → "Eligible" / "Not Eligible")
        ↓
Calculate Confidence Score (max probability from predict_proba)
        ↓
Return Result to User
```

---

## 11. Key Learning Outcomes

Through this project, the following concepts were understood and implemented:

| Concept | Where Applied |
|---|---|
| Dataset Creation | dataset.py |
| Data Cleaning | preprocess.py |
| Label Encoding | preprocess.py |
| Train-Test Split | train.py |
| Decision Tree | train.py |
| Random Forest | train.py |
| Model Evaluation | evaluate.py |
| Prediction Workflow | predict.py |
| REST API Development | main.py |
| UI Development | app.py |
| Data Visualization | visualize.py |

---

## 12. Challenges and Solutions

| Challenge | Solution |
|---|---|
| PowerShell vs CMD differences | Used PowerShell-specific commands (New-Item, .\venv\Scripts\activate) |
| Clipboard restrictions in browser | Files provided as downloadable artifacts |
| Seaborn FutureWarnings | Non-critical warnings, charts generated successfully |
| Class imbalance (157 vs 43) | Noted as a real-world ML challenge; Recall prioritized |

---

## 13. Future Improvements

- Add real NGO datasets for more realistic training
- Implement CSV upload feature for bulk predictions
- Add database (SQLite) for persistent storage
- Deploy to cloud (AWS/GCP/Heroku)
- Add authentication for NGO staff login
- Implement SHAP values for model explainability

---

## 14. Conclusion

The NGO Beneficiary Eligibility Analyzer successfully demonstrates a complete AI application development workflow — from raw data to a deployed prediction API with an interactive UI. The Random Forest model achieved 100% accuracy on the test set, and all required API endpoints were implemented and tested. The Streamlit UI provides an intuitive interface for NGO staff to check eligibility in seconds.

---

**Submitted by:** Nahana Fathima
**Task:** AI + Python — Task 2
**Tools Used:** Python, FastAPI, Scikit-Learn, Pandas, Streamlit, Matplotlib, Seaborn
