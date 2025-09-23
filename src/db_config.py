from typing import TypedDict


class DatabaseConfig(TypedDict):
    host: str
    port: int
    user: str
    password: str
    dbname: str


DATABASE_CONFIG: DatabaseConfig = {
    "host": "localhost",
    "port": 5432,
    "user": "user_hw",
    "password": "12345",
    "dbname": "hh_vacancies"
}
