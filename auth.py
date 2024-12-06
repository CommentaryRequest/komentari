import settings

class Auth:
    def __init__(self):
        self.login = settings.TEST_LOGIN if settings.TESTMODE else settings.LOGIN
        self.key = settings.TEST_APIKEY if settings.TESTMODE else settings.APIKEY

    def __str__(self):
        return f"login={self.login}&api_key={self.key}"
