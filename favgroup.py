import requests

def add_to_favgroup(group_id, post_id, client):
    data = {"post_id": post_id}
    client.put(f"favorite_groups/{group_id}/add_post.json", data)
