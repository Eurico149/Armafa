import sqlite3 as sq
from src.model.Cliente_repository import Cliente_repository as Cr
from src.model.Pedido import Pedido
from src.model.Produto import Produto
from src.model.Singleton import SingletonMeta


class Pedido_repository(metaclass=SingletonMeta):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.__pedidos = self.__get_pedidos()

    def __get_pedidos(self):
        consulta = f"SELECT id_ped, id_cli, data, desconto FROM pedidos"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)

        pedidos = {}
        for p in res:
            pedidos[int(p[0])] = Pedido(int(p[0]), Cr().get_cliente(int(p[1])), p[2], self.__get_pedido_produtos(int(p[0])), int(p[3]))
        return pedidos

    def add_pedido(self, p: Pedido):
        consulta = f"INSERT INTO pedidos(id_ped, id_cli, data, desconto) VALUES (?, ?, ?, ?)"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = p.id_ped, p.cliente.id_cli, p.data, p.desconto
            cur.execute(consulta, data)

        self.__pedidos[p.id_ped] = Pedido(p.id_ped, p.cliente, p.data, p.produtos, p.desconto)

        for i in p.produtos:
            self.add_pro_pre(p.id_ped, i)

    def del_pedido(self, id_ped):
        if id_ped in self.__pedidos:
            consulta1 = f"DELETE FROM pedidos WHERE id_ped={id_ped}"
            consulta2 = f"DELETE FROM pro_ped WHERE id_ped={id_ped}"
            with sq.connect("src/data/dataBase.db") as conn:
                cur = conn.cursor()
                cur.execute(consulta2)
                cur.execute(consulta1)

            del self.__pedidos[id_ped]

    def produto_in_pedidos(self, id_pro: int):
        for p in self.__pedidos.values():
            if p.get_produto(id_pro):
                return True
        return False


    def change_pedido(self, p: Pedido):
        consulta1 = "UPDATE pedidos SET id_cli=?, data=?, desconto=? WHERE id_ped=?"
        consulta2 = f"DELETE FROM pro_ped WHERE id_ped={p.id_ped}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute(consulta2)
            cur.execute(consulta1, (p.cliente.id_cli, p.data, p.desconto, p.id_ped))

        data = []
        for i in range(len(p.produtos)):
            data.append((p.id_ped, p.produtos[i][1].id_pro, p.produtos[i][1].valor, p.produtos[i][0]))

        consulta = f"INSERT INTO pro_ped(id_ped, id_pro, valor_individual, quantidade) VALUES (?, ?, ?, ?)"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.executemany(consulta, data)

        self.__pedidos[p.id_ped] = Pedido(p.id_ped, p.cliente, p.data, p.produtos, p.desconto)

    def change_name_produto(self, id_pro: int, nome: str):
        for p in self.__pedidos.values():
            for i in p.produtos:
                if i[1].id_pro == id_pro:
                    i[1].nome = nome
                    break

    def add_pro_pre(self, id_ped: int, produto: tuple[int, Produto]):
        if id_ped in self.__pedidos:
            consulta = f"INSERT INTO pro_ped VALUES (?, ?, ?, ?)"
            with sq.connect("src/data/dataBase.db") as conn:
                cur = conn.cursor()
                data = (id_ped, produto[1].id_pro, produto[1].valor, produto[0])
                cur.execute(consulta, data)

    def get_pedido_by_id(self, id_ped: int):
        if id_ped in self.__pedidos:
            return self.__pedidos[id_ped]

    def __get_pedido_produtos(self, id_ped):
        consulta = f"SELECT quantidade, id_pro, nome, valor_individual FROM pedido_quantidade_produto WHERE id_ped={id_ped}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        return [(p[0], Produto(int(p[1]), p[2], float(p[3]))) for p in res]

    def get_pedido(self, id_ped: int):
        if not id_ped in self.__pedidos:
            return
        return self.__pedidos[id_ped]

    def get_pedidos_by_cliente(self, ref: str):
        return [p for p in self.__pedidos.values() if ref.lower() in p.cliente.nome.lower()]

    def get_max_id(self):
        if len(self.__pedidos) == 0:
            return 0
        return max(self.__pedidos.keys())

