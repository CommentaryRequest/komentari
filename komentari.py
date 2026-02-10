#!/usr/bin/python3

from auth import Auth
from booru_url import get_booru_url, set_override
from commentary import get_commentary, Commentary
from favgroup import add_to_favgroup
from posts import get_posts
from debug import dprint, set_custom_creds
from tagedit import tag_edit_post, print_tags
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
import cliargs
import automode

HEADERS = {
    "User-Agent": settings.USERAGENT
}

def write_confidence(threshold, pid, commentary, confidence):
    with open(threshold + ".txt", "a", encoding="utf-8") as file:
        file.write(f"================================== post #{pid} ({confidence})\n{commentary}\n\n")

def write_tag_script(output, tag_script):
    with open(output, "w") as output_file:
        json.dump(tag_script, output_file)

# TODO what the fuck is this parameter list
def do_post(post_id, source, post_tags_ini_gen, post_tags_ini_copy, post_tags_ini_char, post_tags_ini_meta, skipped_posts, mode, auth, group_id, quiet, yes_no_tag, yes_no_tag_force, semi_auto, auto, en_log, auto_dbg, edits, tag_script, output, offline_commentary, ignore_skip, test_mode):
    print(f"Post \033]8;;{get_booru_url(test_mode)}/posts/{post_id}\033\\#{post_id}\033]8;;\033\\\n")

    if skipped_posts.is_skipped(post_id) and not ignore_skip:
        print("Skipped by user")
        return 0


    commentary = offline_commentary
    if not commentary:
        commentary = get_commentary(post_id, auth, HEADERS, test_mode)

    is_add_mode = mode == "add" and not offline_commentary

    # Empty commentary
    if len(commentary.og_title.strip() + commentary.og_description.strip()) == 0:
        if is_add_mode:
            print("Adding to favgroup")
            add_to_favgroup(group_id, post_id, auth, test_mode)
        else:
            print("No commentary; skipping")
            return 0

    if is_add_mode:
        print("post ok")
        return 0

    while True:
        if not quiet:
            # Display post information
            if not offline_commentary:
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
                ini_char_split = None if post_tags_ini_char is None else post_tags_ini_char.split()
                parsed_input, manual_input = automode.parse(commentary, semi_auto, en_log, quiet, post_id, ini_char_split, auto_dbg, source)

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
            return 0
        elif parsed_input == parser.QUIT:
            skipped_posts.flush()
            if offline_commentary:
                write_tag_script(output, tag_script)
            print(f"gardened {edits} posts")
            sys.exit(0)
        elif parsed_input == parser.BROWSER:
            link = f"{get_booru_url(test_mode)}/posts/{post_id}"
            print(f"Opening link: {link}")
            webbrowser.open(link)
        elif parsed_input == parser.NONPERMANENT_SKIP:
            if not quiet:
                print("User requested non-permanent skip.")
            return 0
        elif "!!!!!!!!" in parsed_input:
            print("Unknown tag. Try again.")
        else:
            if not quiet:
                print(f"The following tags will be added. Ok?\n{parsed_input}")
            confirm = ""
            if yes_no_tag is not None and not yes_no_tag_force:
                manual_input = True
            if manual_input:
                confirm = input("(y/N)$ ")
            if confirm.lower().strip() == "y" or not manual_input or (len(confirm.lower().strip()) == 0 and yes_no_tag is not None):
                if quiet:
                    print(parsed_input)
                else:
                    print("Sending out change!")

                if offline_commentary:
                    tag_script[post_id] = parsed_input
                    if manual_input:
                        input("press enter...")
                    return 1
                else:
                    edit_result = tag_edit_post(post_id, HEADERS, parsed_input, auth, quiet, edits, test_mode)
                    if manual_input:
                        input("press enter...")
                    return max(0, edit_result)
            elif yes_no_tag is not None:
                print("Skip")
                return 0
            else:
                print("Try again.")

