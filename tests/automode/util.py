import automode
from booru.commentary import Commentary

def detect_tags_simple(commentary):
    return automode.detect_tags_all(commentary, 0, [], False, "https://example.com")

def alt_text_commentary(description, alt_text):
    return Commentary(None, f"{description}\n\n[quote]\nh6. Image Description\n\n{alt_text}\n[/quote]", None, None)
