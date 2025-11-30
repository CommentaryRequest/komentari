import string
import unicodedata
import jpchk
import kkchk

wordlist = set()
wordlist_initialized = False

def fetch_words():
    if not wordlist_initialized:
        with open("./wl.txt", "r") as f:
            wordlist = set([word.lower() for word in f.read().splitlines()])
    return wordlist

def strip_emoji(word):
    return "".join(ch for ch in word if not unicodedata.category(ch).startswith("So") and not ("\uFE00" <= ch <= "\uFE0F"))

def strip_punct(word):
    return word.strip(string.digits + string.punctuation + "…【】”“").lower()

def clean_word(word: str, wl) -> str:
    """
    Normalize a word: strip emojis, punctuation, digits, lowercase, fix 'in' -> 'ing'.
    """
    word = strip_emoji(word)

    # Fix fancy apostrophes
    word = word.replace("’", "'")
    word = word.replace("´", "'")

    word = strip_punct(word)

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
