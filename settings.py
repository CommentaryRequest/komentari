from authsettings import *

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
