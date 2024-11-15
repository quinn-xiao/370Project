import json
import argparse
import os
import csv
from newsapi import NewsApiClient

# Set up argument parser
parser = argparse.ArgumentParser(description="Fetch English news sources from the U.S. and Canada.")
parser.add_argument('api_key', help="Your News API key")  # Positional argument for the API key
args = parser.parse_args()

# Initialize the News API client with the provided API key
newsapi = NewsApiClient(api_key=args.api_key)

# Fetch sources in English from U.S. and Canada
sources_us = newsapi.get_sources(language='en', country='us')
sources_ca = newsapi.get_sources(language='en', country='ca')

# Label the country of each source
for source in sources_us['sources']:
    source['country'] = 'us'
for source in sources_ca['sources']:
    source['country'] = 'ca'

# Combine U.S. and Canadian sources into one list
sources = sources_us['sources'] + sources_ca['sources']

# Create a dictionary in the specified JSON format
data = {
    "status": "ok",
    "sources": sources
}

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the full path to the JSON file in the 'data/raw/' directory
json_path = os.path.join(script_dir, '..', 'data', 'raw', 'news_sources.json')

# Ensure that the 'data/raw/' directory exists
os.makedirs(os.path.dirname(json_path), exist_ok=True)

# Save the data to a JSON file
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"JSON file has been created at: {json_path}")

# Define the full path to the CSV file in the 'data/processed/' directory
csv_path = os.path.join(script_dir, '..', 'data', 'processed', 'news_sources.csv')

# Ensure that the 'data/processed/' directory exists
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

# Write the data to a CSV file
with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['id', 'name', 'country', 'description', 'url', 'category']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the source data to the CSV file
    for source in sources:
        # Extract the relevant fields and write them
        writer.writerow({
            'id': source['id'],
            'name': source['name'],
            'country': source['country'],
            'description': source.get('description', ''),
            'url': source['url'],
            'category': source.get('category', '')
        })

print(f"CSV file has been created at: {csv_path}")
