from debug import dprint, safedumps
from booru_url import get_booru_url
import requests
import json
import urllib.error

# TODO idk if this is the best place to put but also doesn't feel like i should make a new file just for this
def print_tags(g, co, ch, m):
    print(
        f"g: \033[0;34m{g}\033[0m\n"
        f"co: \033[0;35m{co}\033[0m\n"
        f"ch: \033[0;32m{ch}\033[0m\n"
        f"m: \033[0;33m{m}\033[0m\n"
    )

def tag_edit_post(post_id, headers, parsed_input, auth, quiet, edits): 
    uptodate_post = None
    while True:
        try:
            response = requests.get(f"{get_booru_url()}/posts/{post_id}.json", headers=headers)
            uptodate_post = response.json()
            break
        except requests.exceptions.JSONDecodeError:
            print(f"Server returned non-JSON response: {response.text}")
        except (
            urllib.error.URLError,
            requests.exceptions.RequestException
        ) as exc:
            print(f"Failed to fetch page because of {exc}")
    post_tags = uptodate_post["tag_string"]

    new_tags = parsed_input + " " + post_tags
    dprint(f"New tag string: {new_tags}")
    request_data = {
        "old_tag_string": post_tags,
        "tag_string": new_tags
    }
    dprint(f"Request data = {json.dumps(request_data, indent=2)}")
    while True:
        try:
            response = requests.put(f"{get_booru_url()}/posts/{post_id}.json?{str(auth)}", json=request_data, headers=headers)
            updated_post = response.json()
            break
        except requests.exceptions.JSONDecodeError:
            print(f"Server returned non-JSON response: {response.text}")
        except (
            urllib.error.URLError,
            requests.exceptions.RequestException
        ) as exc:
            print(f"Failed to fetch page because of {exc}")

    dprint(f"Server said this: {safedumps(response)}")
    try:
        new_tags_gen = updated_post["tag_string_general"]
        new_tags_copy = updated_post["tag_string_copyright"]
        new_tags_char = updated_post["tag_string_character"]
        new_tags_meta = updated_post["tag_string_meta"]
        if not quiet:
            print(
                "\nTags now:\n"
            )
            print_tags(new_tags_gen, new_tags_copy, new_tags_char, new_tags_meta)
        if response.status_code != 200 and response.status_code != 204:
            print(f"Error {response.status_code}")
        elif response.status_code == 403:
            print("Post forbidden to edit. Skip.")
            ok = True
        else:
            if not quiet:
                print("Edited successfully.")
            edits += 1
            return 1
    except KeyError as exc:
        print(f"Could not edit: {exc}")
        return 0
    return -1
