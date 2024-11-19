import requests
import json
import argparse
from pathlib import Path
import pandas as pd
import re

def fetch_articles(page, api_key):
    base_url = 'https://newsapi.org/v2/everything'

    # Load sources from your new news_sources.json file
    sources_file_path = Path(__file__).parent.parent / 'data/raw/news_sources.json'
    with open(sources_file_path, 'r') as f:
        sources_data = json.load(f)

    # Extract the 'id' from each source
    sources_id = [source['id'] for source in sources_data['sources']]
    
    query_params = {
        'apiKey': api_key,
        'sources': ",".join(sources_id),  # Use the extracted source ids
        'q': 'kamala harris',  # Changed to fetch articles about Kamala Harris
        'language': 'en',
        'page': page
    }

    # Ensure the 'cache' directory exists in the new location (data/raw/articles_cache)
    cache_path = Path(__file__).parent.parent / 'data/raw/articles_cache'
    cache_path.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

    # Define the path where the articles will be saved (in cache folder)
    source_path = cache_path / f'articles_{page}.json'
    
    if not source_path.exists():
        try:
            response = requests.get(base_url, params=query_params)
            response.raise_for_status()
            articles_data = response.json()
            with open(source_path, 'w') as f:
                json.dump(articles_data, f)
            return articles_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles: {e}")
    else:
        return json.load(open(source_path, 'r'))
    

def main():
    articles = []
    for page in range(1, 6):
        response = fetch_articles(page, args.api_key)
        # Filter out articles where the title is '[Removed]'
        filtered_articles = [article for article in response['articles'] if article['title'] != '[Removed]']
        articles += filtered_articles

    # Remove newlines and excess whitespace from descriptions
    for article in articles:
        if 'description' in article:
            # Remove newline characters, tabs, and extra spaces from description
            article['description'] = re.sub(r'\s+', ' ', article['description']).strip()

    for i in articles:
        i['source'] = i['source']['name']
        del i['content']
        del i['urlToImage']
        del i['publishedAt']
    
    # Save articles to the new location under 'data/processed' with the name kamala_articles_500.csv
    processed_path = Path(__file__).parent.parent / 'data/processed/kamala_articles_500.csv'
    df = pd.DataFrame(articles)
    
    # Add a row number column starting from 1
    df.insert(0, 'row_number', range(1, len(df) + 1))
    
    # Add empty columns for category and coverage
    df['category'] = ''
    df['coverage'] = ''
    
    df.to_csv(processed_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('api_key', help='Your NewsAPI key')
    args = parser.parse_args()
    main()
