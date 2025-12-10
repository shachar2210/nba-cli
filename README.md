# 🎯 NBA CLI – Command-Line NBA Browser

A clean, modern, professional Python CLI for browsing **NBA games, teams, and players** — powered by the BallDontLie API.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Features

- **📅 Games Browser**  
  View scheduled games, final scores, and game status for any date.

- **🏀 Team Filtering**  
  Show only games for a specific team (e.g., `LAL`, `DEN`, `BOS`).

- **👤 Player Search**  
  Find players by name and view position, team, physical stats, and draft data.

- **⚡ Fast & Optimized**  
  Static team data is cached automatically to reduce API load.

- **🧽 Clean Results**  
  Auto-filters out legacy / non-NBA teams returned by the API.

- **🐳 Fully Dockerized**  
  Run anywhere, no Python installation required.

> **Note on Time Zones:**  
> Game times are shown in **US Eastern Time (ET)** as provided by the API.

---

# 📦 Installation & Usage

## Option 1 — Docker (Recommended)

Run instantly with zero setup.

### 1️⃣ Build the image

You must run this command from the **project root directory** (`nba-cli/`).

```bash
docker build -t nba-cli .
```

### 2️⃣ Run commands

All API calls require your API key. Obtain a free key from [BallDontLie.io](https://balldontlie.io).

| Command | Description | Example                                                                             |
|--------|-------------|-------------------------------------------------------------------------------------|
| Games (Today) | Show today's games | `docker run --rm -t -e BALLDONTLIE_API_KEY="KEY" nba-cli games`                     |
| Games (Date) | Show games for a specific date | `docker run --rm -t -e BALLDONTLIE_API_KEY="KEY" nba-cli games 2023-12-25`          |
| Games (Team Filter) | Filter by team | `docker run --rm -t -e BALLDONTLIE_API_KEY="KEY" nba-cli games --team LAL`          |
| Teams | List teams | `docker run --rm -t -e BALLDONTLIE_API_KEY="KEY" nba-cli teams`                     |
| Teams Filter | Filter by conference or division | `docker run --rm -t -e BALLDONTLIE_API_KEY="KEY" nba-cli teams --conference West`   |
| Players | Search players | `docker run --rm -t -e BALLDONTLIE_API_KEY="KEY" nba-cli players --search "LeBron"` |
| Help | Show all commands | `docker run --rm -t nba-cli --help`                                                 |

> Replace `"KEY"` with your actual API key.

---

## Option 2 — Local Python Installation

### 1️⃣ Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/nba-cli.git
cd nba-cli
python -m venv .venv
source .venv/bin/activate
pip install .
```

### 2️⃣ Set your API key

```bash
export BALLDONTLIE_API_KEY="your_api_key"
```

### 3️⃣ Run commands

```bash
nba-cli games
nba-cli games 2024-02-07
nba-cli games --team PHX
nba-cli teams --conference East
nba-cli players --search Doncic
```

---

# 📁 Project Structure

```
nba-cli/
├── nba_cli/
│   ├── api.py
│   ├── cli.py
│   ├── models.py
│   └── config.py
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

# 🛣️ Roadmap (v0.2)

- [ ] Live box scores  
- [ ] Team roster lookup  
- [ ] Head-to-head matchup history  
- [ ] Export stats to CSV/JSON  
- [ ] Offline caching  

---

# 📜 License

Licensed under the **MIT License**.