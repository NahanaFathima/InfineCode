# NGO Eligibility Analyzer

A Streamlit-based application that helps assess NGO beneficiary eligibility using a trained machine learning model.

## Project Setup Instructions

### 1. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install streamlit pandas numpy scikit-learn matplotlib seaborn joblib
```

### 3. Prepare the model artifacts

Run the preprocessing and training scripts so the application can load the saved encoder and model files.

```bash
python preprocess.py
python train.py
```

This creates the required files inside the `model/` folder, including:

- `best_model.pkl`
- `encoders.pkl`
- `X_test.pkl`
- `y_test.pkl`

### 4. Launch the app

```bash
streamlit run app.py
```

## Features Implemented

- Home dashboard with summary metrics from the beneficiary dataset.
- Eligibility prediction form for checking a single applicant.
- Confidence score display for each prediction.
- Analytics dashboard with eligibility and employment visualizations.
- Visualizations gallery for charts saved in `data/charts/`.
- Dataset viewer with eligibility filtering and name search.
- Styled UI with a custom dark theme and redesigned sidebar.

## Machine Learning Algorithm Used

The project uses a tree-based classification approach.

- `DecisionTreeClassifier` is trained as one candidate model.
- `RandomForestClassifier` is trained as the primary ensemble model.
- Both models are evaluated on a test split, and the better-performing model is saved as `model/best_model.pkl`.

In practice, the app uses the selected best model for predictions, and the sidebar indicates when the Random Forest model is active.

## Input Features Used For Prediction

The prediction pipeline uses these fields:

- Age
- Family income
- Family members
- Employment status
- Education level
- Disability status

Categorical fields are label-encoded during preprocessing before model training.

## Project Structure

```text
app.py
dataset.py
evaluate.py
main.py
predict.py
preprocess.py
train.py
visualize.py
data/
  beneficiaries.csv
  charts/
model/
```
