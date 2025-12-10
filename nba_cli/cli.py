from __future__ import annotations

import argparse
from datetime import date, datetime
from typing import Optional

from rich.console import Console
from rich.table import Table

from . import __version__
from .api import get_games_for_date, get_teams, search_players

console = Console()


def _parse_date(value: Optional[str]) -> date:
    if not value:
        return date.today()
    return datetime.strptime(value, "%Y-%m-%d").date()


def _matches_team_filter(game, team_filter: Optional[str]) -> bool:
    if game is None:
        return False
    if not team_filter:
        return True

    key = team_filter.strip().lower()
    teams = (game.home_team, game.visitor_team)
    for t in teams:
        if key == t.abbreviation.lower():
            return True
        if key in t.full_name.lower():
            return True
        if key in t.city.lower() or key in t.name.lower():
            return True
    return False


def _format_status(raw: str) -> str:
    if "T" in raw and raw.endswith("Z"):
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return dt.strftime("%H:%M")
        except ValueError:
            return raw
    return raw


def cmd_games(args: argparse.Namespace) -> None:
    day = _parse_date(args.date)
    games = get_games_for_date(day)

    games = [g for g in games if g is not None]

    if args.team:
        games = [g for g in games if _matches_team_filter(g, args.team)]

    if not games:
        msg = f"No games found for {day.isoformat()}"
        if args.team:
            msg += f" and team filter '{args.team}'"
        console.print(f"[bold]{msg}[/bold]")
        return

    table = Table(title=f"NBA games for {day.isoformat()}")
    table.add_column("Date")
    table.add_column("Away")
    table.add_column("Home")
    table.add_column("Score")
    table.add_column("Status")

    for g in games:
        tipoff_str = g.date.strftime("%Y-%m-%d")

        score = "-"
        # Accessing scores should be safe now that _parse_game is complete
        home_score = g.home_team_score if g.home_team_score is not None else 0
        visitor_score = g.visitor_team_score if g.visitor_team_score is not None else 0

        if home_score or visitor_score:
            score = f"{visitor_score} - {home_score}"

        table.add_row(
            tipoff_str,
            g.visitor_team.abbreviation or g.visitor_team.full_name,
            g.home_team.abbreviation or g.home_team.full_name,
            score,
            _format_status(g.status),
        )

    console.print(table)


def cmd_teams(args: argparse.Namespace) -> None:
    conference = args.conference
    division = args.division

    teams = get_teams(conference=conference, division=division)
    if not teams:
        console.print("[bold]No teams found[/bold]")
        return

    if not conference and not division:
        teams = [
            t for t in teams
            if t.conference and t.division and t.city and t.full_name != "Team Name"
        ]

    title_parts = ["NBA teams"]
    if conference:
        title_parts.append(f"conference={conference}")
    if division:
        title_parts.append(f"division={division}")
    title = " - ".join(title_parts)

    table = Table(title=title)
    table.add_column("Abbr")
    table.add_column("Name")
    table.add_column("City")
    table.add_column("Conf")
    table.add_column("Div")

    for t in teams:
        table.add_row(
            t.abbreviation,
            t.full_name or "-",
            t.city or "-",
            t.conference or "-",
            t.division or "-",
        )

    console.print(table)


def cmd_players(args: argparse.Namespace) -> None:
    search_term = args.search
    limit = args.limit

    try:
        players = search_players(search_term, per_page=limit)
    except Exception as e:
        console.print(f"[red]Failed to fetch players: {e}[/red]")
        return

    if not players:
        console.print(f"[bold]No players found for search '{search_term}'[/bold]")
        return

    title = f"Players search: '{search_term}'"

    table = Table(title=title)
    table.add_column("Name")
    table.add_column("Pos")
    table.add_column("Team")
    table.add_column("Country")
    table.add_column("Height")
    table.add_column("Weight")
    table.add_column("Jersey")
    table.add_column("Draft")

    for p in players:
        name = f"{p.first_name} {p.last_name}".strip()
        team_name = p.team.abbreviation if p.team else ""
        draft = ""
        if p.draft_year:
            draft = f"{p.draft_year}"
            if p.draft_round is not None and p.draft_number is not None:
                draft += f" (R{p.draft_round} #{p.draft_number})"

        table.add_row(
            name,
            p.position or "",
            team_name,
            p.country or "",
            p.height or "",
            p.weight or "",
            p.jersey_number or "",
            draft,
        )

    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="nba-cli",
        description="Command-line NBA games browser using the BALLDONTLIE API.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"nba-cli {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    games_parser = subparsers.add_parser(
        "games",
        help="Show games for a date (default: today).",
    )
    games_parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY-MM-DD format (optional).",
    )
    games_parser.add_argument(
        "--team",
        help="Filter games by team code or name.",
    )
    games_parser.set_defaults(func=cmd_games)

    teams_parser = subparsers.add_parser(
        "teams",
        help="List NBA teams.",
    )
    teams_parser.add_argument(
        "--conference",
        help="Filter by conference (East/West).",
    )
    teams_parser.add_argument(
        "--division",
        help="Filter by division (e.g. Pacific).",
    )
    teams_parser.set_defaults(func=cmd_teams)

    players_parser = subparsers.add_parser(
        "players",
        help="Search NBA players.",
    )
    players_parser.add_argument(
        "--search",
        "-s",
        required=True,
        help="Search term for first or last name.",
    )

    players_parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Max number of players to fetch (per_page).",
    )
    players_parser.set_defaults(func=cmd_players)

    args = parser.parse_args()
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return
    func(args)


if __name__ == "__main__":
    main()