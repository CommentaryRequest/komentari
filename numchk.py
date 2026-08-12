import symchk

def is_numbers(text):
    return all(char.isdigit() or char.isspace() or symchk.test_category(char) for char in text)
