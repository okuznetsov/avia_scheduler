from abc import abstractmethod
from typing import List

from .models import Route, Flight


class AbstractRoutesRepository:
    @abstractmethod
    def find_available(self) -> List[Route]:
        ...


class AbstractFlightRepository:
    @abstractmethod
    def save_many(self, flights: List[Flight]):
        ...
