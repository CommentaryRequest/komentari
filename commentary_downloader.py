#!/usr/bin/python3

import settings
import requests
import argparse
import json
from netclient import NetworkClient

class PostCommentary:
    def __init__(self, iden, post_id, original_title, original_description, translated_title, translated_description):
        self.iden = iden
        self.post_id = post_id
        self.original_title = original_title
        self.original_description = original_description
        self.translated_title = translated_title
        self.translated_description = translated_description

    def as_dict(self):
        return {
            "id": self.iden,
            "post_id": self.post_id,
            "og_title": self.original_title,
            "og_description": self.original_description,
            "tl_title": self.translated_title,
            "tl_description": self.translated_description
        }

def main():
    print(f"komentari {settings.PROGRAM_VERSION}/downloader is up")

    parser = argparse.ArgumentParser()
    parser.add_argument("--tags", type=str)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("output", type=str)
    args = parser.parse_args()

    net_client = NetworkClient(False)

    last_id = 0
    commentaries_total = []
    try:
        while True:
            print(f"Grabbing commentaries after commentary #{last_id}")
            commentaries, _ = net_client.get(f"artist_commentaries.json?commit=Search&limit={args.limit}&search%5Border%5D=id_asc&search%5Bpost_tags_match%5D={args.tags}&page=a{last_id}")

            if len(commentaries) == 0:
                print("No commentaries left.")
                break

            for commentary in commentaries:
                commentaries_total.append(PostCommentary(commentary["id"], commentary["post_id"], commentary["original_title"], commentary["original_description"], commentary["translated_title"], commentary["translated_description"]))
            last_id = commentaries[0]["id"]
    except KeyboardInterrupt:
        print("Stopped by user")

    print(f"Grabbed {len(commentaries_total)} commentaries. Now writing.")

    commentaries_dicts = [commentary.as_dict() for commentary in commentaries_total]
    with open(args.output, "w") as output_file:
        json.dump(commentaries_dicts, output_file)

if __name__ == "__main__":
    main()
