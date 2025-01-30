import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from src.controller.Cliente_contorller import Cliente_controller as Clc
from src.model.ArmafaExeption import ArmafaExeption
from src.model.Cliente import Cliente

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
        self.janela.title("Armafa - Cliente")
        self.janela.geometry("480x270+415+215")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap(get_resource_path("src/data/afghanistan.ico"))

    def __aplly_widgets(self):
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

        def change_cli(event):
            index = self.listbox.curselection()[0]
            selecionado = self.listbox.get(index)
            id_cli = int(selecionado.replace(" ", "").split("|")[0])
            c = Clc().get_cliente(id_cli)
            cc = Cliente_changer(self.__master, c)
            self.__master.wait_window(cc.janela)
            self.__atualizar_clientes()

        self.listbox.bind("<Double-1>", change_cli)

        frame2.grid(column=0, row=0, columnspan=2)
        frame1.grid(column=0, row=1, padx=45, pady=40)
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
        ca = Cliente_adder(self.__master)
        self.__master.wait_window(ca.janela)
        self.__atualizar_clientes()
        while ca.valid:
            ca = Cliente_adder(self.__master)
            self.__master.wait_window(ca.janela)
            self.__atualizar_clientes()


class Cliente_adder:

    def __init__(self, master):
        self.master = master
        self.janela = tk.Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__config_janela()
        self.valid = False
        self.__aplly_widgets()


    def __config_janela(self):
        self.janela.title("Armafa - Cliente - Adicionar")
        self.janela.geometry("480x200+430+230")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap(get_resource_path("src/data/afghanistan.ico"))

    def __aplly_widgets(self):

        tk.Frame(self.janela, background="gray25", height=20).grid(row=0, column=0)

        frame11 = tk.Frame(self.janela, bg="gray25")

        frame1 = tk.Frame(frame11, background="gray25")
        ttk.Label(frame1, text="Id:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry1 = ttk.Entry(frame1, width=4)
        entry1.grid(row=0, column=1, sticky="nswe")
        max_id = Clc().get_max_id()
        entry1.insert(0, "0" * (4-len(str(max_id))) + str(max_id))
        entry1.config(state="readonly")
        frame1.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        frame2 = tk.Frame(frame11, background="gray25")
        ttk.Label(frame2, text="Nome:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry2 = ttk.Entry(frame2, width=28)
        entry2.grid(row=0, column=1, sticky="nswe")
        frame2.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        frame3 = tk.Frame(frame11, background="gray25")
        ttk.Label(frame3, text="CPF/CNPJ:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry3 = ttk.Entry(frame3, width=15)
        entry3.grid(row=0, column=1, sticky="nswe")
        frame3.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        frame11.grid(row=1, column=0, sticky="w")

        frame12 = tk.Frame(self.janela, background="gray25")

        frame4 = tk.Frame(frame12, background="gray25")
        ttk.Label(frame4, text="UF:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, sticky="nswe")
        entry4 = ttk.Entry(frame4, width=4)
        entry4.grid(row=0, column=1, sticky="nswe")
        frame4.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        frame5 = tk.Frame(frame12, background="gray25")
        ttk.Label(frame5, text="Cidade:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry5 = ttk.Entry(frame5, width=35)
        entry5.grid(row=0, column=1, sticky="nswe")
        frame5.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        frame6 = tk.Frame(frame12, background="gray25")
        ttk.Label(frame6, text="CEP:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry6 = ttk.Entry(frame6, width=12)
        entry6.grid(row=0, column=1, sticky="nswe")
        frame6.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        frame12.grid(row=2, column=0, sticky="w")

        frame14 = tk.Frame(self.janela, background="gray25")

        frame7 = tk.Frame(frame14, background="gray25")
        ttk.Label(frame7, text="Bairro:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry7 = ttk.Entry(frame7, width=22)
        entry7.grid(row=0, column=1, sticky="nswe")
        frame7.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        frame8 = tk.Frame(frame14, background="gray25")
        ttk.Label(frame8, text="Endereço:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry8 = ttk.Entry(frame8, width=32)
        entry8.grid(row=0, column=1, sticky="nswe")
        frame8.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        frame14.grid(row=3, column=0, sticky="w")

        frame13 = tk.Frame(self.janela, bg="gray25")

        frame9 = tk.Frame(frame13, background="gray25")
        ttk.Label(frame9, text="Fone:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry9 = ttk.Entry(frame9, width=17)
        entry9.grid(row=0, column=1, sticky="nswe")
        frame9.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        frame10 = tk.Frame(frame13, background="gray25")
        ttk.Label(frame10, text="Email:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry10 = ttk.Entry(frame10, width=42)
        entry10.grid(row=0, column=1, sticky="nswe")
        frame10.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        frame13.grid(row=4, column=0, sticky="w")

        adicionar = ttk.Button(self.janela, text="Adicionar", command=lambda: self.__add(entry1.get(), entry2.get(), entry6.get(), entry8.get(), entry4.get(), entry5.get(), entry7.get(), entry3.get(), entry9.get(), entry10.get()))
        adicionar.grid(row=5, column=0, sticky="e", pady=10)
        # id_cli: int, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str

    def __add(self, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10):
        try:
            Clc().add_cliente(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10)
            messagebox.showinfo("Armafa", "Cliente Adicionado com Sucesso!", parent=self.janela)
            self.janela.destroy()
            self.valid = True
        except ArmafaExeption as aerr:
            messagebox.showerror("ERROR", str(aerr), parent=self.janela)
        except Exception:
            messagebox.showerror("ERROR", "Erro Inesperado!")


class Cliente_changer:

    def __init__(self, master, c: Cliente):
        self.master = master
        self.__cliente = c
        self.janela = tk.Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__config_janela()
        self.valid = False
        self.__aplly_widgets()


    def __config_janela(self):
        self.janela.title("Armafa - Cliente - Mudança")
        self.janela.geometry("480x200+430+230")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap(get_resource_path("src/data/afghanistan.ico"))

    def __aplly_widgets(self):

        frame11 = tk.Frame(self.janela, bg="gray25")

        frame1 = tk.Frame(frame11, background="gray25")
        ttk.Label(frame1, text="Id:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry1 = ttk.Entry(frame1, width=4)
        entry1.grid(row=0, column=1, sticky="nswe")
        id_c = "0" * (4 - len(str(self.__cliente.id_cli))) + str(self.__cliente.id_cli)
        entry1.insert(0, id_c)
        entry1.config(state="readonly")
        frame1.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        frame2 = tk.Frame(frame11, background="gray25")
        ttk.Label(frame2, text="Nome:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry2 = ttk.Entry(frame2, width=28)
        entry2.insert(0, self.__cliente.nome)
        entry2.grid(row=0, column=1, sticky="nswe")
        frame2.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        frame3 = tk.Frame(frame11, background="gray25")
        ttk.Label(frame3, text="CPF/CNPJ:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry3 = ttk.Entry(frame3, width=15)
        entry3.insert(0, self.__cliente.cpf_cnpj)
        entry3.grid(row=0, column=1, sticky="nswe")
        frame3.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        frame11.grid(row=1, column=0, sticky="w")

        frame12 = tk.Frame(self.janela, background="gray25")

        frame4 = tk.Frame(frame12, background="gray25")
        ttk.Label(frame4, text="UF:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, sticky="nswe")
        entry4 = ttk.Entry(frame4, width=4)
        entry4.insert(0, self.__cliente.uf)
        entry4.grid(row=0, column=1, sticky="nswe")
        frame4.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        frame5 = tk.Frame(frame12, background="gray25")
        ttk.Label(frame5, text="Cidade:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry5 = ttk.Entry(frame5, width=35)
        entry5.insert(0, self.__cliente.cidade)
        entry5.grid(row=0, column=1, sticky="nswe")
        frame5.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        frame6 = tk.Frame(frame12, background="gray25")
        ttk.Label(frame6, text="CEP:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry6 = ttk.Entry(frame6, width=12)
        entry6.insert(0, self.__cliente.cep)
        entry6.grid(row=0, column=1, sticky="nswe")
        frame6.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        frame12.grid(row=2, column=0, sticky="w")

        frame14 = tk.Frame(self.janela, background="gray25")

        frame7 = tk.Frame(frame14, background="gray25")
        ttk.Label(frame7, text="Bairro:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry7 = ttk.Entry(frame7, width=22)
        entry7.insert(0, self.__cliente.bairro)
        entry7.grid(row=0, column=1, sticky="nswe")
        frame7.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        frame8 = tk.Frame(frame14, background="gray25")
        ttk.Label(frame8, text="Endereço:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry8 = ttk.Entry(frame8, width=32)
        entry8.insert(0, self.__cliente.endereco)
        entry8.grid(row=0, column=1, sticky="nswe")
        frame8.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        frame14.grid(row=3, column=0, sticky="w")

        frame13 = tk.Frame(self.janela, bg="gray25")

        frame9 = tk.Frame(frame13, background="gray25")
        ttk.Label(frame9, text="Fone:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry9 = ttk.Entry(frame9, width=17)
        entry9.insert(0, self.__cliente.fone)
        entry9.grid(row=0, column=1, sticky="nswe")
        frame9.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        frame10 = tk.Frame(frame13, background="gray25")
        ttk.Label(frame10, text="Email:", background="gray25", foreground="white", font=("arial", 10)).grid(row=0, column=0, sticky="nswe")
        entry10 = ttk.Entry(frame10, width=42)
        entry10.insert(0, self.__cliente.email)
        entry10.grid(row=0, column=1, sticky="nswe")
        frame10.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        frame13.grid(row=4, column=0, sticky="w")

        deletar = ttk.Button(self.janela, text="Deletar", command=lambda: self.__delete())
        deletar.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        salvar = ttk.Button(self.janela, text="Salvar", command=lambda: self.__save(entry1.get(), entry2.get(), entry6.get(), entry8.get(), entry4.get(), entry5.get(), entry7.get(), entry3.get(), entry9.get(), entry10.get()))
        salvar.grid(row=5, column=0, sticky="e", pady=10)

    def __save(self, id_cli: str, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str):
        try:
            Clc().change_cliente(id_cli, nome, cep, endereco, uf, cidade, bairro, cpf_cnpj, fone, email)
            messagebox.showinfo("Armafa", "Cliente Modificado com Sucesso!", parent=self.janela)
            self.janela.destroy()
            self.valid = True
        except ArmafaExeption as aerr:
            messagebox.showerror("ERROR", str(aerr), parent=self.janela)
        except Exception:
            messagebox.showerror("ERROR", "Erro Inesperado!", parent=self.janela)


    def __delete(self):
        try:
            Clc().del_cliente(self.__cliente.id_cli)
            messagebox.showinfo("Armafa", "Cliente Deletado com Sucesso!", parent=self.janela)
            self.janela.destroy()
            self.valid = True
        except ArmafaExeption as aerr:
            messagebox.showerror("ERROR", str(aerr), parent=self.janela)
        except Exception:
            messagebox.showerror("ERROR", "Erro Inesperado!", parent=self.janela)





