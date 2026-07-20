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

    def is_empty(self):
        return len(self.og_title.strip() + self.og_description.strip()) == 0

def get_commentary(post_id, auth, headers, test_mode):
    commentary = None
    while True:
        try:
            response = requests.get(f"{get_booru_url(test_mode)}/posts/{post_id}/artist_commentary.json?{str(auth)}", headers=headers)
            commentary = response.json()
            break
        except requests.exceptions.JSONDecodeError:
            print(f"Server returned non-JSON response: {response.text}")
        except (
            urllib.error.URLError,
            requests.exceptions.RequestException
        ) as exc:
            print(f"Failed to fetch page because of {exc}")
    return Commentary(commentary.get("original_title", "").strip(), commentary.get("original_description", "").strip(), commentary.get("translated_title", "").strip(), commentary.get("translated_description", "").strip())
