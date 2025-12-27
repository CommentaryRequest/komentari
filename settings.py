from authsettings import *

PROGRAM_VERSION = "1.22.1"
USERAGENT = f"Komentari/{PROGRAM_VERSION} by user #1054326"

TESTMODE = False
DEBUGMODE = False

TAGS = {
    "r": "commentary_request",
    "c": "commentary",
    "m": "mixed-language_commentary",
    "bi": "bilingual_commentary",
    "bb": "bilingual_commentary commentary",
    "ml": "multilingual_commentary",
    "mll": "multilingual_commentary commentary",
    "e": "english_commentary",
    "ee": "english_commentary commentary",
    "s": "symbol-only_commentary",
    "ho": "hashtag-only_commentary",
    "hr": "hashtag-only_commentary commentary_request",
    "hc": "hashtag-only_commentary commentary",
    "d": "dated_commentary",
    "z": "chinese_commentary",
"zz": "chinese_commentary commentary_request",
    "k": "korean_commentary",
    "kk": "korean_commentary commentary_request",
    "sp": "spanish_commentary",
    "ro": "romaji_commentary",
    "ru": "russian_commentary",
    "er": "engrish_commentary",
    "t": "thai_commentary",
    "f": "french_commentary",
    "v": "vietnamese_commentary",
    "vv": "vietnamese_commentary commentary_request",
    "p": "partial_commentary",
    "at": "alt_text",
    "ty": "commentary_typo"
}

AUTOTAG_EN = "commentary english_commentary" # English commentary
AUTOTAG_HT = "hashtag-only_commentary" # Hashtag-only commentary
AUTOTAG_SY = "symbol-only_commentary" # Symbol-only commentary
AUTOTAG_BL = "commentary" # Bloat-only commentary
AUTOTAG_CT = "commentary" # Chartag-only commentary
AUTOTAG_UN = "commentary" # Untitled commentary
AUTOTAG_KK = "commentary_request korean_commentary" # Korean commentary
AUTOTAG_JP = "commentary_request" # Japanese commentary
AUTOTAG_CN = "commentary_request chinese_commentary" # Chinese commentary
AUTOTAG_NM = "commentary" # Number-only commentary
AUTOTAG_FW = "commentary" # Fullwidth-only commentary
AUTOTAG_NS = "commentary" # Numbers and symbols only

ENGLISH_CONFIDENCE = 0.8

CHINESE_SOURCES = [
    "weibo.com",
    "lofter.com",
    "xiaohongshu.com",
    "bilibili.com",
    "miyoushe.com",
    "huashijie.art",
    "mihuashi.com"
]

CENTAGS = {
    "hashtag-only_commentary"
}

UNRECOG_FAVGROUP = 0

try:
    from usersettings import *
    TAGS.update(CUSTOMTAGS)
except NameError:
    pass
except ImportError:
    pass
