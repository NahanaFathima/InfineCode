import pandas as pd
import numpy as np
import os

# Set a random seed so we get the same data every time we run this
np.random.seed(42)

# Number of applicants we want to generate
NUM_RECORDS = 200

# --- Define possible values for each column ---
names = [
    "Ravi Kumar", "Priya Nair", "Arjun Menon", "Fatima Banu", "Suresh Babu",
    "Lakshmi Devi", "Mohammed Ali", "Anitha Thomas", "Vijay Raj", "Sneha Pillai",
    "Rahul Das", "Meera Krishnan", "Arun Sharma", "Divya Nair", "Sanjay Patel",
    "Rekha Iyer", "Manoj Tiwari", "Pooja Singh", "Deepak Nair", "Kavya Menon"
]

employment_options = ["Employed", "Unemployed", "Self-Employed", "Student"]
education_options  = ["No Education", "Primary", "Secondary", "Undergraduate", "Postgraduate"]
disability_options = ["Yes", "No"]

# --- Generate random data for each column ---
data = {
    "applicant_name":      np.random.choice(names, NUM_RECORDS),
    "age":                 np.random.randint(18, 60, NUM_RECORDS),
    "family_income":       np.random.randint(50000, 500000, NUM_RECORDS),
    "family_members":      np.random.randint(1, 10, NUM_RECORDS),
    "employment_status":   np.random.choice(employment_options, NUM_RECORDS),
    "education_level":     np.random.choice(education_options, NUM_RECORDS),
    "disability_status":   np.random.choice(disability_options, NUM_RECORDS),
}

# --- Create a DataFrame (think of it as a table in Python) ---
df = pd.DataFrame(data)

# --- Define eligibility rules ---
# A person is Eligible if ANY of these are true:
# 1. Family income is less than 150,000
# 2. They are Unemployed
# 3. They have a disability
def determine_eligibility(row):
    if row["family_income"] < 150000:
        return "Eligible"
    if row["employment_status"] == "Unemployed":
        return "Eligible"
    if row["disability_status"] == "Yes":
        return "Eligible"
    return "Not Eligible"

df["eligibility_status"] = df.apply(determine_eligibility, axis=1)

# --- Save to CSV ---
os.makedirs("data", exist_ok=True)
df.to_csv("data/beneficiaries.csv", index=False)

print(f"Dataset created with {len(df)} records!")
print(df.head())  # Show first 5 rows
print("\nEligibility counts:")
print(df["eligibility_status"].value_counts())