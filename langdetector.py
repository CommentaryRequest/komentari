try:
    import langdetect
except ImportError:
    print("Langdetector: langdetect module not installed. Please install for language recognition function.")

import sys

def detectlang(text):
    if "langdetect" in sys.modules:
        return langdetect.detect(text)
    return None
