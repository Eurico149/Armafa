from src.model.Cliente import Cliente
from src.model.Cliente_repository import Cliente_repository as Cr


class Cliente_controller:

    def add_cliente(self, id_cli: int, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str):
        if len(nome) > 50:
            print("0")
            return False
        print(len(cep))
        if cep != "" and len(cep) != 8:
            print("1")
            return False
        if len(endereco) > 100:
            print("2")
            return False
        if uf != "" and len(uf) != 2:
            print("3")
            return False
        if len(cidade) > 40:
            print("4")
            return False
        if len(bairro) > 40:
            print("5")
            return False
        if len(email) > 80:
            print("6")
            return False
        if fone != "" and not (10 <= len(fone) <= 11):
            print("7")
            return False
        if cpf_cnpj != "" and not (len(cpf_cnpj) == 11 or len(cpf_cnpj) == 14):
            print("8")
            return False
        if nome.replace(" ", "") == "":
            print("9")
            return False
        try:
            cliente = Cliente(int(id_cli), nome, cep, endereco, uf, cidade, bairro, cpf_cnpj, fone, email)
            Cr().add_cliente(cliente)
            return True
        except:
            return False

    def del_cliente(self, id_cli: int):
        try:
            Cr().del_cliente(id_cli)
            return True
        except:
            return False

    def change_cliente(self,id_cli: str, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str):
        if len(nome) > 50:
            print("0")
            return False
        if cep != "" and len(cep) != 8:
            print("1")
            return False
        if len(endereco) > 100:
            print("2")
            return False
        if uf != "" and len(uf) != 2:
            print("3")
            return False
        if len(cidade) > 40:
            print("4")
            return False
        if len(bairro) > 40:
            print("5")
            return False
        if len(email) > 80:
            print("6")
            return False
        if fone != "" and not (10 <= len(fone) <= 11):
            print("7")
            return False
        if cpf_cnpj != "" and not (len(cpf_cnpj) == 11 or len(cpf_cnpj) == 14):
            print("8")
            return False
        if nome.replace(" ", "") == "":
            print("9")
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
