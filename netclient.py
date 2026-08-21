import settings
import requests
import time
from booru_url import get_booru_url

class NetworkClient:
    def __init__(self, test_mode):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": settings.USERAGENT
        }

        self.base_url = get_booru_url(test_mode)
        
        if test_mode:
            self.set_auth(settings.TEST_LOGIN, settings.TEST_APIKEY)
        else:
            self.set_auth(settings.LOGIN, settings.APIKEY)

    def set_auth(self, login, key):
        self.session.auth = requests.auth.HTTPBasicAuth(login, key)

    def get(self, url, **kwargs):
        while True:
            try:
                response = self.session.get(f"{self.base_url}/{url}", timeout=10, **kwargs)
                time.sleep(settings.REQUEST_DELAY)
                if response.status_code in (201, 204):
                    return {}, response
                json_resp = response.json()
                if "success" in json_resp and not json_resp["success"]:
                    print(f"Unsuccessful response ({url}): {response.text}")
                    continue
                return json_resp, response
            except requests.exceptions.JSONDecodeError:
                print(f"Server returned non-JSON response ({url}): {response.text}")
                time.sleep(0.5)
            except Exception as exc:
                print(f"Failed to fetch {url}: {exc}")
                time.sleep(0.5)

    def put(self, url, data, **kwargs):
        while True:
            try:
                response = self.session.put(f"{self.base_url}/{url}", timeout=10, json=data, **kwargs)
                time.sleep(settings.REQUEST_DELAY)
                if response.status_code in (201, 204):
                    return {}, response
                json_resp = response.json()
                if "success" in json_resp and not json_resp["success"]:
                    print(f"Unsuccessful response ({url}): {response.text}")
                    continue
                return json_resp, response
            except requests.exceptions.JSONDecodeError:
                print(f"Server returned non-JSON response ({url}): {response.text}")
                time.sleep(0.5)
            except Exception as exc:
                print(f"Failed to fetch {url}: {exc}")
                time.sleep(0.5)
