import datetime
from datetime import timedelta

from .repositories import AbstractRoutesRepository, AbstractFlightRepository
from .services import AbstractFlightService


class ImportFlightsUseCase:
    def __init__(
            self,
            routes_repo: AbstractRoutesRepository,
            flight_service: AbstractFlightService,
            flights_repo: AbstractFlightRepository,
    ):
        self.flights_repo = flights_repo
        self.flight_service = flight_service
        self.routes_repo = routes_repo

    def __call__(self, date_from: datetime.date, date_to: datetime.date):
        routes = self.routes_repo.find_available()

        for route in routes:
            current_date = date_from
            while current_date <= date_to:
                flights = self.flight_service.find(route, current_date)
                self.flights_repo.save_many(flights)
                current_date += timedelta(days=1)
