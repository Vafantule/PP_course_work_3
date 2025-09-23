from typing import Optional


class Company:
    """
    Модель компании.
    """
    def __init__(self, company_id: int, name: str, url: str):
        self.company_id = company_id
        self.name = name
        self.url = url


class Vacancy:
    """
    Модель вакансии.
    """
    def __init__(self,
                 vacancy_id: int,
                 name: str,
                 salary_from: Optional[int],
                 salary_to: Optional[int],
                 url: str,
                 company_id: int):
        self.vacancy_id = vacancy_id
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.url = url
        self.company_id = company_id
