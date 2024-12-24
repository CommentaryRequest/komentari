import requests
import settings
import urllib
from auth import Auth
from booru_url import get_booru_url

def add_to_favgroup(group_id, post_id, auth):
    data = {"post_id": post_id}
    while True:
        try:
            return requests.put(
                f"{get_booru_url()}/favorite_groups/{group_id}/add_post.json?{str(auth)}",
                data=data
            )
        except Exception as exc:
            print(f"Error adding post {post_id} to group {group_id}: {exc}")
