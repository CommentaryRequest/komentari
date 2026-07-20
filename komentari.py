#!/usr/bin/python3

from auth import Auth
from booru_url import get_booru_url, set_override
from commentary import Commentary
from posts import get_posts
from debug import dprint, set_custom_creds
from context import PostInfo, OfflineContext, ExecutionContext, NetworkContext
from tag_script import write_tag_script
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
import cliargs
import automode
import debug
import processor

HEADERS = {
    "User-Agent": settings.USERAGENT
}

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

    page = args.initial_page
    exec_context = ExecutionContext(skipped_posts, 0)
    net_context = NetworkContext(auth, HEADERS, args.test_mode)

    try:
        if args.offline_file:
            for i, (post_id, post) in enumerate(offline.items()):
                ctx = OfflineContext(tag_script, args.offline_output, Commentary(post["og_title"], post["og_description"], post["tl_title"], post["tl_description"]), len(offline), i)
                post_info = PostInfo(post_id, None, None, None, None, None)
                exec_context.edit_count += processor.process_offline(args, post_info, exec_context, ctx)
            print("No more posts.")
            skipped_posts.flush()
            write_tag_script(args.offline_output, tag_script)
        else:
            while True:
                if args.random or args.same_page:
                    print("Getting more posts...")
                else:
                    print(f"Now on page {page}")
                posts, raw_resp = get_posts(args.query, page, net_context)
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
                            add_to_favgroup(settings.BANNED_FAVGROUP, post["id"], net_context)
                        else:
                            print("Is banned; skipping")
                        continue

                    # Getting post information
                    dprint(f"Working with post = {json.dumps(post, indent=2)}")
                    dprint(f"Raw response = {raw_resp}")
                    post_info = PostInfo.from_json(post)
                    exec_context.edit_count += processor.process_online(args, post_info, exec_context, net_context)
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
