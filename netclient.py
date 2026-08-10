import settings
import requests
from booru_url import get_booru_url

class NetworkClient:
    def __init__(self, test_mode):
        self.test_mode = test_mode

        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": settings.USERAGENT
        }
        
        if test_mode:
            self.set_auth(settings.TEST_LOGIN, settings.TEST_APIKEY)
        else:
            self.set_auth(settings.LOGIN, settings.APIKEY)

    def set_auth(self, login, key):
        self.session.auth = requests.auth.HTTPBasicAuth(login, key)

    def get(self, url, **kwargs):
        while True:
            try:
                response = self.session.get(f"{get_booru_url(self.test_mode)}/{url}", timeout=10, **kwargs)
                return response.json(), response
            except requests.exceptions.JSONDecodeError:
                print(f"Server returned non-JSON response ({url}): {response.text}")
            except Exception as exc:
                print(f"Failed to fetch {url}: {exc}")

    def put(self, url, data, **kwargs):
        while True:
            try:
                response = self.session.put(f"{get_booru_url(self.test_mode)}/{url}", timeout=10, json=data, **kwargs)
                return response.json(), response
            except requests.exceptions.JSONDecodeError:
                print(f"Server returned non-JSON response ({url}): {response.text}")
            except Exception as exc:
                print(f"Failed to fetch {url}: {exc}")
