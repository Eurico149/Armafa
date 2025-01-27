from logging import raiseExceptions

from src.model.Produto import Produto
from src.model.Produto_repository import Produto_repository as Por
from src.model.Pedidos_repository import Pedido_repository as Per

class Produto_controller:

    def get_produtos(self, ref: str):
        if ref.isnumeric():
            saida = Por().get_produto(int(ref))
            if not saida:
                return []
            return [saida]
        return Por().get_produtos_by_name(ref)

    def get_produto(self, id_pro):
        return Por().get_produto(id_pro)

    def add_produto(self, id_pro, nome, valor: str):
        if nome == "" or len(nome) > 36:
            return False
        if "," in valor:
            valor = valor.replace(",", ".")
        if valor.count(".") > 1 or (valor.count(".") == 1 and len(valor.split(".")[1]) > 2):
            return False
        try:
            Por().add_produto(Produto(int(id_pro), nome, float(valor)))
            return True
        except:
            return False

    def del_produto(self, id_pro):
        if Per().produto_in_pedidos(id_pro):
            return -1
        try:
            Por().del_produto(id_pro)
            return True
        except:
            return False

    def mudar_produto(self, id_pro, nome, valor):
        if "," in valor:
            valor = valor.replace(",", ".")
        if valor.count(".") > 1 or (valor.count(".") == 1 and len(valor.split(".")[1]) > 2):
            return False
        if nome == "":
            return False
        try:
            Por().change_produto(int(id_pro), nome, float(valor))
            return True
        except:
            return False

    def get_max_id(self):
        saida = Por().get_max_id() + 1
        return saida
