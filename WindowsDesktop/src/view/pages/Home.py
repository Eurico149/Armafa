import customtkinter as ctk
from src import SystemRoot
from src.view.components import Header, ContentFrame


class Home(ctk.CTk):

    def __init__(self, system_root: SystemRoot):
        super().__init__(fg_color="#555555")
        self.geometry("1280x720")
        self.title("Armaca")
        self.minsize(800, 450)

        self.__system_root = system_root

        self._grid_scheme_configure()

        self._add_widgets()

    def _add_widgets(self):
        self.content = ContentFrame(self, fg_color="transparent", corner_radius=0)
        self.content.grid(column=1, row=1, sticky="nsew")

        self._header = Header(self, self.__system_root, fg_color="#272727", corner_radius=0)
        self._header.grid(column=0, row=0, columnspan=2, sticky="nsew")

    def _grid_scheme_configure(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
