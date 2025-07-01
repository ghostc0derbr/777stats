# 🎾 777stats – Sistema Profissional de Análise Esportiva de Tênis

O **777stats** é uma aplicação completa e robusta de análise estatística de partidas de tênis (ATP e WTA), construída com foco em performance, precisão e escalabilidade. Ideal para estudos analíticos, apostas esportivas ou desenvolvimento de modelos preditivos com dados históricos.

---

## ✅ Principais Funcionalidades

- 🔍 **Coleta automatizada** de partidas diárias com `scrape_matches.py`  
- 🧠 **Machine Learning** com dois modelos distintos (ATP e WTA)  
- 🗃️ **Banco de dados completo** com histórico de temporadas anteriores  
- 📊 **Geração de features avançadas**: Elo Geral, Forma Recente, Head-to-Head  
- 📈 **Previsões diárias** em formato de tabela limpa e profissional  
- ⚙️ **Configuração simplificada** via `config.ini`  
- 🔄 **Atualização e retreinamento fácil** com flag `--retrain`  

---

## 🚀 Como Usar

### 1. Coletar jogos do dia

```bash
python scrape_matches.py
2. Executar a análise e visualizar as previsões
bash
Copiar
Editar
python main.py
3. Atualizar e retreinar os modelos
bash
Copiar
Editar
python main.py --retrain
Dica: Mantenha seu arquivo config.ini sempre atualizado com as configurações ideais para cada temporada.

📂 Estrutura do Projeto
bash
Copiar
Editar
777stats/
├── scrape_matches.py      # Coletor diário de jogos
├── main.py                # Analisador e gerador de previsões
├── config.ini             # Arquivo de configuração
├── models/                # Modelos de ML treinados
├── data/                  # Banco de dados de partidas
└── utils/                 # Funções auxiliares
🧭 Próximos Passos (Futuros Recursos)
Quando decidir evoluir o sistema, considere:

✅ Backtesting real com dados históricos (ex: temporada 2024 com modelo 2023)

📌 Novas features estatísticas (aces, duplas faltas, % pontos no serviço)

💬 Modo Interativo com consulta manual a partidas específicas

🎯 Análise Tática Profunda com dados ponto a ponto

🏁 Conclusão
O 777stats representa o estado-da-arte em sistemas de análise preditiva para tênis. Após diversas fases de desenvolvimento, agora você possui uma ferramenta confiável, escalável e altamente personalizável. Aproveite todo o potencial!

📬 Contato e Suporte
Caso queira expandir o sistema, tirar dúvidas ou propor melhorias, estou à disposição.

“Dados vencem opiniões. E agora, você tem os dados do seu lado.”

<br>
Desenvolvido por @ghostc0der


# 🎾 777stats – Professional Tennis Sports Analysis System

**777stats** is a complete and robust application for statistical analysis of tennis matches (ATP and WTA), developed with a focus on performance, accuracy and scalability. Ideal for analytical studies, sports betting or development of predictive models with historical data.

---

## ✅ Main Features

- 🔍 **Automated scraping** of daily matches with `scrape_matches.py`
- 🧠 **Machine Learning** with two distinct models (ATP and WTA)
- 🗃️ **Full database** with history from previous seasons
- 📊 **Advanced feature generation**: Overall elo, Recent form, Head-to-head
- 📈 **Daily predictions** in a clean and professional table format
- ⚙️ **Simple configuration** via `config.ini`
- 🔄 **Easy refresh and retrain** with `--retrain` flag

---
## 🚀 How to use

### 1. Scrape matches of the day

```bash
python scrape_matches.py
2. Perform analysis and visualization of predictions
bash
Copy
Edit
python main.py
3. Update and retrain the models
bash
Copy
Edit
python main.py --retrain
Tip: Always keep the config.ini file updated with the optimal settings for each station.

📂 Project Structure
bash
Copy
Edit
777stats/
├── scrape_matches.py # Daily match collector
├── main.py # Analyzer and prediction generator
├── config.ini # Configuration file
├── models/ # Trained ML models
├── data/ # Match database
└── utils/ # Helper functions
🧭 Next Steps (Future Features)
When deciding to evolve the system, consider:

✅ Real backtesting with historical data (e.g. 2024 season with 2023 model)

📌 New statistical features (aces, double faults, % of points on serve)

💬 Interactive mode with specific manual query for matches

🎯 Deep Tactical Analysis with Point-by-Point Data

🏁 Conclusion
777stats represents the ultimate in predictive analysis systems for tennis. After several development phases, you now have a reliable, scalable and highly customizable tool. Take advantage of its full potential!

📬 Contact and Support
If you want to expand the system, ask questions or suggest improvements, I am at your disposal.

“Data beats opinions. And now, you have the data on your side.”

<br>
Developed by @ghostc0der


