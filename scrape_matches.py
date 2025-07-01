# scrape_matches.py

import pandas as pd
import configparser
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, NavigableString
from src.utils import get_surface_from_tournament

OUTPUT_CSV = "upcoming_matches.csv"

def load_config():
    """Carrega as configurações do arquivo config.ini."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def setup_driver():
    """Configura e inicializa o driver do Selenium em modo headless e mais limpo."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_page_source(driver, url: str) -> str:
    """Navega até a URL e espera inteligentemente até que um link de jogo agendado apareça."""
    print(f"Acessando {url} e aguardando conteúdo...")
    driver.get(url)
    try:
        # Espera até 15 segundos pela presença de um link com a classe 'sched'.
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sched')))
        print("Conteúdo carregado com sucesso.")
        return driver.page_source
    except Exception as e:
        print(f"Erro ao esperar pelo conteúdo da página: {e}")
        return ""

def parse_source_to_dataframe(html_source: str) -> pd.DataFrame:
    """Processa o código HTML e extrai os jogos para um DataFrame."""
    if not html_source:
        return pd.DataFrame()

    soup = BeautifulSoup(html_source, 'lxml')
    all_matches = []
    
    # Encontra todos os links '<a>' que marcam um jogo agendado ('scheduled')
    scheduled_links = soup.select("a.sched")

    for link in scheduled_links:
        try:
            # Pega o texto que vem imediatamente antes do link, que contém os jogadores
            players_text = link.previous_sibling
            if not isinstance(players_text, NavigableString) or ' - ' not in players_text:
                continue
            
            player1, player2 = [p.strip() for p in players_text.split(' - ')]
            
            # Encontra o cabeçalho <h4> mais próximo que vem ANTES do link do jogo
            header = link.find_previous('h4')
            tournament_name = header.text.strip() if header else "Desconhecido"
            
            surface = get_surface_from_tournament(tournament_name)
            circuit = 'wta' if "wta" in tournament_name.lower() else 'atp'

            all_matches.append({
                "Circuit": circuit.upper(),
                "Player 1": player1,
                "Player 2": player2,
                "Tournament": tournament_name,
                "Surface": surface
            })
        except (AttributeError, ValueError, IndexError):
            continue
            
    return pd.DataFrame(all_matches)

def main():
    """Função principal para orquestrar o scraping e salvar em CSV."""
    config = load_config()
    schedule_url = config.get('Scraper', 'schedule_url')
    
    print("Iniciando o scraper de partidas (versão definitiva)...")
    driver = setup_driver()
    
    try:
        html = get_page_source(driver, schedule_url)
        df = parse_source_to_dataframe(html)
    finally:
        driver.quit()

    if df.empty:
        print("Nenhuma partida agendada encontrada. O site pode estar sem jogos ou sua estrutura mudou.")
        pd.DataFrame(columns=["Circuit", "Player 1", "Player 2", "Tournament", "Surface"]).to_csv(OUTPUT_CSV, index=False)
        return

    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f"\nScraping concluído. {len(df)} partidas salvas em '{OUTPUT_CSV}'.")

if __name__ == "__main__":
    main()