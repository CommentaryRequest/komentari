import re
import unicodedata

JP_THRESHOLD = 0.65

def detect_jp_chars(text):
    # Including both full-width and half-width katakana
    return re.findall(r'[\u3040-\u309F\u30A0-\u30FF\uFF00-\uFFEF\u4E00-\u9FFF\uFF61-\uFF9F]', text)

def is_japan(text):
    jp_chars = detect_jp_chars(text)

    if not jp_chars:
        return False

    total_weight = 0
    jp_weight = 0

    for char in text:
        if detect_jp_chars(char):
            jp_weight += 1.0
            total_weight += 1.0
        elif re.match(r'[A-Za-z]', char):
            total_weight += 0.5
        # Everything else is not weighted

    if total_weight == 0:
        return False

    return (jp_weight / total_weight) >= JP_THRESHOLD

