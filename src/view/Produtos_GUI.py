import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from src.model.Db import Db


class Produtos_GUI:

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

        busca = ttk.Entry(self.master, width=54)
        busca.grid(column=0, row=1, sticky="ne", pady=5, padx=35)

        def atualizar_produtos():
            texto = busca.get()
            produtos = Db().get_produtos(ref=texto)
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

        scrollbar.config(command=listbox.yview)

        def change_prod(event):
            index = listbox.curselection()[0]
            selecionado = str(listbox.get(index))
            id_prod = int(selecionado.replace(" ", "").split("|")[0])
            p = Db().get_produto(id_prod)
            Produto_changer(self.master, p)


        listbox.bind("<Double-1>", change_prod)

        frame.grid(column=0, row=1, padx=30, pady=13)
        listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        adicionar = ttk.Button(self.master, text="+", width=10, command=lambda: self.__add_produto((listbox.get(tk.END).replace(" ", "")).split("|")[0]))
        adicionar.grid(column=0, row=1, padx=35, sticky="nw")

    def __voltar(self):
        self.__destruir()
        self.callback()

    def __destruir(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def __add_produto(self, id_pro):
        Produto_adder(self.master, id_pro)


class Produto_adder:

    def __init__(self, master, id_pro):
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__config_janela()
        self.__aplly_widgets(id_pro)

    def __config_janela(self):
        self.janela.title("Armafa")
        self.janela.geometry("300x180")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        #self.janela.iconbitmap("afghanistan.ico")

    def __aplly_widgets(self, id_pro):
        tk.Frame(self.janela, height=35, bg="gray25").grid(row=0, column=1)
        tk.Frame(self.janela, width=50, bg="gray25").grid(row=1, column=0)

        frame1 = ttk.Frame(self.janela)
        label1 = ttk.Label(frame1, text="Id: ", background="gray25", foreground="white", font=("arial", 12))
        label1.grid(row=0, column=0, sticky="nswe")
        entry1 = ttk.Entry(frame1, background="gray25", width=8)
        entry1.insert(0, str(int(id_pro)+1))
        entry1.config(state="readonly")
        entry1.grid(row=0, column=1)
        frame1.grid(row=1, column=1, sticky="w", padx=30, pady=5)

        frame2 = ttk.Frame(self.janela)
        label2 = ttk.Label(frame2, text="Nome: ", background="gray25", foreground="white", font=("arial", 12))
        label2.grid(row=0, column=0, sticky="nswe")
        entry2 = ttk.Entry(frame2, background="gray25", width=15)
        entry2.grid(row=0, column=1)
        frame2.grid(row=2, column=1, sticky="w", pady=5)

        frame3 = ttk.Frame(self.janela)
        label3 = ttk.Label(frame3, text="Valor: ", background="gray25", foreground="white", font=("arial", 12))
        label3.grid(row=0, column=0, sticky="nswe")
        entry3 = ttk.Entry(frame3, background="gray25", width=8)
        entry3.grid(row=0, column=1)
        frame3.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        adicionar = ttk.Button(self.janela, text="adicionar", command=lambda: self.__add(entry1.get(), entry2.get(), entry3.get()))
        adicionar.grid(row=4, column=2, padx=10, pady=5)

    def __add(self, e1, e2, e3):
        try:
            Db().add_produto(int(e1), e2, int(float(e3)*100))
            messagebox.showinfo("Armafa", "Produto Adicionado com Sucesso!")
        except:
            messagebox.showerror("ERROR", "Id, Nome, ou Valor Invalido")


class Produto_changer:

    def __init__(self, master, p):
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.produto = p
        self.__config_janela()
        self.__aplly_widgets()

    def __config_janela(self):
        self.janela.title("Armafa")
        self.janela.geometry("300x180")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        #self.janela.iconbitmap("afghanistan.ico")

    def __aplly_widgets(self):
        tk.Frame(self.janela, height=35, bg="gray25").grid(row=0, column=1)
        tk.Frame(self.janela, width=50, bg="gray25").grid(row=1, column=0)

        frame1 = ttk.Frame(self.janela)
        label1 = ttk.Label(frame1, text="Id: ", background="gray25", foreground="white", font=("arial", 12))
        label1.grid(row=0, column=0, sticky="nswe")
        entry1 = ttk.Entry(frame1, background="gray25", width=8)
        entry1.grid(row=0, column=1)
        entry1.insert(0, self.produto.id_pro)
        entry1.config(state="readonly")
        frame1.grid(row=1, column=1, sticky="w", padx=30, pady=5)

        frame2 = ttk.Frame(self.janela)
        label2 = ttk.Label(frame2, text="Nome: ", background="gray25", foreground="white", font=("arial", 12))
        label2.grid(row=0, column=0, sticky="nswe")
        entry2 = ttk.Entry(frame2, background="gray25", width=15)
        entry2.grid(row=0, column=1)
        entry2.insert(0, self.produto.nome)
        frame2.grid(row=2, column=1, sticky="w", pady=5)

        frame3 = ttk.Frame(self.janela)
        label3 = ttk.Label(frame3, text="Valor: ", background="gray25", foreground="white", font=("arial", 12))
        label3.grid(row=0, column=0, sticky="nswe")
        entry3 = ttk.Entry(frame3, background="gray25", width=8)
        entry3.grid(row=0, column=1)
        entry3.insert(0, self.produto.valor)
        frame3.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        aplicar = ttk.Button(self.janela, text="aplicar", command=lambda: self.__aplicar(self.produto.id_pro, entry2.get(), entry3.get()))
        aplicar.grid(row=4, column=2, padx=10, pady=5)

    def __aplicar(self, e1, e2, e3):
        try:
            Db().change_produto(int(e1), e2, float(int(e3)*100))
            messagebox.showinfo("Armafa", "Produto Atualizado com Sucesso")
        except:
            messagebox.showerror("ERROR", "Nome, ou Valor Invalido")
