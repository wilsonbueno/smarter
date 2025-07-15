# Smarter Social Crawler

This repository provides a simple command line tool to collect data from
Twitter, Reddit, and YouTube using their official APIs.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Set the required environment variables for each service:

- `TWITTER_BEARER_TOKEN` – Twitter API bearer token
- `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` – credentials for Reddit
- `REDDIT_USER_AGENT` – user agent for Reddit requests
- `YOUTUBE_API_KEY` – YouTube Data API key

Run the crawler specifying the service and search parameters.

Examples:

```bash
python social_crawler.py twitter "python" --max-results 5
python social_crawler.py reddit python --limit 5
python social_crawler.py youtube "python tutorial" --max-results 5
```

Each command prints the JSON response from the API.
