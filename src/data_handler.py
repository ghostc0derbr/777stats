# src/data_handler.py

import os
import pandas as pd
import requests
import sqlite3
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "777stats.db")

def init_db():
    """Inicializa o banco de dados e cria as tabelas para ATP e WTA se não existirem."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cria tabela para o circuito ATP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atp_matches (
            tourney_id TEXT, tourney_name TEXT, surface TEXT, tourney_date DATE,
            winner_id INTEGER, winner_name TEXT, loser_id INTEGER, loser_name TEXT,
            UNIQUE(tourney_id, tourney_date, winner_id, loser_id)
        )
    """)
    
    # Cria tabela para o circuito WTA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wta_matches (
            tourney_id TEXT, tourney_name TEXT, surface TEXT, tourney_date DATE,
            winner_id INTEGER, winner_name TEXT, loser_id INTEGER, loser_name TEXT,
            UNIQUE(tourney_id, tourney_date, winner_id, loser_id)
        )
    """)
    
    conn.commit()
    conn.close()

def get_last_year_in_db(circuit: str):
    """Consulta o banco para encontrar o último ano com dados salvos para um circuito."""
    if not os.path.exists(DB_PATH):
        return None
    
    table_name = f"{circuit}_matches"
    conn = sqlite3.connect(DB_PATH)
    try:
        query = f"SELECT MAX(strftime('%Y', tourney_date)) as last_year FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        last_year = df['last_year'].iloc[0]
        return int(last_year) if last_year else None
    except (pd.errors.DatabaseError, IndexError, ValueError):
        return None
    finally:
        conn.close()

def download_and_insert_data(year: int, circuit: str, conn):
    """Baixa os dados de um ano para um circuito e insere no banco de dados."""
    base_url = f"https://raw.githubusercontent.com/JeffSackmann/tennis_{circuit}/master/"
    file_name = f"{circuit}_matches_{year}.csv"
    file_url = f"{base_url}{file_name}"
    table_name = f"{circuit}_matches"
    
    print(f"Verificando dados de {year} para o circuito {circuit.upper()}...")
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        
        df = pd.read_csv(file_url, encoding='utf-8')
        columns_to_keep = ['tourney_id', 'tourney_name', 'surface', 'tourney_date', 'winner_id', 'winner_name', 'loser_id', 'loser_name']
        df = df[columns_to_keep]
        df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        df.dropna(subset=['winner_name', 'loser_name', 'surface'], inplace=True)
        
        cursor = conn.cursor()
        for index, row in df.iterrows():
            cursor.execute(f"""
                INSERT OR IGNORE INTO {table_name} (tourney_id, tourney_name, surface, tourney_date, winner_id, winner_name, loser_id, loser_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(row))
        conn.commit()
        print(f"Dados de {year} ({circuit.upper()}) sincronizados com o banco.")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Dados para o ano {year} ({circuit.upper()}) ainda não disponíveis (404 Not Found).")
        else:
            print(f"Erro HTTP ao baixar dados de {year} ({circuit.upper()}): {e}")
    except Exception as e:
        print(f"Erro inesperado ao processar dados de {year} ({circuit.upper()}): {e}")

def load_all_data_from_db(circuit: str) -> pd.DataFrame:
    """Carrega todos os dados históricos de um circuito a partir do banco de dados."""
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
        
    table_name = f"{circuit}_matches"
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        df.sort_values(by='tourney_date', inplace=True)
        return df
    finally:
        conn.close()