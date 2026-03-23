#!/usr/bin/env python3

import requests
import argparse
import settings
import json
from auth import Auth
from booru_url import get_booru_url

def main():
    print("komentari {settings.PROGRAM_VERSION}/wikilist downloader is up")

    auth = Auth(False)

    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=str)
    args = parser.parse_args()

    headers = {
        "User-Agent": settings.USERAGENT
    }

    last_id = 0
    othernames = set()
    try:
        while True:
            print(f"Grabbing wikis after wiki #{last_id}")
            url = f"{get_booru_url(False)}/wiki_pages.json?search[other_name_count]=1..&search[tag][category]=3,4&search[order]=created_at&page=a{last_id}&{str(auth)}"
            wikis = []
            while True:
                try:
                    wikis = requests.get(url).json()
                    if "success" in wikis and not wikis["success"]:
                        print(f"Unsuccessful response: {wikis}")
                    else:
                        break
                except Exception as exc:
                    print(f"Error fetching wikis: {exc}")

            print(wikis)

            if len(wikis) == 0:
                print("No wikis left.")
                break

            last_id = wikis[0]["id"]

            for wiki in wikis:
                for othername in wiki["other_names"]:
                    othernames.add(othername)
    except KeyboardInterrupt:
        print("Stopped by user")

    print(f"Grabbed {len(othernames)} othernames. Now writing.")
    with open(args.output, "w") as output_file:
        json.dump(list(othernames), output_file)

if __name__ == "__main__":
    main()
