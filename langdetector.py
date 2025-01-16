try:
    import langdetect
except ImportError:
    print("Langdetector: langdetect module not installed. Please install for language recognition function.")

import sys

def detectlang(text):
    if "langdetect" in sys.modules:
        try:
            return langdetect.detect(text)
        except langdetect.lang_detect_exception.LangDetectException as exc:
            print(f"Error suggesting tags: {exc}")
            return None
    return None
