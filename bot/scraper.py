import os
import requests
from bs4 import BeautifulSoup

# Oddshark - Predicted Score
def fetch_predicted_score_oddshark(league="nba"):
    url = f'https://www.oddshark.com/{league}/computer-picks'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    games = []
    for row in soup.select('.op-matchup-wrapper'):
        teams = [x.get_text(strip=True) for x in row.select('.op-matchup-team-name')]
        scores = [x.get_text(strip=True) for x in row.select('.op-matchup-team-score')]
        if len(teams) == 2 and len(scores) == 2:
            games.append({
                'game': f'{teams[0]} x {teams[1]}',
                'score_home': int(scores[0]),
                'score_away': int(scores[1]),
            })
    return games

# TeamRankings - Power Ratings
def fetch_power_ratings_teamrankings(sport="nba"):
    urls = {
        "nba": "https://www.teamrankings.com/nba/power-rankings/",
        "nfl": "https://www.teamrankings.com/nfl/power-rankings/",
        "mlb": "https://www.teamrankings.com/mlb/power-rankings/",
        "ncaab": "https://www.teamrankings.com/ncaa-basketball/power-rankings/",
        "ncaaf": "https://www.teamrankings.com/college-football/power-rankings/",
    }
    url = urls.get(sport, urls["nba"])
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ratings = []
    for row in soup.select('table.tr-table tbody tr'):
        tds = row.find_all('td')
        if len(tds) >= 4:
            team = tds[1].get_text(strip=True)
            rating = float(tds[2].get_text(strip=True))
            ratings.append({'team': team, 'power_rating': rating})
    return ratings

# ESPN - Lesões
def fetch_injuries_espn(league="nba"):
    urls = {
        "nba": "https://www.espn.com/nba/injuries",
        "nfl": "https://www.espn.com/nfl/injuries",
        "mlb": "https://www.espn.com/mlb/injuries",
        "ncaab": "https://www.espn.com/mens-college-basketball/injuries",
        "ncaaf": "https://www.espn.com/college-football/injuries",
    }
    url = urls.get(league, urls["nba"])
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    injuries = []
    tables = soup.find_all("section", {"class": "ResponsiveTable"})
    for table in tables:
        team_header = table.find("span", {"class": "flex items-center"})
        if team_header:
            team = team_header.get_text(strip=True)
            tbody = table.find("tbody")
            for row in tbody.find_all("tr"):
                tds = row.find_all("td")
                if len(tds) >= 3:
                    player = tds[0].text.strip()
                    status = tds[2].text.strip()
                    injuries.append({"team": team, "player": player, "status": status})
    return injuries

# Odds API - Mercado (Pinnacle, Betfair, etc)
def fetch_market_odds_oddsapi(league="basketball_nba", bookmaker="pinnacle"):
    api_key = os.getenv("ODDS_API_KEY")
    url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={api_key}&bookmakers={bookmaker}&markets=h2h,spreads,totals"
    r = requests.get(url)
    data = r.json()
    odds = []
    for g in data:
        home, away = g['home_team'], g['away_team']
        for book in g['bookmakers']:
            if book['key'] == bookmaker:
                for market in book['markets']:
                    outcomes = market['outcomes']
                    odds.append({
                        'game': f"{home} x {away}",
                        'market': market['key'],
                        'odds': [{o['name']: o['price']} for o in outcomes]
                    })
    return odds
