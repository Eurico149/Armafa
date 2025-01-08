import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from src.controller.Pedidos_controller import Pedidos_controller as Pec
from src.controller.Produto_controller import Produto_controller as Prc


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
        busca.grid(column=0, row=1, sticky="ne", pady=5, padx=40)

        def atualizar_pedidos():
            texto = busca.get()
            pedidos = Pec().get_pedidos(texto)
            lista = listbox.get(0, tk.END)

            veri = [str(x) for x in pedidos]
            vali = True

            if len(veri) == len(lista):
                vali = False
                for j in range(len(veri)):
                    if veri[j] != list(lista)[j]:
                        vali = True
                        break

            if vali:
                listbox.delete(0, tk.END)
                for i in pedidos:
                    listbox.insert(tk.END, str(i))

            listbox.after(1000, atualizar_pedidos)

        atualizar_pedidos()

        def change_ped(event):
            index = listbox.curselection()[0]
            selecionado = str(listbox.get(index))
            id_ped = int(selecionado.replace(" ", "").split("|")[0])
            p = Pec().get_pedidos(id_ped)
            Pedido_changer(self.master, p)


        listbox.bind("<Double-1>", change_ped)

        frame.grid(column=0, row=1, padx=40, pady=13)
        listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        adicionar = ttk.Button(self.master, text="+", width=10, command=self.__add_pedido)
        adicionar.grid(column=0, row=1, padx=40, sticky="nw")

    def __add_pedido(self):
        Pedido_adder(self.master)

    def __voltar(self):
        self.__destruir()
        self.callback()

    def __destruir(self):
        for widget in self.master.winfo_children():
            widget.destroy()


class Pedido_adder:

    def __init__(self, master):
        self.master = master
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__config_janela()
        self.__aplly_widgets()

    def __config_janela(self):
        self.janela.title("Armafa")
        self.janela.geometry("480x270")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

    def __aplly_widgets(self):

        frame1 = ttk.Frame(self.janela)
        label1 = ttk.Label(frame1, text="Id: ", background="gray25", foreground="white", font=("arial", 12))
        label1.grid(row=0, column=0, sticky="nswe")
        entry1 = ttk.Entry(frame1, background="gray25", width=4)
        entry1.grid(row=0, column=1)
        max_id = str(Pec().get_max_id() + 1)
        entry1.insert(0, "0" * (4 - len(max_id)) + max_id)
        entry1.config(state="readonly")
        frame1.grid(row=0, column=0, padx=5, pady=10)

        frame2 = ttk.Frame(self.janela)
        label2 = ttk.Label(frame2, text="Cliente: ", background="gray25", foreground="white", font=("arial", 12))
        label2.grid(row=0, column=0, sticky="nswe")
        entry2 = ttk.Entry(frame2, background="gray25", width=20)
        entry2.grid(row=0, column=1)
        frame2.grid(row=0, column=1, padx=30, pady=10)

        frame3 = ttk.Frame(self.janela)
        label3 = ttk.Label(frame3, text="Data: ", background="gray25", foreground="white", font=("arial", 12))
        label3.grid(row=0, column=0, sticky="nswe")
        entry3 = ttk.Entry(frame3, background="gray25", width=10)
        entry3.grid(row=0, column=1)
        entry3.insert(0, Pec().get_data_hoje())
        frame3.grid(row=0, column=2, padx=35, pady=10)

        frame4 = ttk.Frame(self.janela)
        scrollbar1 = tk.Scrollbar(frame4, orient=tk.VERTICAL, width=10)
        listbox1 = tk.Listbox(frame4, height=6, width=55, background="gray60", yscrollcommand=scrollbar1.set, font=("Courier", 8))
        scrollbar1.config(command=listbox1.yview)

        busca = ttk.Entry(frame4, width=65)
        busca.grid(row=0, column=0, sticky="n", columnspan=2)

        def atualizar_produtos():
            texto = busca.get()
            produtos = Prc().get_produtos(texto)
            lista = listbox1.get(0, tk.END)

            veri = [str(x) for x in produtos]
            vali = True

            if len(veri) == len(lista):
                vali = False
                for j in range(len(veri)):
                    if veri[j] != list(lista)[j]:
                        vali = True
                        break

            if vali:
                listbox1.delete(0, tk.END)
                for i in produtos:
                    listbox1.insert(tk.END, str(i))

            listbox1.after(1000, atualizar_produtos)

        atualizar_produtos()

        def add_prod(event):
            index = listbox1.curselection()[0]
            selecionado = str(listbox1.get(index))
            id_prod = int(selecionado.replace(" ", "").split("|")[0])


        listbox1.bind("<Double-1>", add_prod)


        frame4.grid(column=0, row=1, padx=40, pady=5, columnspan=3)
        listbox1.grid(row=1, column=0, sticky="nsew")
        scrollbar1.grid(row=1, column=1, sticky="ns")



        frame5 = ttk.Frame(self.janela)
        scrollbar2 = tk.Scrollbar(frame5, orient=tk.VERTICAL, width=10)
        listbox2 = tk.Listbox(frame5, height=6, width=55, background="gray60", yscrollcommand=scrollbar2.set, font=("Courier", 8))
        scrollbar1.config(command=listbox1.yview)

        def add_prod(event):
            index = listbox2.curselection()[0]
            selecionado = str(listbox1.get(index))
            id_prod = int(selecionado.replace(" ", "").split("|")[0])

        listbox2.bind("<Double-1>", add_prod)

        frame5.grid(column=0, row=2, pady=5, columnspan=3)
        listbox2.grid(row=0, column=0, sticky="nsew")
        scrollbar2.grid(row=0, column=1, sticky="ns")

class Pedido_changer:

    def __init__(self, master, p):
        pass
