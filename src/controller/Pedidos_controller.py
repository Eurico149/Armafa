from datetime import datetime
import pytz
from src.model.Db import Db_pedidos, Db_clientes
from src.model.PDF_creator import PDF_creator


class Pedidos_controller:

    def get_pedidos(self, ref):
        if ref.isnumeric():
            saida = Db_pedidos().get_pedidos_by_id(int(ref))
        else:
            saida = Db_pedidos().get_pedidos_by_cliente(ref)
        return saida

    def get_pedido(self, id_ped):
        return Db_pedidos().get_pedido(id_ped)

    def get_max_id(self):
        saida = list(Db_pedidos().get_max_id())[0][0]
        if saida is None:
            return 0
        return int(saida)

    def get_data_hoje(self):
        formato = pytz.timezone('America/Sao_Paulo')
        dt = datetime.now(formato)
        return dt.strftime("%d/%m/%Y")

    def create_pdf(self, id_cli: int, id_ped: int):
        pedido = Db_pedidos().get_pedido(id_ped)
        cliente = Db_clientes().get_cliente(id_cli)
        nome = str(pedido.id_ped) + "-" + pedido.data + ".pdf"
        PDF_creator(nome, cliente, pedido)


