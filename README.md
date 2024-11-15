# News Article Annotation Project About Kamala Harris

This project helps to collect, process, and annotate news articles fetched using the NewsAPI. 


## Folder Descriptions

### `data/`

- **`raw/`**: Contains the raw data fetched from the NewsAPI.
  - `news_sources.json`: A JSON file that stores details of the fetched news sources.
  - `articles_cache/`: Contains cached JSON files for articles data from different API requests. These files are stored to prevent redundant requests to the API.

- **`processed/`**: Contains cleaned and processed data.
  - `articles_kamala_harris.csv`: A CSV file containing the 500 articles fetched from the NewsAPI, with unnecessary fields removed and columns reordered.
  - `news_sources.csv`: A CSV file containing the fetched news sources, with the added column that specifies the country of origin.

- **`annotations/`**: Contains the annotated data.
  - `annotated_categories.csv`: A CSV file that contains the articles from the `processed` folder with the `category` field annotated.

### `src/`

- **`fetch_data.py`**: Fetches 500 news articles using the NewsAPI. The script makes a request to the NewsAPI to retrieve articles related to a specific query (e.g., "Kamala Harris"). The data is cached to avoid fetching the same data repeatedly.

- **`sources_to_json_and_csv.py`**: Converts and saves the news source data in JSON and CSV format. It fetches sources from the NewsAPI and saves them as a JSON file in the `data/raw/` folder asl well as a CSV file in the `data/processed/` folder.

- **`annotate_categories.py`**: Allows manual annotation of the `category` field for each article. The script takes an input (starting row number) and lets the user annotate 100 rows at a time. It then saves the annotated articles to the `data/annotations/` folder.

- **`annotate_coverage.py`**: This script helps annotate the `coverage` field for each article in a similar manner as the `annotate_categories.py` script.

- **`compute_tfidf.py`**: Computes TF-IDF (Term Frequency-Inverse Document Frequency) scores for the articles. This can be useful for text analysis or understanding the significance of words in the articles.


## Functions Overview

### `fetch_data.py`
- **Main Purpose**: Fetches North American english articles based on a specified query (e.g., "Kamala Harris") using the NewsAPI. The data is cached in the `data/raw/articles_cache/` folder to avoid making repeated requests to the NewsAPI.
  
- **Functionality**: 
  - Fetches 500 articles.
  - Caches the fetched articles in JSON format.
  - Cleans and saves articles into `data/processed/articles_kamala_harris.csv`.

### `sources_to_json_andcsv.py`
- **Main Purpose**: Fetches and saves the available news sources in JSON and CSV format from the NewsAPI. This file contains metadata about news sources like their name, country, and description.
  
- **Functionality**: 
  - Fetches the news sources.
  - Saves the sources as `news_sources.json` in the `data/raw/` folder.
  - Saves the sources as `news_sources.csv` in the `data/processed/` folder.

### `annotate_categories.py`
- **Main Purpose**: Allows manual annotation of the `category` field in the articles' data. It takes a starting row number as input, lets the user annotate 100 rows, and then saves the annotated data to the `data/annotations/` folder.

- **Functionality**: 
  - Prompts the user to input a category for each article.
  - Allows skipping articles if needed.
  - Saves the annotated data in `data/annotations/annotated_categories.csv`.

### `annotate_coverage.py`
- **Main Purpose**: Similar to `annotate_categories.py`, this script can be used to manually annotate the `coverage` field for articles. (Not yet implemented but can be created similarly).

### `compute_tfidf.py`
- **Main Purpose**: Computes TF-IDF scores for articles. This is useful for text analysis and understanding the importance of certain terms in the articles.

- **Functionality**:
  - Computes the TF-IDF scores based on the content of the articles.
  - Outputs the computed TF-IDF scores.
