from src.model.Cliente import Cliente
from src.model.Cliente_repository import Cliente_repository as Cr


class Cliente_controller:

    def add_cliente(self, id_cli: int, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str):
        if nome.replace(" ", "") == "":
            return False
        try:
            cliente = Cliente(int(id_cli), nome, cep, endereco, uf, cidade, bairro, cpf_cnpj, fone, email)
            Cr().add_cliente(cliente)
            return True
        except:
            return False

    def del_cliente(self, id_cli: int):
        Cr().del_cliente(id_cli)

    def change_cliente(self):
        pass

    def get_clientes(self, ref: str):
        if ref.isdigit():
            aux = Cr().get_cliente(int(ref))
            if aux:
                return [aux]
            return []
        return Cr().get_clientes_by_name(ref)

    def get_cliente(self, id_cli: int):
        aux = Cr().get_cliente(id_cli)
        if aux:
            return aux

    def get_max_id(self):
        return Cr().get_max_id() + 1
