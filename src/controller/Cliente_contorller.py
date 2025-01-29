from src.model.ArmafaExeption import ArmafaExeption
from src.model.Cliente import Cliente
from src.model.Cliente_repository import Cliente_repository as Cr
from src.model.Pedidos_repository import Pedido_repository as Per


class Cliente_controller:

    def __strip(self, ent: str) -> str:
        saida = ent.replace(" ", "").replace(".", "").replace(",", "").replace("-", "").replace("_", "")
        saida = saida.replace("(", "").replace(")", "")
        return saida

    def add_cliente(self, id_cli: int, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str) -> None:
        cep = self.__strip(cep)
        cpf_cnpj = self.__strip(cpf_cnpj)
        fone = self.__strip(fone)
        if len(nome) > 50:
            raise ArmafaExeption("Nome do Cliente Deve Ter Ate 50 Caracteres!")
        if cep != "" and len(cep) != 8:
            raise ArmafaExeption("O Cep Deve Ter 8 Numeros!")
        if len(endereco) > 100:
            raise ArmafaExeption("O Endereço Deve Ter Ate 100 Caracteres!")
        if uf != "" and len(uf) != 2:
            raise ArmafaExeption("UF Deve Ter 2 Caracteres!")
        if len(cidade) > 40:
            raise ArmafaExeption("A Cidade Deve Ter Ate 40 Caracteres!")
        if len(bairro) > 40:
            raise ArmafaExeption("O Bairro Deve Ter Ate 40 Caracteres!")
        if len(email) > 80:
            raise ArmafaExeption("O Email Deve Ter Ate 80 Caracteres")
        if fone != "" and not (10 <= len(fone) <= 11):
            raise ArmafaExeption("Fone Invalido!")
        if cpf_cnpj != "" and not (len(cpf_cnpj) == 11 or len(cpf_cnpj) == 14):
            raise ArmafaExeption("CPF/CNPJ Invalido!")
        if nome.replace(" ", "") == "":
            raise ArmafaExeption("O Nome do Cliente Deve Ser Preenchido!")
        cliente = Cliente(int(id_cli), nome, cep, endereco, uf, cidade, bairro, cpf_cnpj, fone, email)
        try:
            Cr().add_cliente(cliente)
        except:
            raise ArmafaExeption("Erro Ao Cadastrar Cliente!")

    def del_cliente(self, id_cli: int) -> None:
        if Per().cliente_in_pedidos(id_cli):
            raise ArmafaExeption("Impossive Apagar Cliente, O Mesmo Ja Esta Vincaulado a um Pedido!")
        try:
            Cr().del_cliente(id_cli)
        except:
            raise ArmafaExeption("Erro Ao Deletar Cliente!")

    def change_cliente(self,id_cli: str, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str) -> None :
        cep = self.__strip(cep)
        cpf_cnpj = self.__strip(cpf_cnpj)
        fone = self.__strip(fone)
        if len(nome) > 50:
            raise ArmafaExeption("Nome do Cliente Deve Ter Ate 50 Caracteres!")
        if cep != "" and len(cep) != 8:
            raise ArmafaExeption("O Cep Deve Ter 8 Numeros!")
        if len(endereco) > 100:
            raise ArmafaExeption("O Endereço Deve Ter Ate 100 Caracteres!")
        if uf != "" and len(uf) != 2:
            raise ArmafaExeption("UF Deve Ter 2 Caracteres!")
        if len(cidade) > 40:
            raise ArmafaExeption("A Cidade Deve Ter Ate 40 Caracteres!")
        if len(bairro) > 40:
            raise ArmafaExeption("O Bairro Deve Ter Ate 40 Caracteres!")
        if len(email) > 80:
            raise ArmafaExeption("O Email Deve Ter Ate 80 Caracteres")
        if fone != "" and not (10 <= len(fone) <= 11):
            raise ArmafaExeption("Fone Invalido!")
        if cpf_cnpj != "" and not (len(cpf_cnpj) == 11 or len(cpf_cnpj) == 14):
            raise ArmafaExeption("CPF/CNPJ Invalido!")
        if nome.replace(" ", "") == "":
            raise ArmafaExeption("O Nome do Cliente Deve Ser Preenchido!")
        cliente = Cliente(int(id_cli), nome, cep, endereco, uf, cidade, bairro, cpf_cnpj, fone, email)
        try:
            Cr().change_cliente(cliente)
        except:
            raise ArmafaExeption("Erro Ao Cadastrar Cliente!")

    def get_clientes(self, ref: str) -> list[Cliente]:
        if ref.isdigit():
            aux = Cr().get_cliente(int(ref))
            if aux:
                return [aux]
            return []
        return Cr().get_clientes_by_name(ref)

    def get_cliente(self, id_cli: int) -> Cliente:
        aux = Cr().get_cliente(id_cli)
        if aux:
            return aux

    def get_max_id(self) -> int:
        return Cr().get_max_id() + 1
