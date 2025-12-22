import re

def is_numbers(text):
    return all(char.isdigit() or char in '.,-/+= ' for char in text)
