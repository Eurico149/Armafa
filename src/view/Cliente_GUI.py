import tkinter as tk
from tkinter import ttk, messagebox
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
        self.janela.geometry("480x270+415+215")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

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
        self.janela.geometry("480x270+430+230")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

    def __aplly_widgets(self):
        frame1 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame1, text="Id:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry1 = ttk.Entry(frame1)
        entry1.grid(row=0, column=1, sticky="nswe")
        max_id = Clc().get_max_id()
        entry1.insert(0, "0" * (4-len(str(max_id))) + str(max_id))
        entry1.config(state="readonly")
        frame1.grid()

        frame2 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame2, text="Nome:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry2 = ttk.Entry(frame2)
        entry2.grid(row=0, column=1, sticky="nswe")
        frame2.grid()

        frame3 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame3, text="CPF/CNPJ:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry3 = ttk.Entry(frame3)
        entry3.grid(row=0, column=1, sticky="nswe")
        frame3.grid()

        frame4 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame4, text="UF:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, sticky="nswe")
        entry4 = ttk.Entry(frame4)
        entry4.grid(row=0, column=1, sticky="nswe")
        frame4.grid()

        frame5 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame5, text="Cidade:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry5 = ttk.Entry(frame5)
        entry5.grid(row=0, column=1, sticky="nswe")
        frame5.grid()

        frame6 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame6, text="CEP:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry6 = ttk.Entry(frame6)
        entry6.grid(row=0, column=1, sticky="nswe")
        frame6.grid()

        frame7 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame7, text="Bairro:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry7 = ttk.Entry(frame7)
        entry7.grid(row=0, column=1, sticky="nswe")
        frame7.grid()

        frame8 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame8, text="Endereço:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry8 = ttk.Entry(frame8)
        entry8.grid(row=0, column=1, sticky="nswe")
        frame8.grid()

        frame9 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame9, text="Fone:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry9 = ttk.Entry(frame9)
        entry9.grid(row=0, column=1, sticky="nswe")
        frame9.grid()

        frame10 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame10, text="Email:", background="gray25", foreground="white", font=("arial", 12)).grid(row=0, column=0, sticky="nswe")
        entry10 = ttk.Entry(frame10)
        entry10.grid(row=0, column=1, sticky="nswe")
        frame10.grid()

        adicionar = ttk.Button(self.janela, text="Adicionar", command=lambda: self.__add(entry1.get(), entry2.get(), entry6.get(), entry8.get(), entry4.get(), entry5.get(), entry7.get(), entry3.get(), entry9.get(), entry10.get(),))
        adicionar.grid()
        # id_cli: int, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str

    def __add(self, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10):
        if Clc().add_cliente(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10):
            messagebox.showinfo("Armafa", "Cliente Adicionado com Sucesso!", parent=self.janela)
            self.janela.destroy()
            self.valid = True
        else:
            messagebox.showerror("ERROR", "Campo Preenchido Invalido!", parent=self.janela)


