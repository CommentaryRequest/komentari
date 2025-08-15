import settings

def parse(user_input):
    result = ""
    tags = user_input.split()
    for tag in tags:
        tag_clean = tag.strip()
        if tag_clean == "h":
            return -1
        elif tag_clean == "sk":
            return -2
        elif tag_clean == "q":
            return -3
        elif tag_clean == "b":
            return -4
        elif tag_clean == "skk":
            return -5
        if len(tag_clean) == 0:
            continue # is empty tag
        print(f"get '{tag_clean}'")
        real_tag = settings.TAGS.get(tag_clean, "!!!!!!!!")
        if real_tag == "!!!!!!!!":
            print(f"'{tag_clean}' unknown tag")
        result += real_tag + " "
    return result.strip()
