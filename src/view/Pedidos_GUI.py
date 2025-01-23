import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, StringVar

from src.controller.Cliente_contorller import Cliente_controller as Clc
from src.controller.Pedidos_controller import Pedidos_controller as Pec
from src.controller.Produto_controller import Produto_controller as Prc
from src.model.Produto import Produto
from src.model.Pedido import Pedido
from src.view.Cliente_GUI import Cliente_GUI


class Pedidos_GUI:

    def __init__(self, root: tk.Tk, funcao):
        self.__master = root
        self.__callback = funcao
        self.__destruir()
        self.__buscar_var = StringVar()
        self.__listbox = None
        self.__aplly_widgets()

    def __aplly_widgets(self):

        voltar = ttk.Button(self.__master, text="Voltar", command=self.__voltar)
        voltar.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        frame1 = ttk.Frame(self.__master)
        scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, width=10)
        self.__listbox = tk.Listbox(frame1, height=10, width=55, background="gray60", yscrollcommand=scrollbar.set, font=("Courier", 8))
        scrollbar.config(command=self.__listbox.yview)

        frame2 = ttk.Frame(frame1)

        adicionar = ttk.Button(frame2, text="+", command=self.__add_pedido)
        adicionar.grid(column=0, row=0, sticky="nsew")

        self.__buscar_var.trace("w", self.__atualizar_pedidos)
        busca = ttk.Entry(frame2, width=53, textvariable=self.__buscar_var)
        busca.grid(column=1, row=0, sticky="nsew")

        self.__atualizar_pedidos()

        def change_ped(event):
            index = self.__listbox.curselection()[0]
            selecionado = str(self.__listbox.get(index))
            id_ped = selecionado.replace(" ", "").split("|")[0]
            p = Pec().get_pedido(int(id_ped))
            aux = Pedido_changer(self.__master, p)
            self.__master.wait_window(aux.janela)
            self.__atualizar_pedidos()


        self.__listbox.bind("<Double-1>", change_ped)

        frame2.grid(column=0, row=0, columnspan=2)
        frame1.grid(column=0, row=1, padx=40, pady=13)
        self.__listbox.grid(row=1, column=0)
        scrollbar.grid(row=1, column=1, sticky="ns")

    def __atualizar_pedidos(self, *args):
        texto = self.__buscar_var.get()
        pedidos = Pec().get_pedidos(texto)
        lista = self.__listbox.get(0, tk.END)

        veri = [str(x) for x in pedidos]
        vali = True

        if len(veri) == len(lista):
            vali = False
            for j in range(len(veri)):
                if veri[j] != list(lista)[j]:
                    vali = True
                    break

        if vali:
            self.__listbox.delete(0, tk.END)
            for i in pedidos:
                self.__listbox.insert(0, str(i))

    def __add_pedido(self):
        Pedido_adder(self.__master, self.__aplly_widgets)

    def __voltar(self):
        self.__destruir()
        self.__callback()

    def __destruir(self):
        for widget in self.__master.winfo_children():
            widget.destroy()


