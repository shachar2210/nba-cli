from __future__ import annotations

from datetime import date, datetime
from functools import lru_cache
from typing import Any, Dict, Iterable, List

import requests

from .config import API_BASE_URL_V1, get_api_key
from .models import Game, Team, Player


def _get_headers() -> Dict[str, str]:
    return {
        "Authorization": get_api_key(),
        "Accept": "application/json",
    }


def _request_paginated(path: str, params: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    cursor = None

    while True:
        request_params = dict(params)
        if cursor is not None:
            request_params["cursor"] = cursor

        url = f"{API_BASE_URL_V1}{path}"
        resp = requests.get(url, headers=_get_headers(), params=request_params, timeout=10)
        resp.raise_for_status()
        payload = resp.json()

        data = payload.get("data") or []
        for item in data:
            yield item

        meta = payload.get("meta") or {}
        cursor = meta.get("next_cursor")
        if not cursor:
            break


def _parse_team(raw: Dict[str, Any]) -> Team:
    return Team(
        id=int(raw["id"]),
        conference=str(raw.get("conference", "")),
        division=str(raw.get("division", "")),
        city=str(raw.get("city", "")),
        name=str(raw.get("name", "")),
        full_name=str(raw.get("full_name", "")),
        abbreviation=str(raw.get("abbreviation", "")),
    )


def _parse_game(raw: Dict[str, Any]) -> Game:
    date_str = str(raw.get("date"))
    try:
        game_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        game_date = date.today()

    dt_str = raw.get("datetime")
    game_dt: datetime | None = None
    if isinstance(dt_str, str):
        try:
            game_dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except ValueError:
            game_dt = None

    home_team = _parse_team(raw.get("home_team", {}))
    visitor_team = _parse_team(raw.get("visitor_team", {}))

    return Game(
        id=int(raw["id"]),
        date=game_date,
        datetime=game_dt,
        home_team=home_team,
        visitor_team=visitor_team,
        home_team_score=raw.get("home_team_score"),
        visitor_team_score=raw.get("visitor_team_score"),
        status=str(raw.get("status", "")),
        season=raw.get("season", 0),
        period=raw.get("period", 0),
        time=str(raw.get("time", "")),
        postseason=raw.get("postseason", False),
    )


def _parse_player(raw: Dict[str, Any]) -> Player:
    team_raw = raw.get("team")
    team = _parse_team(team_raw) if team_raw else None

    return Player(
        id=int(raw["id"]),
        first_name=str(raw.get("first_name", "")),
        last_name=str(raw.get("last_name", "")),
        position=str(raw.get("position", "")),
        height=str(raw.get("height", "")),
        weight=str(raw.get("weight", "")),
        jersey_number=str(raw.get("jersey_number", "")),
        college=str(raw.get("college", "")),
        country=str(raw.get("country", "")),
        draft_year=raw.get("draft_year"),
        draft_round=raw.get("draft_round"),
        draft_number=raw.get("draft_number"),
        team=team,
    )


def search_players(search: str, active_only: bool = False, per_page: int = 25) -> List[Player]:
    path = "/players/active" if active_only else "/players"
    params: Dict[str, Any] = {
        "search": search,
        "per_page": per_page,
    }
    return [_parse_player(raw) for raw in _request_paginated(path, params)]


def get_games_for_date(day: date) -> List[Game]:
    params: Dict[str, Any] = {
        "dates[]": day.isoformat(),
        "per_page": 100,
    }
    return [_parse_game(raw) for raw in _request_paginated("/games", params)]


# Optimization: Cache the teams result so we don't hit the API repeatedly for static data
@lru_cache(maxsize=1)
def get_teams(conference: str | None = None, division: str | None = None) -> List[Team]:
    params: Dict[str, Any] = {}
    if conference:
        params["conference"] = conference
    if division:
        params["division"] = division

    return [_parse_team(raw) for raw in _request_paginated("/teams", params)]