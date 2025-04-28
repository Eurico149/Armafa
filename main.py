import tkinter as tk
import threading
from src.model.Pedidos_repository import Pedido_repository
from src.model.Produto_repository import Produto_repository
from src.view.App import App


def inicializar_singletons():
    threads = [
        threading.Thread(target=Pedido_repository),
        threading.Thread(target=Produto_repository),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


inicializar_singletons()

master = tk.Tk()
root = App(master)

root.mainloop()
