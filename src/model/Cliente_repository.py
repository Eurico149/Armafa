import sqlite3 as sq
from src.model.Cliente import Cliente


class Cliente_repository:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Cliente_repository, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        self.__clientes = self.__get_clientes()

    def __get_clientes(self):
        consulta = "SELECT * FROM clientes"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            res = cur.execute(consulta)
        saida = {}
        for c in res:
            saida[int(c[0])] = Cliente(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9])
        return saida

    def get_cliente(self, id_cli):
        if id_cli in self.__clientes:
            return self.__clientes[id_cli]

    def get_clientes_by_name(self, ref: str):
        return [c for c in self.__clientes.values() if ref in c.nome]

    def add_cliente(self, c: Cliente):
        if c.id_cli in self.__clientes:
            return
        consulta = f"INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            data = (c.id_cli, c.nome, c.cep, c.endereco, c.uf, c.cidade, c.bairro, c.cpf_cnpj, c.fone, c.email)
            cur.execute(consulta, data)

        self.__clientes[c.id_cli] = Cliente(c.id_cli, c.nome, c.cep, c.endereco, c.uf, c.cidade, c.bairro, c.cpf_cnpj, c.fone, c.email)

    def del_cliente(self, id_cli):
        consulta = f"DELETE FROM clientes WHERE id_cli={id_cli}"
        with sq.connect("src/data/dataBase.db") as conn:
            cur = conn.cursor()
            cur.execute(consulta)