import settings

override = None

def set_override(url):
    global override
    override = url

def resolve_url():
    return override if override else "https://danbooru.donmai.us"

def get_booru_url():
    return "https://testbooru.donmai.us" if settings.TESTMODE else resolve_url()
