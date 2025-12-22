import requests

API_BASE = "http://127.0.0.1:8000/API/api/v1/"
LOGIN_URL = "http://127.0.0.1:8000/API/api/v1/auth/login/"
REFRESH_URL = "http://127.0.0.1:8000/API/api/v1/auth/refresh/"


def _url(resource: str, pk=None) -> str:
    base = API_BASE.rstrip("/") + "/"
    if pk is None:
        return f"{base}{resource}/"
    return f"{base}{resource}/{pk}/"


def _headers(request):
    token = request.session.get("api_access")
    scheme = request.session.get("api_scheme", "Bearer")  
    h = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"{scheme} {token}"
    return h



def _refresh_if_needed(request) -> bool:
    refresh = request.session.get("api_refresh")
    if not refresh:
        return False
    r = requests.post(REFRESH_URL, json={"refresh": refresh}, timeout=10)

    if r.status_code == 200:
        data = r.json()
        request.session["api_access"] = data.get("access")
        if data.get("refresh"):
            request.session["api_refresh"] = data.get("refresh")
        return True

    request.session.pop("api_access", None)
    request.session.pop("api_refresh", None)
    return False


def _request(request, method: str, url: str, **kwargs):
    headers = kwargs.pop("headers", {})
    headers = {**headers, **_headers(request)}

    resp = requests.request(method, url, headers=headers, timeout=10, **kwargs)

    # si 401, intentamos refresh y repetimos
    if resp.status_code == 401 and _refresh_if_needed(request):
        headers = {**headers, **_headers(request)}
        resp = requests.request(method, url, headers=headers, timeout=10, **kwargs)

    resp.raise_for_status()
    return resp


def api_list(request, resource):
    return _request(request, "GET", _url(resource)).json()


def api_get(request, resource, obj_id):
    return _request(request, "GET", _url(resource, obj_id)).json()


def api_create(request, resource, payload):
    return _request(request, "POST", _url(resource), json=payload).json()


def api_update(request, resource, obj_id, payload):
    return _request(request, "PUT", _url(resource, obj_id), json=payload).json()


def api_delete(request, resource, obj_id):
    _request(request, "DELETE", _url(resource, obj_id))
    return True
