import re

BLOAT = [
    "pixiv",
    "fanbox",
    "skeb",
    "fantia",
    "rkgk",
    "twitter",
    "misskey"
]

def remove_hashtags(text):
    return re.sub(r'"#.*?":\[\S+?\]', "", text)

def remove_urls(text):
    return re.sub(r"https?://\S+", "", text)

def remove_twitter_links(text):
    return re.sub(r'\[b\]"twitter\/\S+":\[https?:\/\/\S+\]\[/b\]', "", text)

def remove_bloat(text):
    pattern = re.compile("|".join(re.escape(word) for word in BLOAT), re.IGNORECASE)
    return pattern.sub("", text)
