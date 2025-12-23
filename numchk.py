import re
import emjchk

def is_numbers(text):
    return all(char.isdigit() or char in emjchk.symbols_punct for char in text)
