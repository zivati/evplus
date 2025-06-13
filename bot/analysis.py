def calculate_ev(odds, model_prob):
    return round(((model_prob * odds) - (1 - model_prob)) * 100, 2)

def get_score_confidence(sources):
    score = 7
    if sources.get('injury') and sources['injury']['status'] == 'Out':
        score += 1
    return min(score, 10)

def suggest_stake(score):
    return round((score / 10) * 2.5, 2)

def run_full_analysis(data):
    analysis = []
    for game in data['scores']:
        ev = calculate_ev(2.4, 0.47)  # Exemplo, adapte conforme a fonte/modelo real
        score = get_score_confidence({'injury': None})  # Adapte para ligar aos dados de fato
        stake = suggest_stake(score)
        if ev > 5 and score >= 7:
            analysis.append({
                'game': game['game'],
                'ev': ev,
                'score': score,
                'stake': stake,
                'odd': 2.4,
                'type': 'Moneyline',
                'motivos': 'Consenso alto e lesão adversária',
            })
    return analysis
