from src.exception import ArmafaExeption
from src.model import Produto
from src.repository import PedidoRepository, ProdutoRepository


class Produto_controller:
    def __init__(self, produto_repo: ProdutoRepository, pedido_repo: PedidoRepository):
        self.__pedido_repo = pedido_repo
        self.__produto_repo = produto_repo

    def get_produtos(self, ref: str) -> list[Produto]:
        if ref.isnumeric():
            saida = self.__produto_repo.get_produto(int(ref))

            if not saida:
                return []
            return [saida]

        return self.__produto_repo.get_produtos_by_name(ref)

    def get_produto(self, id_pro) -> Produto:
        return self.__produto_repo.get_produto(id_pro)

    def add_produto(self, id_pro, nome, valor: str) -> None:
        if nome == "":
            raise ArmafaExeption("O Nome do Produto Não Foi Preenchido!")
        if len(nome) > 36:
            raise ArmafaExeption("O Nome do Produto Não deve Utrapassar 36 Caracteres!")
        if "," in valor:
            valor = valor.replace(",", ".")
        # .0, 0.0, 0., .
        if valor.count(".") > 1 or (valor.count(".") == 1 and 0 > len(valor.split(".")[1]) > 2):
            raise ArmafaExeption("Valor Invalido!")
        try:
            self.__produto_repo.add_produto(Produto(int(id_pro), nome, float(valor)))
        except Exception as err:
            raise ArmafaExeption("Erro Ao Cadastrar Produto!") from err

    def del_produto(self, id_pro) -> None:
        if self.__pedido_repo.produto_in_pedidos(id_pro):
            raise ArmafaExeption("Impossivel Deletar Produto, o Proprio Ja Esta Cadastrado em um Pedido!")
        try:
            self.__produto_repo.del_produto(id_pro)
        except Exception as err:
            raise ArmafaExeption("Erro Ao Deletar Produto!") from err

    def mudar_produto(self, id_pro, nome, valor) -> None:
        if "," in valor:
            valor = valor.replace(",", ".")
        if valor.count(".") > 1 or (valor.count(".") == 1 and len(valor.split(".")[1]) > 2):
            raise ArmafaExeption("Valor Invalido!")
        if nome == "":
            raise ArmafaExeption("O Nome do Produto Não Foi Preenchido!")
        if len(nome) > 36:
            raise ArmafaExeption("O Nome do Produto Não deve Utrapassar 36 Caracteres!")
        try:
            self.__produto_repo.change_produto(int(id_pro), nome, float(valor))
        except Exception as err:
            raise ArmafaExeption("Erro ao Mudar Pedido!") from err

    def get_max_id(self) -> int:
        saida = self.__produto_repo.get_max_id() + 1
        return saida
