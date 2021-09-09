import datetime
from typing import List

from yandex_rasp import YandexRasp
from yandex_rasp.api.exceptions import YandexException

from app.domain.models import Route, Flight
from app.domain.services import AbstractFlightService


class YandexFlightService(AbstractFlightService):
    def __init__(self, api_client: YandexRasp):
        self.api_client = api_client

    def find(self, route: Route, date: datetime.datetime) -> List[Flight]:
        try:
            search_result = self.api_client.search(
                from_=route.from_,
                to=route.to,
                date=date.strftime("%Y-%m-%d"),
                transport_types="plane",
                coding_system="iata",
                result_timezone="",
                lang="ru_RU"
            )
        except YandexException:
            return []
        else:
            return [
                Flight.from_route_and_segment(route, segment)
                for segment in search_result.get("segments", [])
            ]
