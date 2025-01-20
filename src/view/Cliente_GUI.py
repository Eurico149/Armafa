import tkinter as tk
from tkinter import ttk
from src.controller.Cliente_contorller import Cliente_controller as Clc


class Cliente_GUI:

    def __init__(self, master):
        self.__master = master
        self.janela = tk.Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__config_janela()
        self.__buscar_var = tk.StringVar()
        self.__aplly_widgets()

    def __config_janela(self):
        self.janela.title("Armafa")
        self.janela.geometry("480x270")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

    def __aplly_widgets(self):
        voltar = ttk.Button(self.janela, text="Voltar")
        voltar.grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        frame1 = ttk.Frame(self.janela)
        scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, width=10)
        self.listbox = tk.Listbox(frame1, height=10, width=55, background="gray60", yscrollcommand=scrollbar.set,
                                  font=("Courier", 8))
        scrollbar.config(command=self.listbox.yview)

        frame2 = ttk.Frame(frame1)

        self.__buscar_var.trace("w", self.__atualizar_clientes)
        busca = ttk.Entry(frame2, width=53, textvariable=self.__buscar_var)
        busca.grid(column=1, row=0, sticky="nsew")

        adicionar = ttk.Button(frame2, text="+", command=self.__add_cliente)
        adicionar.grid(column=0, row=0, sticky="nsew")

        self.__atualizar_clientes()

        """def change_prod(event):
            index = self.listbox.curselection()[0]
            selecionado = self.listbox.get(index)
            id_pro = int(selecionado.replace(" ", "").split("|")[0])
            p = Prc().get_produto(id_pro)
            pc = Produto_changer(self.__master, p)
            self.__master.wait_window(pc.janela)
            self.__atualizar_produtos()

        self.listbox.bind("<Double-1>", change_prod)"""

        frame2.grid(column=0, row=0, columnspan=2)
        frame1.grid(column=0, row=1, padx=40, pady=13)
        self.listbox.grid(row=1, column=0)
        scrollbar.grid(row=1, column=1, sticky="ns")

    def __atualizar_clientes(self, *args):
        texto = self.__buscar_var.get()
        clientes = Clc().get_clientes(texto)
        lista = self.listbox.get(0, tk.END)

        veri = [str(x) for x in clientes]
        vali = True

        if len(veri) == len(lista):
            vali = False
            for j in range(len(veri)):
                if veri[j] != list(lista)[j]:
                    vali = True
                    break

        if vali:
            self.listbox.delete(0, tk.END)
            for i in clientes:
                self.listbox.insert(tk.END, str(i))

    def __add_cliente(self):
        """pa = Produto_adder(self.__master)
        self.__master.wait_window(pa.janela)
        self.__atualizar_produtos()
        while pa.valid:
            pa = Produto_adder(self.__master)
            self.__master.wait_window(pa.janela)
            self.__atualizar_produtos()"""
        pass
