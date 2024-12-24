
import tkinter as tk
from tkinter import ttk

def criar_interface():
    root = tk.Tk()
    root.title("Alterar Tamanho da Fonte no Botão")

    # Criando o estilo personalizado para o botão
    estilo = ttk.Style()

    # Definindo o estilo da fonte com tamanho grande
    estilo.configure("Custom.TButton",
                     font=("Arial", 10),  # Fonte Arial, tamanho 20
                     foreground="white",
                     background="blue")

    # Criando o botão com o estilo personalizado
    botao1 = ttk.Button(root, text="Botão com Fonte Grande", style="Custom.TButton")
    botao1.pack(padx=20, pady=20)

    root.mainloop()

criar_interface()
