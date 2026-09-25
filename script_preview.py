#!/usr/bin/python3

import json
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commentaries_file")
    parser.add_argument("script_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    commentaries_data = []
    with open(args.commentaries_file, "r") as file:
        commentaries_data = json.load(file)

    script_data = {}
    with open(args.script_file, "r") as file:
        script_data = json.load(file)

    with open(args.output_file, "w") as file:
        file.write(f"{len(script_data)} changes to execute:\n\n")
        for commentary in commentaries_data:
            post_id = str(commentary["post_id"])
            if post_id in script_data:
                original_title = commentary["og_title"]
                original_desc = commentary["og_description"]
                translated_title = commentary["tl_title"]
                translated_desc = commentary["tl_description"]
                commentary_id = commentary["id"]
                tags = script_data[post_id]

                post_link = f"https://danbooru.donmai.us/posts/{post_id}"

                file.write(f"post #{post_id} ( {post_link} )\ncommentary #{commentary_id}\n")
                if original_title:
                    file.write(f"Original title: {original_title}\n")
                if original_desc:
                    file.write(f"Original description: {original_desc}\n")
                if translated_title:
                    file.write(f"Translated title: {translated_title}\n")
                if translated_desc:
                    file.write(f"Translated description: {translated_desc}\n")
                file.write(f"Tags: {tags}\n{"=" * 30}\n\n")

    print(f"Report written to {args.output_file}")

if __name__ == "__main__":
    main()
