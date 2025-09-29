
"""Модуль Order: создание и оформление заказа"""
from datetime import datetime
from typing import List
from medicine import Medicine
from pharmacy import Pharmacy

class OrderItem:
    """Позиция в заказе: ссылка на Medicine и количество"""
    def __init__(self, medicine_name: str, quantity: int, unit_price: float):
        self.medicine_name = medicine_name
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def total(self) -> float:
        return self.unit_price * self.quantity

    def __repr__(self):
        return f"OrderItem({self.medicine_name!r}, qty={self.quantity}, unit_price={self.unit_price})"

class Order:
    """Класс заказа.

    Атрибуты:
        items (list[OrderItem])
        total (float)
        created_at (datetime)
    """
    def __init__(self):
        self.items: List[OrderItem] = []
        self.created_at = datetime.now()

    def add_item(self, medicine_name: str, quantity: int, unit_price: float) -> None:
        """Добавляет позицию в заказ (не взаимодействует с аптекой напрямую)."""
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self.items.append(OrderItem(medicine_name, quantity, unit_price))

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

    def checkout(self, pharmacy: Pharmacy) -> None:
        """Оформляет заказ: проверяет доступность и уменьшает количество в аптеке.

        Бросает ValueError, если какая-либо позиция недоступна (нет в нужном количестве или просрочена).
        """
        # проверяем все позиции сначала — атомарно
        for item in self.items:
            exact = pharmacy.get_exact_item(item.medicine_name, item.quantity)
            if exact is None:
                raise ValueError(f"Товар '{item.medicine_name}' недоступен в количестве {item.quantity} или просрочен")
        # если проверка пройдена — уменьшаем количество
        for item in self.items:
            exact = pharmacy.get_exact_item(item.medicine_name, item.quantity)
            # exact не может быть None здесь
            exact.purchase(item.quantity)

    def __repr__(self):
        return f"Order(items={self.items}, total={self.total:.2f}, created_at={self.created_at})"
