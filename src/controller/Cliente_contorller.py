from src.model.Cliente import Cliente
from src.model.Cliente_repository import Cliente_repository as Cr
from src.model.Pedidos_repository import Pedido_repository as Per


class Cliente_controller:

    def __strip(self, ent: str):
        saida = ent.replace(" ", "").replace(".", "").replace(",", "").replace("-", "").replace("_", "")
        saida = saida.replace("(", "").replace(")", "")
        return saida

    def add_cliente(self, id_cli: int, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str):
        cep = self.__strip(cep)
        cpf_cnpj = self.__strip(cpf_cnpj)
        fone = self.__strip(fone)
        if len(nome) > 50:
            return False
        if cep != "" and len(cep) != 8:
            return False
        if len(endereco) > 100:
            return False
        if uf != "" and len(uf) != 2:
            return False
        if len(cidade) > 40:
            return False
        if len(bairro) > 40:
            return False
        if len(email) > 80:
            return False
        if fone != "" and not (10 <= len(fone) <= 11):
            return False
        if cpf_cnpj != "" and not (len(cpf_cnpj) == 11 or len(cpf_cnpj) == 14):
            return False
        if nome.replace(" ", "") == "":
            return False
        try:
            cliente = Cliente(int(id_cli), nome, cep, endereco, uf, cidade, bairro, cpf_cnpj, fone, email)
            Cr().add_cliente(cliente)
            return True
        except:
            return False

    def del_cliente(self, id_cli: int):
        if Per().cliente_in_pedidos(id_cli):
            return -1
        try:
            Cr().del_cliente(id_cli)
            return True
        except:
            return False

    def change_cliente(self,id_cli: str, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str):
        if len(nome) > 50:
            return False
        if cep != "" and len(cep) != 8:
            return False
        if len(endereco) > 100:
            return False
        if uf != "" and len(uf) != 2:
            return False
        if len(cidade) > 40:
            return False
        if len(bairro) > 40:
            return False
        if len(email) > 80:
            return False
        if fone != "" and not (10 <= len(fone) <= 11):
            return False
        if cpf_cnpj != "" and not (len(cpf_cnpj) == 11 or len(cpf_cnpj) == 14):
            return False
        if nome.replace(" ", "") == "":
            return False
        try:
            cliente = Cliente(int(id_cli), nome, cep, endereco, uf, cidade, bairro, cpf_cnpj, fone, email)
            Cr().change_cliente(cliente)
            return True
        except:
            return False

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
