
"""Простой пример использования модулей: создание аптеки, добавление лекарств и оформление заказа."""
from datetime import date, timedelta
from medicine import Medicine
from pharmacy import Pharmacy
from order import Order


def main():
    # создаём аптеку
    apteka = Pharmacy("Здоровье", "ул. Ленина, 1")

    # создаём несколько лекарств 
    today = date.today()
    med1 = Medicine("Парацетамол", "ФармКорп", 50.0, today + timedelta(days=365), 20)
    med2 = Medicine("Анальгин", "МедиКо", 30.0, today - timedelta(days=10), 10)  # просрочен
    med3 = Medicine("Ибупрофен", "HealLab", 80.0, today + timedelta(days=180), 5)

    # добавляем в аптеку
    apteka.add_medicine(med1)
    apteka.add_medicine(med2)
    apteka.add_medicine(med3)

    print(apteka)

    # ищем
    print('Поиск "парацет" ->', apteka.find_by_name('парацет'))

    print(f"Просрочен ли {med1.name}", med1.is_expired())
    print(f"Просрочен ли {med2.name}", med2.is_expired())
    print(f"Просрочен ли {med3.name}", med3.is_expired())

    # создаём заказ
    order = Order()
    order.add_item('Парацетамол', 2, med1.price)
    order.add_item('Ибупрофен', 1, med3.price)

    print('Сумма заказа:', order.total)

    # оформляем и проверяем, что количество уменьшилось
    try:
        order.checkout(apteka)
        print('Заказ оформлен успешно')
    except ValueError as e:
        print('Ошибка при оформлении заказа:', e)

    print('Остатки после покупки:')
    for m in apteka.inventory:
        print(m)


if __name__ == '__main__':
    main()
