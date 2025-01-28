import json
import os

class SkippedPosts:
    def __init__(self):
        self.skipped_posts = []
        if os.path.exists("./skipped.json"):
            with open("./skipped.json", "r", encoding="utf-8") as skipped_json:
                self.skipped_posts = json.load(skipped_json)["posts"]

    def add(self, post):
        self.skipped_posts.append(post)

    def is_skipped(self, post):
        return post in self.skipped_posts

    def flush(self):
        with open("./skipped.json", "w", encoding="utf-8") as skipped_json:
            skipped_json.write(json.dumps({"posts": self.skipped_posts}))
