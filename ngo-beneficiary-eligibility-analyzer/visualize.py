import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visualizations():
    # --- Load dataset ---
    df = pd.read_csv("data/beneficiaries.csv")

    # Create folder to save charts
    os.makedirs("data/charts", exist_ok=True)

    # --- Set a nice style for all charts ---
    sns.set_theme(style="whitegrid")

    # ============================================================
    # Chart 1: Eligibility Distribution (Pie Chart)
    # ============================================================
    plt.figure(figsize=(6, 6))
    counts = df["eligibility_status"].value_counts()
    plt.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",        # Show percentage on each slice
        colors=["#2ecc71", "#e74c3c"],
        startangle=90
    )
    plt.title("Eligibility Distribution")
    plt.savefig("data/charts/eligibility_distribution.png")
    plt.close()
    print("Chart 1 saved: Eligibility Distribution")

    # ============================================================
    # Chart 2: Income Distribution (Histogram)
    # ============================================================
    plt.figure(figsize=(8, 5))
    sns.histplot(df["family_income"], bins=20, color="#3498db", kde=True)
    # kde=True adds a smooth curve over the histogram
    plt.title("Family Income Distribution")
    plt.xlabel("Family Income")
    plt.ylabel("Number of Applicants")
    plt.savefig("data/charts/income_distribution.png")
    plt.close()
    print("Chart 2 saved: Income Distribution")

    # ============================================================
    # Chart 3: Education Level Distribution (Bar Chart)
    # ============================================================
    plt.figure(figsize=(8, 5))
    edu_counts = df["education_level"].value_counts()
    sns.barplot(x=edu_counts.index, y=edu_counts.values, palette="viridis")
    plt.title("Education Level Distribution")
    plt.xlabel("Education Level")
    plt.ylabel("Number of Applicants")
    plt.xticks(rotation=15)       # Rotate labels so they don't overlap
    plt.savefig("data/charts/education_distribution.png")
    plt.close()
    print("Chart 3 saved: Education Level Distribution")

    # ============================================================
    # Chart 4: Income vs Eligibility (Box Plot)
    # ============================================================
    plt.figure(figsize=(8, 5))
    sns.boxplot(
        x="eligibility_status",
        y="family_income",
        data=df,
        palette={"Eligible": "#2ecc71", "Not Eligible": "#e74c3c"}
    )
    plt.title("Income vs Eligibility Status")
    plt.xlabel("Eligibility Status")
    plt.ylabel("Family Income")
    plt.savefig("data/charts/income_vs_eligibility.png")
    plt.close()
    print("Chart 4 saved: Income vs Eligibility")

    print("\nAll charts saved to data/charts/")
    return "Charts generated successfully!"

# Run if this file is executed directly
if __name__ == "__main__":
    generate_visualizations()