class Pedido_adder():

    def __init__(self, master, funcao):
        self.__callback = funcao
        self.__master = master
        self.__master.geometry("592x333")
        self.__destruir()
        self.__bucar_var = StringVar()
        self.__pdf_var = tk.IntVar()
        self.__desc_var = StringVar()
        self.__total1_var = StringVar()
        self.__total2_var = StringVar()
        self.__produtos: list[tuple[int, Produto]] = []
        self.__aplly_widgets()

    def __aplly_widgets(self):

        voltar = ttk.Button(self.__master, text="Voltar", command=self.__voltar)
        voltar.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        frame1 = tk.Frame(self.__master, background="gray25")
        ttk.Label(frame1, text="Data: ", background="gray25", foreground="white", font=("Segoe UI", 12)).grid(column=0, row=0)
        entry3 = ttk.Entry(frame1, background="gray25", width=10)
        entry3.grid(row=0, column=1, sticky="w")
        entry3.insert(0, Pec().get_data_hoje())

        frame2 = tk.Frame(frame1, background="gray25")
        cb = ttk.Combobox(frame2, width=15)
        cb.config(values=Clc().get_clientes(cb.get()))
        cb.insert(0, "Cliente")
        cb.grid(row=0, column=0, sticky="nsew")
        adicionar_cliente = ttk.Button(frame2, text="...", width=3, command=lambda: Cliente_GUI(self.__master))
        adicionar_cliente.grid(row=0, column=1, sticky="nsew")
        frame2.grid(row=1, column=0, columnspan=2, pady=15)

        frame1.grid(row=1, column=1)

        aux = str(Pec().get_max_id())
        text = "0" * (4 - len(aux)) + aux
        label1 = ttk.Label(self.__master, text=f"PEDIDO Nº{text}", background="gray25", foreground="yellow", font=("Segoe UI", 14))
        label1.grid(row=0, column=1, pady=2, sticky="ne")

        frame4 = tk.Frame(self.__master)
        scrollbar1 = tk.Scrollbar(frame4, orient=tk.VERTICAL, width=10)
        listbox1 = tk.Listbox(frame4, height=7, width=55, background="gray60", yscrollcommand=scrollbar1.set, font=("Courier", 8))
        scrollbar1.config(command=listbox1.yview)

        self.__bucar_var.trace("w", lambda name, index, value: self.__atualizar_produtos(listbox1))
        busca = ttk.Entry(frame4, width=65, textvariable=self.__bucar_var)
        busca.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.__atualizar_produtos(listbox1)

        def add_prod(event):
            index = listbox1.curselection()[0]
            selecionado = listbox1.get(index)
            id_pro = int(selecionado.replace(" ", "").split("|")[0])
            produto = Prc().get_produto(id_pro)
            qg = Quantidade_getter(self.__master, produto)
            self.__master.wait_window(qg.janela)
            if not qg.valid:
                return
            quantidade = qg.quantidade
            if quantidade == 0:
                return
            for i in range(len(self.__produtos)):
                if id_pro == self.__produtos[i][1].id_pro:
                    nova_qtd = self.__produtos[i][0] + quantidade
                    self.__produtos[i] = (nova_qtd, produto)
                    listbox2.delete(i)
                    str_p = self.__format_listbox(produto, nova_qtd)
                    listbox2.insert(i, str_p)
                    self.__get_total()
                    self.__veri_desc()
                    return
            self.__produtos.append((quantidade, produto))
            str_p = self.__format_listbox(produto, quantidade)
            listbox2.insert(tk.END, str_p)
            self.__get_total()
            self.__veri_desc()

        listbox1.bind("<Double-1>", add_prod)

        frame4.grid(column=0, row=1)
        listbox1.grid(row=1, column=0, sticky="nsew")
        scrollbar1.grid(row=1, column=1, sticky="ns")

        frame5 = tk.Frame(self.__master)
        scrollbar2 = tk.Scrollbar(frame5, orient=tk.VERTICAL, width=10)
        listbox2 = tk.Listbox(frame5, height=7, width=55, background="gray60", yscrollcommand=scrollbar2.set, font=("Courier", 8))
        scrollbar1.config(command=listbox1.yview)

        def del_prod(event):
            index = listbox2.curselection()[0]
            id_pro = int(listbox2.get(index).replace(" ", "").split("|")[0])
            p = Prc().get_produto(id_pro)
            pc = Produto_changer(self.__master, (self.__produtos[index][0], p))
            self.__master.wait_window(pc.janela)
            if pc.valid is None:
                return
            if pc.valid:
                if pc.quantidade < 1:
                    return
                self.__produtos[index] = (pc.quantidade, p)
                listbox2.delete(index)
                listbox2.insert(index, self.__format_listbox(p, pc.quantidade))
            else:
                self.__produtos.pop(index)
                listbox2.delete(index)
            self.__get_total()
            self.__veri_desc()

        listbox2.bind("<Double-1>", del_prod)

        frame5.grid(column=0, row=2)
        listbox2.grid(row=0, column=0, sticky="nsew")
        scrollbar2.grid(row=0, column=1, sticky="ns")

        frame6 = tk.Frame(self.__master)
        check_pdf = tk.Checkbutton(frame6, background="gray25", variable=self.__pdf_var)
        check_pdf.select()
        check_pdf.grid(row=0, column=1, sticky="w")
        ttk.Label(frame6, background="gray25", foreground="white", text="Gerar PDF").grid(row=0, column=0, sticky="nsew")
        frame6.grid(row=2, column=1, sticky="e")

        valalidar_ent = self.__master.register(self.__validate_ent)
        self.__desc_var.trace("w", self.__veri_desc)

        frame7 = tk.Frame(self.__master, background="gray25")
        entry4 = ttk.Entry(frame7, width=12, textvariable=self.__total2_var)
        entry4.insert(0, "R$ 0,00")
        entry4.config(state="readonly")
        entry4.grid(row=0, column=0)
        entry5 = ttk.Entry(frame7, width=12, textvariable=self.__total1_var)
        entry5.insert(0, "R$ 0,00")
        entry5.config(state="readonly")
        entry5.grid(row=1, column=0)

        framedesc = tk.Frame(frame7, background="gray25")
        desc = ttk.Entry(framedesc, width=3, textvariable=self.__desc_var)
        desc.insert(0, "0")
        desc.config(validate="key", validatecommand=(valalidar_ent, "%P"))
        desc.grid(row=0, column=0, sticky="w")
        ttk.Label(framedesc, text="%", background="gray25", foreground="white").grid(row=0, column=1, sticky="w")
        framedesc.grid(row=2, column=0, sticky="w")
        frame7.grid(row=2, column=0, columnspan=2, sticky="e", padx=102)

        adicionar = ttk.Button(self.__master, text="Adicionar", command=lambda: self.__adicionar(int(text), cb.get(), entry3.get(), desc.get()))
        adicionar.grid(column=1, row=2, sticky="se", pady=10, padx=10)

    def __get_total(self):
        valor = sum([p[1].valor * p[0] for p in self.__produtos])
        valor = f"R$ {valor:.2f}".replace(".", ",")
        self.__total2_var.set(valor)

    def __veri_desc(self, *args):
        if not (self.__desc_var.get() == "" or 0 <= int(self.__desc_var.get()) <= 100):
            self.__desc_var.set("100")
        if self.__desc_var.get() != "":
            valor = float(self.__total2_var.get().replace(",", ".").split(" ")[1])
            valor = valor * ((100 - int(self.__desc_var.get())) / 100)
            valor = f"R$ {valor:.2f}".replace(".", ",")
        else:
            valor = self.__total2_var.get()
        self.__total1_var.set(valor)

    def __validate_ent(self, p):
        if p == "" or p.isdigit():
            return True
        else:
            return False

    def __format_listbox(self, produto: Produto, quantidade: int):
        str_p = " " + ((4 - len(str(produto.id_pro))) * "0" + str(produto.id_pro))
        str_p += " | " + produto.nome[0:15] + (15 - len(produto.nome)) * " "
        str_p += " | " + (4 - len(str(quantidade))) * " " + str(quantidade)
        str_p += " | " + (3 - len(str(int(produto.valor)))) * " " + f"R${produto.valor:.2f}"
        str_p += f" | R${quantidade*produto.valor:.2f}"
        return str_p

    def __atualizar_produtos(self, listbox):
        texto = self.__bucar_var.get()
        produtos = Prc().get_produtos(texto)
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

    def __adicionar(self, id_ped: int, id_cli: str, data: str, desconto):
        if len(self.__produtos) == 0:
            return messagebox.showerror("ERROR", "Impossivel salvar Pedido Sem Produtos!")
        if not desconto.isdigit():
            desconto = 0
        else:
            desconto = int(desconto)
        if not Pec().add_pedido(id_ped, id_cli, data, self.__produtos, desconto):
            return messagebox.showerror("ERROR", "Erro ao Criar Pedido")
        if self.__pdf_var.get() == 1:
            Pec().create_pdf(id_ped)
        messagebox.showinfo("Armafa", "Pedido Adicionado Com Sucesso!")
        self.__destruir()
        self.__master.geometry("480x270")
        self.__callback()

    def __voltar(self):
        self.__destruir()
        self.__master.geometry("480x270")
        self.__callback()

    def __destruir(self):
        for widget in self.__master.winfo_children():
            widget.destroy()


