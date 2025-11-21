import os
import tkinter as tk
from src.view.App import App
from src.entity.CreateDB import create


if not os.path.exists("src/data/dataBase.db"):
    create()

master = tk.Tk()
root = App(master)

root.mainloop()
