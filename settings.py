from authsettings import *

PROGRAM_VERSION = "2.0"
USERAGENT = f"Komentari/{PROGRAM_VERSION} by user #1054326"

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
    "s": "untranslatable_commentary",
    "ho": "hashtag-only_commentary",
    "hr": "hashtag-only_commentary commentary_request",
    "hc": "hashtag-only_commentary commentary",
    "d": "dated_commentary",
    "z": "chinese_commentary",
    "zz": "chinese_commentary commentary_request",
    "k": "korean_commentary",
    "kk": "korean_commentary commentary_request",
    "sp": "spanish_commentary",
    "ss": "spanish_commentary commentary_request",
    "ro": "romaji_commentary",
    "ror": "romaji_commentary commentary_request",
    "ru": "russian_commentary",
    "rr": "russian_commentary commentary_request",
    "er": "engrish_commentary",
    "t": "thai_commentary",
    "tt": "thai_commentary commentary_request",
    "f": "french_commentary",
    "v": "vietnamese_commentary",
    "vv": "vietnamese_commentary commentary_request",
    "p": "partial_commentary",
    "at": "alt_text",
    "ty": "commentary_typo"
}

# Auto mode tag definitions
AUTOTAG_EN = "commentary english_commentary" # English
AUTOTAG_HU = "untranslatable_commentary" # Hashtag-only untranslatable
AUTOTAG_HR = "commentary_request" # Hashtag-only translatable
AUTOTAG_HC = "commentary" # Hashtag-only commentary
AUTOTAG_SY = "untranslatable_commentary" # Symbol-only
AUTOTAG_BL = "commentary" # Bloat-only
AUTOTAG_CT = "commentary" # Chartag-only
AUTOTAG_UN = "commentary" # Untitled
AUTOTAG_KK = "commentary_request korean_commentary" # Korean
AUTOTAG_JP = "commentary_request" # Japanese
AUTOTAG_TH = "commentary_request thai_commentary" # Thai
AUTOTAG_CN = "commentary_request chinese_commentary" # Chinese
AUTOTAG_NM = "commentary" # Number-only
AUTOTAG_FW = "commentary" # Fullwidth-only
AUTOTAG_NS = "commentary" # Numbers and symbols only
AUTOTAG_UR = "commentary" # URLs only
AUTOTAG_TF = "commentary" # Full translation
AUTOTAG_TP = "partial_commentary" # Partial translation

ENGLISH_CONFIDENCE = -7.5

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
SKIP_BANNED_POSTS = False
BANNED_FAVGROUP = 0

BOORU_URL = "https://danbooru.donmai.us"
TESTBOORU_URL = "https://testbooru.donmai.us"

try:
    from usersettings import *
    TAGS.update(CUSTOMTAGS)
except NameError:
    pass
except ImportError:
    pass
