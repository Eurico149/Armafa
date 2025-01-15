from src.model.Cliente import Cliente
from src.model.Cliente_repository import Cliente_repository as Cr


class Cliente_controller:

    def add_cliente(self, id_cli: int, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str):
        cliente = Cliente(id_cli, nome, cep, endereco, uf, cidade, bairro, cpf_cnpj, fone, email)
        Cr().add_cliente(cliente)

    def get_clientes(self, ref: str):
        if ref.isnumeric():
            return Cr().get_cliente(int(ref))
        return Cr().get_clientes_by_name(ref)
