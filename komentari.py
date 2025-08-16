#!/usr/bin/python3

from auth import Auth
from booru_url import get_booru_url
from commentary import get_commentary
from favgroup import add_to_favgroup
from posts import get_posts
import settings
import post_check
import requests
import urllib.error
import urllib
import parser
import skipped
import json
import sys
import argparse
import webbrowser
import re
import jpchk
import kkchk

__version__ = "1.14.1"
USERAGENT = f"Komentari/{__version__} by user #1054326"

LANGS = {
    "en": "english_commentary commentary",
    "ja": "commentary_request",
    "cn": "chinese_commentary commentary_request",
    "th": "thai_commentary commentary_request"
}

def dprint(message):
    if not settings.DEBUGMODE:
        return
    print(f"dbg: {message}")

def add_negative_tags():
    for tag, expand in settings.TAGS.copy().items(): # TODO might be a breaking change but rename to lowercase (not really a const...)
        settings.TAGS["-" + tag] = "-" + expand

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
    aparser.add_argument("--random", action="store_true", help="select posts at random")
    aparser.add_argument("--limit", type=int, default=None, help="change the post limit")
    aparser.add_argument("--ynt", type=str, default=None, help="yes/no tag: press enter to apply tag for each post found, any key + enter to skip")
    aparser.add_argument("--ynty", action="store_true", help="automatically add the chosen tag when using yes/no tag. (warning: dangerous. only use if you know what you're doing.)")
    aparser.add_argument("--auto", action="store_true", help="automatically detect language and add tag. if language not detected, skip post")
    args = aparser.parse_args()

    random_mode = args.random
    limit = args.limit
    yes_no_tag = args.ynt
    yes_no_tag_force = args.ynty
    auto = args.auto

    confirm_string = "y"
    if yes_no_tag is not None or auto:
        confirm_string = ""

    args.query += "+status:any"
    if random_mode:
        args.query += "+random:20"
    if limit is not None:
        args.query += f"+limit:{limit}"

    print(f"Query = {args.query}")

    auth = Auth()

    headers = {
        "User-Agent": USERAGENT
    }

    skipped_posts = skipped.SkippedPosts()
    mode = args.mode
    group_id = args.group
    if mode != "garden" and mode != "add":
        print(f"Unknown operation mode: '{mode}'")
        sys.exit(1)

    if mode == "add" and group_id == 0:
        print(f"Group id required in add mode")
        sys.exit(1)

    add_negative_tags()

    page = args.page
    edits = 0
    try:
        while True:
            if random_mode:
                print("Getting more posts...")
            else:
                print(f"Now on page {page}")
            posts = get_posts(args.query, auth, page, headers)
            if posts == []:
                print("No more posts lol")
                skipped_posts.flush()
                print(f"gardened {edits} posts")
                break

            for post in posts:
                dprint(f"Working with post = {json.dumps(post, indent=2)}")
                post_id = post["id"]
                post_tags_ini_gen = post["tag_string_general"]
                post_tags_ini_copy = post["tag_string_copyright"]
                post_tags_ini_char = post["tag_string_character"]
                post_tags_ini_meta = post["tag_string_meta"]
                print(f"Post \033]8;;{get_booru_url()}/posts/{post_id}\033\\#{post_id}\033]8;;\033\\\n")

                if skipped_posts.is_skipped(post_id):
                    print("Skipped by user")
                    continue

                check_result, bad_tag = post_check.check_post(post)

                if check_result == post_check.POST_CHECK_CENTAG:
                    print(f"Contains unwanted tag: {bad_tag}")
                    continue
                elif check_result == post_check.POST_CHECK_IS_BANNED:
                    print("Is banned; skipping")
                    continue

                commentary = get_commentary(post_id, auth, headers)

                if len(commentary.og_title.strip() + commentary.og_description.strip()) == 0:
                    if mode == "add":
                        print("Adding to favgroup")
                        add_to_favgroup(group_id, post_id, auth)
                    else:
                        print("No commentary; skipping")
                    continue

                if mode == "add":
                    print("post ok")
                    continue

                ok = False
                while not ok:
                    print(f"==================================================\nCurrent tags:\n\ng: \033[0;34m{post_tags_ini_gen}\033[0m\n\nco: \033[0;35m{post_tags_ini_copy}\033[0m\n\nch: \033[0;32m{post_tags_ini_char}\033[0m\n\nm: \033[0;33m{post_tags_ini_meta}\033[0m\n\nTitle: \033[0;36m{commentary.og_title}\033[0m\n\nDescription:\n\n\033[0;36m{commentary.og_description}\033[0m\n\n")
                    if len(commentary.tl_title) != 0 or len(commentary.tl_description) != 0:
                        print(f"TRANSLATED Title: \033[0;36m{commentary.tl_title}\033[0m\n\nTRANSLATED Description:\n\n\033[0;36m{commentary.tl_description}\033[0m\n\n")
                    print("(h for help)")
                    parsed_input = ""
                    while True:
                        if yes_no_tag is not None:
                            parsed_input = yes_no_tag
                        elif auto:
                            clean_commentary = commentary.og_title + commentary.og_description
                            clean_commentary = re.sub(r'"#.*?":\[\S+?\]', "", clean_commentary)
                            if len(clean_commentary.strip()) == 0:
                                parsed_input = "hashtag-only_commentary"
                            else:
                                clean_commentary = re.sub(r"https?://\S+", "", clean_commentary)
                                print(f"Clean commentary = {clean_commentary}")
                                is_japan = jpchk.is_japan(clean_commentary)
                                is_korea = kkchk.is_korea(clean_commentary)
                                if is_korea:
                                    parsed_input = "commentary_request korean_commentary"
                                elif is_japan:
                                    parsed_input = "commentary_request"
                                else:
                                    parsed_input = -5
                        else:
                            user_input = input("$ ")
                            parsed_input = parser.parse(user_input)
                        if isinstance(parsed_input, int) or parsed_input.strip() != "":
                            break
                    if parsed_input == -1:
                        print("Configured tags:")
                        for short, tag in settings.TAGS.items():
                            if not short.startswith("-"):
                                print(f" - {short} = {tag}")
                        print("Type h for help, b to open in browser, q to quit.")
                    elif parsed_input == -2:
                        print("User requested skip.")
                        skipped_posts.add(post_id)
                        ok = True
                    elif parsed_input == -3:
                        skipped_posts.flush()
                        print(f"gardened {edits} posts")
                        sys.exit(0)
                    elif parsed_input == -4:
                        link = f"{get_booru_url()}/posts/{post_id}"
                        print(f"Opening link: {link}")
                        webbrowser.open(link)
                    elif parsed_input == -5:
                        print("User requested non-permanent skip.")
                        ok = True
                    elif "!!!!!!!!" in parsed_input:
                        print("Unknown tag. Try again.")
                    else:
                        print(f"The following tags will be added. Ok?\n{parsed_input}")
                        confirm = ""
                        if (yes_no_tag and not yes_no_tag_force or not yes_no_tag) and not auto:
                            confirm = input("(y/N)$ ")
                        if confirm.lower().strip() == confirm_string:
                            print("Sending out change!")
                            uptodate_post = None
                            while True:
                                try:
                                    uptodate_post = requests.get(f"{get_booru_url()}/posts/{post_id}.json", headers=headers).json()
                                    break
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
                            if not (yes_no_tag and yes_no_tag_force) and not auto:
                                input("press enter...")
                        elif yes_no_tag is not None:
                            print("Skip")
                            ok = True
                        else:
                            print("Try again.")

            page += 0 if random_mode else 1
    except KeyboardInterrupt:
        skipped_posts.flush()
        print(f"gardened {edits} posts")
        sys.exit(0)
    except Exception as exc:
        skipped_posts.flush()
        print(f"gardened {edits} posts")
        raise exc

if __name__ == "__main__":
    main()
