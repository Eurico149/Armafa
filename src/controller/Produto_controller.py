from src.model.Db import Db_produtos

class Produto_controller:

    def get_produtos(self, ref: str):
        if ref.isnumeric():
            saida = Db_produtos().get_produtos_by_id(int(ref))
        else:
            saida = Db_produtos().get_produtos_by_name(ref)
        return saida

    def get_produto(self, id_pro):
        return Db_produtos().get_produto(id_pro)

    def add_produto(self, id_pro, nome, valor: str):
        if nome == "":
            return False
        if "," in valor:
            valor = valor.replace(",", ".")
        if valor.count(".") > 1 or (valor.count(".") == 1 and len(valor.split(".")[1]) > 2):
            return False
        try:
            Db_produtos().add_produto(int(id_pro), nome, float(valor))
            return True
        except:
            return False

    def del_produto(self, id_pro):
        try:
            Db_produtos().del_produto(id_pro)
            return True
        except:
            return False

    def mudar_produto(self, id_pro, nome, valor):
        if "," in valor:
            valor = valor.replace(",", ".")
        try:
            Db_produtos().change_produto(int(id_pro), nome, float(valor))
            return True
        except:
            return False

    def get_max_id(self):
        saida = list(Db_produtos().get_max_id())[0][0]
        if saida is None:
            return 0
        return int(saida)
