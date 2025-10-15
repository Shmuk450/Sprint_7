import requests
import random
import string
from urls import COURIER, COURIER_LOGIN, courier_delete
from data import ORDER_BASE

def gen_str(n=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

def register_new_courier_and_return_login_password():
    login, password, first_name = gen_str(), gen_str(), gen_str()
    payload = {"login": login, "password": password, "firstName": first_name}
    r = requests.post(COURIER, data=payload)
    if r.status_code == 201:
        return [login, password, first_name]
    return []

def delete_courier_if_possible(login: str, password: str):
    """Пробуем залогиниться и удалить курьера, если получили id."""
    try:
        r = requests.post(COURIER_LOGIN, data={"login": login, "password": password})
        if r.status_code == 200 and 'id' in r.json():
            cid = r.json()['id']
            requests.delete(courier_delete(cid))
    except Exception:
        pass

def order_payload_with_colors(colors):
    body = dict(ORDER_BASE)  # копия
    body['color'] = colors
    return body