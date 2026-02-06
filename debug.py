import settings
import json
import requests

custom_login = None
custom_apikey = None

def redact_auth_info(text):
    global custom_login, custom_apikey
    if custom_login:
        text = text.replace(f"login={custom_login}", "login=[custom login]")
    if custom_apikey:
        text = text.replace(custom_apikey, "[custom apikey]")
    return (text
        .replace(f"login={settings.TEST_LOGIN}", "login=[test login]")
        .replace(settings.TEST_APIKEY, "[test apikey]")
        .replace(f"login={settings.LOGIN}", "login=[login]")
        .replace(settings.APIKEY, "[apikey]")
    )

def set_custom_creds(login, apikey):
    global custom_login, custom_apikey
    custom_login = login
    custom_apikey = apikey

def dprint(message):
    if not settings.DEBUGMODE:
        return
    print(f"dbg: {redact_auth_info(message)}")

def safedumps(response):
    try:
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.JSONDecodeError:
        return response.text
