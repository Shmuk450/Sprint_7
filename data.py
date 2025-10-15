
# Позитивное тело для создания курьера (фиксированное — удобно для повторного запуска)
COURIER_OK = {"login": "auto_login_ok", "password": "auto_pass_ok", "firstName": "auto_name_ok"}

# Дубликат — создадим 2 раза одного и того же
COURIER_DUP = {"login": "dup_login", "password": "dup_pass", "firstName": "dup_name"}

# Наборы с пропущенными обязательными полями (для 400)
COURIER_MISSING_SETS = [
    {"password": "x", "firstName": "x"},   # без login
    {"login": "x", "firstName": "x"},      # без password
    {"login": "x", "password": "x"},       # без firstName (некоторые ревью просят тоже проверить)
]

# Базовый заказ (цвет добавляется параметром)
ORDER_BASE = {
    "firstName": "Иван",
    "lastName": "Иванов",
    "address": "Москва, Тверская 1",
    "metroStation": 4,
    "phone": "+7 800 555 35 35",
    "rentTime": 5,
    "deliveryDate": "2025-10-10",
    "comment": "Автотест"
}

# Варианты цветов под параметризацию
ORDER_COLORS = [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    []
]