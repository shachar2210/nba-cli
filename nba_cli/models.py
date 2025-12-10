from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Team:
    id: int
    conference: str
    division: str
    city: str
    name: str
    full_name: str
    abbreviation: str


@dataclass
class Game:
    id: int
    date: date
    datetime: datetime | None
    season: int
    status: str
    period: int
    time: str
    postseason: bool
    home_team_score: int
    visitor_team_score: int
    home_team: Team
    visitor_team: Team


@dataclass
class Player:
    id: int
    first_name: str
    last_name: str
    position: str
    height: str
    weight: str
    jersey_number: str
    college: str
    country: str
    draft_year: int | None
    draft_round: int | None
    draft_number: int | None
    team: Team | None
