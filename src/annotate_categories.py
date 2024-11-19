import os
import pandas as pd
from pathlib import Path
import numpy as np

# Define categories
CATEGORIES = {
    "1": "Election Dynamics",
    "2": "Campaign Strategies and Public Engagement",
    "3": "Policy and Governance",
    "4": "Cultural Influence and Public Perception",
    "5": "Endorsements and Opposition",
    "6": "Technology, Media, and Communication"
}

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent  # Root project directory
INPUT_FILE = BASE_DIR / "data/processed/articles_kamala_harris.csv"
OUTPUT_DIR = BASE_DIR / "data/annotations"

def annotate_categories(start_row):
    # Ensure the annotations directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load the CSV file
    if not INPUT_FILE.exists():
        print(f"Error: Input file not found at {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)
    if "category" not in df.columns:
        df["category"] = ""  # Add a category column if not present

    # Make a copy of the file in the annotations folder
    output_file = OUTPUT_DIR / "annotated_categories.csv"
    df.to_csv(output_file, index=False)
    print(f"Working on a copy of the file saved at {output_file}")

    # Start annotating
    for i in range(start_row - 1, len(df)):  
        row = df.iloc[i]
        print(f"\nRow {i + 1}:")
        print(f"Title: {row['title']}")
        print(f"Description: {row['description']}")
        print(f"Source: {row['source']}")
        print(f"Current Category: {row['category'] if pd.notna(row['category']) else 'No category assigned.'}")

        # If a category exists, ask if it should be changed
        if pd.notna(row["category"]):
            change = input("This article already has a category. Do you want to change it? (y/n): ").strip().lower()
            if change != "y":
                continue
        else:
            print("No category assigned yet.")

        # Show options and get user input
        print("\nSelect a category:")
        for key, category in CATEGORIES.items():
            print(f"Press {key} for \"{category}\"")
        print("Enter 'q' to quit.")

        choice = input("Your choice: ").strip()
        if choice == "q":
            print("Exiting annotation process.")
            break
        elif choice in CATEGORIES:
            df.at[i, "category"] = CATEGORIES[choice]
            print(f"Category \"{CATEGORIES[choice]}\" assigned to row {i + 1}.")
        else:
            print("Invalid choice. Please try again.")

    # Save the updated file
    df.to_csv(output_file, index=False)
    print(f"\nAnnotation complete. File saved at {output_file}")

if __name__ == "__main__":
    # Get starting row
    try:
        start_row = int(input("Enter the starting row number: ").strip())
    except ValueError:
        print("Invalid input. Please enter a valid row number.")
        exit(1)

    annotate_categories(start_row)
