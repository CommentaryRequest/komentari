import unicodedata

def is_han(ch):
    # CJK Unified Ideographs + Extension A
    return (
        '\u4e00' <= ch <= '\u9fff' or
        '\u3400' <= ch <= '\u4dbf'
    )

def contains_kana(text):
    for ch in text:
        # Hiragana
        if '\u3040' <= ch <= '\u309f':
            return True
        # Katakana
        if '\u30a0' <= ch <= '\u30ff':
            return True
    return False

def zhongwen_yuyan_jiance_xitong(text):
    if contains_kana(text):
        return False

    han = 0
    meaningful = 0
    for ch in text:
        if ch.isspace():
            continue
        category = unicodedata.category(ch)
        if category.startswith("P"):
            continue
        meaningful += 1
        if is_han(ch):
            han += 1
    if meaningful == 0:
        return False
    han_ratio = han / meaningful
    return han_ratio >= 0.4
