from datetime import datetime
import pytz
from src.model.Pedidos_repository import Pedido_repository as Pr
from src.model.PDF_creator import PDF_creator


class Pedidos_controller:

    def get_pedidos(self, ref):
        if ref.isnumeric():
            saida = Pr().get_pedido_by_id(int(ref))
        else:
            saida = Pr().get_pedidos_by_cliente(ref)
        return saida

    def get_pedido(self, id_ped):
        return Pr().get_pedido(id_ped)

    def get_max_id(self):
        saida = Pr().get_max_id() + 1
        return saida

    def get_data_hoje(self):
        formato = pytz.timezone('America/Sao_Paulo')
        dt = datetime.now(formato)
        return dt.strftime("%d/%m/%Y")

    def create_pdf(self, id_cli: int, id_ped: int):
        pedido = Pr().get_pedido(id_ped)
        nome = str(pedido.id_ped) + "-" + pedido.data + ".pdf"
        PDF_creator(nome, pedido.cliente, pedido)


