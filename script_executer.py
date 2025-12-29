#!/usr/bin/python3

import argparse
import settings
import json
from auth import Auth
from posts import get_posts
from tagedit import tag_edit_post
from komentari import HEADERS

def check_post(post_id, exclude_tags, skip_translated, auth):
    if not exclude_tags and not skip_translated:
        return True # nothing to check

    query = f"id:{post_id}"
    if exclude_tags:
        query += f" -({' or '.join(exclude_tags.split(' '))})"
    if skip_translated:
        query += f" commentary:untranslated"

    posts, _ = get_posts(query, auth, 1, HEADERS)
    return len(posts) != 0

def main():
    print(f"komentari {settings.PROGRAM_VERSION}/script executer is up")

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    parser.add_argument("--exclude-tags", type=str)
    parser.add_argument("--skip-translated", action="store_true")
    parser.add_argument("--resume", type=int, default=0)
    args = parser.parse_args()

    script_filename = args.file
    exclude_tags = args.exclude_tags or ""
    skip_translated = args.skip_translated
    resume = args.resume

    auth = Auth()

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

            if not check_post(post_id, exclude_tags, skip_translated, auth):
                print("Post unsuited. Skip.")
                continue

            print(f"Adding: {script_tags}")

            edits += max(0, tag_edit_post(post_id, HEADERS, script_tags, auth, True, edits))
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