def main():
    print(f"komentari {settings.PROGRAM_VERSION} is up")

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
    same_page = args.same_page
    auto_dbg = args.auto_dbg
    override_domain = args.domain
    override_login = args.login
    override_apikey = args.apikey
    file = args.file
    output = args.output
    file_resume = args.file_resume
    ignore_skip = args.ignore_skip
    test_mode = args.test

    if test_mode:
        print("=== RUNNING IN TEST MODE ===")

    if (file and not output) or (output and not file):
        print("output and file option have to be used together always")
        sys.exit(1)

    tag_script = {}
    offline = {}
    
    if file:
        with open(file, "r") as commentaries_file:
            offline = {entry["post_id"]: entry for entry in json.load(commentaries_file) if entry["post_id"] >= file_resume}

    if (override_login and not override_apikey) or (not override_login and override_apikey):
        print("you gotta override both apikey and login")
        sys.exit(1)

    if not auto or semi_auto:
        quiet = False

    if semi_auto and not auto:
        auto = True

    args.query += "+status:any"
    if random_mode:
        args.query += "+random:20"
    if limit is not None:
        args.query += f"+limit:{limit}"

    if file:
        print(f"File = {file}")
    else:
        print(f"Query = {args.query}")

    auth = None
    if not file:
        auth = Auth(test_mode)

    if override_login and override_apikey:
        auth.set_auth(override_login, override_apikey)
        set_custom_creds(override_login, override_apikey)
    if override_domain:
        set_override(override_domain)


    skipped_posts = skipped.SkippedPosts()
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
        if file:
            for post_id, post in offline.items():
                edits += do_post(post_id, None, None, None, None, None, skipped_posts, mode, auth, group_id, quiet, yes_no_tag, yes_no_tag_force, semi_auto, auto, en_log, auto_dbg, edits, tag_script, output, Commentary(post["og_title"], post["og_description"], "", ""), ignore_skip, test_mode)
            print("No more posts lol")
            skipped_posts.flush()
            write_tag_script(output, tag_script)
        else:
            while True:
                if random_mode or same_page:
                    print("Getting more posts...")
                else:
                    print(f"Now on page {page}")
                posts, raw_resp = get_posts(args.query, auth, page, HEADERS, test_mode)
                if posts == []:
                    print("No more posts lol")
                    skipped_posts.flush()
                    print(f"gardened {edits} posts")
                    break

                for post in posts:
                    # checking posts for unwanted tags
                    check_result, bad_tag = post_check.check_post(post)
                    if check_result == post_check.POST_CHECK_CENTAG:
                        print(f"Contains unwanted tag: {bad_tag}")
                        continue
                    elif check_result == post_check.POST_CHECK_IS_BANNED:
                        print("Is banned; skipping")
                        continue

                    # Getting post information
                    dprint(f"Working with post = {json.dumps(post, indent=2)}")
                    dprint(f"Raw response = {raw_resp}")
                    post_id = post["id"]
                    source = post["source"]
                    post_tags_ini_gen = post["tag_string_general"]
                    post_tags_ini_copy = post["tag_string_copyright"]
                    post_tags_ini_char = post["tag_string_character"]
                    post_tags_ini_meta = post["tag_string_meta"]
                    edits += do_post(post_id, source, post_tags_ini_gen, post_tags_ini_copy, post_tags_ini_char, post_tags_ini_meta, skipped_posts, mode, auth, group_id, quiet, yes_no_tag, yes_no_tag_force, semi_auto, auto, en_log, auto_dbg, edits, None, None, None, ignore_skip, test_mode)

                page += 0 if random_mode or same_page else 1
    except KeyboardInterrupt:
        skipped_posts.flush()
        if file:
            write_tag_script(output, tag_script)
        print(f"gardened {edits} posts")
        sys.exit(0)
    except Exception as exc:
        skipped_posts.flush()
        if file:
            write_tag_script(output, tag_script)
        print(f"gardened {edits} posts")
        raise

if __name__ == "__main__":
    main()
