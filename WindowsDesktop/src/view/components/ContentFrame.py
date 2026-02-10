from tkinter import ttk
import customtkinter as ctk
from reportlab.lib.PyFontify import fontify


# https://github.com/TomSchimansky/CustomTkinter/discussions/431
class ContentFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._search_bar = None
        self.tree = None

        self._generate_style()

        self.font = ctk.CTkFont(family="Inter", size=14)
        self._grid_scheme_configure()

    def change_content(self, data: dict[str, list[tuple[str]] | dict[str, list[dict[str, str]]]]):
        if self._search_bar is not None:
            self._search_bar.destroy()
            self._search_bar = None

        self._search_bar = ctk.CTkEntry(self,
                                        fg_color="#EFEFEF",
                                        text_color="#000000",
                                        font=self.font,
                                        corner_radius=8,
                                        border_color="#000000",
                                        border_width=1)
        self._search_bar.grid(row=0, column=0, sticky="nsew", padx=20, pady=12)

        self._create_table(data)

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

    def _generate_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=26,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=("Cascadia Mono", 9)
                        )
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",
                        background="#464a4d",
                        foreground="white",
                        relief="flat",
                        font=("Cascadia Mono", 12, "bold"))
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

    def _grid_scheme_configure(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
