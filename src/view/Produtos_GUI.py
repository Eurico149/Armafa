import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, StringVar
from src.controller.Produto_controller import Produto_controller as Prc
from src.model.Produto import Produto


# Atualizar listbox apos produto adder
class Produtos_GUI:

    def __init__(self, root: tk.Tk, funcao):
        self.__master = root
        self.callback = funcao
        self.__destruir()
        self.__buscar_var = StringVar()
        self.listbox = None
        self.__aplly_widgets()

    def __aplly_widgets(self):

        voltar = ttk.Button(self.__master, text="Voltar", command=self.__voltar)
        voltar.grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        frame1 = ttk.Frame(self.__master)
        scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, width=10)
        self.listbox = tk.Listbox(frame1, height=10, width=55, background="gray60", yscrollcommand=scrollbar.set, font=("Courier", 8))
        scrollbar.config(command=self.listbox.yview)

        frame2 = ttk.Frame(frame1)

        self.__buscar_var.trace("w", self.__atualizar_produtos)
        busca = ttk.Entry(frame2, width=53, textvariable=self.__buscar_var)
        busca.grid(column=1, row=0, sticky="nsew")

        adicionar = ttk.Button(frame2, text="+", command=self.__add_produto)
        adicionar.grid(column=0, row=0, sticky="nsew")

        self.__atualizar_produtos()

        def change_prod(event):
            index = self.listbox.curselection()[0]
            selecionado = self.listbox.get(index)
            id_pro = int(selecionado.replace(" ", "").split("|")[0])
            p = Prc().get_produto(id_pro)
            pc = Produto_changer(self.__master, p)
            self.__master.wait_window(pc.janela)
            self.__atualizar_produtos()


        self.listbox.bind("<Double-1>", change_prod)

        frame2.grid(column=0 ,row=0, columnspan=2)
        frame1.grid(column=0, row=1, padx=40, pady=13)
        self.listbox.grid(row=1, column=0)
        scrollbar.grid(row=1, column=1, sticky="ns")

    def __atualizar_produtos(self, *args):
        texto = self.__buscar_var.get()
        produtos = Prc().get_produtos(texto)
        lista = self.listbox.get(0, tk.END)

        veri = [str(x) for x in produtos]
        vali = True

        if len(veri) == len(lista):
            vali = False
            for j in range(len(veri)):
                if veri[j] != list(lista)[j]:
                    vali = True
                    break

        if vali:
            self.listbox.delete(0, tk.END)
            for i in produtos:
                self.listbox.insert(tk.END, str(i))

    def __voltar(self):
        self.__destruir()
        self.callback()

    def __destruir(self):
        for widget in self.__master.winfo_children():
            widget.destroy()

    def __add_produto(self):
        pa = Produto_adder(self.__master)
        self.__master.wait_window(pa.janela)
        self.__atualizar_produtos()
        while pa.valid:
            pa = Produto_adder(self.__master)
            self.__master.wait_window(pa.janela)
            self.__atualizar_produtos()


class Produto_adder:

    def __init__(self, master):
        self.master = master
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__config_janela()
        self.valid = False
        self.__aplly_widgets()

    def __config_janela(self):
        self.janela.title("Armafa - Produto - Adicionar")
        self.janela.geometry("300x180+630+230")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

    def __aplly_widgets(self):
        tk.Frame(self.janela, height=35, bg="gray25").grid(row=0, column=1)
        tk.Frame(self.janela, width=50, bg="gray25").grid(row=1, column=0)

        frame1 = ttk.Frame(self.janela)
        label1 = ttk.Label(frame1, text="Id: ", background="gray25", foreground="white", font=("arial", 12))
        label1.grid(row=0, column=0, sticky="nswe")
        entry1 = ttk.Entry(frame1, background="gray25", width=4)
        max_id = str(Prc().get_max_id())
        entry1.insert(0, "0" * (4 - len(max_id)) + max_id)
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
        if Prc().add_produto(e1, e2, e3):
            messagebox.showinfo("Armafa", "Produto Adicionado com Sucesso!", parent=self.janela)
            self.janela.destroy()
            self.valid = True
        else:
            messagebox.showerror("ERROR", "Id, Nome, ou Valor Invalido", parent=self.janela)


class Produto_changer:

    def __init__(self, master, p: Produto):
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.produto = p
        self.__config_janela()
        self.__aplly_widgets()

    def __config_janela(self):
        self.janela.title("Armafa - Produto - Mudança")
        self.janela.geometry("300x180+630+230")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

    def __aplly_widgets(self):
        tk.Frame(self.janela, height=35, bg="gray25").grid(row=0, column=1)
        tk.Frame(self.janela, width=50, bg="gray25").grid(row=1, column=0)

        frame1 = ttk.Frame(self.janela)
        label1 = ttk.Label(frame1, text="Id: ", background="gray25", foreground="white", font=("arial", 12))
        label1.grid(row=0, column=0, sticky="nswe")
        entry1 = ttk.Entry(frame1, background="gray25", width=4)
        entry1.grid(row=0, column=1)
        aux = str(self.produto.id_pro)
        entry1.insert(0, "0" * (4 - len(aux)) + aux)
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
        entry3.insert(0, f"{self.produto.valor:.2f}")
        frame3.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        aplicar = ttk.Button(self.janela, text="Aplicar", command=lambda: self.__aplicar(self.produto.id_pro, entry2.get(), entry3.get()))
        aplicar.grid(row=4, column=2, padx=10, pady=5)

        deletar = ttk.Button(self.janela, text="Deletar", command=lambda: self.__deletar(self.produto.id_pro))
        deletar.grid(row=0, column=2, padx=10, pady=10)

    def __aplicar(self, e1, e2, e3):
        if Prc().mudar_produto(e1, e2, e3):
            messagebox.showinfo("Armafa", "Produto Atualizado com Sucesso", parent=self.janela)
        else:
            messagebox.showerror("ERROR", "Nome, ou Valor Invalido", parent=self.janela)

    def __deletar(self, id_pro):
        aux = Prc().del_produto(id_pro)
        if aux == -1:
            messagebox.showerror("ERROR", "Impossivel Deletar Produto, o Mesmo ja Esta Cadastrado em Outro Pedido", parent=self.janela)
        elif aux:
            messagebox.showinfo("Armafa", "Produto Deletado com Sucesso", parent=self.janela)
            self.janela.destroy()
        else:
            messagebox.showerror("ERROR", "Erro Inesperado", parent=self.janela)




