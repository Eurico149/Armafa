from src.model.Cliente import Cliente
from src.model.Produto import Produto


class Pedido:
    def __init__(self, id_ped: int, cliente: Cliente, data: str, produtos: list[tuple[int, Produto]]):
        self.id_ped = id_ped
        self.cliente = cliente
        self.produtos = produtos
        self.valor_total = sum([i[0] * i[1].valor for i in produtos])
        self.data = data

    def __str__(self):
        saida = " "
        saida += "0" * (4 - len(str(self.id_ped))) + str(self.id_ped) + " | "
        saida += str(self.cliente.nome) + ((25 - len(self.cliente.nome)) * " ") + "| "
        saida += self.data + " | "
        saida += "R$" + f"{self.valor_total:.2f}"
        return saida

    def __eq__(self, other):
        if isinstance(other, Pedido):
            return (self.id_ped == other.id_ped) and (self.cliente == other.cliente) and (self.data == other.data)
        return False
