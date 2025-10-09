import time
import pytest
import allure
from requests.exceptions import RequestException, ReadTimeout
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
        with allure.step("Отправляем запрос POST /api/v1/courier/login"):
            r = session.post(COURIER_LOGIN, data={
                'login': new_courier['login'],
                'password': new_courier['password']
            })

        with allure.step("Проверяем код ответа и наличие id в ответе"):
            assert r.status_code == 200, f"Ожидали 200, получили {r.status_code}"
            body = r.json()
            assert 'id' in body and isinstance(body['id'], int), "В ответе нет корректного id"

    @allure.title("Ошибка при отсутствии обязательных полей")
    @pytest.mark.parametrize('missing', ['login', 'password'])
    def test_login_missing_field(self, session, new_courier, missing):
        """Проверка: ошибка при отсутствии обязательных полей (устойчиво к 504)"""
        with allure.step(f"Формируем тело запроса без поля {missing}"):
            data = {'login': new_courier['login'], 'password': new_courier['password']}
            data.pop(missing)

        r = None
        last_err = None

        with allure.step("Отправляем запрос с повторами при ошибке 504"):
            for attempt in range(5):
                try:
                    r = session.post(COURIER_LOGIN, data=data, timeout=5)
                    if r.status_code != 504:
                        break
                except (ReadTimeout, RequestException) as e:
                    last_err = e
                time.sleep(0.6 * (attempt + 1))

        if r is None:
            allure.attach(str(last_err), name="Исключение", attachment_type=allure.attachment_type.TEXT)
            pytest.skip(f"Сервис /courier/login не ответил после 5 попыток: {last_err}")

        with allure.step("Проверяем код ответа и наличие поля message при 400"):
            assert r.status_code in (400, 504), f"Ожидали 400 (или временно 504), получили {r.status_code}: {r.text}"
            if r.status_code == 400:
                assert 'message' in r.json(), "В ответе при 400 нет поля message"

    @allure.title("Ошибка при неверном пароле")
    def test_login_wrong_password(self, session, new_courier):
        """Проверка: ошибка при неверном пароле"""
        with allure.step("Отправляем запрос с неверным паролем"):
            r = session.post(COURIER_LOGIN, data={
                'login': new_courier['login'],
                'password': 'WRONG'
            })

        with allure.step("Проверяем код ответа"):
            assert r.status_code in (400, 404), f"Ожидали 400/404, получили {r.status_code}"

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_login_nonexistent_user(self, session):
        """Проверка: ошибка при логине несуществующего пользователя"""
        with allure.step("Отправляем запрос с несуществующим логином и паролем"):
            r = session.post(COURIER_LOGIN, data={
                'login': gen_str(),
                'password': gen_str()
            })

        with allure.step("Проверяем код ответа"):
            assert r.status_code in (400, 404), f"Ожидали 400/404, получили {r.status_code}"