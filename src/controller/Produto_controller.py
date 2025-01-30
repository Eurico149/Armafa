from src.model.ArmafaExeption import ArmafaExeption
from src.model.Produto import Produto
from src.model.Produto_repository import Produto_repository as Por
from src.model.Pedidos_repository import Pedido_repository as Per

class Produto_controller:

    def get_produtos(self, ref: str) -> list[Produto]:
        if ref.isnumeric():
            saida = Por().get_produto(int(ref))
            if not saida:
                return []
            return [saida]
        return Por().get_produtos_by_name(ref)

    def get_produto(self, id_pro) -> Produto:
        return Por().get_produto(id_pro)

    def add_produto(self, id_pro, nome, valor: str) -> None:
        if nome == "":
            raise ArmafaExeption("O Nome do Produto Não Foi Preenchido!")
        if len(nome) > 36:
            raise ArmafaExeption("O Nome do Produto Não deve Utrapassar 36 Caracteres!")
        if "," in valor:
            valor = valor.replace(",", ".")
        # .0, 0.0, 0., .
        if valor.count(".") > 1 or (valor.count(".") == 1 and 0 > len(valor.split(".")[1]) > 2):
            raise ArmafaExeption("Valor Invalido!")
        try:
            Por().add_produto(Produto(int(id_pro), nome, float(valor)))
        except:
            raise ArmafaExeption("Erro Ao Cadastrar Produto!")

    def del_produto(self, id_pro) -> None:
        if Per().produto_in_pedidos(id_pro):
            raise ArmafaExeption("Impossivel Deletar Produto, o Proprio Ja Esta Cadastrado em um Pedido!")
        try:
            Por().del_produto(id_pro)
        except:
            raise ArmafaExeption("Erro Ao Deletar Produto!")

    def mudar_produto(self, id_pro, nome, valor) -> None:
        if "," in valor:
            valor = valor.replace(",", ".")
        if valor.count(".") > 1 or (valor.count(".") == 1 and len(valor.split(".")[1]) > 2):
            raise ArmafaExeption("Valor Invalido!")
        if nome == "":
            raise ArmafaExeption("O Nome do Produto Não Foi Preenchido!")
        if len(nome) > 36:
            raise("O Nome do Produto Não deve Utrapassar 36 Caracteres!")
        try:
            Por().change_produto(int(id_pro), nome, float(valor))
        except:
            raise ArmafaExeption("Erro ao Mudar Pedido!")

    def get_max_id(self) -> int:
        saida = Por().get_max_id() + 1
        return saida
