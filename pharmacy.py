"""Модуль Pharmacy: аптека и работа со списком лекарств"""
from typing import List
from medicine import Medicine

class Pharmacy:
    """Класс аптеки.

    Атрибуты:
        name (str): название аптеки
        address (str): адрес
        inventory (list[Medicine]): список лекарств
    """

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.inventory: List[Medicine] = []

    def add_medicine(self, medicine: Medicine) -> None:
        """Добавляет лекарство в инвентарь. Если лекарство с таким же именем и производителем уже
        присутствует — увеличивает количество.
        """
        for item in self.inventory:
            if item.name.lower() == medicine.name.lower() and item.manufacturer.lower() == medicine.manufacturer.lower() and item.expiry_date == medicine.expiry_date and item.price == medicine.price:
                # считаем это тем же товаром с теми же свойствами и датой — просто объединяем количество
                item.quantity += medicine.quantity
                return
        # иначе добавляем как новый товар
        self.inventory.append(medicine)

    def find_by_name(self, name: str) -> List[Medicine]:
        """Ищет лекарства по названию (регистронезависимо). Возвращает список совпадений."""
        name_lower = name.strip().lower()
        return [m for m in self.inventory if name_lower in m.name.lower()]

    def check_availability(self, name: str, quantity: int = 1) -> bool:
        """Проверяет, доступно ли требуемое количество не-просроченного товара по названию.

        Возвращает True, если нашёлся товар с достаточным количеством и не просроченный.
        """
        matches = self.find_by_name(name)
        for m in matches:
            if not m.is_expired() and m.quantity >= quantity:
                return True
        return False

    def get_exact_item(self, name: str, quantity: int = 1) -> Medicine | None:
        """Возвращает конкретный объект Medicine, который можно продать (непросроченный и достаточное количество).
        Если несколько с разными датами — отдаём тот, у которого раньше срок годности (FIFO по expiry_date).
        """
        matches = [m for m in self.find_by_name(name) if not m.is_expired() and m.quantity >= quantity]
        if not matches:
            return None
        # сортируем по expiry_date — продаём ближайший к истечению
        matches.sort(key=lambda x: x.expiry_date)
        return matches[0]

    def __repr__(self):
        return f"Pharmacy(name={self.name!r}, address={self.address!r}, inventory_size={len(self.inventory)})"
