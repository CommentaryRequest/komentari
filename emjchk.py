import emoji
import string
import re

symbols_emoji = list(emoji.EMOJI_DATA)
symbols_punct = list(string.punctuation)
symbols = symbols_emoji + symbols_punct + [" "]

def is_emoji(text):
    text = text.strip().replace("\uFE0F", "") # variatoin selector
    if not text:
        return False

    text = re.sub(r"[\u2800-\u283F\u2840-\u28FF]", "", text).strip()
    if len(text) == 0:
        return True

    return all(ch in symbols for ch in text)
