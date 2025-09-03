import string
import re
import urllib.parse
import jpchk
import kkchk
import unicodedata

def fetch_words():
    with open("./wl.txt", "r") as file:
        return file.read().split("\n")

def rms(old, current):
    if old == current:
        return current
    return rms(current, current.strip(string.digits).strip(string.punctuation))

def ing(word):
    if len(word) > 3 and word.endswith(("in", "in'")):
        return word.rstrip("'") + "g"
    return word

def unemoji(text):
    return "".join(ch for ch in text if not unicodedata.category(ch).startswith("So") and not ("\uFE00" <= ch <= "\uFE0F"))

def clean(word):
    return ing(rms("", unemoji(word)).lower()).strip()

def is_number(word: str):
    try:
        float(word)
        return True
    except ValueError:
        try:
            float(word.replace(",", "."))
        except ValueError:
            return False
        return True

def is_url(word: str):
    return word.startswith(("http://", "https://"))

def is_emoji(word):
    return all(unicodedata.category(char).startswith("So") or ("\uFE00" <= char <= "\uFE0F") for char in word)

def recog(text):
    if jpchk.detect_jp_chars(text) or kkchk.detect_kr_chars(text):
        return 0

    words = fetch_words()
    text_words = text.split()
    real_words = 0
    fake_words = 0
    for word in text_words:
        # emoji
        if is_emoji(word.strip()):
            continue

        cword = clean(word)

        # empty words
        if not cword.strip():
            fake_words += 1
            continue

        # single letter words
        if len(cword) == 1 and cword.lower() not in ("a", "i"):
            fake_words += 1
            continue

        # number words
        if is_number(cword):
            fake_words += 1
            continue

        # url words
        if is_url(cword):
            fake_words += 1
            continue

        # real word
        if cword in words:
            real_words += 1
            print(f"real: '{cword}' (dirty: '{word}')")

        # fake word
        else:
            print(f"what: '{cword}' (dirty: '{word}')")
            pass

    total_not_fake_words = (len(text_words) - fake_words)
    if total_not_fake_words == 0 or real_words == 0:
        return 0

    return real_words / total_not_fake_words
