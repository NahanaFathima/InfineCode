import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Import our preprocessing function
from preprocess import preprocess_data

def train_model():
    # --- Step 1: Get preprocessed data ---
    X, y, encoders = preprocess_data()

    # --- Step 2: Split data into Training and Testing sets ---
    # We keep 20% of data aside for testing (the model never sees this during training)
    # This way we can fairly evaluate how well the model learned
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,    # 20% for testing, 80% for training
        random_state=42   # Same split every time
    )

    print(f"Training samples: {len(X_train)}")  # 80% of 200 = 160
    print(f"Testing samples:  {len(X_test)}")   # 20% of 200 = 40

    # --- Step 3: Train Decision Tree Model ---
    print("\nTraining Decision Tree...")
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)  # This is where learning happens!
    dt_accuracy = dt_model.score(X_test, y_test)
    print(f"Decision Tree Accuracy: {dt_accuracy * 100:.2f}%")

    # --- Step 4: Train Random Forest Model ---
    # Random Forest = many Decision Trees working together (more accurate!)
    print("\nTraining Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)  # Learning happens here too!
    rf_accuracy = rf_model.score(X_test, y_test)
    print(f"Random Forest Accuracy: {rf_accuracy * 100:.2f}%")

    # --- Step 5: Pick the best model ---
    if rf_accuracy >= dt_accuracy:
        best_model = rf_model
        best_name = "Random Forest"
        best_accuracy = rf_accuracy
    else:
        best_model = dt_model
        best_name = "Decision Tree"
        best_accuracy = dt_accuracy

    print(f"\nBest Model: {best_name} with {best_accuracy * 100:.2f}% accuracy")

    # --- Step 6: Save the best model to a file ---
    os.makedirs("model", exist_ok=True)
    joblib.dump(best_model, "model/best_model.pkl")
    joblib.dump(X_test, "model/X_test.pkl")
    joblib.dump(y_test, "model/y_test.pkl")
    print("Model saved to model/best_model.pkl")

    return best_model, X_test, y_test, best_name, best_accuracy

# Run if this file is executed directly
if __name__ == "__main__":
    model, X_test, y_test, name, accuracy = train_model()
    print(f"\nTraining complete!")
    print(f"Model: {name}")
    print(f"Accuracy: {accuracy * 100:.2f}%")