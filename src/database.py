import psycopg2
from typing import List
from db_config import DATABASE_CONFIG
from vacancy import Company, Vacancy


def create_database() -> None:
    """
    Создание базы данных hh_vacancies
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        host=DATABASE_CONFIG["host"],
        port=DATABASE_CONFIG["port"]
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("CREATE DATABASE hh_vacancies")
    cur.close()
    conn.close()


def create_tables() -> None:
    """
    Создание таблиц vacancies & companies.
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        url TEXT NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        salary_from INTEGER,
        salary_to INTEGER,
        url, TEXT NOT NULL,
        company_id INTEGER REFERENCES companies(company_id)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_companies(companies: List[Company]) -> None:
    """
    Заполнение таблицы companies.
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    for company in companies:
        cur.execute(
            "INSERT INTO companies (company_id, name, url) VALUES (%s, %s, %s) ON CONFLICT (company_id) DO NOTHING",
            (company.company_id, company.name, company.url)
        )
    conn.commit()
    cur.close()
    conn.close()


def insert_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Заполнение таблицы companies.
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    for vacancy in vacancies:
        cur.execute(
            "INSERT INTO vacancies (vacancy_id, name, salary_from, salary_to, url, company_id) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING",
            (vacancy.vacancy_id, vacancy.name, vacancy.salary_from, vacancy.salary_to, vacancy.url, vacancy.company_id)
        )
    conn.commit()
    cur.close()
    conn.close()
