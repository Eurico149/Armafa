import tkinter as tk
from tkinter import ttk
from src.view.Produtos_GUI import Produtos_GUI


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
        #self.master.iconbitmap("afghanistan.ico")

    def aplly_widgets(self):
        self.master.grid_rowconfigure(0, weight=10)
        self.master.grid_columnconfigure(0, weight=30)
        self.master.grid_rowconfigure(1, weight=30)
        self.master.grid_columnconfigure(1, weight=30)
        self.master.grid_rowconfigure(2, weight=10)

        estilo_botao_fechar = ttk.Style()
        estilo_botao_fechar.configure("Custom.TButton", foreground="black", font=("Arial", 10))

        fechar = ttk.Button(self.master, text="X", command=self.master.destroy, style="Custom.TButton", width=3)
        fechar.grid(column=1, row=0, padx=10, pady=10, sticky="ne")

        botao1 = ttk.Button(self.master, text="Pedidos", width=18)
        botao1.grid(column=0, row=1, padx=50, pady=70, sticky="nswe")

        botao2 = ttk.Button(self.master, text="Produtos", width=18, command=self.press_produtos)
        botao2.grid(column=1, row=1, padx=50, pady=70, sticky="nswe")

        frame = tk.Frame(self.master, height=30, bg="gray25")
        frame.grid(column=0, row=2)

    def press_produtos(self):
        Produtos_GUI(self.master, self.aplly_widgets)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()
