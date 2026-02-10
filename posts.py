from booru_url import get_booru_url
from debug import dprint
import requests
import urllib

def get_posts(query, auth, page, headers, test_mode):
    while True:
        try:
            posts_url = f"{get_booru_url(test_mode)}/posts.json?tags={query}&{str(auth)}&page={page}"
            dprint(f"Execute request to {posts_url}")
            response = requests.get(posts_url, timeout=10, headers=headers)
            return response.json(), response.text
        except requests.exceptions.JSONDecodeError:
            print(f"Server returned non-JSON response: {response.text}")
        except (
            urllib.error.URLError,
            requests.exceptions.RequestException
        ) as exc:
            print(f"Failed to fetch page because of {exc}")
