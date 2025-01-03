import settings

POST_CHECK_OK = 0
POST_CHECK_CENTAG = 1
POST_CHECK_NO_COMMENTARY = 2
POST_CHECK_IS_BANNED = 3

def centags_check(tags):
    for tag in tags.split():
        if tag.strip() in settings.CENTAGS:
            return tag
    return None

def check_post(post, commentary):
    gentags = post["tag_string_general"]
    metatags = post["tag_string_meta"]

    unwanted_tag = centags_check(gentags)
    if unwanted_tag is not None:
        return POST_CHECK_CENTAG, unwanted_tag
    unwanted_tag = centags_check(metatags)
    if unwanted_tag is not None:
        return POST_CHECK_CENTAG, unwanted_tag

    if len(commentary.og_title) == 0 and len(commentary.og_description) == 0:
        return POST_CHECK_NO_COMMENTARY, None

    if post["is_banned"] == True:
        return POST_CHECK_IS_BANNED, None

    return POST_CHECK_OK, None
