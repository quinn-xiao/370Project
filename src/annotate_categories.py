import argparse
import pandas as pd
import os

# Function to annotate categories for the articles
def annotate_categories(start_row):
    # Load the CSV file containing the articles data
    processed_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'articles_kamala_harris.csv')
    df = pd.read_csv(processed_file)

    # Get the rows to annotate (100 rows from the starting point)
    end_row = start_row + 100
    annotated_df = df.iloc[start_row - 1:end_row].copy()

    # Annotate each article one at a time
    for idx, row in annotated_df.iterrows():
        print(f"Annotating row {idx + 1}:")
        print(f"Title: {row['title']}")
        print(f"Description: {row['description']}")
        print(f"Source: {row['source']}")
        
        # Ask for the category annotation
        category = input("Enter category for this article (or 'skip' to skip): ")
        
        if category.lower() != 'skip':
            annotated_df.at[idx, 'category'] = category

    # Save the annotated data to the 'data/annotations' folder
    annotated_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'annotations', 'annotated_categories.csv')
    os.makedirs(os.path.dirname(annotated_file), exist_ok=True)
    annotated_df.to_csv(annotated_file, index=False)
    print(f"Annotations saved to '{annotated_file}'.")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Annotate categories for articles.")
    parser.add_argument('start_row', type=int, help="The starting row number for annotations.")
    args = parser.parse_args()

    # Validate the starting row input
    if args.start_row < 1:
        print("Starting row must be a positive integer.")
        return

    # Call the function to annotate the categories
    annotate_categories(args.start_row)

# Entry point of the script
if __name__ == '__main__':
    main()
