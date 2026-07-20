from debug import dprint, safedumps
from booru_url import get_booru_url
from context import PostInfo
import requests
import json
import urllib.error

# TODO idk if this is the best place to put but also doesn't feel like i should make a new file just for this
def print_tags(post):
    print(
        f"g: \033[0;34m{' '.join(post.gentags)}\033[0m\n"
        f"co: \033[0;35m{' '.join(post.copytags)}\033[0m\n"
        f"ch: \033[0;32m{' '.join(post.chartags)}\033[0m\n"
        f"m: \033[0;33m{' '.join(post.metatags)}\033[0m\n"
    )

def tag_edit_post(post_id, headers, parsed_input, auth, quiet, edits, test_mode):
    request_data = {
        "post": {
            "old_tag_string": "",
            "tag_string": parsed_input
        }
    }

    dprint(f"Request data = {json.dumps(request_data, indent=2)}")

    while True:
        try:
            response = requests.put(
                f"{get_booru_url(test_mode)}/posts/{post_id}.json?{str(auth)}",
                json=request_data,
                headers=headers
            )
            updated_post = response.json()
            break

        except requests.exceptions.JSONDecodeError:
            print(f"Server returned non-JSON response: {response.text}")

        except (
            urllib.error.URLError,
            requests.exceptions.RequestException
        ) as exc:
            print(f"Failed to edit post because of {exc}")

    dprint(f"Server said this: {safedumps(response)}")

    try:
        updated_post = PostInfo.from_json(updated_post)

        if not quiet:
            print("\nTags now:\n")
            print_tags(updated_post)

        if response.status_code not in (200, 204):
            print(f"Error {response.status_code}")

        elif response.status_code == 403:
            print("Post forbidden to edit. Skip.")
            return 0

        else:
            if not quiet:
                print("Edited successfully.")

            edits += 1
            return 1

    except KeyError as exc:
        print(f"Could not edit: {exc}")
        return 0

    return -1
