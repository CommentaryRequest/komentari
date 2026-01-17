import emoji
import string
import re
import unicodedata

symbols_emoji = list(emoji.EMOJI_DATA)
symbols_punct = list(string.punctuation)
symbols = symbols_emoji + symbols_punct + [" "] # this one is here just in case. idk.

symbol_categories = ["Po", "Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Sm", "Sc", "Sk", "So"]

def test_category(ch):
    for cat in symbol_categories:
        if unicodedata.category(ch) == cat:
            return True
    return False

def is_symbol(ch):
    return ch in symbols or test_category(ch)

def is_emoji(text):
    text = text.strip().replace("\uFE0F", "") # variatoin selector
    if not text:
        return False

    # fuckig braille
    text = re.sub(r"[\u2800-\u283F\u2840-\u28FF]", "", text).strip()
    if len(text) == 0:
        return True

    return all(is_symbol(ch) for ch in text)
