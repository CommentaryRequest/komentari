#!/usr/bin/python3

from auth import Auth
from booru_url import get_booru_url, set_override
from commentary import get_commentary, Commentary
from favgroup import add_to_favgroup
from posts import get_posts
from debug import dprint, set_custom_creds
from tagedit import tag_edit_post, print_tags
from context import PostInfo, OfflineContext, ExecutionContext
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
import debug

HEADERS = {
    "User-Agent": settings.USERAGENT
}

def write_tag_script(output, tag_script):
    with open(output, "w") as output_file:
        json.dump(tag_script, output_file)

# TODO what the fuck is this parameter list
def do_post(args, post, ctx, offline):
    print(f"Post \033]8;;{get_booru_url(args.test_mode)}/posts/{post.id}\033\\#{post.id}\033]8;;\033\\\n")

    if ctx.skipped_posts.is_skipped(post.id) and not args.ignore_skipped:
        print("Skipped by user")
        return 0

    commentary = offline.commentary if offline else get_commentary(post.id, ctx.auth, HEADERS, args.test_mode)

    is_add_mode = args.mode == "add" and not offline

    # Empty commentary
    if len(commentary.og_title.strip() + commentary.og_description.strip()) == 0:
        if is_add_mode:
            print("Adding to favgroup")
            add_to_favgroup(args.add_favgroup_id, post.id, ctx.auth, HEADERS, args.test_mode)
        elif not args.no_commentary_check:
            print("No commentary; skipping")
            return 0

    if is_add_mode:
        print("post ok")
        return 0

    while True:
        if not args.quiet:
            # Display post information
            if not offline:
                print(
                    "==================================================\nCurrent tags:\n\n"
                )
                print_tags(post)
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
            if args.yes_no_tag is not None:
                parsed_input = args.yes_no_tag
                manual_input = False
            elif args.auto:
                parsed_input, manual_input = automode.parse(commentary, args.semi_auto, args.quiet, post.id, post.chartags, args.auto_debug, post.source)

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
            print("Special commands:")
            for short, tag in parser.SPECIAL_TAGS.items():
                print(f" - {short} = {tag[1]}")
        elif parsed_input == parser.SKIP:
            print("User requested skip.")
            ctx.skipped_posts.add(post.id)
            return 0
        elif parsed_input == parser.QUIT:
            ctx.skipped_posts.flush()
            if offline:
                write_tag_script(args.offline_output, offline.tag_script)
            print(f"gardened {ctx.edit_count} posts")
            sys.exit(0)
        elif parsed_input == parser.BROWSER:
            link = f"{get_booru_url(args.test_mode)}/posts/{post.id}"
            print(f"Opening link: {link}")
            webbrowser.open(link)
        elif parsed_input == parser.NONPERMANENT_SKIP:
            if not args.quiet:
                print("User requested non-permanent skip.")
            return 0
        elif parsed_input == parser.PROGRESS_CHECK:
            if not offline:
                print("Only works in offline mode.")
            else:
                print(f"Progress: {offline.index}/{offline.post_count} ({offline.post_count - offline.index} left)")
        elif "!!!!!!!!" in parsed_input:
            print("Unknown tag. Try again.")
        else:
            if not args.quiet:
                print(f"The following tags will be added. Ok?\n{parsed_input}")
            confirm = ""
            if args.yes_no_tag is not None and not args.yes_no_tag_force:
                manual_input = True
            if manual_input:
                confirm = input("(y/N)$ ")
            if confirm.lower().strip() == "y" or not manual_input or (len(confirm.lower().strip()) == 0 and args.yes_no_tag is not None):
                if args.quiet:
                    print(parsed_input)
                else:
                    print("Sending out change!")

                if offline:
                    offline.tag_script[post.id] = parsed_input
                    if manual_input:
                        input("press enter...")
                    return 1
                else:
                    edit_result = tag_edit_post(post.id, HEADERS, parsed_input, ctx.auth, args.quiet, ctx.edit_count, args.test_mode)
                    if manual_input:
                        input("press enter...")
                    return max(0, edit_result)
            elif args.yes_no_tag is not None:
                print("Skip")
                return 0
            else:
                print("Try again.")

