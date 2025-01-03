from booru_url import get_booru_url
import requests
import urllib

def get_posts(query, auth, page, headers):
    while True:
        try:
            return requests.get(f"{get_booru_url()}/posts.json?tags={query}&{str(auth)}&page={page}", timeout=10, headers=headers).json()
        except (
            urllib.error.URLError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError
        ) as exc:
            print(f"Failed to fetch page because of {exc}")
