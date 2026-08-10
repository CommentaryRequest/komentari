import requests
import urllib
from dataclasses import dataclass

@dataclass
class Commentary:
    og_title: str
    og_description: str
    tl_title: str
    tl_description: str

    def is_empty(self):
        return len(self.og_title.strip() + self.og_description.strip()) == 0

def get_commentary(post_id, client):
    commentary, _ = client.get(f"posts/{post_id}/artist_commentary.json")
    return Commentary(commentary.get("original_title", "").strip(), commentary.get("original_description", "").strip(), commentary.get("translated_title", "").strip(), commentary.get("translated_description", "").strip())