def main():
    print(f"komentari {settings.PROGRAM_VERSION} is up")

    dprint("Debug mode enabled")

    args = cliargs.parse_args()

    if args.test_mode:
        print("=== RUNNING IN TEST MODE ===")

    if (args.offline_file and not args.offline_output) or (args.offline_output and not args.offline_file):
        print("output and file option have to be used together always")
        sys.exit(1)

    tag_script = {}
    offline = {}

    if args.offline_file:
        with open(args.offline_file, "r") as commentaries_file:
            offline = {entry["post_id"]: entry for entry in json.load(commentaries_file) if entry["post_id"] >= args.file_resume}

    if (args.override_login and not args.override_apikey) or (not args.override_login and args.override_apikey):
        print("you gotta override both apikey and login")
        sys.exit(1)

    if args.random:
        args.query += "+random:20"
    if args.limit:
        args.query += f"+limit:{args.limit}"

    if args.offline_file:
        print(f"File = {args.offline_file}")
    else:
        print(f"Query = {args.query}")

    auth = None
    if not args.offline_file:
        auth = Auth(args.test_mode)

    if args.override_login and args.override_apikey:
        auth.set_auth(args.override_login, args.override_apikey)
        set_custom_creds(args.override_login, args.override_apikey)
    if args.override_domain:
        set_override(args.override_domain)

    skipped_posts = skipped.SkippedPosts()
    if args.mode != "garden" and args.mode != "add":
        print(f"Unknown operation mode: '{args.mode}'")
        sys.exit(1)

    if args.mode == "add" and args.add_favgroup_id == 0:
        print(f"Group id required in add mode")
        sys.exit(1)

    page = args.initial_page
    exec_context = ExecutionContext(skipped_posts, auth, 0)

    try:
        if args.offline_file:
            for i, (post_id, post) in enumerate(offline.items()):
                ctx = OfflineContext(tag_script, args.offline_output, Commentary(post["og_title"], post["og_description"], post["tl_title"], post["tl_description"]), len(offline), i)
                exec_context.edit_count += do_post(args, PostInfo(post_id, None, None, None, None, None), exec_context, ctx)
            print("No more posts.")
            skipped_posts.flush()
            write_tag_script(args.offline_output, tag_script)
        else:
            while True:
                if args.random or args.same_page:
                    print("Getting more posts...")
                else:
                    print(f"Now on page {page}")
                posts, raw_resp = get_posts(args.query, auth, page, HEADERS, args.test_mode)
                if posts == []:
                    print("No more posts.")
                    skipped_posts.flush()
                    print(f"gardened {exec_context.edit_count} posts")
                    break

                debug.dprint(f"post response: {posts}")

                for post in posts:
                    # checking posts for unwanted tags
                    check_result, bad_tag = post_check.check_post(post)
                    if check_result == post_check.POST_CHECK_CENTAG:
                        print(f"Contains unwanted tag: {bad_tag}")
                        continue
                    elif check_result == post_check.POST_CHECK_IS_BANNED:
                        if settings.BANNED_FAVGROUP:
                            print(f"Is banned; adding to favgroup #{settings.BANNED_FAVGROUP}")
                            add_to_favgroup(settings.BANNED_FAVGROUP, post["id"], auth, HEADERS, args.test_mode)
                        else:
                            print("Is banned; skipping")
                        continue

                    # Getting post information
                    dprint(f"Working with post = {json.dumps(post, indent=2)}")
                    dprint(f"Raw response = {raw_resp}")
                    post_info = PostInfo.from_json(post)
                    exec_context.edit_count += do_post(args, post_info, exec_context, None)
                page += 0 if args.random or args.same_page else 1
    except KeyboardInterrupt:
        skipped_posts.flush()
        if args.offline_file:
            write_tag_script(args.offline_output, tag_script)
        print(f"gardened {exec_context.edit_count} posts")
        sys.exit(0)
    except Exception as exc:
        skipped_posts.flush()
        if args.offline_file:
            write_tag_script(args.offline_output, tag_script)
        print(f"gardened {exec_context.edit_count} posts")
        raise

if __name__ == "__main__":
    main()
