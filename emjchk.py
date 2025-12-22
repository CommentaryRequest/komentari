import emoji
import string

symbols_emoji = list(emoji.EMOJI_DATA)
symbols_punct = list(string.punctuation)
symbols = symbols_emoji + symbols_punct + [" "]

def is_emoji(text):
    text = text.strip().replace("\uFE0F", "") # variatoin selector
    if not text:
        return False

    return all(ch in symbols for ch in text)
