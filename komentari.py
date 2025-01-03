#!/usr/bin/python3

from auth import Auth
from booru_url import get_booru_url
from commentary import get_commentary
from favgroup import add_to_favgroup
from posts import get_posts
import post_check
import requests
import urllib.error
import urllib
import settings
import parser
import json
import sys
import argparse
import webbrowser

__version__ = "1.6"
USERAGENT = f"Komentari/{__version__} by user #1054326"

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
    aparser.add_argument("--mode", type=str, default="garden", help="garden: gardening commentary tags. add: add posts with no commentary to fav group")
    aparser.add_argument("--group", type=int, default=0, help="posts with no commentary will be added to this fav group (necessary if mode is add)")
    args = aparser.parse_args()

    print(f"Query = {args.query}")

    auth = Auth()

    headers = {
        "User-Agent": USERAGENT
    }

    mode = args.mode
    group_id = args.group
    if mode != "garden" and mode != "add":
        print(f"Unknown operation mode: '{mode}'")
        sys.exit(1)

    if mode == "add" and group_id == 0:
        print(f"Group id required in add mode")
        sys.exit(1)

    page = args.page
    edits = 0
    try:
        while True:
            print(f"Now on page {page}")
            posts = get_posts(args.query, auth, page)

            for post in posts:
                dprint(f"Working with post = {json.dumps(post, indent=2)}")
                post_id = post["id"]
                post_tags_ini_gen = post["tag_string_general"]
                post_tags_ini_copy = post["tag_string_copyright"]
                post_tags_ini_char = post["tag_string_character"]
                post_tags_ini_meta = post["tag_string_meta"]
                print(f"Post #{post_id}\n")
                commentary = get_commentary(post_id, auth, headers)

                check_result, bad_tag = post_check.check_post(post, commentary)

                if check_result == post_check.POST_CHECK_CENTAG:
                    print(f"Contains unwanted tag: {bad_tag}")
                    continue
                elif check_result == post_check.POST_CHECK_NO_COMMENTARY:
                    if mode == "add":
                        print("Adding to favgroup")
                        add_to_favgroup(group_id, post_id, auth)
                    else:
                        print("No commentary; skipping")
                    continue
                elif check_result == post_check.POST_CHECK_IS_BANNED:
                    print("Is banned; skipping")
                    continue

                if mode == "add":
                    print("post ok")
                    continue

                ok = False
                while not ok:
                    print(f"==================================================\nCurrent tags:\n\ng: \033[0;34m{post_tags_ini_gen}\033[0m\n\nco: \033[0;35m{post_tags_ini_copy}\033[0m\n\nch: \033[0;32m{post_tags_ini_char}\033[0m\n\nm: \033[0;33m{post_tags_ini_meta}\033[0m\n\nTitle: \033[0;36m{commentary.og_title}\033[0m\n\nDescription:\n\n\033[0;36m{commentary.og_description}\033[0m\n\n")
                    if len(commentary.tl_title) != 0 or len(commentary.tl_description) != 0:
                        print(f"TRANSLATED Title: \033[0;36m{commentary.tl_title}\033[0m\n\nTRANSLATED Description:\n\n\033[0;36m{commentary.tl_description}\033[0m\n\n")
                    print("Type tags, type h for help, type b to open in browser.")
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
                    elif parsed_input == -4:
                        link = f"{get_booru_url()}/posts/{post_id}"
                        print(f"Opening link: {link}")
                        webbrowser.open(link)
                    elif "!!!!!!!!" in parsed_input:
                        print("Try again.")
                    else:
                        print(f"The following tags will be added. Ok?\n{parsed_input}")
                        confirm = input("(y/N)$ ")
                        if confirm.lower().strip() == "y":
                            print("Sending out change!")
                            try:
                                uptodate_post = requests.get(f"{get_booru_url()}/posts/{post_id}.json", headers=headers).json()
                            except (
                                urllib.error.URLError,
                                requests.exceptions.ReadTimeout,
                                requests.exceptions.ConnectionError
                            ) as exc:
                                print(f"Failed to fetch page because of {exc}")
                            post_tags = uptodate_post["tag_string"]
                            new_tags = post_tags + " " + parsed_input
                            dprint(f"New tag string: {new_tags}")
                            request_data = {
                                "tag_string": new_tags,
                                "old_tag_string": post_tags
                            }
                            dprint(f"Request data = {json.dumps(request_data, indent=2)}")
                            try:
                                request = requests.put(f"{get_booru_url()}/posts/{post_id}.json?{str(auth)}", json=request_data, headers=headers)
                            except (
                                urllib.error.URLError,
                                requests.exceptions.ReadTimeout,
                                requests.exceptions.ConnectionError
                            ) as exc:
                                print(f"Failed to fetch page because of {exc}")
                                
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
