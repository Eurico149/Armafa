from datetime import datetime
import pytz

from src.model.Cliente import Cliente
from src.model.Cliente_repository import Cliente_repository as Clr
from src.model.Pedido import Pedido
from src.model.Pedidos_repository import Pedido_repository as Pr
from src.model.PDF_creator import PDF_creator
from src.model.Produto import Produto


class Pedidos_controller:

    def add_pedido(self, id_ped: int, id_cli: int, date: str, p: list[tuple[int, Produto]]):
        cliente = Cliente(
            id_cli=1,
            nome="João Silva",
            cep="12345-678",
            endereco="Rua A, 123",
            uf="SP",
            cidade="São Paulo",
            bairro="Centro",
            cpf_cnpj="123.456.789-00",
            fone="11-98765-4321",
            email="joao@exemplo.com"
        )
        Clr().add_cliente(cliente)
        Pr().add_pedido(Pedido(id_ped, cliente, date, p))

    def add_pro_pre(self, id_ped, produto: tuple[int, Produto]):
        Pr().add_pro_pre(id_ped, produto)

    def get_pro_pre(self, id_ped: int):
        return Pr().get_pedido(id_ped).produtos

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

    def create_pdf(self, id_ped: int):
        pedido = Pr().get_pedido(id_ped)
        nome = str(pedido.id_ped) + "-" + pedido.data + ".pdf"
        PDF_creator(nome, pedido.cliente, pedido)


