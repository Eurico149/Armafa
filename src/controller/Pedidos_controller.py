from datetime import datetime
import pytz

from src.model.Cliente_repository import Cliente_repository as Clr
from src.model.Pedido import Pedido
from src.model.Pedidos_repository import Pedido_repository as Pr
from src.model.PDF_creator import PDF_creator, Pdf_espelho
from src.model.Produto import Produto


class Pedidos_controller:

    # 12/02/2022
    def __validar_data(self, data: str):
        if len(data) != 10:
            return False
        if (data[2], data[5]) != ("/", "/") or data.count("/") != 2:
            return False
        d = data.split("/")
        if not (d[0].isdigit() and d[1].isdigit() and d[2].isdigit()):
            return False
        if not (12 >= int(d[1]) >= 1):
            return False
        if not (31 >= int(d[0]) >= 1):
            return False
        if not (4 == len(d[2])):
            return False
        return True

    def add_pedido(self, id_ped: int, id_cli: str, date: str, p: list[tuple[int, Produto]], desconto: int):
        aux = id_cli.replace(" ", "").split("|")[0]
        if not aux.isdigit():
            return False
        if self.__validar_data(date):
            Pr().add_pedido(Pedido(id_ped, Clr().get_cliente(int(aux)), date, p, desconto))
            return True
        return False

    def change_pedido(self, id_ped: int, id_cli: int, date: str, p: list[tuple[int, Produto]], desconto: int):
        cliente = Clr().get_cliente(id_cli)
        if len(p) == 0:
            return False
        if cliente is None:
            return False
        if not self.__validar_data(date):
            return False
        if desconto < 0:
            return False
        ped = Pedido(id_ped, cliente, date, p, desconto)
        Pr().change_pedido(ped)
        return True

    def add_pro_pre(self, id_ped, produto: tuple[int, Produto]):
        Pr().add_pro_pre(id_ped, produto)

    def del_pedido(self, id_ped: int):
        Pr().del_pedido(id_ped)

    def get_pedidos(self, ref):
        if ref.isdigit():
            saida = Pr().get_pedido_by_id(int(ref))
            if saida is None:
                return []
            return [saida]
        else:
            saida = Pr().get_pedidos_by_cliente(ref)
        return saida

    def get_pedido(self, id_ped):
        return Pr().get_pedido(id_ped)

    def get_max_id(self):
        return Pr().get_max_id() + 1

    def get_data_hoje(self):
        formato = pytz.timezone('America/Sao_Paulo')
        dt = datetime.now(formato)
        return dt.strftime("%d/%m/%Y")

    def create_pdf(self, id_ped: int):
        pedido = Pr().get_pedido(id_ped)
        nome = str(pedido.id_ped) + "-" + pedido.data.replace("/", "") + ".pdf"
        PDF_creator(nome, pedido.cliente, pedido)

    def create_espelho(self, id_ped: int):
        pedido = Pr().get_pedido(id_ped)
        nome = "espelho-" + str(pedido.id_ped) + "-" + pedido.data.replace("/", "") + ".pdf"
        Pdf_espelho(nome, pedido.cliente, pedido)
