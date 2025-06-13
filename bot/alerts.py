import requests
from .config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_alert(analysis):
    for bet in analysis:
        msg = (
            f"[{bet.get('liga','')}] 🟢 EV+ Detectado!\n"
            f"Jogo: {bet['game']}\n"
            f"Tipo: {bet['type']}\n"
            f"Odd: {bet['odd']}\n"
            f"EV%: {bet['ev']}\n"
            f"Score Confiança: {bet['score']}\n"
            f"Stake sugerida: {bet['stake']}% do bankroll\n"
            f"Motivos: {bet['motivos']}\n"
            f"[Concordo] [Discordo] [Reportar erro]\n"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

def send_report(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
