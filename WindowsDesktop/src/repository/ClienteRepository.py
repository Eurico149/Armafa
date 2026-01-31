from sqlalchemy import delete, select, insert, update
from src.model import Cliente
from src.repository.DBConfig import DBConfig
from src.entity import get_clientes_entity


class ClienteRepository:

    def __init__(self, dbconfig: DBConfig):
        self.__clientes_table = get_clientes_entity(dbconfig.metadata)
        self.__engine = dbconfig.engine
        self.__clientes = self.__get_clientes()

    def __get_clientes(self):
        with self.__engine.connect() as conn:
            stmt = select(self.__clientes_table)
            res = conn.execute(stmt)
        clientes = {row.id_cli: Cliente(**row._mapping) for row in res}
        return clientes

    def get_cliente(self, id_cli):
        if id_cli in self.__clientes:
            return self.__clientes[id_cli]

    def get_clientes_by_name(self, ref: str):
        return [c for c in self.__clientes.values() if ref.lower() in c.nome.lower()]

    def add_cliente(self, c: Cliente):
        if c.id_cli in self.__clientes:
            return
        with self.__engine.connect() as conn:
            dados = {col: getattr(c, col) for col in self.__clientes_table.c.keys()}
            stmt = insert(self.__clientes_table).values(dados)
            conn.execute(stmt)
            conn.commit()
        self.__clientes[c.id_cli] = Cliente(c.id_cli, c.nome, c.cep, c.endereco, c.uf, c.cidade, c.bairro, c.cpf_cnpj, c.fone, c.email)

    def del_cliente(self, id_cli: int):
        with self.__engine.connect() as conn:
            stmt = delete(self.__clientes_table).where(
                self.__clientes_table.c.id_cli == id_cli
            )
            conn.execute(stmt)
            conn.commit()
        del self.__clientes[id_cli]

    def change_cliente(self, c: Cliente):
        if c.id_cli in self.__clientes:
            with self.__engine.connect() as conn:
                dados = {col: getattr(c, col) for col in self.__clientes_table.c.keys()}
                stmt = update(self.__clientes_table).where(
                    self.__clientes_table.c.id_cli == c.id_cli
                ).values(dados)
                conn.execute(stmt)
                conn.commit()
            self.__clientes[c.id_cli] = c

    def get_max_id(self):
        if len(self.__clientes) == 0:
            return 0
        return max(self.__clientes.keys())
