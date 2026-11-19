import re

KR_THRESHOLD = 0.65

def detect_kr_chars(text):
    # Match all Hangul blocks
    return re.findall(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]', text)

def is_korea(text):
    kr_chars = detect_kr_chars(text)

    if not kr_chars:
        return False

    total_weight = 0
    kr_weight = 0

    for char in text:
        if detect_kr_chars(char):
            kr_weight += 1.0
            total_weight += 1.0
        elif re.match(r'[A-Za-z]', char):
            total_weight += 0.5

    if total_weight == 0:
        return False

    return (kr_weight / total_weight) >= KR_THRESHOLD
