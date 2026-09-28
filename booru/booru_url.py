import settings

override = None

def set_override(url):
    global override
    override = url

def resolve_url():
    return override if override else settings.BOORU_URL

def get_booru_url(test_mode):
    return settings.TESTBOORU_URL if test_mode else resolve_url()
