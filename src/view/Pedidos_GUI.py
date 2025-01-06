import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from src.Controller.Pedidos_controller import Pedidos_controller as Pec


class Pedidos_GUI:

    def __init__(self, root: tk.Tk, funcao):
        self.master = root
        self.callback = funcao
        self.__destruir()
        self.__aplly_widgets()

    def __aplly_widgets(self):

        voltar = ttk.Button(self.master, text="Voltar", command=self.__voltar)
        voltar.grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        frame = ttk.Frame(self.master)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, width=10)
        listbox = tk.Listbox(frame, height=10, width=55, background="gray60", yscrollcommand=scrollbar.set, font=("Courier", 8))
        scrollbar.config(command=listbox.yview)

        busca = ttk.Entry(self.master, width=54)
        busca.grid(column=0, row=1, sticky="ne", pady=5, padx=35)

        def atualizar_produtos():
            texto = busca.get()
            produtos = Pec().get_pedidos(texto)
            lista = listbox.get(0, tk.END)

            veri = [str(x) for x in produtos]
            vali = True

            if len(veri) == len(lista):
                vali = False
                for j in range(len(veri)):
                    if veri[j] != list(lista)[j]:
                        vali = True
                        break

            if vali:
                listbox.delete(0, tk.END)
                for i in produtos:
                    listbox.insert(tk.END, str(i))

            listbox.after(1000, atualizar_produtos)

        atualizar_produtos()

        def change_prod(event):
            index = listbox.curselection()[0]
            selecionado = str(listbox.get(index))
            id_prod = int(selecionado.replace(" ", "").split("|")[0])
            p = Pec().get_pedidos(id_prod)
            #Produto_changer(self.master, p)


        listbox.bind("<Double-1>", change_prod)

        frame.grid(column=0, row=1, padx=30, pady=13)
        listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        adicionar = ttk.Button(self.master, text="+", width=10)
        adicionar.grid(column=0, row=1, padx=35, sticky="nw")

    def __voltar(self):
        self.__destruir()
        self.callback()

    def __destruir(self):
        for widget in self.master.winfo_children():
            widget.destroy()