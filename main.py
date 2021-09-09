import os
from datetime import date, timedelta

import mysql.connector
from yandex_rasp import YandexRasp

from app.domain.use_cases import ImportFlightsUseCase
from app.infra.repositories import CSVRouteRepository, MysqlFlightRepository
from app.infra.services import YandexFlightService


def main():
    connection = mysql.connector.connect(
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        host=os.environ.get("MYSQL_HOST"),
        database=os.environ.get("MYSQL_DATABASE"),
        port=os.environ.get("MYSQL_PORT"),
    )
    connection.autocommit = True
    yandex_api_client = YandexRasp(
        api_key=os.environ.get("YANDEX_API_KEY"),
        domain="",
    )
    import_flights = ImportFlightsUseCase(
        routes_repo=CSVRouteRepository(os.environ.get("CSV_ROUTE_FILE")),
        flight_service=YandexFlightService(yandex_api_client),
        flights_repo=MysqlFlightRepository(connection),
    )
    import_flights(
        date.today(),
        date.today() + timedelta(days=int(os.environ.get("IMPORT_DAYS")))
    )
    connection.close()


if __name__ == '__main__':
    main()
