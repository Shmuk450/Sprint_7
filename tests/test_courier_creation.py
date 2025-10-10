import pytest
import allure
from urls import COURIER
from data import COURIER_OK, COURIER_DUP, COURIER_MISSING_SETS
from helpers import gen_str


@pytest.mark.usefixtures("session")
@allure.epic("API Яндекс.Самокат")
@allure.feature("Курьер: создание")
class TestCourierCreation:
    """Тесты для ручки создания курьера"""

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, session):
        data = COURIER_OK.copy()
        data["login"] = f"autotest_{gen_str()}"

        r = session.post(COURIER, data=data)

        assert r.status_code == 201, f"Ожидали 201, а получили {r.status_code}: {r.text}"
        body = r.json()
        assert body.get("ok") is True, "В ответе нет ok:true"

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_courier_duplicate(self, session):
        session.post(COURIER, data=COURIER_DUP)
        r2 = session.post(COURIER, data=COURIER_DUP)

        assert r2.status_code == 409, f"Ожидали 409, а получили {r2.status_code}"
        body = r2.json()
        assert "message" in body, "В ответе нет поля 'message'"
        assert isinstance(body["message"], str) and body["message"].strip(), "Поле 'message' пустое"


    @allure.title("Ошибка при создании курьера без логина")
    def test_create_courier_without_login(self, session):
        data = {"password": "1234", "firstName": "TestName"}
        r = session.post(COURIER, data=data)

        assert r.status_code == 400, f"Ожидали 400, получили {r.status_code}: {r.text}"
        body = r.json()
        assert "message" in body, "Нет поля message"
        assert "недостаточно данных" in body["message"].lower(), "Некорректный текст ошибки"

    @allure.title("Ошибка при создании курьера без пароля")
    def test_create_courier_without_password(self, session):
        data = {"login": f"autotest_{gen_str()}", "firstName": "TestName"}
        r = session.post(COURIER, data=data)

        assert r.status_code == 400, f"Ожидали 400, получили {r.status_code}: {r.text}"
        body = r.json()
        assert "message" in body, "Нет поля message"
        assert "недостаточно данных" in body["message"].lower(), "Некорректный текст ошибки"

    @allure.title("Создание курьера без firstName (поле не обязательно)")
    def test_create_courier_without_first_name(self, session):
        data = {"login": f"autotest_{gen_str()}", "password": "1234"}
        r = session.post(COURIER, data=data)

        assert r.status_code == 201, f"Ожидали 201, получили {r.status_code}: {r.text}"
        body = r.json()
        assert body.get("ok") is True, "В ответе нет ok:true"