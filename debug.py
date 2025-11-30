import settings
import json
import requests

def dprint(message):
    if not settings.DEBUGMODE:
        return
    print(f"dbg: {message}")

def safedumps(response):
    try:
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.JSONDecodeError:
        return response.text