class Pedido_changer:

    def __init__(self, master, p: Pedido):
        self.__pedido = p
        self._master = master
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__bucar_var = StringVar()
        self.__pdf_var = tk.IntVar()
        self.__desc_var = StringVar()
        self.__total1_var = StringVar()
        self.__total2_var = StringVar()
        self.__produtos: list[tuple[int, Produto]] = p.produtos.copy()
        self.__config_janela()
        self.__aplly_widgets()

    def __config_janela(self):
        self.janela.title("Armafa - Pedido - Mudança")
        self.janela.geometry("592x333+615+215")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

    def __aplly_widgets(self):

        deletar = ttk.Button(self.janela, text="Deletar", command=self.__deletar)
        deletar.grid(row=0, column=1, sticky="sw", pady=5)

        frame1 = tk.Frame(self.janela, background="gray25")
        ttk.Label(frame1, text="Data: ", background="gray25", foreground="white", font=("Segoe UI", 12)).grid(column=0,
                                                                                                              row=0)
        entry3 = ttk.Entry(frame1, background="gray25", width=10)
        entry3.grid(row=0, column=1, sticky="w")
        entry3.insert(0, self.__pedido.data)

        frame2 = tk.Frame(frame1, background="gray25")
        cb = ttk.Combobox(frame2, width=15)
        cb.config(values=Clc().get_clientes(cb.get()))
        cb.insert(0, str(self.__pedido.cliente))
        cb.grid(row=0, column=0, sticky="nsew")
        adicionar_cliente = ttk.Button(frame2, text="...", width=3, command=lambda: Cliente_GUI(self.janela))
        adicionar_cliente.grid(row=0, column=1, sticky="nsew")
        frame2.grid(row=1, column=0, columnspan=2, pady=15)

        frame1.grid(row=1, column=2, columnspan=2, sticky="e", padx=15)

        aux = str(self.__pedido.id_ped)
        text = "0" * (4 - len(aux)) + aux
        label1 = ttk.Label(self.janela, text=f"PEDIDO Nº{text}", background="gray25", foreground="yellow",
                           font=("Segoe UI", 14))
        label1.grid(row=0, column=3, pady=2, sticky="ne", padx=2)

        tk.Frame(self.janela, width=10, background="gray25").grid(row=0, column=0)

        tk.Frame(self.janela, width=30, background="gray25").grid(row=0, column=2)

        frame4 = tk.Frame(self.janela)
        scrollbar1 = tk.Scrollbar(frame4, orient=tk.VERTICAL, width=10)
        listbox1 = tk.Listbox(frame4, height=7, width=55, background="gray60", yscrollcommand=scrollbar1.set,
                              font=("Courier", 8))
        scrollbar1.config(command=listbox1.yview)

        self.__bucar_var.trace("w", lambda name, index, value: self.__atualizar_produtos(listbox1))
        busca = ttk.Entry(frame4, width=65, textvariable=self.__bucar_var)
        busca.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.__atualizar_produtos(listbox1)

        def add_prod(event):
            index = listbox1.curselection()[0]
            selecionado = listbox1.get(index)
            id_pro = int(selecionado.replace(" ", "").split("|")[0])
            produto = Prc().get_produto(id_pro)
            qg = Quantidade_getter(self.janela, produto)
            self.janela.wait_window(qg.janela)
            if not qg.valid:
                return
            quantidade = qg.quantidade
            if quantidade == 0:
                return
            for i in range(len(self.__produtos)):
                if id_pro == self.__produtos[i][1].id_pro:
                    nova_qtd = self.__produtos[i][0] + quantidade
                    self.__produtos[i] = (nova_qtd, produto)
                    listbox2.delete(i)
                    str_p = self.__format_listbox(produto, nova_qtd)
                    listbox2.insert(i, str_p)
                    self.__get_total()
                    self.__veri_desc()
                    return
            self.__produtos.append((quantidade, produto))
            str_p = self.__format_listbox(produto, quantidade)
            listbox2.insert(tk.END, str_p)
            self.__get_total()
            self.__veri_desc()

        listbox1.bind("<Double-1>", add_prod)

        frame4.grid(column=1, row=1, pady=15)
        listbox1.grid(row=1, column=0, sticky="nsew")
        scrollbar1.grid(row=1, column=1, sticky="ns")

        frame5 = tk.Frame(self.janela)
        scrollbar2 = tk.Scrollbar(frame5, orient=tk.VERTICAL, width=10)
        listbox2 = tk.Listbox(frame5, height=7, width=55, background="gray60", yscrollcommand=scrollbar2.set,
                              font=("Courier", 8))
        scrollbar1.config(command=listbox1.yview)

        for p in self.__produtos:
            listbox2.insert(tk.END, self.__format_listbox(p[1], p[0]))

        def del_prod(event):
            index = listbox2.curselection()[0]
            id_pro = int(listbox2.get(index).replace(" ", "").split("|")[0])
            p = Prc().get_produto(id_pro)
            pc = Produto_changer(self.janela, (self.__produtos[index][0], p))
            self.janela.wait_window(pc.janela)
            if pc.valid is None:
                return
            if pc.valid:
                if pc.quantidade < 1:
                    return
                self.__produtos[index] = (pc.quantidade, p)
                listbox2.delete(index)
                listbox2.insert(index, self.__format_listbox(p, pc.quantidade))
            else:

                self.__produtos.pop(index)
                listbox2.delete(index)
            self.__get_total()
            self.__veri_desc()

        listbox2.bind("<Double-1>", del_prod)

        frame5.grid(column=1, row=2, pady=15)
        listbox2.grid(row=0, column=0, sticky="nsew")
        scrollbar2.grid(row=0, column=1, sticky="ns")

        valalidar_ent = self.janela.register(self.__validate_ent)
        self.__desc_var.trace("w", self.__veri_desc)

        frame8 = tk.Frame(self.janela, background="gray25")
        tk.Frame(frame8, width=58, height=1, background="gray25").grid(row=0, column=0)
        frame6 = tk.Frame(frame8)
        check_pdf = tk.Checkbutton(frame6, background="gray25", variable=self.__pdf_var)
        check_pdf.grid(row=0, column=1, sticky="w")
        ttk.Label(frame6, background="gray25", foreground="white", text="Gerar PDF").grid(row=0, column=0,
                                                                                          sticky="nsew")
        frame6.grid(row=0, column=1, sticky="e")
        salvar = ttk.Button(frame8, text="Salvar", command=lambda: self.__salvar(cb.get(), entry3.get(), desc.get()))
        salvar.grid(row=1, column=1, padx=10, pady=10)
        frame8.grid(row=2, column=3, sticky="se")

        frame7 = tk.Frame(self.janela, background="gray25")
        entry4 = ttk.Entry(frame7, width=12, textvariable=self.__total2_var)
        entry4.insert(0, "R$ 0,00")
        entry4.config(state="readonly")
        entry4.grid(row=0, column=0)
        entry5 = ttk.Entry(frame7, width=12, textvariable=self.__total1_var)
        entry5.insert(0, "R$ 0,00")
        entry5.config(state="readonly")
        entry5.grid(row=1, column=0)

        framedesc = tk.Frame(frame7, background="gray25")
        desc = ttk.Entry(framedesc, width=3, textvariable=self.__desc_var)
        desc.insert(0, str(self.__pedido.desconto))
        desc.config(validate="key", validatecommand=(valalidar_ent, "%P"))
        desc.grid(row=0, column=0, sticky="w")
        ttk.Label(framedesc, text="%", background="gray25", foreground="white").grid(row=0, column=1, sticky="w")
        framedesc.grid(row=2, column=0, sticky="w")
        frame7.grid(row=2, column=2, columnspan=2, sticky="w")

        self.__get_total()
        self.__veri_desc()

    def __deletar(self):
        if messagebox.askyesno("Comfimação", f"Tem Certeza que Deseja Deletar o Pedido {self.__pedido.id_ped}?", parent=self.janela):
            Pec().del_pedido(self.__pedido.id_ped)
            self.janela.destroy()


    def __get_total(self):
        valor = sum([p[1].valor * p[0] for p in self.__produtos])
        valor = f"R$ {valor:.2f}".replace(".", ",")
        self.__total2_var.set(valor)

    def __veri_desc(self, *args):
        if not (self.__desc_var.get() == "" or 0 <= int(self.__desc_var.get()) <= 100):
            self.__desc_var.set("100")
        if self.__desc_var.get() != "":
            valor = float(self.__total2_var.get().replace(",", ".").split(" ")[1])
            valor = valor * ((100 - int(self.__desc_var.get())) / 100)
            valor = f"R$ {valor:.2f}".replace(".", ",")
        else:
            valor = self.__total2_var.get()
        self.__total1_var.set(valor)

    def __validate_ent(self, p):
        if p == "" or p.isdigit():
            return True
        else:
            return False

    def __format_listbox(self, produto: Produto, quantidade: int):
        str_p = " " + ((4 - len(str(produto.id_pro))) * "0" + str(produto.id_pro))
        str_p += " | " + produto.nome[0:15] + (15 - len(produto.nome)) * " "
        str_p += " | " + (4 - len(str(quantidade))) * " " + str(quantidade)
        str_p += " | " + (3 - len(str(int(produto.valor)))) * " " + f"R${produto.valor:.2f}"
        str_p += f" | R${quantidade * produto.valor:.2f}"
        return str_p

    def __atualizar_produtos(self, listbox):
        texto = self.__bucar_var.get()
        produtos = Prc().get_produtos(texto)
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

    def __salvar(self, id_cli: str, data: str, desconto):
        if not desconto.isdigit():
            desconto = 0
        else:
            desconto = int(desconto)
        id_c = id_cli.replace(" ", "").split("|")[0]
        if id_c.isdigit():
            id_c = int(id_c)
        else:
            messagebox.showerror("ERROR", "Cliente Invalido!", parent=self.janela)
            return
        if Pec().change_pedido(self.__pedido.id_ped, id_c, data, self.__produtos, desconto):
            messagebox.showinfo("Armafa", "Pedido Modificado Com Sucesso!", parent=self.janela)
            self.janela.destroy()
        else:
            messagebox.showerror("ERROR", "Não Foi Possivel Modificar Esse pedido!", parent=self.janela)


