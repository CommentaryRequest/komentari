import re

BLOAT = [
    "pixiv",
    "fanbox",
    "skeb",
    "fantia",
    "rkgk",
    "twitter",
    "misskey",
    "patreon",
    "bluesky",
    "dlsite",
    "log",
    "oc",
    "psd",
    "miku"
]

INVISIBLE_CHARS = [
    chr(0x3164) # U+3164 Hangul Filler
]

def remove_invisible_chars(text):
    for char in INVISIBLE_CHARS:
        text = text.replace(char, "")
    return text

def remove_hashtags(text):
    return re.sub(r'"#.*?":\[\S+?\]', "", text)

def remove_urls(text):
    text = re.sub(r"<https?://\S+>", "", text)
    text = re.sub(r'\[b\]"twitter\/\S+":\[https?:\/\/\S+\]\[\/b\]', "", text)
    text = re.sub(r'\[b\]"user\/\S+":\[https:\/\/\S+\] "»":\[\/\S+\]\[\/b\]', "", text)
    text = re.sub(r'\[b\]pixiv #\d+ "»":\[\S+\]\[\/b\]', "", text)
    text = re.sub(r'"@\S+":\[https?://\S+\]', "", text)
    return re.sub(f"https?://\S+", "", text)

def remove_bloat(text):
    pattern = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(map(re.escape, BLOAT)) + r")(?![A-Za-z0-9])", re.IGNORECASE)
    return pattern.sub("", text)
