import customtkinter as ctk


class ContentFrame(ctk.CTkFrame):

    def __init__(self, master, table: list[dict[str, dict[str, str]]], **kwargs):
        super().__init__(master, **kwargs)
        self._table = None
        self._search_bar = None

        self.font = ctk.CTkFont(family="Inter", size=14)
        self._grid_scheme_configure()

        self.change_content(table)

    def change_content(self, table: list[dict[str, dict[str, str]]]):
        self._table = table

        if self._search_bar is not None:
            self._search_bar.destroy()
        self._search_bar = ctk.CTkEntry(self,
                                        fg_color="#EFEFEF",
                                        text_color="#000000",
                                        font=self.font,
                                        corner_radius=8,
                                        border_color="#000000",
                                        border_width=1)
        self._search_bar.grid(row=0, column=0, sticky="nsew", padx=20, pady=12)

        self._content_scrollable_frame = ctk.CTkScrollableFrame(self,
                                                                fg_color="transparent",
                                                                orientation=("vertical", "honizontal"))
        self._content_scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=12)

        self._create_table()

    def _create_table(self):
        pass

    def _grid_scheme_configure(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
