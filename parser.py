import settings
import debug

# returned by parse for special commands
HELP = -1
SKIP = -2
QUIT = -3
BROWSER = -4
NONPERMANENT_SKIP = -5
PROGRESS_CHECK = -6

SPECIAL_TAGS = {
    "h": (HELP, "Show this help"),
    "sk": (SKIP, "Skip this post"),
    "q": (QUIT, "Quit"),
    "b": (BROWSER, "Open post in the browser"),
    "skk": (NONPERMANENT_SKIP, "Skip this post once"),
    "?": (PROGRESS_CHECK, "Check progress (offline only)")
}

ERROR = "!!!!!!!!"

def negate_tags(tags):
    sp = tags.split()
    result = ""
    for tag in sp:
        result += f"-{tag} "
    return result.rstrip()

def parse(user_input):
    result = ""
    tags = user_input.split()
    for tag in tags:
        tag_clean = tag.strip()
        negative = tag_clean[0] == "-"
        tag_clean = tag.lstrip("-")

        if len(tag_clean) == 0:
            continue # is empty tag
        if tag_clean[0] == "~":
            result += ("-" if negative else "") + tag_clean[1:] + " "
            continue

        if tag in SPECIAL_TAGS:
            return SPECIAL_TAGS[tag][0]
        debug.dprint(f"get '{tag_clean}'")
        real_tag = settings.TAGS.get(tag_clean, ERROR)
        if real_tag == ERROR:
            print(f"'{tag_clean}' unknown tag")
        result += (negate_tags(real_tag) if negative else real_tag) + " "
    return result.strip()
