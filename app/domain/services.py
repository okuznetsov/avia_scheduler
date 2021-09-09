import datetime
from abc import abstractmethod
from typing import List

from .models import Flight, Route


class AbstractFlightService:
    @abstractmethod
    def find(self, route: Route, date: datetime.date) -> List[Flight]:
        ...
