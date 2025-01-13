import sqlite3 as sq
from src.model.Cliente_repository import Cliente_repository as Cr
from src.model.Pedido import Pedido
from src.model.Produto import Produto


class Pedido_repository:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Pedido_repository, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        self.__pedidos = self.__get_pedidos()

    def __get_pedidos(self):
        consulta = f"SELECT id_ped, id_cli, data FROM pedidos"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)

        pedidos = {}
        for p in res:
            pedidos[int(p[0])] = Pedido(int(p[0]), Cr().get_cliente(int(p[1])), p[2], [])
        return pedidos

    def add_pedido(self, id_ped: int, id_cli: int, date: str):
        consulta = "INSERT INTO pedido VALUES(?, ?, ?)"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = (id_ped, id_cli, date)
            cur.execute(consulta, data)

        self.__pedidos[id_ped] = Pedido(id_ped, Cr().get_cliente(id_cli), date, [])

    def get_pedido_by_id(self, id_ped: int):
        if id_ped in self.__pedidos:
            return self.__pedidos[id_ped]
        return []

    # pp.id_ped, pp.id_pro, pro.nome, pp.quantidade, pp.valor_individual
    def __get_pedido_produtos(self, id_ped):
        consulta = f"SELECT quantidade, id_pro, nome, valor_individual FROM pedido_quantidade_produto WHERE id_ped={id_ped}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return [(p[0], Produto(int(p[1]), p[2], float(p[3]))) for p in res]

    def get_pedido(self, id_ped: int):
        aux = self.__pedidos[id_ped]
        return Pedido(aux.id_ped, aux.cliente, aux.data, self.__get_pedido_produtos(id_ped))

    def get_pedidos_by_cliente(self, ref: str):
        return [p for p in self.__pedidos.values() if ref in p.cliente.nome]

    def get_max_id(self):
        if len(self.__pedidos) == 0:
            return 0
        return max(self.__pedidos.keys())

