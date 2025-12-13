import requests


API_BASE = "http://127.0.0.1:8000/API/api/v1"

def _url(resource: str, pk=None):
    
    if pk is None:
        return f"{API_BASE}/{resource}/"
    return f"{API_BASE}/{resource}/{pk}/"

def api_list(resource: str):
    r = requests.get(_url(resource), timeout=10)
    r.raise_for_status()
    return r.json()

def api_get(resource: str, pk: int):
    r = requests.get(_url(resource, pk), timeout=10)
    r.raise_for_status()
    return r.json()

def api_create(resource: str, data: dict):
    r = requests.post(_url(resource), json=data, timeout=10)
    r.raise_for_status()
    return r.json()

def api_update(resource: str, pk: int, data: dict):
    r = requests.put(_url(resource, pk), json=data, timeout=10)
    r.raise_for_status()
    return r.json()

def api_delete(resource: str, pk: int):
    r = requests.delete(_url(resource, pk), timeout=10)
    r.raise_for_status()
    return True
