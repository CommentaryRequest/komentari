import re

def extract_hashtags(text):
    pattern = r'"#([^"]+)"'
    return re.findall(pattern, text)
