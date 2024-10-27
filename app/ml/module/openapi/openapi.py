# rental_housing.py

import requests
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = 'http://rental.housing.ru'


def get_rentals(filter=False, filter_object=None):
    """
    Получает список доступных для аренды объектов.

    :param filter: Булево значение, указывающее применять ли фильтр.
    :param filter_object: Словарь с критериями фильтрации.
    :return: Список объявлений (список словарей) или None в случае ошибки.
    """
    url = f"{BASE_URL}/renta"
    params = {}
    headers = {'Content-Type': 'application/json'}

    if filter:
        params['filter'] = 'true'

    try:
        if filter and filter_object:
            response = requests.get(url, params=params, data=json.dumps(filter_object), headers=headers)
        else:
            response = requests.get(url, params=params, headers=headers)

        response.raise_for_status()
        rentals = response.json()
        logger.info(f"Получено {len(rentals)} объявлений для аренды.")
        return rentals

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при получении списка аренды: {e}")
        return None


def get_rental_details(uid):
    """
    Получает детали объявления по его UID.

    :param uid: Уникальный идентификатор объявления.
    :return: Детали объявления (словарь) или None в случае ошибки.
    """
    if not uid:
        logger.error("UID объявления обязателен.")
        return None

    url = f"{BASE_URL}/renta/{uid}"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        details = response.json()
        logger.info(f"Детали объявления UID {uid} успешно получены.")
        return details

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при получении деталей аренды для UID {uid}: {e}")
        return None


def format_rental_list(rentals):
    """
    Форматирует список объявлений для удобного отображения.

    :param rentals: Список объявлений.
    :return: Отформатированная строка.
    """
    if not rentals:
        return "Нет доступных объявлений для аренды."

    formatted_list = ""
    for rental in rentals:
        formatted_list += (
            f"ID: {rental.get('uid')}\n"
            f"Заголовок: {rental.get('title')}\n"
            f"Описание: {rental.get('description')}\n"
            f"Адрес: {rental.get('address')}\n"
            f"Количество комнат: {rental.get('countOfRooms')}\n"
            f"Площадь: {rental.get('area')} м²\n"
            f"Этаж: {rental.get('apartmentFloor')}\n"
            f"Контакты: Телефон - {rental.get('contacts', {}).get('phoneNumber', 'Не указан')}, "
            f"Email - {rental.get('contacts', {}).get('email', 'Не указан')}\n"
            "----------------------------------------\n"
        )
    return formatted_list


def format_rental_details(details):
    """
    Форматирует детали объявления для удобного отображения.

    :param details: Детали объявления.
    :return: Отформатированная строка.
    """
    if not details:
        return "Детали объявления не найдены."

    contacts = details.get('contacts', {})
    formatted_details = (
        f"ID: {details.get('uid')}\n"
        f"Заголовок: {details.get('title')}\n"
        f"Описание: {details.get('description')}\n"
        f"Адрес: {details.get('address')}\n"
        f"Количество комнат: {details.get('countOfRooms')}\n"
        f"Общая площадь: {details.get('area')} м²\n"
        f"Площадь кухни: {details.get('kitchenArea')} м²\n"
        f"Количество этажей: {details.get('countOfFloors')}\n"
        f"Этаж квартиры: {details.get('apartmentFloor')}\n"
        f"Площадь ванной: {details.get('areaBathroom')} м²\n"
        f"Тип ванной: {details.get('typeBathroom')}\n"
        f"Тип ремонта: {details.get('typeRepair')}\n"
        f"Мебель: {', '.join(details.get('furniture', []))}\n"
        f"Техника: {', '.join(details.get('equipment', []))}\n"
        f"Условия аренды: {format_terms(details.get('rentalTerms', []))}\n"
        f"Правила аренды: {format_rules(details.get('rules', []))}\n"
        f"Контакты: Телефон - {contacts.get('phoneNumber', 'Не указан')}, "
        f"Email - {contacts.get('email', 'Не указан')}\n"
    )
    return formatted_details


def format_terms(rental_terms):
    """
    Форматирует условия аренды.

    :param rental_terms: Список условий аренды.
    :return: Строка с условиями.
    """
    if not rental_terms:
        return "Не указаны условия аренды."

    terms = []
    for term in rental_terms:
        term_type = term.get('typeOfTerms', 'Не указано')
        term_value = term.get('valueOfTerms', 'Не указано')
        terms.append(f"{term_type}: {term_value}")
    return "; ".join(terms)


def format_rules(rules):
    """
    Форматирует правила аренды.

    :param rules: Список правил аренды.
    :return: Строка с правилами.
    """
    if not rules:
        return "Не указаны правила аренды."

    formatted_rules = []
    for rule in rules:
        rule_type = rule.get('typeOfRule', 'Не указано')
        rule_value = rule.get('valueOfRules', 'Не указано')
        formatted_rules.append(f"{rule_type}: {rule_value}")
    return "; ".join(formatted_rules)


# Пример использования модуля
if __name__ == "__main__":
    # Получение списка аренды без фильтра
    rentals = get_rentals()
    print("Список доступных квартир для аренды:\n")
    print(format_rental_list(rentals))

    # Пример фильтрации
    filter_obj = {
        "minSum": 10000,
        "maxSum": 50000,
        "keyWords": ["центр", "новостройка"],
        "typeCountOfRooms": [{"typeOfRoom": "двухкомнатная"}],
        "minArea": 50,
        "maxArea": 100,
        "minFloor": 1,
        "maxFloor": 10
    }
    filtered_rentals = get_rentals(filter=True, filter_object=filter_obj)
    print("\nСписок квартир для аренды с фильтрацией:\n")
    print(format_rental_list(filtered_rentals))

    # Получение деталей конкретного объявления
    example_uid = '4527b1ba-2b7c-454a-a591-e83a239d4faf'
    details = get_rental_details(example_uid)
    print(f"\nДетали объявления UID {example_uid}:\n")
    print(format_rental_details(details))
