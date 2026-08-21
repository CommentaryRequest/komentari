#!/usr/bin/python3

import argparse
import settings
import json
from posts import get_posts
from tagedit import tag_edit_post
from netclient import NetworkClient

def check_post(post_id, exclude_tags, skip_translated, net_client):
    if not exclude_tags and not skip_translated:
        return True # nothing to check

    query = f"id:{post_id}"
    if exclude_tags:
        query += f" -({' or '.join(exclude_tags.split(' '))})"
    if skip_translated:
        query += f" commentary:untranslated"

    posts = get_posts(query, 1, net_client)
    return len(posts) != 0

def main():
    print(f"komentari {settings.PROGRAM_VERSION}/script executor is up")

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    parser.add_argument("--exclude-tags", type=str)
    parser.add_argument("--skip-translated", action="store_true")
    parser.add_argument("--resume", type=int, default=0)
    parser.add_argument("--login", type=str)
    parser.add_argument("--api-key", type=str)
    args = parser.parse_args()

    script_filename = args.file
    exclude_tags = args.exclude_tags or ""
    skip_translated = args.skip_translated
    resume = args.resume

    net_client = NetworkClient(False)
    if args.login and args.api_key:
        net_client.set_auth(args.login, args.api_key)

    script = {}
    with open(script_filename, "r") as script_file:
        script = json.load(script_file)

    if resume:
        print(f"Resuming from post #{resume}")

    edits = 0
    last_id = 0
    try:
        for post_id in sorted(script, key=int):
            script_tags = script[post_id]
            post_id = int(post_id)
            if post_id < resume:
                continue

            last_id = post_id

            print(f"Post #{post_id}")

            if not check_post(post_id, exclude_tags, skip_translated, net_client):
                print("Post unsuited. Skip.")
                continue

            print(f"Adding: {script_tags}")

            edits += max(0, tag_edit_post(post_id, script_tags, True, edits, net_client))
            print("Edited.\n")

            if edits % 100 == 0:
                print(f" * last id = post #{last_id} *")
    except KeyboardInterrupt:
        print(f"gardened {edits} posts, stopped at post #{last_id}")
    except Exception as exc:
        print(f"gardened {edits} posts, interrupted at post #{last_id}")
        raise

if __name__ == "__main__":
    main()
