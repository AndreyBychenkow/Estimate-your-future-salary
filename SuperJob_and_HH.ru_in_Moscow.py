import os

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable

SITY_ID_MOSCOW = 4
CATALOGUE_ID_PROGRAMMING = 48
PROGRAMMING_LANGUAGES = ["Python", "Java", "JavaScript", "C++", "C#", "PHP",
                         "Ruby", "Go", "Swift", "Kotlin"]


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    return None


def predict_rub_salary_hh(vacancy):
    salary = vacancy.get('salary')
    if not salary or salary.get('currency') != 'RUR':
        return None
    return predict_salary(salary.get('from'), salary.get('to'))


def predict_rub_salary_sj(vacancy):
    if vacancy.get('currency') != 'rub':
        return None
    return predict_salary(vacancy.get('payment_from'),
                          vacancy.get('payment_to'))


def get_hh_vacancies(language):
    url = "https://api.hh.ru/vacancies"
    params = {
        'text': language,
        'area': SITY_ID_MOSCOW,
        'per_page': 100
    }

    all_vacancies = []
    page = 0
    total_found = 0

    while True:
        params['page'] = page
        response = requests.get(url, params=params)
        if not response.ok:
            print(f"Ошибка: {response.status_code}")
            break

        hh_response = response.json()
        total_found = hh_response.get('found',
                                      0)
        vacancies = hh_response.get('items', [])

        if not vacancies:
            break

        all_vacancies.extend(vacancies)
        page += 1

    return all_vacancies, total_found


def get_superjob_vacancies(API_KEY_SUPERJOB, keyword):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": API_KEY_SUPERJOB
    }
    params = {
        'town': SITY_ID_MOSCOW,
        'catalogues': CATALOGUE_ID_PROGRAMMING,
        'keyword': keyword,
        'count': 100
    }

    all_vacancies = []
    page = 0
    total_found = 0

    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        if not response.ok:
            print(f"Ошибка: {response.status_code}")
            break

        superjob_response = response.json()
        total_found = superjob_response.get('total',
                                            0)
        vacancies = superjob_response.get('objects', [])

        if not vacancies:
            break

        all_vacancies.extend(vacancies)
        page += 1

    return all_vacancies, total_found


def calculate_average_salary_hh():
    language_stats = {}

    for language in PROGRAMMING_LANGUAGES:
        vacancies, total_found = get_hh_vacancies(language)
        vacancies_processed = 0
        total_salary = 0

        for vacancy in vacancies:
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                total_salary += salary
                vacancies_processed += 1

        average_salary = int(
            total_salary / vacancies_processed) if vacancies_processed else None

        language_stats[language] = {
            "vacancies_found": total_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }

    return language_stats


def calculate_average_salary_sj(api_key_superjob):
    language_stats = {}

    for language in PROGRAMMING_LANGUAGES:
        vacancies, total_found = get_superjob_vacancies(api_key_superjob,
                                                        language)
        vacancies_processed = 0
        total_salary = 0

        for vacancy in vacancies:
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                total_salary += salary
                vacancies_processed += 1

        average_salary = int(
            total_salary / vacancies_processed) if vacancies_processed else None

        language_stats[language] = {
            "vacancies_found": total_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }

    return language_stats


def print_salary_table(language_stats, title):
    table_data = [
        ["Язык программирования", "Найдено вакансий", "Обработано вакансий",
         "Средняя зарплата"]
    ]

    for language, stats in language_stats.items():
        table_data.append([
            language.lower(),
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary'] if stats[
                                           'average_salary'] is not None else "Не указана"
        ])

    table = AsciiTable(table_data)
    table.title = title
    print(table.table)


def main():
    load_dotenv()
    api_key_superjob = os.getenv('API_KEY_SUPERJOB')

    if not api_key_superjob:
        print("Не удалось загрузить API ключ. Проверьте файл .env")
        return

    print("Выполняем расчет по HeadHunter...")
    hh_stats = calculate_average_salary_hh()
    print_salary_table(hh_stats, "HeadHunter Moscow")

    print("\nВыполняем расчет по SuperJob...")
    sj_stats = calculate_average_salary_sj(api_key_superjob)
    print_salary_table(sj_stats, "SuperJob Moscow")


if __name__ == "__main__":
    main()
