import re

def is_japan(text):
    # Including both full-width and half-width katakana
    jp_chars = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\uFF00-\uFFEF\u4E00-\u9FFF\uFF61-\uFF9F]', text)
    latin_chars = re.findall(r'[A-Za-z]', text)

    if not jp_chars:
        return False

    return len(latin_chars) < len(jp_chars) * 0.15

