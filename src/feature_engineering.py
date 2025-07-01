# src/feature_engineering.py

import pandas as pd
from src.elo_model import TennisEloModel
from src.utils import get_h2h_record
from typing import Tuple
from tqdm import tqdm # <<< NOVA IMPORTAÇÃO

def create_feature_vector(p1_name: str, p2_name: str, surface: str, elo_model: TennisEloModel, h2h: dict) -> list:
    """Cria um vetor de características numéricas para uma única partida."""
    elo_geral_p1 = elo_model._get_rating(p1_name, surface, recent=False)
    elo_geral_p2 = elo_model._get_rating(p2_name, surface, recent=False)
    elo_recente_p1 = elo_model._get_rating(p1_name, surface, recent=True)
    elo_recente_p2 = elo_model._get_rating(p2_name, surface, recent=True)
    h2h_surface = h2h.get(surface, {'p1_wins': 0, 'p2_wins': 0})
    features = [
        elo_geral_p1 - elo_geral_p2,
        elo_recente_p1 - elo_recente_p2,
        h2h['overall']['p1_wins'],
        h2h['overall']['p2_wins'],
        h2h_surface['p1_wins'],
        h2h_surface['p2_wins'],
    ]
    return features

def create_dataset_for_ml(circuit: str, historical_data: pd.DataFrame, elo_model: TennisEloModel) -> Tuple[list, list]:
    """Processa todos os dados históricos para criar um dataset de features (X) e rótulos (y)."""
    print(f"Iniciando engenharia de features para o dataset {circuit.upper()} de Machine Learning...")
    X, y, h2h_cache = [], [], {}

    # <<< ALTERAÇÃO AQUI: Envolvendo o loop com tqdm >>>
    # O 'desc' mostra uma descrição, e 'total' ajuda a tqdm a calcular o tempo restante.
    loop_description = f"Processando {circuit.upper()}"
    for index, match in tqdm(historical_data.iterrows(), total=historical_data.shape[0], desc=loop_description):
        p1_name, p2_name, surface = match['winner_name'], match['loser_name'], match['surface']
        import random
        if random.random() < 0.5:
            p1_name, p2_name = p2_name, p1_name
        
        label = 1 if p1_name == match['winner_name'] else 0
        h2h_key = tuple(sorted((p1_name, p2_name)))
        if h2h_key not in h2h_cache:
            h2h_cache[h2h_key] = get_h2h_record(circuit, p1_name, p2_name)
        h2h = h2h_cache[h2h_key]

        features = create_feature_vector(p1_name, p2_name, surface, elo_model, h2h)
        X.append(features)
        y.append(label)

    print(f"Engenharia de features concluída. Dataset criado com {len(X)} exemplos.")
    return X, y