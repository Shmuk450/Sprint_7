import pytest
import random
import string
import allure
from urls import COURIER
from data import COURIER_OK, COURIER_DUP, COURIER_MISSING_SETS


def _rnd(n=8) -> str:
    """Генерирует случайную строку для уникального логина"""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))


@pytest.mark.usefixtures("session")
@allure.epic("API Яндекс.Самокат")
@allure.feature("Курьер: создание")
class TestCourierCreation:
    """Тесты для ручки создания курьера"""

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, session):
        """Проверка: курьера можно создать"""
        with allure.step("Готовим уникальные данные курьера"):
            data = COURIER_OK.copy()
            data["login"] = f"autotest_{_rnd()}"

        with allure.step("Отправляем POST /api/v1/courier"):
            r = session.post(COURIER, data=data)

        with allure.step("Проверяем код 201 и тело ответа {ok: true}"):
            assert r.status_code == 201, f"Ожидали 201, а получили {r.status_code}, тело: {r.text}"
            assert r.json().get("ok") is True

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_courier_duplicate(self, session):
        """Проверка: нельзя создать двух одинаковых курьеров"""
        with allure.step("Создаём курьера впервые"):
            session.post(COURIER, data=COURIER_DUP)

        with allure.step("Пытаемся создать того же курьера ещё раз"):
            r2 = session.post(COURIER, data=COURIER_DUP)

        with allure.step("Ожидаем код 409"):
            assert r2.status_code == 409, f"Ожидали 409, а получили {r2.status_code}"

    @allure.title("Отсутствие обязательных полей при создании курьера")
    @pytest.mark.parametrize("payload", COURIER_MISSING_SETS)
    def test_create_courier_missing_required_field(self, session, payload):
        """
        Если отсутствует login или password — 400.
        Если отсутствует только firstName — 201 (firstName не обязателен).
        """
        with allure.step("Готовим тело запроса с пропущенным полем"):
            data = payload.copy()
            if "login" in data:
                data["login"] = f"autotest_{_rnd()}"

        with allure.step("Отправляем POST /api/v1/courier"):
            r = session.post(COURIER, data=data)

        if "login" not in data or "password" not in data:
            with allure.step("Проверяем, что вернулся 400 из-за отсутствия обязательного поля"):
                assert r.status_code == 400, f"Ожидали 400, получили {r.status_code}, тело: {r.text}"
        else:
            with allure.step("Проверяем, что firstName не обязателен — код 201"):
                assert r.status_code == 201, f"Ожидали 201 (firstName не обязателен), получили {r.status_code}"
                assert r.json().get("ok") is True