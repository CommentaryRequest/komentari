import re

BLOAT = [
    "pixiv",
    "fanbox",
    "skeb",
    "fantia",
    "rkgk",
    "twitter",
    "misskey",
    "pixiv",
    "patreon",
    "bluesky"
]

def remove_hashtags(text):
    return re.sub(r'"#.*?":\[\S+?\]', "", text)

def remove_urls(text):
    no_dtext_urls = re.sub(r"<https?://\S+>", "", text)
    no_twitter_links = re.sub(r'\[b\]"twitter\/\S+":\[https?:\/\/\S+\]\[\/b\]', "", no_dtext_urls)
    no_at_mentions = re.sub(r'"@\S+":\[https?://\S+\]', "", no_twitter_links)
    return re.sub(f"https?://\S+", "", no_at_mentions)

def remove_bloat(text):
    pattern = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(map(re.escape, BLOAT)) + r")(?![A-Za-z0-9])", re.IGNORECASE)
    return pattern.sub("", text)
