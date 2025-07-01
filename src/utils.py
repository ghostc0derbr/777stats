# src/utils.py

import sqlite3
import os
from typing import Tuple

DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "777stats.db")

TOURNAMENT_SURFACES = {
    # ... (dicionário de torneios permanece o mesmo) ...
    'Wimbledon': 'Grass', 'Halle': 'Grass', 'Stuttgart': 'Grass', "'s-Hertogenbosch": 'Grass', 'Newport': 'Grass', 'Eastbourne': 'Grass', 'Mallorca': 'Grass', "Queen's Club": 'Grass',
    'Roland Garros': 'Clay', 'Monte-Carlo': 'Clay', 'Rome': 'Clay', 'Madrid': 'Clay', 'Hamburg': 'Clay', 'Barcelona': 'Clay', 'Rio de Janeiro': 'Clay', 'Estoril': 'Clay', 'Gstaad': 'Clay', 'Kitzbuhel': 'Clay', 'Bastad': 'Clay', 'Cordoba': 'Clay', 'Santiago': 'Clay', 'Buenos Aires': 'Clay',
    'Australian Open': 'Hard', 'US Open': 'Hard', 'Indian Wells': 'Hard', 'Miami': 'Hard', 'Cincinnati': 'Hard', 'Shanghai': 'Hard', 'Paris Masters': 'Hard', 'Canada Masters': 'Hard', 'Toronto': 'Hard', 'Montreal': 'Hard', 'ATP Finals': 'Hard', 'WTA Finals': 'Hard', 'Dubai': 'Hard', 'Acapulco': 'Hard', 'Beijing': 'Hard', 'Tokyo': 'Hard', 'Vienna': 'Hard', 'Basel': 'Hard'
}

def get_surface_from_tournament(tournament_name: str) -> str:
    for key, surface in TOURNAMENT_SURFACES.items():
        if key.lower() in tournament_name.lower():
            return surface
    return 'Unknown'

def normalize_player_name(scraped_name: str, known_players: set) -> str | None:
    if scraped_name in known_players: return scraped_name
    parts = scraped_name.split(' ')
    if len(parts) > 1 and len(parts[-1]) == 2 and parts[-1].endswith('.'):
        last_name = parts[0]
        initial = parts[-1][0]
        matches = [name for name in known_players if last_name in name and name.startswith(initial)]
        if len(matches) == 1: return matches[0]
    last_name_only = parts[0]
    matches = [name for name in known_players if last_name_only in name]
    if len(matches) == 1: return matches[0]
    return None

def get_h2h_record(circuit: str, player1_name: str, player2_name: str) -> dict:
    h2h_results = {'overall': {'p1_wins': 0, 'p2_wins': 0}, 'Hard': {'p1_wins': 0, 'p2_wins': 0}, 'Clay': {'p1_wins': 0, 'p2_wins': 0}, 'Grass': {'p1_wins': 0, 'p2_wins': 0}}
    if not os.path.exists(DB_PATH): return h2h_results

    table_name = f"{circuit}_matches"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        query = f"SELECT winner_name, loser_name, surface FROM {table_name} WHERE (winner_name = ? AND loser_name = ?) OR (winner_name = ? AND loser_name = ?)"
        cursor.execute(query, (player1_name, player2_name, player2_name, player1_name))
        matches = cursor.fetchall()
    except sqlite3.OperationalError: # Se a tabela não existir, não falha
        matches = []
    finally:
        conn.close()

    for winner, loser, surface in matches:
        if winner == player1_name: h2h_results['overall']['p1_wins'] += 1
        else: h2h_results['overall']['p2_wins'] += 1
        if surface in h2h_results:
            if winner == player1_name: h2h_results[surface]['p1_wins'] += 1
            else: h2h_results[surface]['p2_wins'] += 1
    return h2h_results