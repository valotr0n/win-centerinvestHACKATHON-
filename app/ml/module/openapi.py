import requests


def hh(profession, page=0, area=1, per_page=3):

    # URL и параметры запроса к API hh.ru
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': profession,
        'area': area,
        'page': page,
        'per_page': per_page
    }

    # Отправка запроса к API
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}")
        return []

    data = response.json()
    vacancies = []

    z = ""
    for item in data.get('items', []):
        vacancy = {
            'name': item['name'],
            'employer': item['employer']['name'] if item.get('employer') else "Не указано",
            'salary': item['salary'],
            'area': item['area']['name'],
            'url': item['alternate_url']
        }
        vacancies.append(vacancy)
    for v in vacancies:
        z += f"Вакансия: {v['name']}, Работодатель: {v['employer']}, ЗП: {v['salary']}, Город: {v['area']}, URL: {v['url']}"
    return z