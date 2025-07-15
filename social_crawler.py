import argparse
import os
import requests


class TwitterCrawler:
    BASE_URL = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    def search(self, query: str, max_results: int = 10):
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        params = {"query": query, "max_results": max_results}
        resp = requests.get(self.BASE_URL, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()


class RedditCrawler:
    BASE_URL = "https://oauth.reddit.com"

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.token = self.get_token()

    def get_token(self):
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        data = {"grant_type": "client_credentials"}
        headers = {"User-Agent": self.user_agent}
        resp = requests.post("https://www.reddit.com/api/v1/access_token",
                             auth=auth, data=data, headers=headers)
        resp.raise_for_status()
        token = resp.json()["access_token"]
        return token

    def subreddit_new(self, subreddit: str, limit: int = 10):
        headers = {
            "Authorization": f"bearer {self.token}",
            "User-Agent": self.user_agent,
        }
        url = f"{self.BASE_URL}/r/{subreddit}/new"
        params = {"limit": limit}
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()


class YouTubeCrawler:
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: str, max_results: int = 5):
        params = {
            "part": "snippet",
            "q": query,
            "maxResults": max_results,
            "key": self.api_key,
        }
        resp = requests.get(self.BASE_URL, params=params)
        resp.raise_for_status()
        return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Simple social media crawler")
    subparsers = parser.add_subparsers(dest="service", required=True)

    twitter_p = subparsers.add_parser("twitter", help="Search recent tweets")
    twitter_p.add_argument("query", help="Search query")
    twitter_p.add_argument("--max-results", type=int, default=10, dest="max_results")

    reddit_p = subparsers.add_parser("reddit", help="Get new posts from subreddit")
    reddit_p.add_argument("subreddit", help="Subreddit name")
    reddit_p.add_argument("--limit", type=int, default=10)

    yt_p = subparsers.add_parser("youtube", help="Search YouTube videos")
    yt_p.add_argument("query", help="Search query")
    yt_p.add_argument("--max-results", type=int, default=5, dest="max_results")

    args = parser.parse_args()

    if args.service == "twitter":
        token = os.environ.get("TWITTER_BEARER_TOKEN")
        if not token:
            raise SystemExit("TWITTER_BEARER_TOKEN env var not set")
        crawler = TwitterCrawler(token)
        data = crawler.search(args.query, args.max_results)
        print(data)
    elif args.service == "reddit":
        cid = os.environ.get("REDDIT_CLIENT_ID")
        secret = os.environ.get("REDDIT_CLIENT_SECRET")
        ua = os.environ.get("REDDIT_USER_AGENT", "social-crawler")
        if not cid or not secret:
            raise SystemExit("REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET env vars required")
        crawler = RedditCrawler(cid, secret, ua)
        data = crawler.subreddit_new(args.subreddit, args.limit)
        print(data)
    elif args.service == "youtube":
        key = os.environ.get("YOUTUBE_API_KEY")
        if not key:
            raise SystemExit("YOUTUBE_API_KEY env var not set")
        crawler = YouTubeCrawler(key)
        data = crawler.search(args.query, args.max_results)
        print(data)


if __name__ == "__main__":
    main()
