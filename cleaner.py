import re

# Ignore words from this list
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
    "ci-en",
    "pixivfanbox",
    "baraag",
    "instagram",
    "booth",
    "niconico",
    "ko-fi",
    "gumroad",
    "vgen",
    "cm",
    "tumblr",
    "pawoo",
    "ych",
    "fannbox",
    "cms",
    "fa",
    "wip"
]

INVISIBLE_CHARS = [
    chr(0x3164), # U+3164 Hangul Filler
    chr(0x115f), # U+115F Hangul Choseong Filler
    chr(0x1160), # U+1160 Hangul Jungseong Filler
    chr(0xffa0), # U+FFA0 Halfwidth Hangul Filler
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
    text = re.sub(r'twitter\/\S+', "", text)
    text = re.sub(r'\[b\]"user\/\S+":\[https:\/\/\S+\] "»":\[\/\S+\]\[\/b\]', "", text)
    text = re.sub(r'\[b\]pixiv #\d+ "»":\[\S+\]\[\/b\]', "", text)
    text = re.sub(r'"@\S+":\[https?://\S+\]', "", text)
    return re.sub(r"https?://\S+", "", text)

def remove_bloat(text):
    pattern = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(map(re.escape, BLOAT)) + r")(?![A-Za-z0-9])", re.IGNORECASE)
    return pattern.sub("", text)

def remove_fullwidth(text):
    return re.sub(r"[\uFF01-\uFF5E]", "", text);
