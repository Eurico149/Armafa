from src.model.Db import Db_pedidos


class Pedidos_controller:

    def get_pedidos(self, ref: str):
        if ref.isnumeric():
            saida = Db_pedidos().get_pedidos_by_id(int(ref))
        else:
            saida = Db_pedidos().get_pedidos_by_cliente(ref)
        return saida

    def get_pedidos(self, id_ped):
        return Db_pedidos().get_pedido(id_ped)
