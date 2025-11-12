import re

def is_numbers(text):
    stripped = re.sub(r'[A-Za-z\S]', '', text)
    if not stripped:
        return False
    return all(char.isdigit() or char in '.,-/ ' for char in stripped) # TODO more special chars