class Quantidade_getter:

    def __init__(self, master, produto: Produto):
        self.quantidade = 0
        self.__p = produto
        self.__master = master
        self.__ent2_var = StringVar()
        self.__ent4_var = StringVar()
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__config_janela()
        self.valid = False
        self.__aplly_widgets()

    def __config_janela(self):
        self.janela.title("Armafa")
        self.janela.geometry("300x180+615+215")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

    def __aplly_widgets(self):
        tk.Frame(self.janela, height=40, bg="gray25").grid(row=0, column=1)
        tk.Frame(self.janela, width=30, bg="gray25").grid(row=1, column=0)

        frame1 = tk.Frame(self.janela)

        ttk.Label(frame1, foreground="white", text="Produto: ", font=("Segoe UI", 12), background="gray25").grid(row=0, column=0)
        entry1 = ttk.Entry(frame1)
        entry1.insert(0, self.__p.nome)
        entry1.config(state="readonly")
        entry1.grid(row=0, column=1)

        frame1.grid(row=1, column=1, sticky="w")

        frame2 = tk.Frame(self.janela, background="gray25")

        ttk.Label(frame2, foreground="white", text="Qtd.", background="gray25").grid(row=0, column=0, sticky="nsew")
        self.__ent2_var.trace("w", self.__atualiza_valor)
        valalidar_ent = self.janela.register(self.__validar_int)
        entry2 = ttk.Entry(frame2, validate="key", validatecommand=(valalidar_ent, "%P"), width=4, textvariable=self.__ent2_var)
        entry2.insert(0, "1")
        entry2.grid(row=0, column=1)


        ttk.Label(frame2, text=" X ", background="gray25", foreground="white").grid(row=0, column=2)
        entry3 = ttk.Entry(frame2, width=8)
        entry3.insert(0, f"R${self.__p.valor:.2f}")
        entry3.config(state="readonly")
        entry3.grid(row=0, column=3)

        entry4 = ttk.Entry(frame2, width=10, textvariable=self.__ent4_var)
        entry4.config(state="readonly")
        ttk.Label(frame2, text=" = ", foreground="white", background="gray25").grid(row=0, column=4)
        entry4.grid(row=0, column=5)

        frame2.grid(row=2, column=1, sticky="w", padx=40, pady=10)

        adicionar = ttk.Button(self.janela, text="Adicionar", command=self.__validate)
        adicionar.grid(row=3, column=1, pady=35, sticky="e", padx=35)

    def __validate(self):
        self.valid = True
        self.janela.destroy()

    def __atualiza_valor(self, *args):
        if not self.__ent2_var.get() == "":
            self.quantidade = int(self.__ent2_var.get())
            self.__ent4_var.set(f"R${self.quantidade * self.__p.valor:.2f}")
        else:
            self.__ent4_var.set("R$0.00")

    def __validar_int(self, P):
        if P == "" or P.isdigit():
            return True
        else:
            return False

