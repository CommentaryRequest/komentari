import re
import unicodedata
import debug

JP_THRESHOLD = 0.6

def detect_jp_chars(text):
    if not text:
        return []

    # Including both full-width and half-width katakana
    return re.findall(r'[\u3040-\u309F\u30A0-\u30FF\uFF00-\uFFEF\u4E00-\u9FFF\uFF61-\uFF9F]', text)

def is_japan(text):
    debug.dprint(f"jpchk: {text}")
    jp_chars = detect_jp_chars(text)

    if not jp_chars:
        debug.dprint(f"  jp chars not found")
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

    ratio = (jp_weight / total_weight)
    debug.dprint(f"  ratio {jp_weight} / {total_weight} = {ratio} | thr={JP_THRESHOLD}")
    return ratio >= JP_THRESHOLD

