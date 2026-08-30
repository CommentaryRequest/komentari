import requests
import urllib
from dataclasses import dataclass

@dataclass
class Commentary:
    og_title: str = ""
    og_description: str = ""
    tl_title: str = ""
    tl_description: str = ""

    def is_empty(self):
        return len(self.og_title.strip() + self.og_description.strip() + self.tl_title.strip() + self.tl_description.strip()) == 0

def get_commentary(post_id, client):
    commentary, _ = client.get(f"posts/{post_id}/artist_commentary.json")
    return Commentary(commentary.get("original_title", "").strip(), commentary.get("original_description", "").strip(), commentary.get("translated_title", "").strip(), commentary.get("translated_description", "").strip())

def get_commentary_list(post_ids, client):
    query = "id:" + ",".join([str(i) for i in post_ids])
    commentaries_json, _ = client.get(f"artist_commentaries.json?commit=Search&search[post_tags_match]={query}&limit=200")
    commentaries = {}
    for commentary in commentaries_json:
        commentaries[commentary["post_id"]] = Commentary(commentary["original_title"], commentary["original_description"], commentary["translated_title"], commentary["translated_description"])
    return commentaries
