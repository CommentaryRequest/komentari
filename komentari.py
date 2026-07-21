#!/usr/bin/python3

from auth import Auth
from commentary import Commentary
from posts import get_posts
from debug import dprint, set_custom_creds
from context import PostInfo, OfflineContext, ExecutionContext, NetworkContext
from tag_script import write_tag_script
import booru_url
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

def run_offline(offline_posts, tag_script, args, exec_ctx):
    for i, (post_id, post) in enumerate(offline_posts.items()):
        ctx = OfflineContext(tag_script, args.offline_output, Commentary(post["og_title"], post["og_description"], post["tl_title"], post["tl_description"]), len(offline_posts), i)
        post_info = PostInfo(post_id, None, None, None, None, None)
        exec_ctx.edit_count += processor.process_offline(args, post_info, exec_ctx, ctx)
    print("No more posts.")
    exec_ctx.skipped_posts.flush()
    write_tag_script(args.offline_output, tag_script)

def run_online(args, exec_ctx, net_ctx):
    page = args.initial_page
    while True:
        if args.random or args.same_page:
            print("Getting more posts...")
        else:
            print(f"Now on page {page}")
        posts, raw_resp = get_posts(args.query, page, net_ctx)
        if posts == []:
            print("No more posts.")
            skipped_posts.flush()
            print(f"gardened {exec_ctx.edit_count} posts")
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
                    add_to_favgroup(settings.BANNED_FAVGROUP, post["id"], net_ctx)
                else:
                    print("Is banned; skipping")
                continue

            # Getting post information
            dprint(f"Working with post = {json.dumps(post, indent=2)}")
            dprint(f"Raw response = {raw_resp}")
            post_info = PostInfo.from_json(post)
            exec_ctx.edit_count += processor.process_online(args, post_info, exec_ctx, net_ctx)
        page += 0 if args.random or args.same_page else 1

def init_auth(args):
    auth = None
    if not args.offline_file:
        auth = Auth(args.test_mode)

    if args.override_login and args.override_apikey:
        auth.set_auth(args.override_login, args.override_apikey)
        set_custom_creds(args.override_login, args.override_apikey)
    if args.override_domain:
        booru_url.set_override(args.override_domain)

    return auth

def init_offline(args):
    offline_posts = {}
    if args.offline_file:
        # TODO handle resumes better as the IDs might be out of order
        with open(args.offline_file, "r") as commentaries_file:
            offline_posts = {entry["post_id"]: entry for entry in json.load(commentaries_file) if entry["post_id"] >= args.file_resume}
    return offline_posts

def main():
    print(f"komentari {settings.PROGRAM_VERSION} is up")

    dprint("Debug mode enabled")

    args = cliargs.load_args()

    if args.test_mode:
        print("=== RUNNING IN TEST MODE ===")

    if args.offline_file:
        print(f"File = {args.offline_file}")
    else:
        print(f"Query = {args.query}")

    tag_script = {}
    offline_posts = init_offline(args)

    auth = init_auth(args)

    skipped_posts = skipped.SkippedPosts()
    exec_context = ExecutionContext(skipped_posts, 0)
    net_context = NetworkContext(auth, HEADERS, args.test_mode)

    try:
        if args.offline_file:
            run_offline(offline_posts, tag_script, args, exec_context)
        else:
            run_online(args, exec_context, net_context)
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
