import tkinter as tk
from tkinter import ttk
from Pedidos import Pedidos

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__config_app()
        self.aplly_widgets()

    def __config_app(self):
        self.master.title("Armafa")
        self.master.geometry("480x270")
        self.master.resizable(False, False)
        self.master.configure(bg="gray25")

    def aplly_widgets(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=100)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        estilo_botao_fechar = ttk.Style()
        estilo_botao_fechar.configure("Custom.TButton", background="firebrick2", foreground="black", font=("Arial", 20))

        fechar = ttk.Button(self.master, text="X", command=self.master.destroy, style="Custom.TButton")
        fechar.grid(column=1, row=0, padx=10, pady=10, sticky="e")

        botao1 = ttk.Button(self.master, text="Pedidos", command=self.press_pedidos, width=15)
        botao1.grid(column=0, row=1, pady=80, sticky="n")
        botao2 = ttk.Button(self.master, text="Produtos", width=15)
        botao2.grid(column=1, row=1, pady=80, sticky="n")

    def press_pedidos(self):
        Pedidos(self.master, self.aplly_widgets)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()
