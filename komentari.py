#!/usr/bin/python3

from auth import Auth
from booru_url import get_booru_url
from commentary import get_commentary
import requests
import urllib.error
import urllib
import settings
import parser
import json
import sys
import argparse

__version__ = "1.2.1"

def dprint(message):
    if not settings.DEBUGMODE:
        return
    print(f"dbg: {message}")

def main():
    print(f"komentari {__version__} is up")

    if settings.TESTMODE:
        print("=== RUNNING IN TEST MODE ===")

    dprint("Debug mode enabled")

    aparser = argparse.ArgumentParser()
    aparser.add_argument("--page", type=int, default=1)
    aparser.add_argument("--query", type=str, default="-commentary+-commentary_request")
    args = aparser.parse_args()

    print(f"Query = {args.query}")

    auth = Auth()

    page = args.page
    edits = 0
    try:
        while True:
            print(f"Now gardening page {page}")
            posts = None
            while True:
                try:
                    posts = requests.get(f"{get_booru_url()}/posts.json?tags={args.query}&{str(auth)}&page={page}", timeout=10).json()
                    break
                except (
                    urllib.error.URLError,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError
                ) as exc:
                    print(f"Failed to fetch page because of {exc}")

            for post in posts:
                dprint(f"Working with post = {json.dumps(post, indent=2)}")
                post_id = post["id"]
                post_tags_ini_gen = post["tag_string_general"]
                post_tags_ini_copy = post["tag_string_copyright"]
                post_tags_ini_char = post["tag_string_character"]
                post_tags_ini_meta = post["tag_string_meta"]
                print(f"Post #{post_id}\n")
                title, description = get_commentary(post_id, auth)

                if len(title) == 0 and len(description) == 0:
                    print("No commentary skipping")
                    continue
                if post["is_banned"] == True:
                    print("Is banned skipping")
                    continue

                bad_tag = False
                for tag_ini_gen in post_tags_ini_gen.split():
                    if tag_ini_gen.strip() in settings.CENTAGS:
                        print(f"Contains censored tag {tag_ini_gen}")
                        bad_tag = True
                        break
                for tag_ini_meta in post_tags_ini_meta.split():
                    if tag_ini_meta in settings.CENTAGS:
                        print(f"Contains unwanted metatag {tag_ini_meta}")
                        bad_tag = True
                        break
                if bad_tag:
                    continue

                ok = False
                while not ok:
                    print(f"==================================================\nCurrent tags:\n\ng: \033[0;34m{post_tags_ini_gen}\033[0m\n\nco: \033[0;35m{post_tags_ini_copy}\033[0m\n\nch: \033[0;32m{post_tags_ini_char}\033[0m\n\nm: \033[0;33m{post_tags_ini_meta}\033[0m\n\nTitle: \033[0;36m{title}\033[0m\n\nDescription:\n\n\033[0;36m{description}\033[0m\n\nType tags, type h for help.")
                    user_input = input("$ ")
                    parsed_input = parser.parse(user_input)
                    if parsed_input == -1:
                        for short, tag in settings.TAGS.items():
                            print(f" - {short} = {tag}")
                    elif parsed_input == -2:
                        print("User requested skip.")
                        ok = True
                    elif parsed_input == -3:
                        print(f"gardened {edits} posts")
                        sys.exit(0)
                    elif "!!!!!!!!" in parsed_input:
                        print("Try again.")
                    else:
                        print(f"The following tags will be added. Ok?\n{parsed_input}")
                        confirm = input("(y/N)$ ")
                        if confirm.lower().strip() == "y":
                            print("Sending out change!")
                            uptodate_post = requests.get(f"{get_booru_url()}/posts/{post_id}.json").json()
                            post_tags = uptodate_post["tag_string"]
                            new_tags = post_tags + " " + parsed_input
                            dprint(f"New tag string: {new_tags}")
                            request_data = {
                                "tag_string": new_tags,
                                "old_tag_string": post_tags
                            }
                            dprint(f"Request data = {json.dumps(request_data, indent=2)}")
                            request = requests.put(f"{get_booru_url()}/posts/{post_id}.json?{str(auth)}", json=request_data)
                            dprint(f"Server said this: {json.dumps(request.json(), indent=2)}")
                            try:
                                new_tags_gen = request.json()["tag_string_general"]
                                new_tags_copy = request.json()["tag_string_copyright"]
                                new_tags_char = request.json()["tag_string_character"]
                                new_tags_meta = request.json()["tag_string_meta"]
                                print(f"\nTags now:\ng: \033[0;34m{new_tags_gen}\033[0m\n\nco:\033[0;35m{new_tags_copy}\033[0m\n\nch:\033[0;32m{new_tags_char}\033[0m\n\nm:\033[0;33m{new_tags_meta}\033[0m\n\n")
                                if request.status_code != 200 and request.status_code != 204:
                                    print(f"Error {request.status_code}")
                                elif request.status_code == 403:
                                    print("Post forbidden to edit. Skip.")
                                    ok = True
                                else:
                                    print("Edited successfully.")
                                    edits += 1
                                    ok = True
                            except KeyError:
                                print("Could not edit not sure why") # TODO why
                                ok = True
                            input("press enter...")
                        else:
                            print("Try again.")

            page += 1
    except KeyboardInterrupt:
        print(f"gardened {edits} posts")
        sys.exit(0)
    except Exception as exc:
        print(f"gardened {edits} posts")
        raise exc

if __name__ == "__main__":
    main()
