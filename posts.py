from booru_url import get_booru_url
from debug import dprint
from context import NetworkContext
import requests
import urllib

def get_posts(query, page, net_ctx):
    while True:
        try:
            posts_url = f"{get_booru_url(net_ctx.test_mode)}/posts.json?tags={query}&{str(net_ctx.auth)}&page={page}"
            dprint(f"Execute request to {posts_url}")
            response = requests.get(posts_url, timeout=10, headers=net_ctx.headers)
            if "success" in response.json() and not response.json()["success"]:
                print(f"Unsuccessful response: {response.json()}")
            else:
                return response.json(), response.text
        except requests.exceptions.JSONDecodeError:
            print(f"Server returned non-JSON response: {response.text}")
        except (
            urllib.error.URLError,
            requests.exceptions.RequestException
        ) as exc:
            print(f"Failed to fetch page because of {exc}")
