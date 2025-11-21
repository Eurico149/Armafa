from sqlalchemy import select, insert, update, delete
from src.model import Produto
from src.repository import PedidoRepository as Per
from src.repository.Singleton import SingletonMeta
from src.repository.DBConfig import DBConfig
from src.entity import get_produtos_entity, get_pedido_quantidade_produto_entity


class ProdutoRepository(metaclass=SingletonMeta):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            dbconfig = DBConfig()
            self.__engine = dbconfig.engine
            self.__produtos_table = get_produtos_entity(dbconfig.metadata)
            self.__pedido_quantidade_produto_table = get_pedido_quantidade_produto_entity(dbconfig.metadata, dbconfig.engine)
            self.__produtos = self.__get_produtos()

    def __get_produtos(self):
        with self.__engine.connect() as conn:
            stmt = select(self.__produtos_table)
            res = conn.execute(stmt)

        saida: dict[int, Produto] = {}
        for p in res:
            saida[p.id_pro] = Produto(p.id_pro, p.nome, p.valor)
        return saida

    def get_produto(self, id_pro: int):
        if id_pro in self.__produtos:
            return self.__produtos[id_pro]

    def get_produtos_by_name(self, ref: str):
        return [v for v in self.__produtos.values() if ref.lower() in v.nome.lower()]

    def add_produto(self, p:  Produto):
        with self.__engine.connect() as conn:
            data = {
                "id_pro": p.id_pro,
                "nome": p.nome,
                "valor": p.valor
            }
            stmt = insert(self.__produtos_table).values(data)

            conn.execute(stmt)
            conn.commit()

        self.__produtos[p.id_pro] = Produto(p.id_pro, p.nome, p.valor)

    def change_produto(self, id_prod: int, nome: str, valor: float):
        with self.__engine.connect() as conn:
            stmt = update(self.__produtos_table).values(nome=nome, valor=valor).where(
                self.__produtos_table.c.id_pro == id_prod
            )

            conn.execute(stmt)
            conn.commit()

        self.__produtos[id_prod] = Produto(id_prod, nome, valor)
        Per().change_name_produto(id_prod, nome)

    def del_produto(self, id_pro):
        with self.__engine.connect() as conn:
            stmt = delete(self.__produtos_table).where(
                self.__produtos_table.c.id_pro == id_pro
            )
            conn.execute(stmt)
            conn.commit()

        del self.__produtos[id_pro]

    def get_max_id(self):
        if len(self.__produtos) == 0:
            return 0
        return max(self.__produtos.keys())

    def get_produtos_pedido(self, id_ped: int):
        with self.__engine.connect() as conn:
            stmt = select(
                self.__pedido_quantidade_produto_table.c.quantidade,
                self.__pedido_quantidade_produto_table.c.id_pro,
                self.__pedido_quantidade_produto_table.c.nome,
                self.__pedido_quantidade_produto_table.c.valor_individual
            ).where(
                self.__pedido_quantidade_produto_table.c.id_ped == id_ped
            )
            res = conn.execute(stmt)
            conn.commit()
        return [(p.quantidade, Produto(p.id_pro, p.nome, p.valor_individual)) for p in res]
