import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)

def evaluate_model():
    # --- Step 1: Load saved model and test data ---
    model  = joblib.load("model/best_model.pkl")
    X_test = joblib.load("model/X_test.pkl")
    y_test = joblib.load("model/y_test.pkl")

    # --- Step 2: Make predictions on test data ---
    y_pred = model.predict(X_test)

    # --- Step 3: Calculate Metrics ---

    # ACCURACY: Out of all predictions, how many were correct?
    accuracy = accuracy_score(y_test, y_pred)

    # PRECISION: Out of all "Eligible" predictions, how many were truly Eligible?
    # (Avoids giving benefits to people who don't deserve them)
    precision = precision_score(y_test, y_pred)

    # RECALL: Out of all truly Eligible people, how many did we correctly find?
    # (Avoids missing people who genuinely need help)
    recall = recall_score(y_test, y_pred)

    print("=" * 40)
    print("       MODEL EVALUATION RESULTS")
    print("=" * 40)
    print(f"Accuracy  : {accuracy  * 100:.2f}%")
    print(f"Precision : {precision * 100:.2f}%")
    print(f"Recall    : {recall    * 100:.2f}%")

    # --- Step 4: Confusion Matrix ---
    # Shows exactly where the model got confused
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print("                  Predicted")
    print("                  Eligible  Not Eligible")
    print(f"Actual Eligible      {cm[0][0]}          {cm[0][1]}")
    print(f"Actual Not Eligible  {cm[1][0]}          {cm[1][1]}")

    print("\nDetailed Report:")
    print(classification_report(y_test, y_pred, target_names=["Eligible", "Not Eligible"]))

    return accuracy, precision, recall, cm

# Run if this file is executed directly
if __name__ == "__main__":
    accuracy, precision, recall, cm = evaluate_model()