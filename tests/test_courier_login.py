import pytest
import allure
from urls import COURIER_LOGIN
from helpers import gen_str


@pytest.mark.usefixtures("session")
@allure.epic("API Яндекс.Самокат")
@allure.feature("Авторизация курьера")
class TestCourierLogin:
    """Тесты для логина курьера"""

    @allure.title("Успешная авторизация курьера")
    def test_courier_can_login(self, session, new_courier):
        """Проверка: курьер может авторизоваться"""
        with allure.step("POST /api/v1/courier/login с валидными кредами"):
            r = session.post(COURIER_LOGIN, data={
                "login": new_courier["login"],
                "password": new_courier["password"],
            })

        with allure.step("Ожидаем 200 и наличие id в ответе"):
            assert r.status_code == 200, f"Ожидали 200, получили {r.status_code}"
            body = r.json()
            assert "id" in body and isinstance(body["id"], int), "В ответе нет корректного id"

    @allure.title("Ошибка при отсутствии обязательных полей (ожидаем 400)")
    @pytest.mark.parametrize("missing", ["login", "password"])
    def test_login_missing_field(self, session, new_courier, missing):
        """Если отсутствует login или password — 400 c message"""
        with allure.step(f"Готовим тело запроса без поля {missing}"):
            data = {"login": new_courier["login"], "password": new_courier["password"]}
            data.pop(missing)

        with allure.step("POST /api/v1/courier/login"):
            r = session.post(COURIER_LOGIN, data=data)

        with allure.step("Ожидаем ровно 400 и валидный message"):
            assert r.status_code == 400, f"Ожидали 400, получили {r.status_code}: {r.text}"
            body = r.json()
            assert "message" in body, "В ответе нет поля 'message'"
            assert "недостаточно данных" in body["message"].lower(), "Текст message не соответствует ожиданиям"

    @allure.title("Ошибка при неверном пароле (ожидаем 404)")
    def test_login_wrong_password(self, session, new_courier):
        """При неверном пароле — 404 c message"""
        with allure.step("POST /api/v1/courier/login с неверным паролем"):
            r = session.post(COURIER_LOGIN, data={
                "login": new_courier["login"],
                "password": "WRONG",
            })

        with allure.step("Ожидаем ровно 404 и валидный message"):
            assert r.status_code == 404, f"Ожидали 404, получили {r.status_code}: {r.text}"
            body = r.json()
            assert "message" in body, "В ответе нет поля 'message'"
            assert isinstance(body["message"], str) and body["message"].strip(), "Поле 'message' пустое"

    @allure.title("Ошибка при авторизации несуществующего пользователя (ожидаем 404)")
    def test_login_nonexistent_user(self, session):
        """Неизвестный логин/пароль — 404 c message"""
        with allure.step("POST /api/v1/courier/login с рандомными логином/паролем"):
            r = session.post(COURIER_LOGIN, data={
                "login": gen_str(),
                "password": gen_str(),
            })

        with allure.step("Ожидаем ровно 404 и валидный message"):
            assert r.status_code == 404, f"Ожидали 404, получили {r.status_code}: {r.text}"
            body = r.json()
            assert "message" in body, "В ответе нет поля 'message'"
            assert isinstance(body["message"], str) and body["message"].strip(), "Поле 'message' пустое"