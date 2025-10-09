BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

# Курьеры
COURIER = f'{BASE_URL}/courier'
COURIER_LOGIN = f'{BASE_URL}/courier/login'
def courier_delete(courier_id: int) -> str:
    return f'{COURIER}/{courier_id}'

# Заказы
ORDERS = f'{BASE_URL}/orders'