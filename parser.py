import settings

# returned by parse for special commands
HELP = -1
SKIP = -2
QUIT = -3
BROWSER = -4
NONPERMANENT_SKIP = -5

def parse(user_input):
    result = ""
    tags = user_input.split()
    for tag in tags:
        tag_clean = tag.strip()
        if tag_clean == "h":
            return HELP
        elif tag_clean == "sk":
            return SKIP
        elif tag_clean == "q":
            return QUIT
        elif tag_clean == "b":
            return BROWSER
        elif tag_clean == "skk":
            return NONPERMANENT_SKIP
        if len(tag_clean) == 0:
            continue # is empty tag
        print(f"get '{tag_clean}'")
        real_tag = settings.TAGS.get(tag_clean, "!!!!!!!!")
        if real_tag == "!!!!!!!!":
            print(f"'{tag_clean}' unknown tag")
        result += real_tag + " "
    return result.strip()
