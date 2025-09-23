import requests

from src.api import HHAPI
from src.vacancy import Company, Vacancy
from src.database import create_database, create_tables, insert_companies, insert_vacancies
from src.db_manager import DataBaseManager


def main() -> None:
    """
    Основная функция проекта.
    """
    print("Создание базы данных и таблиц...")
    try:
        create_database()
    except Exception as error:
        print(f"База данных уже существует. {error}")
    create_tables()

    hh = HHAPI()
    employer_ids = [1740, 3529, 3776, 4185, 1327, 78638, 907345, 955103, 1122462, 1057]
    companies = []
    vacancies = []
    print("Получение данных о компаниях и вакансиях...")

    for employer_id in employer_ids:
        try:
            employer = hh.get_employer(employer_id)
        except requests.HTTPError as error:
            # print(f"Ошибка при получении работодателя {employer_id}: {error}")
            continue

        companies.append(Company(employer["id"], employer["name"], employer["alternate_url"]))
        employer_vacancies = hh.get_vacancies(employer_id)
        for vacancy in employer_vacancies:
            salary = vacancy.get("salary")
            vacancies.append(Vacancy(
                vacancy_id=int(vacancy['id']),
                name=vacancy['name'],
                salary_from=salary['from'] if salary and salary.get('from') else None,
                salary_to=salary['to'] if salary and salary.get('to') else None,
                url=vacancy['alternate_url'],
                company_id=int(vacancy['employer']['id'])
            ))

    insert_companies(companies)
    insert_vacancies(vacancies)

    database_manager = DataBaseManager()
    while True:
        print("\nВыберите действие:")
        print("1 - Показать компании и количество вакансий")
        print("2 - Показать все вакансии")
        print("3 - Показать среднюю зарплату")
        print("4 - Вакансии с зарплатой выше средней")
        print("5 - Найти вакансии по ключевому слову")
        print("0 - Выход")
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            for company, count in database_manager.get_companies_and_vacancies_count():
                print(f"{company}: {count} вакансий.")
        elif choice == "2":
            for company, vacancy, salary_from, salary_to, url in database_manager.get_all_vacancies():
                if salary_from and salary_to:
                    salary_str = f"{salary_from} - {salary_to}"
                elif salary_from:
                    salary_str = f"{salary_from}"
                else:
                    salary_str = "Не указана"
                print(f"{company} | {vacancy} | Зарплата: {salary_str} | Ссылка: {url}")
        elif choice == "3":
            avg_salary = database_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary:.2f}")
        elif choice == "4":
            for company, vacancy, salary_from, salary_to, url in (
                    database_manager.get_vacancies_with_higher_salary()):
                if salary_from and salary_to:
                    salary_str = f"{salary_from} - {salary_to}"
                elif salary_from:
                    salary_str = f"{salary_from}"
                else:
                    salary_str = "Не указана"
                print(f"{company} | {vacancy} | Зарплата: {salary_str} | Ссылка: {url}")
        elif choice == "5":
            keyword = input("Введите ключевое слово для отбора: ")
            for company, vacancy, salary_from, salary_to, url in (
                    database_manager.get_vacancies_with_keyword(keyword)):
                if salary_from and salary_to:
                    salary_str = f"{salary_from} - {salary_to}"
                elif salary_from:
                    salary_str = f"{salary_from}"
                else:
                    salary_str = "Не указана"
                print(f"{company} | {vacancy} | Зарплата: {salary_str} | Ссылка: {url}")
        elif choice == "0":
            database_manager.close()
            print("Работа завершена.")
            break
        else:
            print("Выбор некорректный.")


if __name__ == "__main__":
    main()
