import os
from src.view import Home
from src.entity.CreateDB import create


if not os.path.exists("src/data/dataBase.db"):
    create()

root = Home()

root.mainloop()
