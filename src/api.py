from typing import Any

import requests


class HHAPI:
    """
    Класс, взаимодействия с публичным API hh.ru.
    """
    BASE_URL = "https://api.hh.ru"

    def get_employer(self, employer_id: int) -> dict[str, Any]:
        """
        Получает информацию о работодателе по ID.
        """
        response = requests.get(f"{self.BASE_URL}/employers/{employer_id}")
        response.raise_for_status()
        data: Any = response.json()
        if isinstance(data, dict):
            return data
        raise TypeError("Ответ API работодателя не является словарём")

    def get_vacancies(self, employer_id: int) -> list[dict[str, Any]]:
        """
        Получает список вакансий работодателя.
        """
        params = {"employer_id": employer_id, "per_page": 100}
        response = requests.get(f"{self.BASE_URL}/vacancies", params=params)
        response.raise_for_status()
        items: Any = response.json().get("items", [])
        if isinstance(items, list) and all(isinstance(item, dict) for item in items):
            return items
        raise TypeError("Ответ API вакансий не является списком словарей")
