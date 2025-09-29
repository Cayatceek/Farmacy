"""Тесты для аптеки с использованием pytest"""
from datetime import date, timedelta
import pytest

from medicine import Medicine
from pharmacy import Pharmacy
from order import Order


def setup_sample_pharmacy():
    today = date.today()
    p = Pharmacy('ТестАптека', 'Тестовая 1')
    p.add_medicine(Medicine('Парацетамол', 'Фарм', 50.0, today + timedelta(days=100), 10))
    p.add_medicine(Medicine('Ибупрофен', 'Heal', 80.0, today + timedelta(days=30), 5))
    p.add_medicine(Medicine('Анальгин', 'Меди', 30.0, today - timedelta(days=1), 10))  # просрочен
    return p


def test_find_by_name():
    p = setup_sample_pharmacy()
    found = p.find_by_name('парацет')
    assert len(found) == 1
    assert found[0].name == 'Парацетамол'


def test_check_availability_and_purchase():
    p = setup_sample_pharmacy()
    assert p.check_availability('Парацетамол', 2) is True
    item = p.get_exact_item('Парацетамол', 2)
    price = item.price
    # имитируем покупку
    total = item.purchase(2)
    assert total == price * 2
    assert item.quantity == 8


def test_cannot_sell_expired():
    p = setup_sample_pharmacy()
    # Анальгин просрочен
    assert p.check_availability('Анальгин', 1) is False
    assert p.get_exact_item('Анальгин', 1) is None


def test_order_checkout_reduces_stock_and_calculates_total():
    p = setup_sample_pharmacy()
    order = Order()
    order.add_item('Парацетамол', 3, 50.0)
    order.add_item('Ибупрофен', 2, 80.0)
    assert order.total == 3*50.0 + 2*80.0
    order.checkout(p)
    # после оформления
    para = p.get_exact_item('Парацетамол', 1)
    ibup = p.get_exact_item('Ибупрофен', 1)
    # Проверяем, что остатки уменьшились корректно
    # Напомним: первоначально парацетамол 10, ибупрофен 5
    assert para.quantity == 7
    assert ibup.quantity == 3

