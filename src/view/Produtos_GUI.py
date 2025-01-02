import tkinter as tk
from tkinter import ttk

class Produtos_GUI:

    def __init__(self, root: tk.Tk, funcao):
        self.master = root
        self.callback = funcao
        self.__destruir()
        self.__aplly_widgets()

    def __aplly_widgets(self):

        voltar = ttk.Button(text="Voltar", command=self.__voltar)
        voltar.grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        listbox = tk.Listbox(self.master, height=10, width=70, background="gray60")
        self.__adicionar_produtos(listbox)
        listbox.grid(column=0, row=1, padx=30)

        adicionar = ttk.Button(self.master, text="+")
        adicionar.grid(column=0, row=1, padx=30, sticky="nw")

    def __voltar(self):
        self.__destruir()
        self.callback()

    def __destruir(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def __adicionar_produtos(self, listbox):
        for i in range(100):
            listbox.insert(tk.END, f" {i} | lepra")


class Produto_adder():

    def __init__(self):
        pass

