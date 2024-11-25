import os
import csv

# Define the paths
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_path = os.path.join(base_path, "data", "annotations")
csv_file = os.path.join(data_path, "annotated_articles.csv")

# Define the categories
categories = [
    "Election Dynamics",
    "Campaign Strategies and Public Engagement",
    "Policy and Governance",
    "Cultural Influence and Public Perception",
    "Technology and Media",
    "Political Disputes and Controversies"
]

def arrange_articles_by_category():
    # Ensure the data path exists
    if not os.path.exists(data_path):
        print(f"Data path does not exist: {data_path}")
        return

    # Dictionary to store rows for each category
    category_rows = {category: [] for category in categories}

    # Read the CSV file and categorize rows
    try:
        with open(csv_file, "r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = row.get("category")
                if category in categories:
                    category_rows[category].append(row)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")
        return
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    # Write rows to separate files for each category
    for category, rows in category_rows.items():
        if rows:  # Only write if there are rows in this category
            category_file = os.path.join(data_path, f"{category.replace(' ', '_')}.csv")
            try:
                with open(category_file, "w", newline='', encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                print(f"Written {len(rows)} rows to {category_file}")
            except Exception as e:
                print(f"Error writing to file {category_file}: {e}")

if __name__ == "__main__":
    arrange_articles_by_category()
