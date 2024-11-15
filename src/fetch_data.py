import requests
import json
import argparse
from pathlib import Path
import pandas as pd
import os

# Function to fetch articles from NewsAPI
def fetch_articles(page, query_params):
    base_url = 'https://newsapi.org/v2/everything'

    # Change the path to cache the JSON files in the data/raw/ directory
    source_path = Path(__file__).parent.parent / f'data/raw/articles_cache/articles_{page}.json'
    if not source_path.exists():
        # Ensure the cache directory exists
        cache_dir = source_path.parent
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)

        try:
            response = requests.get(base_url, params=query_params)
            response.raise_for_status()
            articles_data = response.json()
            with open(source_path, 'w') as f:
                json.dump(articles_data, f)
            return articles_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles: {e}")
            return {'articles': []}
    else:
        return json.load(open(source_path, 'r'))

# Main function to get and process the articles
def main():
    # Set up the query parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('api_key', help='Your NewsAPI key')  # Only the API key is now required
    args = parser.parse_args()
    
    # Load the sources directly from the news_sources.json file
    sources_file = Path(__file__).parent.parent / 'data/raw/news_sources.json'
    with open(sources_file, 'r') as f:
        sources_data = json.load(f)
    
    # Extract the source IDs and countries from the sources list
    sources_info = {source['id']: source['country'] for source in sources_data['sources']}
    
    # Set up the query parameters to pull articles related to "Kamala Harris"
    query_params = {
        'apiKey': args.api_key,
        'q': 'Kamala Harris',
        'language': 'en',
        'pageSize': 100,  # maximum per request
        'sortBy': 'relevancy',  # Ensure the most relevant articles
        'sources': ",".join(sources_info.keys())  # Filter articles by the specified sources
    }

    # List to hold the valid articles
    articles = []
    page = 1
    
    # Loop until we have 500 articles or pages are exhausted
    while len(articles) < 500:
        print(f"Fetching page {page}...")
        response = fetch_articles(page, query_params)
        
        # Add valid articles (those with a title that is not '[Removed]')
        for article in response['articles']:
            if article['title'] != '[Removed]':
                # Add the country information to the article
                article['country'] = sources_info.get(article['source']['id'], 'Unknown')
                
                # Add missing fields if they don't exist
                article['category'] = article.get('category', None)  # Default to None if not present
                article['coverage'] = article.get('coverage', None)  # Default to None if not present

                articles.append(article)
            
            # Stop if we have enough articles
            if len(articles) >= 500:
                break
        
        page += 1

    # Process the articles: Remove unwanted fields and clean up data
    for i in articles:
        i['source'] = i['source']['name']
        del i['content']
        del i['urlToImage']
        del i['publishedAt']
    
    # Convert the articles to a pandas DataFrame
    df = pd.DataFrame(articles)
    
    # Reorder columns to make sure 'country' is before 'description' and add missing columns
    df = df[['country', 'source', 'author', 'title', 'description', 'url', 'category', 'coverage']]

    # Save the data to a CSV file in the processed folder
    csv_path = Path(__file__).parent.parent / 'data/processed/articles_kamala_harris.csv'
    df.to_csv(csv_path, index=False)
    print(f"Finished saving articles to '{csv_path}'.")

# Entry point of the script
if __name__ == '__main__':
    main()
