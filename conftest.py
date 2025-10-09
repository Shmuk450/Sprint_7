import pytest
import requests
from helpers import register_new_courier_and_return_login_password, delete_courier_if_possible

@pytest.fixture
def session():
    s = requests.Session()
    yield s
    s.close()

@pytest.fixture
def new_courier():
    """Регистрирует курьера и возвращает его креды; в конце — пытается удалить."""
    creds = register_new_courier_and_return_login_password()
    assert creds, 'Не удалось зарегистрировать тестового курьера (201 не получен)'
    login, password, first_name = creds
    yield {"login": login, "password": password, "firstName": first_name}
    delete_courier_if_possible(login, password)