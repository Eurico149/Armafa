from src.model.Produto_repository import Produto_repository as Pr

class Produto_controller:

    def get_produtos(self, ref: str):
        if ref.isnumeric():
            saida = Pr().get_produto(int(ref))
        else:
            saida = Pr().get_produtos_by_name(ref)
        return saida

    def get_produto(self, id_pro):
        return Pr().get_produto(id_pro)[0]

    def add_produto(self, id_pro, nome, valor: str):
        if nome == "":
            return False
        if "," in valor:
            valor = valor.replace(",", ".")
        if valor.count(".") > 1 or (valor.count(".") == 1 and len(valor.split(".")[1]) > 2):
            return False
        try:
            Pr().add_produto(int(id_pro), nome, float(valor))
            return True
        except:
            return False

    def del_produto(self, id_pro):
        try:
            Pr().del_produto(id_pro)
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
            Pr().change_produto(int(id_pro), nome, float(valor))
            return True
        except:
            return False

    def get_max_id(self):
        saida = Pr().get_max_id() + 1
        return saida

    def extrair_info(self, produtos: str):
        saida = []
        for p in produtos.split("|"):
            saida.append(p.replace(" ", ""))
        return saida
