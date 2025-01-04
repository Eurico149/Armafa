from src.model.Produto import Produto
import sqlite3 as sq


class Db_pedidos:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Db_pedidos, cls).__new__(cls)
        return cls._instancia

    def get_produtos_by_id(self, ref: int):
        consulta = f"SELECT * FROM produtos WHERE id_pro={int(ref)}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return [Produto(p[0], p[1], p[2]) for p in res]

    def get_produtos_by_name(self, ref: str):
        consulta = f"SELECT * FROM produtos WHERE nome LIKE '%{ref}%'"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return [Produto(p[0], p[1], p[2]) for p in res]

    def add_produto(self, id_pro, nome, valor):
        consulta = "INSERT INTO produtos VALUES(?, ?, ?)"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = (id_pro, nome, valor)
            cur.execute(consulta, data)

    def get_produto(self, id_prod):
        consulta = f"SELECT * FROM produtos WHERE id_pro={id_prod}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = list(cur.execute(consulta))[0]
        return Produto(res[0], res[1], res[2])

    def change_produto(self, id_prod, nome, valor):
        consulta = "UPDATE produtos SET nome=?, valor=? WHERE id_pro=?"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute(consulta, (nome, valor, id_prod))

    def del_produto(self, id_pro):
        consulta = f"DELETE FROM produtos WHERE id_pro={id_pro}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute(consulta)

