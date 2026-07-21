import requests
from booru_url import get_booru_url

def add_to_favgroup(group_id, post_id, net_ctx):
    data = {"post_id": post_id}
    while True:
        try:
            return requests.put(
                f"{get_booru_url(net_ctx.test_mode)}/favorite_groups/{group_id}/add_post.json?{str(net_ctx.auth)}",
                data=data,
                headers=net_ctx.headers
            )
        except Exception as exc:
            print(f"Error adding post {post_id} to group {group_id}: {exc}")
