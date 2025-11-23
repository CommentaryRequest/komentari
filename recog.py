import string
import unicodedata
import jpchk
import kkchk

def fetch_words():
    with open("./wl.txt", "r") as f:
        return set([word.lower() for word in f.read().splitlines()])

def clean_word(word: str, wl) -> str:
    """
    Normalize a word: strip emojis, punctuation, digits, lowercase, fix 'in' -> 'ing'.
    """
    # Remove emojis
    word = "".join(ch for ch in word if not unicodedata.category(ch).startswith("So") and not ("\uFE00" <= ch <= "\uFE0F"))
    # Fix fancy apostrophes
    word = word.replace("’", "'")
    word = word.replace("´", "'")
    # Remove digits and punctuation
    word = word.strip(string.digits + string.punctuation).lower()
    # Convert "in'" -> "ing"
    if len(word) > 3 and word.endswith(("in", "in'")) and word not in wl:
        word = word.rstrip("'") + "g"
    return word

def is_number(word: str) -> bool:
    try:
        float(word)
        return True
    except ValueError:
        try:
            float(word.replace(",", "."))
            return True
        except ValueError:
            return False

def is_url(word: str) -> bool:
    return word.startswith(("http://", "https://"))

def is_emoji(word: str) -> bool:
    return all(unicodedata.category(ch).startswith("So") or ("\uFE00" <= ch <= "\uFE0F") for ch in word)

def recog(text: str) -> float:
    """
    Returns confidence that text is valid English.
    """
    # Reject Japanese or Korean entirely
    if jpchk.detect_jp_chars(text) or kkchk.detect_kr_chars(text):
        return 0.0

    words = fetch_words()
    text_words = text.split()

    # Filter out words that are empty, emojis, numbers, URLs, or meaningless single letters
    valid_words = []
    real_words = 0

    for w in text_words:
        if is_emoji(w) or not w.strip():
            continue
        cw = clean_word(w, words)
        if not cw:
            continue
        if len(cw) == 1 and cw not in ("a", "i"):
            continue
        if is_number(cw) or is_url(cw):
            continue

        valid_words.append(cw)
        if cw in words:
            print(f"good word: {cw}")
            real_words += 1
        else:
            print(f"bad word: {cw}")

    print(f"valid words: {valid_words} | real words: {real_words}")

    if not valid_words or real_words == 0:
        return 0.0

    return real_words / len(valid_words)
