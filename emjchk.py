import emoji

def is_emoji(text):
    text = text.strip().replace("\uFE0F", "") # variatoin selector
    if not text:
        return False

    return all(ch in emoji.EMOJI_DATA for ch in text)
