import requests
import settings
from auth import Auth
from booru_url import get_booru_url

def get_commentary(post_id, auth):
    commentary = None
    while True:
        try:
            commentary = requests.get(f"{get_booru_url()}/posts/{post_id}/artist_commentary.json?{str(auth)}").json()
            break
        except (
            urllib.error.URLError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError
        ) as exc:
            print(f"Failed to fetch commentary because of {exc}")
    return commentary.get("original_title", "").strip(), commentary.get("original_description", "").strip()
