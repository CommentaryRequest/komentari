import re
import debug

# TODO make a generic module for writing system detectors

TH_THRESHOLD = 0.6

def detect_th_chars(text):
    if not text:
        return []

    return re.findall(r'[\u0E00-\u0E7F]', text)

def is_thai(text):
    debug.dprint(f"thchk: {text}")
    th_chars = detect_th_chars(text)

    if not th_chars:
        debug.dprint(f"  th chars not found")
        return False

    total_weight = 0
    th_weight = 0

    for char in text:
        if detect_th_chars(char):
            th_weight += 1.0
            total_weight += 1.0
        elif re.match(r'[A-Za-z]', char):
            total_weight += 0.5
        # Everything else is not weighted

    if total_weight == 0:
        return False

    ratio = (th_weight / total_weight)
    debug.dprint(f"  ratio {th_weight} / {total_weight} = {ratio} | thr={TH_THRESHOLD}")
    return ratio >= TH_THRESHOLD

