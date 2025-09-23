import psycopg2
from db_config import DATABASE_CONFIG
from typing import List, Tuple


class DataBaseManager:
    """
    Класс управления данными в базе данных PostgreSQL.
    """
    def __init__(self):
        """
        Инициализация соединения с БД.
        """
        self.conn = psycopg2.connect(**DATABASE_CONFIG)
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получение списка вакансий компаний и количество вакансий у компаний.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT companies.name, COUNT(vacancies.vacancy_id)
            FROM companies
            LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
            GROUP BY companies.name
            ORDER BY companies.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, int]]:
        """
        Получение списка вакансий с указанными параметрами.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT companies.name, vacancies.name, COALESCE(vacancies.salary_from, 0), COALESCE(vacancies.salary_to, 0),vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.company_id
            ORDER BY companies.name, vacancies.name
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Получение средней зарплаты по вакансиям.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                   SELECT AVG(COALESCE(salary_from, 0))
                   FROM vacancies
                   """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, int]]:
        """
        Получение списка вакансий, с зарплатой выше средней.
        """
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT companies.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.company_id
            WHERE vacancies.salary_from > %s
            ORDER BY vacancies.salary_from DESC
            """, (avg_salary, ))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, int]]:
        """
        Получение списка вакансий, с заданными словами для отбора.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT companies.name, vacancies.name, COALESCE(salary_from, 0), COALESCE(salary_to, 0), vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.company_id
            WHERE vacancies.name LIKE %s
            ORDER BY companies.name, vacancies.name
            """, (f"{keyword}", ))
            return cur.fetchall()

    def cose(self) -> None:
        """
        Закрывает соединение с БД.
        """
        if self.conn:
            self.conn.close()
