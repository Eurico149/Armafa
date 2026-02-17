from sqlalchemy import delete, insert, select, update

from src.entity import (
    get_pedido_quantidade_produto_entity,
    get_pedidos_entity,
    get_produtos_pedidos_entity,
)
from src.exception import ArmafaExeption
from src.model import Pedido, Produto
from src.repository import ClienteRepository
from src.repository.DBConfig import DBConfig


class PedidoRepository:
    def __init__(self, dbconfig: DBConfig, cliente_repo: ClienteRepository):
        self.__cliente_repo = cliente_repo
        self.__engine = dbconfig.engine
        self.__pedidos_table = get_pedidos_entity(dbconfig.metadata)
        self.__produtos_pedidos_table = get_produtos_pedidos_entity(dbconfig.metadata)
        self.__pedidos_quantidade_produto_table = get_pedido_quantidade_produto_entity(
            dbconfig.metadata, dbconfig.engine
        )
        self.__pedidos = self.__get_pedidos()

    def __get_pedidos(self):
        with self.__engine.connect() as conn:
            stmt = select(self.__pedidos_table)
            res = conn.execute(stmt)

        pedidos = {}
        for p in res:
            pedidos[p.id_ped] = Pedido(
                p.id_ped,
                self.__cliente_repo.get_cliente(p.id_cli),
                p.data,
                self.__get_pedido_produtos(p.id_ped),
                p.desconto,
            )
        return pedidos

    def add_pedido(self, p: Pedido):
        with self.__engine.connect() as conn:
            dados = {
                "id_ped": p.id_ped,
                "id_cli": p.cliente.id_cli,
                "data": p.data,
                "desconto": p.desconto,
            }
            stmt = insert(self.__pedidos_table).values(dados)
            conn.execute(stmt)
            conn.commit()

        self.__pedidos[p.id_ped] = Pedido(p.id_ped, p.cliente, p.data, p.produtos, p.desconto)

        for i in p.produtos:
            self.add_pro_pre(p.id_ped, i)

    def del_pedido(self, id_ped):
        if id_ped in self.__pedidos:
            with self.__engine.connect() as conn:
                stmt1 = delete(self.__pedidos_table).where(self.__pedidos_table.c.id_ped == id_ped)
                stmt2 = delete(self.__produtos_pedidos_table).where(self.__produtos_pedidos_table.c.id_ped == id_ped)
                conn.execute(stmt1)
                conn.execute(stmt2)
                conn.commit()

            del self.__pedidos[id_ped]
        else:
            raise ArmafaExeption(mensagem="Impossivel Deletar Pedido, Pedido Nao Existe")

    def produto_in_pedidos(self, id_pro: int) -> bool:
        for p in self.__pedidos.values():
            if p.get_produto(id_pro):
                return True
        return False

    def cliente_in_pedidos(self, id_cli: int) -> bool:
        for p in self.__pedidos.values():
            if p.cliente.id_cli == id_cli:
                return True
        return False

    def change_pedido(self, p: Pedido):
        data = []
        for i in range(len(p.produtos)):
            aux = {
                "id_ped": p.id_ped,
                "id_pro": p.produtos[i][1].id_pro,
                "valor_individual": p.produtos[i][1].valor,
                "quantidade": p.produtos[i][0],
            }
            data.append(aux)

        with self.__engine.connect() as conn:
            stmt1 = (
                update(self.__pedidos_table)
                .where(self.__pedidos_table.c.id_ped == p.id_ped)
                .values(id_cli=p.cliente.id_cli, data=p.data, desconto=p.desconto)
            )
            stmt2 = delete(self.__produtos_pedidos_table).where(self.__produtos_pedidos_table.c.id_ped == p.id_ped)
            stmt3 = insert(self.__produtos_pedidos_table).values(data)

            conn.execute(stmt1)
            conn.execute(stmt2)
            conn.execute(stmt3)
            conn.commit()

        self.__pedidos[p.id_ped] = Pedido(p.id_ped, p.cliente, p.data, p.produtos, p.desconto)

    def change_name_produto(self, id_pro: int, nome: str):
        for p in self.__pedidos.values():
            for i in p.produtos:
                if i[1].id_pro == id_pro:
                    i[1].nome = nome
                    break

    def add_pro_pre(self, id_ped: int, produto: tuple[int, Produto]):
        if id_ped in self.__pedidos:
            with self.__engine.connect() as conn:
                data = {
                    "id_ped": id_ped,
                    "id_pro": produto[1].id_pro,
                    "valor_individual": produto[1].valor,
                    "quantidade": produto[0],
                }
                stmt = insert(self.__produtos_pedidos_table).values(data)

                conn.execute(stmt)
                conn.commit()
        else:
            raise ArmafaExeption(mensagem="Impossivel Adicionar Produto ao Pedido, Pedido Nao Existe")

    def get_pedido_by_id(self, id_ped: int):
        if id_ped in self.__pedidos:
            return self.__pedidos[id_ped]

    def __get_pedido_produtos(self, id_ped):
        with self.__engine.connect() as conn:
            stmt = select(
                self.__pedidos_quantidade_produto_table.c.quantidade,
                self.__pedidos_quantidade_produto_table.c.id_pro,
                self.__pedidos_quantidade_produto_table.c.nome,
                self.__pedidos_quantidade_produto_table.c.valor_individual,
            ).where(self.__pedidos_quantidade_produto_table.c.id_ped == id_ped)
            res = conn.execute(stmt)
        return [(p.quantidade, Produto(p.id_pro, p.nome, p.valor_individual)) for p in res]

    def get_pedido(self, id_ped: int):
        if id_ped not in self.__pedidos:
            return
        return self.__pedidos[id_ped]

    def get_pedidos_by_cliente(self, ref: str):
        return [p for p in self.__pedidos.values() if ref.lower() in p.cliente.nome.lower()]

    def get_max_id(self):
        if len(self.__pedidos) == 0:
            return 0
        return max(self.__pedidos.keys())
