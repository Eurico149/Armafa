import os
import sqlite3 as sq
import sys

from src.model.Produto import Produto
from src.model.Pedidos_repository import Pedido_repository as Per
from src.model.Singleton import SingletonMeta

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Produto_repository(metaclass=SingletonMeta):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.__produtos: dict = self.__get_produtos()

    def __get_produtos(self):
        consulta = f"SELECT * FROM produtos"
        with sq.connect(get_resource_path("src/data/dataBase.db")) as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        saida: dict[int, Produto] = {}
        for i in res:
            p = Produto(i[0], i[1], i[2])
            saida[p.id_pro] = p
        return saida

    def get_produto(self, id_pro: int):
        if id_pro in self.__produtos:
            return self.__produtos[id_pro]

    def get_produtos_by_name(self, ref: str):
        return [v for v in self.__produtos.values() if ref.lower() in v.nome.lower()]

    def add_produto(self, p:  Produto):
        consulta = f"INSERT INTO produtos VALUES (?, ?, ?)"
        with sq.connect(get_resource_path("src/data/dataBase.db")) as conn:
            cur = conn.cursor()
            data = (p.id_pro, p.nome, p.valor)
            cur.execute(consulta, data)

        self.__produtos[p.id_pro] = Produto(p.id_pro, p.nome, p.valor)

    def change_produto(self, id_prod: int, nome: str, valor: float):
        consulta = "UPDATE produtos SET nome=?, valor=? WHERE id_pro=?"
        with sq.connect(get_resource_path("src/data/dataBase.db")) as conn:
            cur = conn.cursor()
            cur.execute(consulta, (nome, valor, id_prod))

        self.__produtos[id_prod] = Produto(id_prod, nome, valor)
        Per().change_name_produto(id_prod, nome)

    def del_produto(self, id_pro):
        consulta = f"DELETE FROM produtos WHERE id_pro={id_pro}"
        with sq.connect(get_resource_path("src/data/dataBase.db")) as conn:
            cur = conn.cursor()
            cur.execute(consulta)

        del self.__produtos[id_pro]

    def get_max_id(self):
        if len(self.__produtos) == 0:
            return 0
        return max(self.__produtos.keys())

    def get_produtos_pedido(self, id_ped: int):
        consulta = f"SELECT quantidade, id_pro, nome, valor_individual FROM pedido_quantidade_produto WHERE id_ped={id_ped}"
        with sq.connect(get_resource_path("src/data/dataBase.db")) as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return [(int(p[0]), Produto(int(p[1]), p[2], int(p[3]))) for p in res]
