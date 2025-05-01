from datetime import datetime

en_alphabet: str = 'abcdefghijklmnopqrstuvwxyz'
ru_alphabet: str = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


def is_valid_name(name: str) -> bool:
    for char in name:
        if char.lower() not in en_alphabet:
            return False

    return True


def is_valid_date(date: str) -> bool:
    """
    Проверяет, является ли строка корректной датой в формате дд.мм.гггг.

    :param date: Строка с датой в формате дд.мм.гггг.
    :return: True, если дата корректна, иначе False.
    """
    try:
        datetime.strptime(date, "%d.%m.%Y")
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    # Примеры использования
    print(is_valid_date("29.02.2020"))  # True, високосный год
    print(is_valid_date("29.02.2019"))  # False, не високосный год
    print(is_valid_date("31.04.2021"))  # False, апрель имеет только 30 дней
    print(is_valid_date("15.08.2023"))  # True
    print(is_valid_date("31.11.2023"))  # False, ноября имеет только 30 дней

