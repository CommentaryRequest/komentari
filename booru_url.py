import settings

def get_booru_url():
    return "https://testbooru.donmai.us" if settings.TESTMODE else "https://danbooru.donmai.us"
