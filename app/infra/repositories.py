import csv
from typing import List

from app.domain.models import Route, Flight
from app.domain.repositories import AbstractRoutesRepository, AbstractFlightRepository


class CSVRouteRepository(AbstractRoutesRepository):
    def __init__(self, path: str):
        self.path = path

        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            self._routes = [Route(row[0], row[1]) for row in reader]

    def find_available(self) -> List[Route]:
        return self._routes


class MysqlFlightRepository(AbstractFlightRepository):
    def __init__(self, conn):
        self.conn = conn

    def save_many(self, flights: List[Flight]) -> None:
        cursor = self.conn.cursor(dictionary=True)
        query = """
            INSERT INTO flights (
                iata_from, 
                iata_to, 
                line, 
                day_1,
                day_2,
                day_3,
                day_4,
                day_5,
                day_6,
                day_7,
                departure,
                arrival,
                departure_loc, 
                arrival_loc, 
                departure_gdelta,
                arrival_gdelta,
                duration,
                aircraft_type,
                valid_from,
                valid_to,
                source
            )
            VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
        """

        inserted = []

        for flight in flights:
            cursor.execute("""
                SELECT * FROM flights 
                WHERE 
                    iata_from = %s AND iata_to = %s 
                    AND line = %s AND departure = %s 
                    AND arrival = %s AND source = %s
            """, [
                flight.iata_from,
                flight.iata_to,
                flight.line,
                flight.departure,
                flight.arrival,
                flight.source,
            ])
            e = cursor.fetchone()
            if e:
                cursor.execute("""
                    UPDATE flights 
                        SET day_1 = %s, day_2 = %s, day_3 = %s, day_4 = %s, day_5 = %s, day_6 = %s, day_7 = %s 
                    WHERE id = %s
                """, [
                    max(flight.day_1, e["day_1"]),
                    max(flight.day_2, e["day_2"]),
                    max(flight.day_3, e["day_3"]),
                    max(flight.day_4, e["day_4"]),
                    max(flight.day_5, e["day_5"]),
                    max(flight.day_6, e["day_6"]),
                    max(flight.day_7, e["day_7"]),
                    e["id"],
                ])
            else:
                inserted.append(flight)

        if inserted:
            cursor.executemany(query, [flight.as_tuple() for flight in inserted])

        cursor.close()
