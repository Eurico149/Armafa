import customtkinter as ctk
from PIL import Image
from src import SystemRoot
from src.model import Produto, Cliente, Pedido
from src.view.components.Button import Button
from src.view.utils import convert_to_table_content


class Header(ctk.CTkFrame):

    def __init__(self, master, systemroot: SystemRoot, **kwargs):
        super().__init__(master, **kwargs)
        self.menu_button_is_active = False
        self.__menu_frame = MenuSideBar(self.master,
                                        systemroot,
                                        fg_color="#272727",
                                        corner_radius=0)
        self.__menu_frame.buttons["Pedidos"].invoke()
        self.__menu_frame.buttons["Pedidos"].press()

        self._menu_icon = ctk.CTkImage(Image.open("src/view/images/menu_icon.png"), size=(25,25))
        self._settings_icon = ctk.CTkImage(Image.open("src/view/images/settings_icon.png"), size=(25,25))

        self._grid_scheme_configure()

        self._add_widgets()

    def _add_widgets(self):
        self._menu = ctk.CTkButton(self,
                                   command=self._menu_button_action,
                                   image=self._menu_icon,
                                   text="",
                                   fg_color="transparent",
                                   hover_color="#363636",
                                   width=0,
                                   height=0)
        self._menu.grid(row=0, column=0, sticky="e", padx=5, pady=4)

        self._settings = ctk.CTkButton(self,
                                       image=self._settings_icon,
                                       text="",
                                       fg_color="transparent",
                                       hover_color="#363636",
                                       width=0,
                                       height=0)
        self._settings.grid(row=0, column=2, sticky="w", padx=5, pady=4)

        self._menu_button_action()

    def _menu_button_action(self):
        if self.menu_button_is_active:
            self.__menu_frame.grid_remove()
            self.menu_button_is_active = False
        else:
            self.__menu_sidebar()
            self.menu_button_is_active = True


    def __menu_sidebar(self):
        self.__menu_frame.grid(row=1, column=0, sticky="nsew")

    def _grid_scheme_configure(self):
        self.grid_columnconfigure(1, weight=1)


class MenuSideBar(ctk.CTkFrame):

    def __init__(self, master, systemroot: SystemRoot, **kwargs):
        super().__init__(master, **kwargs)
        self.__systemroot = systemroot
        self.buttons = {}

        self.font =ctk.CTkFont(family="Inter", size=14)

        self._add_widgets()

    def _add_widgets(self):

        pedidos_button = Button(self,
                                text="Pedidos",
                                fg_color="transparent",
                                hover_color="#20446C",
                                font=self.font,
                                border_spacing=6,
                                command=lambda: self.__orders_button_action(self.__systemroot.pedidos_controller.get_pedidos("")))
        pedidos_button.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.buttons[pedidos_button.cget("text")] = pedidos_button

        products_button = Button(self,
                                 text="Produtos",
                                 fg_color="transparent",
                                 hover_color="#20446C",
                                 font=self.font,
                                 border_spacing=6,
                                 command=lambda: self.__products_button_action(self.__systemroot.produtos_controller.get_produtos("")))
        products_button.grid(row=1, column=0, padx=10, pady=8)
        self.buttons[products_button.cget("text")] = products_button

        clients_button = Button(self,
                                text="Clientes",
                                fg_color="transparent",
                                hover_color="#20446C",
                                font=self.font,
                                border_spacing=6,
                                command=lambda: self.__clients_button_action(self.__systemroot.cliente_controller.get_clientes("")))
        clients_button.grid(row=2, column=0, padx=10)
        self.buttons[clients_button.cget("text")] = clients_button

    def __orders_button_action(self, data: list[Pedido]):
        content = convert_to_table_content(data_type="Pedidos", data=data)

        self.master.content.change_content(content)
        for button in self.buttons.values():
            if button.cget("command") != self.__orders_button_action:
                if button.is_pressed():
                    button.press()


    def __products_button_action(self, data: list[Produto]):
        content = convert_to_table_content(data_type="Produtos", data=data)

        self.master.content.change_content(content)
        for button in self.buttons.values():
            if button.cget("command") != self.__products_button_action:
                if button.is_pressed():
                    button.press()

    def __clients_button_action(self, data: list[Cliente]):
        content = convert_to_table_content(data_type="Clientes", data=data)

        self.master.content.change_content(content)
        for button in self.buttons.values():
            if button.cget("command") != self.__clients_button_action:
                if button.is_pressed():
                    button.press()

