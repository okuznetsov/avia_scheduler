import datetime
from dataclasses import dataclass

from dateutil.parser import parse
from dateutil.tz import UTC


@dataclass
class Route:
    from_: str
    to: str


@dataclass
class Timetable:
    local: int
    utc: int
    utc_offset: int
    local_day: int
    local_datetime: datetime.datetime

    @classmethod
    def parse(cls, time_str: str):
        parsed_local = parse(time_str)
        parsed_utc = parsed_local.astimezone(UTC)

        return cls(
            local=(parsed_local.hour * 60 + parsed_local.minute),
            utc=(parsed_utc.hour * 60 + parsed_utc.minute),
            utc_offset=int(parsed_local.utcoffset().seconds / 60),
            local_day=parsed_local.isoweekday(),
            local_datetime=parsed_local,
        )


@dataclass
class Flight:
    iata_from: str
    iata_to: str
    line: str

    # region Время
    valid_from: datetime.datetime
    valid_to: datetime.datetime
    departure_loc: int
    arrival_loc: int
    departure: int  # utc
    arrival: int
    departure_gdelta: int  # timezone
    arrival_gdelta: int
    duration: int
    # endregion

    aircraft_type: str

    # region Регулярность
    day_1: int = 0
    day_2: int = 0
    day_3: int = 0
    day_4: int = 0
    day_5: int = 0
    day_6: int = 0
    day_7: int = 0
    # endregion

    source: str = "YANDEX"

    # iata_from, iata_to, line, departure, arrival, source
    def as_tuple(self):
        return (
            self.iata_from,
            self.iata_to,
            self.line,
            self.day_1,
            self.day_2,
            self.day_3,
            self.day_4,
            self.day_5,
            self.day_6,
            self.day_7,
            self.departure,
            self.arrival,
            self.departure_loc,
            self.arrival_loc,
            self.departure_gdelta,
            self.arrival_gdelta,
            self.duration,
            self.aircraft_type,
            self.valid_from,
            self.valid_to,
            self.source,
        )

    @classmethod
    def from_route_and_segment(cls, route, segment):
        arrival = Timetable.parse(segment["arrival"])
        departure = Timetable.parse(segment["departure"])

        year = datetime.datetime.now().year
        valid_from = datetime.datetime(year, 1, 1)
        valid_to = datetime.datetime(year + 1, 1, 1)

        return Flight(
            iata_from=route.from_,
            iata_to=route.to,
            line=segment.get("thread", {}).get("number"),
            day_1=1 if departure.local_day == 1 else 0,
            day_2=1 if departure.local_day == 2 else 0,
            day_3=1 if departure.local_day == 3 else 0,
            day_4=1 if departure.local_day == 4 else 0,
            day_5=1 if departure.local_day == 5 else 0,
            day_6=1 if departure.local_day == 6 else 0,
            day_7=1 if departure.local_day == 7 else 0,
            departure_loc=departure.local,
            arrival_loc=arrival.local,
            departure=departure.utc,
            arrival=arrival.utc,
            departure_gdelta=departure.utc_offset,
            arrival_gdelta=arrival.utc_offset,
            duration=int(segment.get("duration", 0) / 60),
            aircraft_type=segment.get("thread", {}).get("vehicle"),
            valid_from=valid_from,
            valid_to=valid_to,
        )
