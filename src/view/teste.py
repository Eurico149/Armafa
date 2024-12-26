import tkinter as tk
from tkinter import ttk

def criar_layout():
    root = tk.Tk()
    root.geometry("400x200")  # Definindo o tamanho da janela

    # Configurando o grid para garantir o ajuste adequado
    root.grid_columnconfigure(0, weight=1)  # A primeira coluna terá peso 1
    root.grid_columnconfigure(1, weight=1)  # A segunda coluna terá peso 1
    root.grid_columnconfigure(2, weight=0)  # A terceira coluna não se expandirá
    root.grid_rowconfigure(0, weight=1)     # Linha 0 terá peso 1
    root.grid_rowconfigure(1, weight=0)     # Linha 1 não se expandirá

    # Botões centralizados
    botao_esquerdo = ttk.Button(root, text="Botão Esquerdo")
    botao_esquerdo.grid(row=0, column=0, padx=10, pady=20, sticky="ew")

    botao_direito = ttk.Button(root, text="Botão Direito")
    botao_direito.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

    # Botão na ponta direita
    botao_ponta_direita = ttk.Button(root, text="Botão Ponta Direita")
    botao_ponta_direita.grid(row=1, column=2, padx=10, pady=10, sticky="e")

    root.mainloop()

criar_layout()
