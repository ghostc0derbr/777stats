# src/elo_model.py

import math
import pandas as pd
from datetime import timedelta

class TennisEloModel:
    """
    Uma classe para calcular e gerenciar ratings Elo para jogadores de tênis,
    com ratings separados por superfície e para forma geral vs. recente.
    """
    def __init__(self, base_rating=1500, k_factor=32):
        self.base_rating = base_rating
        self.k_factor = k_factor
        
        # Dicionários para o Elo Geral (longo prazo)
        self.ratings_hard = {}
        self.ratings_clay = {}
        self.ratings_grass = {}

        # Dicionários para o Elo de Forma Recente (curto prazo)
        self.recent_ratings_hard = {}
        self.recent_ratings_clay = {}
        self.recent_ratings_grass = {}

    def _get_ratings_for_surface(self, surface: str, recent=False):
        """Método auxiliar para retornar o dicionário de ratings correto (geral ou recente)."""
        if recent:
            if surface == 'Hard': return self.recent_ratings_hard
            if surface == 'Clay': return self.recent_ratings_clay
            if surface == 'Grass': return self.recent_ratings_grass
        else:
            if surface == 'Hard': return self.ratings_hard
            if surface == 'Clay': return self.ratings_clay
            if surface == 'Grass': return self.ratings_grass
        return {}

    def _get_rating(self, player_name: str, surface: str, recent=False) -> float:
        """Obtém o rating de um jogador para uma superfície específica (geral ou recente)."""
        ratings = self._get_ratings_for_surface(surface, recent)
        return ratings.get(player_name, self.base_rating)

    def get_win_probability(self, player_a_name: str, player_b_name: str, surface: str, recent=False) -> float:
        """Calcula a probabilidade de vitória do Jogador A (geral ou recente)."""
        rating_a = self._get_rating(player_a_name, surface, recent)
        rating_b = self._get_rating(player_b_name, surface, recent)
        
        expected_prob_a = 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))
        return expected_prob_a

    def _update_ratings(self, winner_name: str, loser_name: str, surface: str, recent=False):
        """Atualiza os ratings Elo de ambos os jogadores (geral ou recente)."""
        ratings = self._get_ratings_for_surface(surface, recent)
        
        winner_rating = self._get_rating(winner_name, surface, recent)
        loser_rating = self._get_rating(loser_name, surface, recent)

        prob_winner = self.get_win_probability(winner_name, loser_name, surface, recent)
        rating_change = self.k_factor * (1 - prob_winner)

        ratings[winner_name] = winner_rating + rating_change
        ratings[loser_name] = loser_rating - rating_change

    def train_general(self, historical_data: pd.DataFrame):
        """Treina o modelo Elo Geral com todos os dados históricos."""
        print(f"Treinando o modelo Elo Geral com {len(historical_data)} partidas...")
        for index, match in historical_data.iterrows():
            self._update_ratings(match['winner_name'], match['loser_name'], match['surface'], recent=False)
        print("Treinamento do Elo Geral completo!")

    def train_recent_form(self, historical_data: pd.DataFrame, months=6):
        """Treina o modelo Elo de Forma Recente com os dados dos últimos X meses."""
        if historical_data.empty:
            print("Nenhum dado para treinar a forma recente.")
            return
            
        # Garante que a coluna de data esteja no formato correto
        historical_data['tourney_date'] = pd.to_datetime(historical_data['tourney_date'])
        
        # Filtra os dados para o período desejado
        last_date = historical_data['tourney_date'].max()
        cutoff_date = last_date - timedelta(days=months * 30)
        recent_data = historical_data[historical_data['tourney_date'] >= cutoff_date]

        print(f"Treinando o modelo de Forma Recente com {len(recent_data)} partidas dos últimos {months} meses...")
        for index, match in recent_data.iterrows():
            self._update_ratings(match['winner_name'], match['loser_name'], match['surface'], recent=True)
        print("Treinamento de Forma Recente completo!")