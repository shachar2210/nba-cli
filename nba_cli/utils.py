from __future__ import annotations

from datetime import date, datetime


def format_tipoff(game_date: date, game_dt: datetime | None) -> str:
    """
    For now, show only the date (YYYY-MM-DD), ignore time zone stuff.
    """
    return game_date.strftime("%Y-%m-%d")
