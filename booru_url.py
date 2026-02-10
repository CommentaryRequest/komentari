import settings

override = None

def set_override(url):
    global override
    override = url

def resolve_url():
    return override if override else "https://danbooru.donmai.us"

def get_booru_url(test_mode):
    return "https://testbooru.donmai.us" if test_mode else resolve_url()
