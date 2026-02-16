from authsettings import *

PROGRAM_VERSION = "1.25.6"
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

AUTOTAG_EN = "commentary english_commentary" # English
AUTOTAG_HT = "hashtag-only_commentary" # Hashtag-only
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
DISABLE_AUTO_TRANSLATED = True

try:
    from usersettings import *
    TAGS.update(CUSTOMTAGS)
except NameError:
    pass
except ImportError:
    pass
