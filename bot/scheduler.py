import schedule
import time
from datetime import datetime
from .scraper import (
    fetch_predicted_score_oddshark,
    fetch_power_ratings_teamrankings,
    fetch_injuries_espn,
    fetch_market_odds_oddsapi
)
from .analysis import run_full_analysis
from .alerts import send_alert, send_report

def collect_and_analyze(league, league_api, league_name):
    try:
        data = {
            'scores': fetch_predicted_score_oddshark(league),
            'ratings': fetch_power_ratings_teamrankings(league),
            'injuries': fetch_injuries_espn(league),
            'odds': fetch_market_odds_oddsapi(league_api, 'pinnacle')
        }
        analysis = run_full_analysis(data)
        if analysis:
            # Adiciona prefixo da liga na mensagem
            for bet in analysis:
                bet['liga'] = league_name.upper()
            send_alert(analysis)
        else:
            send_report(f"[{league_name.upper()}] Sem EV+ relevante hoje.")
    except Exception as e:
        send_report(f"[{league_name.upper()}] Erro crítico: {e}")

def job():
    # NBA
    collect_and_analyze('nba', 'basketball_nba', 'NBA')
    # NFL
    collect_and_analyze('nfl', 'americanfootball_nfl', 'NFL')
    # MLB
    collect_and_analyze('mlb', 'baseball_mlb', 'MLB')
    # NCAAB (Basquete Universitário)
    collect_and_analyze('ncaab', 'basketball_ncaab', 'NCAAB')
    # NCAAF (Futebol Americano Universitário)
    collect_and_analyze('ncaaf', 'americanfootball_ncaaf', 'NCAAF')

def start_scheduler():
    schedule.every().day.at("11:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(30)
