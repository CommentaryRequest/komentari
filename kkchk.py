import re

def detect_kr_chars(text):
    # Match all Hangul blocks
    return re.findall(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]', text)

def is_korea(text):
    kr_chars = detect_kr_chars(text)
    latin_chars = re.findall(r'[A-Za-z]', text)

    if not kr_chars:
        return False

    return len(latin_chars) < len(kr_chars) * 0.15

