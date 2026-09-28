import string
import re
import unicodedata

symbol_categories = ["Po", "Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Sm", "Sc", "Sk", "So"]

def test_category(ch):
    for cat in symbol_categories:
        if unicodedata.category(ch) == cat:
            return True
    return False

def strip_punct(word):
    return word.strip(string.digits + string.punctuation + "…【】”“").lower()

def strip_symbols(word):
    return "".join(ch for ch in word if not test_category(ch) and not ("\uFE00" <= ch <= "\uFE0F"))

def is_symbol_only(text):
    text = text.strip().replace("\uFE0F", "") # variatoin selector
    if not text:
        return False

    # fuckig braille
    text = re.sub(r"[\u2800-\u283F\u2840-\u28FF]", "", text).strip()
    if len(text) == 0:
        return True

    return all(test_category(ch) for ch in text)
