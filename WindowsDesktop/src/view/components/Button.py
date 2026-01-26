import customtkinter as ctk


class Button(ctk.CTkButton):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.__hover_color = kwargs.get("hover_color")
        self.__fg_color = kwargs.get("fg_color")
        self._press = False
        self.bind("<Button-1>", self.press)

    def press(self, event=None):
        if not self._press:
            self._press = True
            self.configure(fg_color=self.__hover_color)
        else:
            self.configure(fg_color=self.__fg_color)
            self._press = False

    def is_pressed(self):
        return self._press

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Button):
            return False
        return self.cget("text") == other.cget("text") and self.cget("command") == other.cget("command")