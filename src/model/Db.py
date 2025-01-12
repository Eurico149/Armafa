from src.model.Produto import Produto
from src.model.Pedido import Pedido
from src.model.Cliente import Cliente
import sqlite3 as sq


class Db_produtos:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Db_produtos, cls).__new__(cls)
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
        consulta = f"INSERT INTO produtos VALUES (?, ?, ?)"
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

    def get_produtos(self, id_ped: int):
        consulta = f"SELECT quantidade, id_pro, nome, valor_individual FROM pedido_quantidade_produto WHERE id_ped={id_ped}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return [(int(p[0]), Produto(int(p[1]), p[2], int(p[3]))) for p in res]

    def del_produto(self, id_pro):
        consulta = f"DELETE FROM produtos WHERE id_pro={id_pro}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute(consulta)

    def get_max_id(self):
        consulta = "SELECT max(id_pro) FROM produtos"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return res


class Db_pedidos:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Db_pedidos, cls).__new__(cls)
        return cls._instancia

    def add_pedido(self, id_ped: int, id_cli: int, data: str):
        consulta = "INSERT INTO pedido VALUES(?, ?, ?)"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = (id_ped, id_cli, data)
            cur.execute(consulta, data)

    def add_pro_pedido(self, id_ped: int, id_pro: int, valor: int, quantidade: int):
        consulta = "INSERT INTO pro_ped VALUES(?, ?, ?, ?)"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = (id_ped, id_pro, valor, quantidade)
            cur.execute(consulta, data)

    def get_pedidos_by_id(self, ref: int):
        consulta = f"SELECT id_ped, id_cli, data FROM pedidos WHERE id_ped={ref}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = list(cur.execute(consulta))
        return [Pedido(int(p[0]), Db_clientes().get_cliente(int(p[1])), p[2], []) for p in res]

    # errado: deve dar o nome do cliente e relacionar com o bd
    def get_pedidos_by_cliente(self, ref: str):
        consulta = f"SELECT id_ped, id_cli, data FROM pedidos WHERE id_cli LIKE '%{ref}%'"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return [Pedido(p[0], Db_clientes().get_cliente(p[1]), p[2], []) for p in res]

    def get_pedido(self, id_ped):
        consulta = f"SELECT id_ped, id_cli, data FROM pedidos WHERE id_ped={id_ped}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = list(cur.execute(consulta))[0]
        return Pedido(res[0], Db_clientes().get_cliente(res[1]), res[2], Db_produtos().get_produtos(id_ped))

    def get_max_id(self):
        consulta = "SELECT max(id_ped) FROM pedidos"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return res


class Db_clientes:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Db_clientes, cls).__new__(cls)
        return cls._instancia

    def get_cliente(self, id_cli):
        consulta = f"SELECT * FROM clientes WHERE id_cli={id_cli}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = list(cur.execute(consulta))[0]
        return Cliente(int(res[0]), res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9])


