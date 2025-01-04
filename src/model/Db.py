from src.model.Produto import Produto
import sqlite3 as sq


class Db:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Db, cls).__new__(cls)
        return cls._instancia

    def get_produtos(self, ref=""):
        consulta = f"SELECT * FROM produtos WHERE nome LIKE '%{ref}%'"
        if ref.isnumeric():
            consulta = f"SELECT * FROM produtos WHERE id_pro = {int(ref)}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        produtos = []
        for i in res:
            p = Produto(i[0], i[1], i[2])
            produtos.append(p)
        return produtos

    def add_produto(self, id_pro, nome, valor):
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = (id_pro, nome, valor)
            cur.execute("INSERT INTO produtos VALUES(?, ?, ?)", data)

    def get_produto(self, id_prod):
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            resu = list(cur.execute(f"SELECT * FROM produtos WHERE id_pro={id_prod}"))[0]
        return Produto(resu[0], resu[1], resu[2])

    def change_produto(self, id_prod, nome, valor):
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute("UPDATE produtos SET nome=?, valor=? WHERE id_pro=?", (nome, valor, id_prod))

    def del_produto(self, id_pro):
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM produtos WHERE id_pro={id_pro}")



if __name__ == "__main__":
    print(Db().get_produtos())



