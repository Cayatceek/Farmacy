"""Модуль Medicine: описание лекарства"""
from datetime import date

class Medicine:
    """Класс, представляющий лекарство.

    Атрибуты:
        name (str): название лекарства
        manufacturer (str): производитель
        price (float): цена за одну единицу
        expiry_date (date): дата окончания срока годности
        quantity (int): количество в запасе
    """

    def __init__(self, name: str, manufacturer: str, price: float, expiry_date: date, quantity: int):
        self.name = name
        self.manufacturer = manufacturer
        self.price = float(price)
        self.expiry_date = expiry_date
        self.quantity = int(quantity)

    def is_expired(self, on_date: date | None = None) -> bool:
        """Проверяет, просрочено ли лекарство на указанную дату (по умолчанию — сегодня).

        Аргументы:
            on_date (date | None): дата для проверки

        Возвращает:
            bool: True, если лекарство просрочено
        """
        if on_date is None:
            on_date = date.today()
        return self.expiry_date < on_date

    def purchase(self, amount: int) -> float:
        """Уменьшает количество при покупке и возвращает стоимость.

        Бросает ValueError если недостаточно товара или запрошено отрицательное количество.
        """
        if amount <= 0:
            raise ValueError("Количество для покупки должно быть положительным")
        if amount > self.quantity:
            raise ValueError(f"Недостаточно товара: доступно {self.quantity}, запрошено {amount}")
        self.quantity -= amount
        total_price = self.price * amount
        return total_price

    def __repr__(self):
        return (
            f"Medicine(name={self.name!r}, manufacturer={self.manufacturer!r}, "
            f"price={self.price}, expiry_date={self.expiry_date}, quantity={self.quantity})"
        )