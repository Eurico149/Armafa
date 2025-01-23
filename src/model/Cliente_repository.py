import sqlite3 as sq
from src.model.Cliente import Cliente
from src.model.Singleton import SingletonMeta


class Cliente_repository(metaclass=SingletonMeta):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.__clientes = self.__get_clientes()
            print("clientes")

    def __get_clientes(self):
        consulta = "SELECT * FROM clientes"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        saida = {}
        for c in res:
            saida[c[0]] = Cliente(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9])
        return saida

    def get_cliente(self, id_cli):
        if id_cli in self.__clientes:
            return self.__clientes[id_cli]

    def get_clientes_by_name(self, ref: str):
        return [c for c in self.__clientes.values() if ref.lower() in c.nome.lower()]

    def add_cliente(self, c: Cliente):
        if c.id_cli in self.__clientes:
            return
        consulta = f"INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = (c.id_cli, c.nome, c.cep, c.endereco, c.uf, c.cidade, c.bairro, c.cpf_cnpj, c.fone, c.email)
            cur.execute(consulta, data)

        self.__clientes[c.id_cli] = Cliente(c.id_cli, c.nome, c.cep, c.endereco, c.uf, c.cidade, c.bairro, c.cpf_cnpj, c.fone, c.email)

    def del_cliente(self, id_cli: int):
        consulta = f"DELETE FROM clientes WHERE id_cli={id_cli}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute(consulta)

        del self.__clientes[id_cli]

    def change_cliente(self, c: Cliente):
        if not c.id_cli in self.__clientes:
            return
        consulta = "UPDATE clientes SET nome=?, cep=?, endereco=?, uf=?, cidade=?, bairro=?, cpf_cnpj=?, fone=?, email=? WHERE id_cli=?"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = (c.nome, c.cep, c.endereco, c.uf, c.cidade, c.bairro, c.cpf_cnpj, c.fone, c.email, c.id_cli)
            cur.execute(consulta, data)

        self.__clientes[c.id_cli] = c

    def get_max_id(self):
        if len(self.__clientes) == 0:
            return 0
        return max(self.__clientes.keys())
