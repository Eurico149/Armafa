from datetime import datetime
import pytz
from src.model.ArmafaExeption import ArmafaExeption
from src.model.Cliente_repository import Cliente_repository as Clr
from src.model.Pedido import Pedido
from src.model.Pedidos_repository import Pedido_repository as Pr
from src.model.PDF_creator import PDF_creator, Pdf_espelho
from src.model.Produto import Produto


class Pedidos_controller:

    # 12/02/2022
    def __validar_data(self, data: str) -> bool:
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

    def add_pedido(self, id_ped: int, id_cli: str, date: str, p: list[tuple[int, Produto]], desconto: str) -> None:
        aux = id_cli.replace(" ", "").split("|")[0]
        if not aux.isdigit():
            raise ArmafaExeption("Id do Cliente Invalido!")
        cliente = Clr().get_cliente(int(aux))
        if len(p) == 0:
            raise ArmafaExeption("Um Pedido Deve Ter no Minimo 1 Produto!")
        if cliente is None:
            raise ArmafaExeption("Cliente Invalido!")
        if not self.__validar_data(date):
            raise ArmafaExeption("Data Invalida!")
        if not desconto.isdigit():
            desconto = 0
        else:
            desconto = int(desconto)
        try:
            Pr().add_pedido(Pedido(id_ped, cliente, date, p, desconto))
        except:
            raise ArmafaExeption("Erro Ao Cadastrar Pedido!")


    def change_pedido(self, id_ped: int, id_cli: str, date: str, p: list[tuple[int, Produto]], desconto: str) -> None:
        id_cli = id_cli.replace(" ", "").split("|")[0]
        if id_cli.isdigit():
            id_cli = int(id_cli)
        cliente = Clr().get_cliente(id_cli)
        if len(p) == 0:
            raise ArmafaExeption("Um Pedido Deve Ter no Minimo 1 Produto!")
        if cliente is None:
            raise ArmafaExeption("Cliente Invalido!")
        if not self.__validar_data(date):
            raise ArmafaExeption("Data Invalida!")
        if not desconto.isdigit():
            desconto = 0
        else:
            desconto = int(desconto)
        if desconto < 0:
            raise ArmafaExeption("Desconto Deve Ser Maior que Zero!")
        ped = Pedido(id_ped, cliente, date, p, desconto)
        try:
            Pr().change_pedido(ped)
        except:
            raise ArmafaExeption("Erro Ao Mudar Pedido!")

    def add_pro_pre(self, id_ped, produto: tuple[int, Produto]) -> None:
        Pr().add_pro_pre(id_ped, produto)

    def del_pedido(self, id_ped: int) -> None:
        try:
            Pr().del_pedido(id_ped)
        except:
            raise ArmafaExeption("Erro Ao Deletar Pedido!")

    def get_pedidos(self, ref) -> list[Pedido]:
        if ref.isdigit():
            saida = Pr().get_pedido_by_id(int(ref))
            if saida is None:
                return []
            return [saida]
        else:
            saida = Pr().get_pedidos_by_cliente(ref)
        return saida

    def get_pedido(self, id_ped) -> Pedido:
        return Pr().get_pedido(id_ped)

    def get_max_id(self) -> int:
        return Pr().get_max_id() + 1

    def get_data_hoje(self) -> str:
        formato = pytz.timezone('America/Sao_Paulo')
        dt = datetime.now(formato)
        return dt.strftime("%d/%m/%Y")

    def create_pdf(self, id_ped: int) -> None:
        pedido = Pr().get_pedido(id_ped)
        nome = str(pedido.id_ped) + "-" + pedido.data.replace("/", "") + ".pdf"
        PDF_creator(nome, pedido.cliente, pedido)

    def create_espelho(self, id_ped: int) -> None:
        pedido = Pr().get_pedido(id_ped)
        nome = "espelho-" + str(pedido.id_ped) + "-" + pedido.data.replace("/", "") + ".pdf"
        Pdf_espelho(nome, pedido.cliente, pedido)
