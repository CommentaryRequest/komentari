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
    no_dtext_urls = re.sub(r"<https?://\S+>", "", text)
    no_twitter_links = re.sub(r'\[b\]"twitter\/\S+":\[https?:\/\/\S+\]\[\/b\]', "", no_dtext_urls)
    return re.sub(f"https?://\S+", "", no_twitter_links)

def remove_bloat(text):
    pattern = re.compile("|".join(re.escape(word) for word in BLOAT), re.IGNORECASE)
    return pattern.sub("", text)
