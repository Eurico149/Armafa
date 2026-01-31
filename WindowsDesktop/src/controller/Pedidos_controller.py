import pytz
from datetime import datetime
from src.exception import ArmafaExeption
from src.repository import ClienteRepository, PedidoRepository
from src.model import Pedido
from src.model import PDF_creator, Pdf_espelho
from src.model import Produto


class Pedidos_controller:

    def __init__(self, pedido_repo: PedidoRepository, cliente_repo: ClienteRepository):
        self.__pedido_repo = pedido_repo
        self.__cliente_repo = cliente_repo

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
        cliente = self.__cliente_repo.get_cliente(int(aux))
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
            self.__pedido_repo.add_pedido(Pedido(id_ped, cliente, date, p, desconto))
        except Exception as err:
            raise ArmafaExeption("Erro Ao Cadastrar Pedido!")


    def change_pedido(self, id_ped: int, id_cli: str, date: str, p: list[tuple[int, Produto]], desconto: str) -> None:
        id_cli = id_cli.replace(" ", "").split("|")[0]
        if id_cli.isdigit():
            id_cli = int(id_cli)
        cliente = self.__cliente_repo.get_cliente(id_cli)
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
            self.__pedido_repo.change_pedido(ped)
        except:
            raise ArmafaExeption("Erro Ao Mudar Pedido!")

    def add_pro_pre(self, id_ped, produto: tuple[int, Produto]) -> None:
        self.__pedido_repo.add_pro_pre(id_ped, produto)

    def del_pedido(self, id_ped: int) -> None:
        try:
            self.__pedido_repo.del_pedido(id_ped)
        except:
            raise ArmafaExeption("Erro Ao Deletar Pedido!")

    def get_pedidos(self, ref: str = "") -> list[Pedido]:
        if ref.isdigit():
            saida = self.__pedido_repo.get_pedido_by_id(int(ref))
            if saida is None:
                return []
            return [saida]
        else:
            saida = self.__pedido_repo.get_pedidos_by_cliente(ref)
        return saida

    def get_pedido(self, id_ped) -> Pedido:
        return self.__pedido_repo.get_pedido(id_ped)

    def get_max_id(self) -> int:
        return self.__pedido_repo.get_max_id() + 1

    def get_data_hoje(self) -> str:
        formato = pytz.timezone('America/Sao_Paulo')
        dt = datetime.now(formato)
        return dt.strftime("%d/%m/%Y")

    def create_pdf(self, id_ped: int) -> None:
        pedido = self.__pedido_repo.get_pedido(id_ped)
        nome = str(pedido.id_ped) + "-" + pedido.data.replace("/", "") + ".pdf"
        PDF_creator(nome, pedido.cliente, pedido)

    def create_espelho(self, id_ped: int) -> None:
        pedido = self.__pedido_repo.get_pedido(id_ped)
        nome = "espelho-" + str(pedido.id_ped) + "-" + pedido.data.replace("/", "") + ".pdf"
        Pdf_espelho(nome, pedido.cliente, pedido)
