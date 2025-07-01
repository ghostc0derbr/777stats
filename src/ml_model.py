# src/ml_model.py

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

class MLModel:
    """
    Uma classe para encapsular o modelo de Machine Learning.
    """
    def __init__(self):
        # O StandardScaler ajuda a normalizar nossas features, o que melhora o desempenho do modelo.
        self.scaler = StandardScaler()
        # A Regressão Logística é o nosso algoritmo de previsão.
        self.model = LogisticRegression(solver='liblinear', random_state=42)

    def train(self, X_train: list, y_train: list):
        """
        Treina o scaler e o modelo de ML com os dados de treinamento.
        
        :param X_train: Lista de vetores de features.
        :param y_train: Lista de rótulos (resultados das partidas).
        """
        print("Treinando o modelo de Machine Learning...")
        
        # Primeiro, ajustamos o scaler aos dados de treino e os transformamos.
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Depois, treinamos o modelo com os dados escalados.
        self.model.fit(X_scaled, y_train)
        
        print("Treinamento do modelo de ML concluído.")

    def predict_proba(self, X_predict: list) -> np.ndarray:
        """
        Prevê a probabilidade de vitória para um novo conjunto de features.
        
        :param X_predict: Lista (ou lista de listas) de vetores de features para prever.
        :return: Um array com as probabilidades [prob_derrota, prob_vitoria].
        """
        # Usamos o scaler já treinado para transformar os novos dados.
        X_scaled = self.scaler.transform(X_predict)
        
        # Fazemos a previsão de probabilidade.
        return self.model.predict_proba(X_scaled)