# gui_app.py

import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela Principal ---
        self.title("777stats - Painel de Controle")
        self.geometry("500x350")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.set_appearance_mode("dark") # Define o tema escuro

        # --- Frame Superior: Título ---
        self.title_frame = ctk.CTkFrame(self, corner_radius=0)
        self.title_frame.grid(row=0, column=0, sticky="ew")
        self.title_label = ctk.CTkLabel(self.title_frame, text="777stats", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # --- Frame Central: Botões de Ação ---
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Botão de Start
        self.start_button = ctk.CTkButton(self.button_frame, text="Iniciar Análise", command=self.start_analysis)
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Botão de Start com Retrain
        self.retrain_button = ctk.CTkButton(self.button_frame, text="Iniciar com Retreinamento", command=self.start_retrain_analysis)
        self.retrain_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Botão para ver a Dashboard
        self.dashboard_button = ctk.CTkButton(self.button_frame, text="Ver Dashboard", state="disabled", command=self.open_dashboard)
        self.dashboard_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # --- Frame Inferior: Status e Animação ---
        self.status_frame = ctk.CTkFrame(self, corner_radius=0)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Status: Aguardando Comando")
        self.status_label.grid(row=0, column=0, sticky="w", padx=10)

        # Barra de Progresso como "Animação"
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, mode='indeterminate')
        
        # Botão de Desligar
        self.quit_button = ctk.CTkButton(self, text="Desligar", command=self.quit_app, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.quit_button.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

    # --- Funções dos Botões (por enquanto, apenas imprimem no console) ---
    def start_analysis(self):
        print("Botão 'Iniciar Análise' clicado. Lógica a ser implementada.")
        self.status_label.configure(text="Status: Análise iniciada...")
        self.progress_bar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.progress_bar.start()

    def start_retrain_analysis(self):
        print("Botão 'Iniciar com Retreinamento' clicado. Lógica a ser implementada.")
        self.status_label.configure(text="Status: Retreinamento iniciado (pode levar vários minutos)...")
        self.progress_bar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.progress_bar.start()

    def open_dashboard(self):
        print("Botão 'Ver Dashboard' clicado. Lógica a ser implementada.")

    def quit_app(self):
        print("Desligando a aplicação.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()