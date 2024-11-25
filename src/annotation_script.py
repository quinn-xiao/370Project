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
    "5": "Technology and Media",
    "6": "Political Disputes and Controversies"
}

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent  # Root project directory
INPUT_FILE = BASE_DIR / "data/processed/kamala_articles_500.csv"
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
    if "coverage" not in df.columns:
        df["coverage"] = ""  # Add a coverage column if not present

    # Explicitly set data types to object to avoid type mismatch warnings
    df["category"] = df["category"].astype("object")
    df["coverage"] = df["coverage"].astype("object")

    # Make a copy of the file in the annotations folder if it doesn't exist
    output_file = OUTPUT_DIR / "annotated_categories.csv"
    if output_file.exists():
        annotated_df = pd.read_csv(output_file)  # Load existing annotations
        # Merge the existing annotations with the new data
        df["category"] = annotated_df["category"]
        df["coverage"] = annotated_df["coverage"]
        print(f"Existing annotations found. Continuing from row {start_row}.")
    else:
        print(f"Working on a new annotated file at {output_file}")
    
    # Start annotating
    for i in range(start_row - 1, len(df)):
        row = df.iloc[i]
        print(f"\nRow {i + 1}:")
        print(f"Title: {row['title']}")
        print(f"Description: {row['description']}")
        print(f"Source: {row['source']}")
        print(f"Current Category: {row['category'] if pd.notna(row['category']) else 'No category assigned.'}")
        print(f"Current Coverage: {row['coverage'] if pd.notna(row['coverage']) else 'No coverage assigned.'}")

        # Annotate the category
        while True:
            print("\nSelect a category:")
            for key, category in CATEGORIES.items():
                print(f"Press {key} for \"{category}\"")
            print("Enter 'q' to quit.")

            choice = input("Your choice: ").strip()
            if choice == "q":
                print("Exiting annotation process.")
                df.to_csv(output_file, index=False)  # Save progress before quitting
                return
            elif choice in CATEGORIES:
                df.at[i, "category"] = CATEGORIES[choice]
                print(f"Category \"{CATEGORIES[choice]}\" assigned to row {i + 1}.")
                break  # Exit the loop after valid input
            else:
                print("Invalid choice. Please try again.")

        # Annotate the coverage
        while True:
            print("\nAssign coverage for this article:")
            print("Press 1 for Positive")
            print("Press 2 for Negative")
            print("Press 3 for Neutral")

            coverage_choice = input("Your choice: ").strip()
            if coverage_choice in ["1", "2", "3"]:
                coverage_mapping = {"1": "Positive", "2": "Negative", "3": "Neutral"}
                df.at[i, "coverage"] = coverage_mapping[coverage_choice]
                print(f"Coverage \"{coverage_mapping[coverage_choice]}\" assigned to row {i + 1}.")
                break  # Exit the loop after valid input
            else:
                print("Invalid coverage choice. Please try again.")

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
