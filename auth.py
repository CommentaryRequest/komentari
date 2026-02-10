import settings

class Auth:
    def __init__(self, test_mode):
        self.login = settings.TEST_LOGIN if test_mode else settings.LOGIN
        self.key = settings.TEST_APIKEY if test_mode else settings.APIKEY

    def set_auth(self, login, key):
        self.login = login
        self.key = key

    def __str__(self):
        return f"login={self.login}&api_key={self.key}"
