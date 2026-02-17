import os

from src import SystemRoot
from src.entity.CreateDB import create
from src.view import Home

if not os.path.exists("src/data/dataBase.db"):
    create()

root = Home(SystemRoot())

root.mainloop()
