from tkinter import ttk

import customtkinter as ctk

from src import SystemRoot
from src.view.utils import convert_to_table_content


class ContentFrame(ctk.CTkFrame):
    tree = None
    _search_bar = None
    _search_var = None
    __active_table = None

    def __init__(self, master, system_root: SystemRoot, **kwargs):
        super().__init__(master, **kwargs)
        self.__system_root = system_root

        self._generate_style()

        self.font = ctk.CTkFont(family="Inter", size=14)
        self._grid_scheme_configure()

    def change_content(self, data: dict[str, list[tuple[str]] | dict[str, list[dict[str, str]]]]):
        if self._search_bar is not None:
            self._search_bar.destroy()
            self._search_bar = None

        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", self._on_search_change)

        self._search_bar = ctk.CTkEntry(
            self,
            fg_color="#EFEFEF",
            text_color="#000000",
            font=self.font,
            corner_radius=8,
            border_color="#000000",
            border_width=1,
            textvariable=self._search_var,
        )
        self._search_bar.grid(row=0, column=0, sticky="nsew", padx=20, pady=12)

        self._create_table(data)
        self.__active_table = data["meta"]["table_title"]

    def _create_table(self, data: dict[str, list[tuple[str]] | dict[str, list[dict[str, str]]]]):
        if self.tree is not None:
            self.tree.destroy()
            self.tree = None

        heading = data["meta"]["columns"]
        self.tree = ttk.Treeview(
            self,
            columns=[h["name"] for h in heading],
            show="headings",
        )

        for h in heading:
            if h["width"] == "auto":
                self.tree.column(h["name"], anchor=h["location"], stretch=True)
                self.tree.heading(h["name"], text=h["name"], anchor=h["location"])
            else:
                self.tree.column(h["name"], anchor=h["location"], width=int(h["width"]), stretch=False)
                self.tree.heading(h["name"], text=h["name"], anchor="center")

        for i in data["data"]:
            self.tree.insert("", "end", values=tuple(i))
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def _on_search_change(self, *args):
        texto = self._search_var.get()

        content = {}
        match self.__active_table:
            case "Pedidos":
                data = self.__system_root.pedidos_controller.get_pedidos(texto)
                content = convert_to_table_content(data_type=self.__active_table, data=data)

            case "Produtos":
                data = self.__system_root.produtos_controller.get_produtos(texto)
                content = convert_to_table_content(data_type=self.__active_table, data=data)

            case "Clientes":
                data = self.__system_root.cliente_controller.get_clientes(texto)
                content = convert_to_table_content(data_type=self.__active_table, data=data)

        self._create_table(content)

    def _generate_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=26,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
            font=("Cascadia Mono", 9),
        )
        style.map("Treeview", background=[("selected", "#22559b")])
        style.configure(
            "Treeview.Heading",
            background="#464a4d",
            foreground="white",
            relief="flat",
            font=("Cascadia Mono", 12, "bold"),
        )
        style.map("Treeview.Heading", background=[("active", "#3484F0")])

    def _grid_scheme_configure(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
