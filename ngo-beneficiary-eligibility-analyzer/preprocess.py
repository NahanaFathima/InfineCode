import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def preprocess_data():
    # --- Step 1: Load the CSV file ---
    df = pd.read_csv("data/beneficiaries.csv")
    print("Original Data Shape:", df.shape)  # (rows, columns)

    # --- Step 2: Check for missing values ---
    print("\nMissing Values:")
    print(df.isnull().sum())  # Count missing values in each column

    # --- Step 3: Drop the name column ---
    # 'applicant_name' is just an identifier, not useful for prediction
    df = df.drop(columns=["applicant_name"])

    # --- Step 4: Label Encoding ---
    # Convert text columns to numbers so the ML model can understand them

    # These are the columns that contain text
    categorical_columns = [
        "employment_status",
        "education_level",
        "disability_status",
        "eligibility_status"
    ]

    # Create a dictionary to store encoders (we need them later for prediction)
    encoders = {}

    for column in categorical_columns:
        le = LabelEncoder()                        # Create a new encoder
        df[column] = le.fit_transform(df[column])  # Convert text to numbers
        encoders[column] = le                      # Save the encoder
        print(f"\n{column} encoding:")
        # Show what each number means
        for i, class_ in enumerate(le.classes_):
            print(f"  {class_} → {i}")

    # --- Step 5: Separate Features and Target ---
    # Features (X) = what we use to predict
    # Target  (y) = what we want to predict
    X = df.drop(columns=["eligibility_status"])  # Everything except the answer
    y = df["eligibility_status"]                 # Just the answer column

    print("\nFeatures (X) columns:", list(X.columns))
    print("Target  (y) name:     eligibility_status")
    print("\nPreprocessed Data Sample:")
    print(df.head())

    # --- Step 6: Save encoders for later use in prediction ---
    os.makedirs("model", exist_ok=True)
    joblib.dump(encoders, "model/encoders.pkl")
    print("\nEncoders saved to model/encoders.pkl")

    return X, y, encoders

# Run if this file is executed directly
if __name__ == "__main__":
    X, y, encoders = preprocess_data()
    print("\nPreprocessing complete!")
    print(f"Features shape: {X.shape}")
    print(f"Target shape:   {y.shape}")