import requests
import settings
import urllib
from auth import Auth
from booru_url import get_booru_url
from dataclasses import dataclass

@dataclass
class Commentary:
    og_title: str
    og_description: str
    tl_title: str
    tl_description: str

def get_commentary(post_id, auth, headers):
    commentary = None
    while True:
        try:
            response = requests.get(f"{get_booru_url()}/posts/{post_id}/artist_commentary.json?{str(auth)}", headers=headers)
            commentary = response.json()
            break
        except (
            urllib.error.URLError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ChunkedEncodingError
        ) as exc:
            print(f"Failed to fetch commentary because of {exc}")
        except requests.exceptions.JSONDecodeError:
            print(f"Server returned non-JSON response: {response.text}")
    return Commentary(commentary.get("original_title", "").strip(), commentary.get("original_description", "").strip(), commentary.get("translated_title", "").strip(), commentary.get("translated_description", "").strip())
