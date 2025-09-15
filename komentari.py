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
import emjchk
import cleaner
import cliargs
import recog

__version__ = "1.16"

USERAGENT = f"Komentari/{__version__} by user #1054326"

UNTITLED_TITLES = [
    "untitled",
    "no title",
    "no_title"
]

def dprint(message):
    if not settings.DEBUGMODE:
        return
    print(f"dbg: {message}")

def add_negative_tags():
    for tag, expand in settings.TAGS.copy().items(): # TODO might be a breaking change but rename to lowercase (not really a const...)
        expand_split = expand.split()
        negative_expand_split = ["-" + tag for tag in expand_split]
        negative_expand = " ".join(negative_expand_split)
        settings.TAGS["-" + tag] = negative_expand

def print_tags(g, co, ch, m):
    print(
        f"g: \033[0;34m{g}\033[0m\n"
        f"co: \033[0;35m{co}\033[0m\n"
        f"ch: \033[0;32m{ch}\033[0m\n"
        f"m: \033[0;33m{m}\033[0m\n"
    )

def safedumps(response):
    try:
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.JSONDecodeError:
        return response.text

def write_confidence(threshold, pid, commentary, confidence):
    with open(threshold + ".txt", "a", encoding="utf-8") as file:
        file.write(f"================================== post #{pid} ({confidence})\n{commentary}\n\n")

def check_en(commentary, pid, en_log):
    confidence = recog.recog(commentary)

    if en_log:
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        for threshold in thresholds:
            if confidence >= threshold:
                write_confidence(str(threshold), pid, commentary, confidence)
    return confidence

def main():
    print(f"komentari {__version__} is up")

    if settings.TESTMODE:
        print("=== RUNNING IN TEST MODE ===")

    dprint("Debug mode enabled")

    args = cliargs.parse_args()

    random_mode = args.random
    limit = args.limit
    yes_no_tag = args.ynt
    yes_no_tag_force = args.ynty
    auto = args.auto
    semi_auto = args.semi_auto
    en_log = args.en_log
    quiet = args.quiet

    if not auto or semi_auto:
        quiet = False

    if semi_auto and not auto:
        auto = True

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

                # Empty commentary
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
                    if not quiet:
                        print(
                            "==================================================\nCurrent tags:\n\n"
                        )
                        print_tags(post_tags_ini_gen, post_tags_ini_copy, post_tags_ini_char, post_tags_ini_meta)
                        print(
                            f"Title: \033[0;36m{commentary.og_title}\033[0m\n\n"
                            f"Description:\n\n\033[0;36m{commentary.og_description}\033[0m\n\n"
                        )
                        if len(commentary.tl_title) != 0 or len(commentary.tl_description) != 0:
                            print(
                                f"TRANSLATED Title: \033[0;36m{commentary.tl_title}\033[0m\n\n"
                                f"TRANSLATED Description:\n\n\033[0;36m{commentary.tl_description}\033[0m\n\n"
                            )
                    parsed_input = ""
                    while True:
                        manual_input = True
                        if yes_no_tag is not None:
                            parsed_input = yes_no_tag
                            manual_input = False
                        elif auto:
                            if commentary.og_title.strip().lower() in UNTITLED_TITLES and len(commentary.og_description.strip()) == 0:
                                parsed_input = "commentary"
                                manual_input = False
                            else:
                                clean_commentary = commentary.og_title + commentary.og_description

                                clean_commentary = cleaner.remove_hashtags(clean_commentary)
                                manual_input = False
                                if len(clean_commentary.strip()) == 0:
                                    # The commentary only contained hashtags
                                    parsed_input = "hashtag-only_commentary"
                                else:
                                    clean_commentary = cleaner.remove_urls(clean_commentary)
                                    is_emoji = emjchk.is_emoji(clean_commentary)
                                    if is_emoji:
                                        parsed_input = "symbol-only_commentary"
                                    else:
                                        clean_commentary = cleaner.remove_bloat(clean_commentary)
                                        if not quiet:
                                            print(f"Clean commentary = {clean_commentary}")
                                        is_japan = jpchk.is_japan(clean_commentary)
                                        is_korea = kkchk.is_korea(clean_commentary)
                                        if is_korea:
                                            parsed_input = "commentary_request korean_commentary"
                                        elif is_japan:
                                            parsed_input = "commentary_request"
                                        else:
                                            confidence = check_en(clean_commentary, post_id, en_log)
                                            if confidence >= 0.9:
                                                parsed_input = "commentary english_commentary"
                                            else:
                                                parsed_input = parser.NONPERMANENT_SKIP
                                                manual_input = semi_auto

                        if manual_input:
                            print("(h for help)")
                            user_input = input("$ ")
                            parsed_input = parser.parse(user_input)

                        if isinstance(parsed_input, int) or parsed_input.strip() != "":
                            break
                    if parsed_input == parser.HELP:
                        print("Configured tags:")
                        for short, tag in settings.TAGS.items():
                            if not short.startswith("-"):
                                print(f" - {short} = {tag}")
                        print("Type h for help, b to open in browser, q to quit.")
                    elif parsed_input == parser.SKIP:
                        print("User requested skip.")
                        skipped_posts.add(post_id)
                        ok = True
                    elif parsed_input == parser.QUIT:
                        skipped_posts.flush()
                        print(f"gardened {edits} posts")
                        sys.exit(0)
                    elif parsed_input == parser.BROWSER:
                        link = f"{get_booru_url()}/posts/{post_id}"
                        print(f"Opening link: {link}")
                        webbrowser.open(link)
                    elif parsed_input == parser.NONPERMANENT_SKIP:
                        if not quiet:
                            print("User requested non-permanent skip.")
                        ok = True
                    elif "!!!!!!!!" in parsed_input:
                        print("Unknown tag. Try again.")
                    else:
                        if not quiet:
                            print(f"The following tags will be added. Ok?\n{parsed_input}")
                        confirm = ""
                        if manual_input:
                            confirm = input("(y/N)$ ")
                        if confirm.lower().strip() == "y" or not manual_input:
                            if quiet:
                                print(parsed_input)
                            else:
                                print("Sending out change!")

                            # Tags on the post may have changed between fetching the post and confirming entered tags.
                            # This loads the latest tags, ensuring no conflict.
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

                            new_tags = post_tags + " " + parsed_input
                            dprint(f"New tag string: {new_tags}")
                            request_data = {
                                "tag_string": new_tags,
                                "old_tag_string": post_tags
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
                                    ok = True
                            except KeyError as exc:
                                print(f"Could not edit: {exc}")
                                ok = True
                            if manual_input:
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
        raise

if __name__ == "__main__":
    main()
