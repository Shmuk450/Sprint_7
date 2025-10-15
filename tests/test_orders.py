import pytest
import allure
from urls import ORDERS
from data import ORDER_COLORS
from helpers import order_payload_with_colors


@pytest.mark.usefixtures("session")
@allure.epic("API Яндекс.Самокат")
@allure.feature("Создание и получение заказов")
class TestOrders:
    """Тесты для ручек, связанных с заказами"""

    @allure.title("Создание заказа с комбинацией цветов: {colors}")
    @pytest.mark.parametrize("colors", ORDER_COLORS)
    def test_create_order_with_colors(self, session, colors):
        """Проверка: заказ можно создать с любыми комбинациями цветов"""
        with allure.step("Формируем тело запроса с выбранными цветами"):
            payload = order_payload_with_colors(colors)

        with allure.step("POST /api/v1/orders"):
            r = session.post(ORDERS, json=payload)

        with allure.step("Ожидаем 201 и тело с track"):
            assert r.status_code == 201, f"Ожидали 201, получили {r.status_code}: {r.text}"
            body = r.json()
            assert "track" in body, "В ответе нет поля 'track'"
            assert isinstance(body["track"], int) and body["track"] > 0, "Поле 'track' должно быть положительным числом"

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, session):
        """Проверка: возвращается список заказов"""
        with allure.step("GET /api/v1/orders"):
            r = session.get(ORDERS)

        with allure.step("Ожидаем 200 и наличие списка заказов"):
            assert r.status_code == 200, f"Ожидали 200, получили {r.status_code}: {r.text}"
            body = r.json()
            assert "orders" in body and isinstance(body["orders"], list), "Нет поля 'orders' или неверный тип"