class Produto_changer:

    def __init__(self, master, p: tuple[int, Produto]):
        self.quantidade = 0
        self.__p = p
        self.__master = master
        self.__ent2_var = StringVar()
        self.__ent4_var = StringVar()
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.grab_set()
        self.__config_janela()
        self.valid = None
        self.__aplly_widgets()

    def __config_janela(self):
        self.janela.title("Armafa")
        self.janela.geometry("300x180")
        self.janela.resizable(False, False)
        self.janela.configure(bg="gray25")
        self.janela.iconbitmap("src/data/afghanistan.ico")

    def __aplly_widgets(self):
        tk.Frame(self.janela, height=40, bg="gray25").grid(row=0, column=1)
        tk.Frame(self.janela, width=30, bg="gray25").grid(row=1, column=0)

        frame1 = tk.Frame(self.janela)

        ttk.Label(frame1, foreground="white", text="Produto: ", font=("Segoe UI", 12), background="gray25").grid(row=0, column=0)
        entry1 = ttk.Entry(frame1)
        entry1.insert(0, self.__p[1].nome)
        entry1.config(state="readonly")
        entry1.grid(row=0, column=1)

        frame1.grid(row=1, column=1, sticky="w", pady=10)

        frame2 = tk.Frame(self.janela, background="gray25")

        ttk.Label(frame2, foreground="white", text="Qtd.", background="gray25").grid(row=0, column=0, sticky="nsew")
        self.__ent2_var.trace("w", self.__atualiza_valor)
        valalidar_ent = self.janela.register(self.__validar_int)
        entry2 = ttk.Entry(frame2, validate="key", validatecommand=(valalidar_ent, "%P"), width=4, textvariable=self.__ent2_var)
        entry2.insert(0, str(self.__p[0]))
        entry2.grid(row=0, column=1)

        ttk.Label(frame2, text=" X ", background="gray25", foreground="white").grid(row=0, column=2)
        entry3 = ttk.Entry(frame2, width=8)
        entry3.insert(0, f"R${self.__p[1].valor:.2f}")
        entry3.config(state="readonly")
        entry3.grid(row=0, column=3)

        entry4 = ttk.Entry(frame2, width=10, textvariable=self.__ent4_var)
        entry4.config(state="readonly")
        ttk.Label(frame2, text=" = ", foreground="white", background="gray25").grid(row=0, column=4)
        entry4.grid(row=0, column=5)

        frame2.grid(row=2, column=1, sticky="w", padx=40)

        adicionar = ttk.Button(self.janela, text="OK", command=self.__validate)
        adicionar.grid(row=3, column=1, pady=35, sticky="e", padx=35)

        deletar = ttk.Button(self.janela, text="Deletar", command=self.__delete)
        deletar.grid(row=0, column=1, sticky="e", padx=35)

    def __validate(self):
        if self.__ent2_var.get() == "":
            self.valid = True
            self.janela.destroy()
            return
        self.quantidade = int(self.__ent2_var.get())
        self.valid = True
        self.janela.destroy()

    def __delete(self):
        aux = messagebox.askyesno("Comfirmação", f"Tem Certeza que Deseja Retirar {self.__p[1].nome} do pedido?", parent=self.janela)
        if aux:
            self.valid = False
        self.janela.destroy()

    def __atualiza_valor(self, *args):
        if not self.__ent2_var.get() == "":
            self.quantidade = int(self.__ent2_var.get())
            self.__ent4_var.set(f"R${self.quantidade * self.__p[1].valor:.2f}")
        else:
            self.__ent4_var.set("R$0.00")

    def __validar_int(self, p):
        if p == "" or p.isdigit():
            return True
        else:
            return False

