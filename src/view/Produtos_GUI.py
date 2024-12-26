import tkinter as tk
from tkinter import ttk

class Produtos_GUI:

    def __init__(self, root: tk.Tk, funcao):
        self.master = root
        self.callback = funcao
        self.__destruir()
        self.__aplly_widgets()

    def __aplly_widgets(self):
        voltar = ttk.Button(text="cancer", command=self.__voltar)
        voltar.grid(column=0, row=1, pady=80, sticky="n")


    def __voltar(self):
        self.__destruir()
        self.callback()

    def __destruir(self):
        for widget in self.master.winfo_children():
            widget.destroy()
