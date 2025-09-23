import requests
from typing import List, Dict


class HHAPI:
    """
    Класс, взаимодействия с публичным API hh.ru.
    """
    BASE_URL = "https://api.hh.ru"

    def get_employer(self, employer_id: int) -> Dict:
        """
        Получает информацию о работодателе по ID.
        """
        response = requests.get(f"{self.BASE_URL}/работодатели/{employer_id}")
        response.raise_for_status()
        return response.json()

    def get_vacancies(self, employer_id: int) -> List[Dict]:
        """
        Получает список вакансий работодателя.
        """
        params = {"employer_id": employer_id, "per_page": 100}
        response = requests.get(f"{self.BASE_URL}/вакансии", params=params)
        response.raise_for_status()
        return response.json().get("items", [])
