# main.py

import pickle
import os
import sqlite3
import sys
import configparser
import pandas as pd
from datetime import datetime
from tabulate import tabulate
from src.data_handler import init_db, get_last_year_in_db, download_and_insert_data, load_all_data_from_db
from src.elo_model import TennisEloModel
from src.utils import normalize_player_name, get_h2h_record
from src.feature_engineering import create_feature_vector, create_dataset_for_ml
from src.ml_model import MLModel

def load_config():
    """Carrega as configurações do arquivo config.ini."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def sync_data(config):
    """Sincroniza o banco de dados para os circuitos ATP e WTA."""
    init_db()
    data_up_to_year = config.getint('DataSource', 'data_up_to_year')
    start_year_default = config.getint('DataSource', 'start_year_default')
    circuits = ['atp', 'wta']
    for circuit in circuits:
        print(f"\n--- Sincronizando circuito {circuit.upper()} ---")
        last_year_in_db = get_last_year_in_db(circuit)
        start_year = last_year_in_db + 1 if last_year_in_db else start_year_default
        if last_year_in_db is None:
            print(f"Nenhum dado encontrado para {circuit.upper()}. Iniciando download desde {start_year}...")
        conn = sqlite3.connect(os.path.join("data", "777stats.db"))
        try:
            for year in range(start_year, data_up_to_year + 1):
                download_and_insert_data(year, circuit, conn)
        finally:
            conn.close()

def train_and_save_model(config, circuit):
    """Função para treinar e salvar o modelo de um circuito específico."""
    model_filename = config.get('Model', f'model_filename_{circuit}')
    print(f"\nNenhum modelo de ML ({circuit.upper()}) encontrado. Iniciando pipeline de treinamento...")
    historical_data = load_all_data_from_db(circuit)
    if historical_data.empty:
        print(f"Nenhum dado histórico da {circuit.upper()} para treinar.")
        return None
    elo_model = TennisEloModel()
    elo_model.train_general(historical_data)
    elo_model.train_recent_form(historical_data, months=config.getint('Model', 'recent_form_months'))
    X_train, y_train = create_dataset_for_ml(circuit, historical_data, elo_model)
    ml_model = MLModel()
    ml_model.train(X_train, y_train)
    print(f"Salvando modelo de ML ({circuit.upper()}) treinado em '{model_filename}'...")
    with open(model_filename, 'wb') as f:
        pickle.dump(ml_model, f)
    print("Modelo salvo!")
    return ml_model

def main():
    """Função principal para executar o fluxo do sistema."""
    config = load_config()
    circuits = ['atp', 'wta']
    ml_models, elo_models, known_players_map = {}, {}, {}

    print("--- INICIANDO SISTEMA DE ANÁLISE DE TÊNIS 777stats ---")
    if '--retrain' in sys.argv:
        print("Flag '--retrain' detectada. Todos os modelos serão treinados do zero.")
        for c in circuits:
            fname = config.get('Model', f'model_filename_{c}')
            if os.path.exists(fname): os.remove(fname)
            print(f"Arquivo de modelo antigo '{fname}' removido.")
    
    sync_data(config)

    for circuit in circuits:
        model_filename = config.get('Model', f'model_filename_{circuit}')
        if os.path.exists(model_filename):
            print(f"\nCarregando modelo de ML ({circuit.upper()})...")
            with open(model_filename, 'rb') as f: ml_models[circuit] = pickle.load(f)
            print(f"Modelo ({circuit.upper()}) carregado!")
        else:
            ml_models[circuit] = train_and_save_model(config, circuit)
        
        print(f"Preparando gerador de features para jogos futuros ({circuit.upper()})...")
        historical_data = load_all_data_from_db(circuit)
        if not historical_data.empty:
            elo_model = TennisEloModel()
            elo_model.train_general(historical_data)
            elo_model.train_recent_form(historical_data, months=config.getint('Model', 'recent_form_months'))
            elo_models[circuit] = elo_model
            known_players_map[circuit] = set(elo_model.ratings_hard.keys()) | set(elo_model.ratings_clay.keys()) | set(elo_model.ratings_grass.keys())

    try:
        upcoming_matches_df = pd.read_csv("upcoming_matches.csv")
    except FileNotFoundError:
        print("\nArquivo 'upcoming_matches.csv' não encontrado. Por favor, execute 'scrape_matches.py' primeiro.")
        return
        
    if upcoming_matches_df.empty:
        print("\nNenhum jogo encontrado no arquivo 'upcoming_matches.csv' para análise.")
        return

    results_data, headers = [], ["Circuito", "Jogador 1", "Jogador 2", "Superfície", "H2H Geral", "Prob. P1 (ML)"]
    for index, match in upcoming_matches_df.iterrows():
        circuit = match['Circuit'].lower()
        surface = match['Surface']
        scraped_p1 = match['Player 1']
        scraped_p2 = match['Player 2']

        if circuit not in ml_models or ml_models[circuit] is None or surface == 'Unknown':
            continue

        known_players = known_players_map.get(circuit, set())
        full_name_p1 = normalize_player_name(scraped_p1, known_players)
        full_name_p2 = normalize_player_name(scraped_p2, known_players)
        
        if not full_name_p1 or not full_name_p2:
            continue
        
        h2h = get_h2h_record(circuit, full_name_p1, full_name_p2)
        h2h_str = f"{h2h['overall']['p1_wins']} - {h2h['overall']['p2_wins']}"
        
        elo_model_for_prediction = elo_models[circuit]
        feature_vector = create_feature_vector(full_name_p1, full_name_p2, surface, elo_model_for_prediction, h2h)
        
        prediction = ml_models[circuit].predict_proba([feature_vector])
        prob_p1_wins = prediction[0][1]
        
        results_data.append([circuit.upper(), full_name_p1, full_name_p2, surface, h2h_str, f"{prob_p1_wins:.2%}"])

    print("\n--- ANÁLISE DOS PRÓXIMOS JOGOS (MODELO MACHINE LEARNING) ---")
    if not results_data:
        print("Nenhuma partida com dados completos foi encontrada para hoje.")
    else:
        print(tabulate(results_data, headers=headers, tablefmt="grid"))
        print("\nCompare a probabilidade final (Prob. P1) com as odds do mercado para o Jogador 1!")

if __name__ == "__main__":
    main()