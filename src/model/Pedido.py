from src.model.Cliente import Cliente
from src.model.Produto import Produto


class Pedido:
    def __init__(self, id_ped: int, cliente: Cliente, data: str, produtos: list[tuple[int, Produto]], desconto: int):
        self.id_ped = id_ped
        self.cliente = cliente
        self.produtos = produtos
        self.valor_total = sum([i[0] * i[1].valor for i in produtos])
        self.desconto = desconto
        self.data = data

    def get_produto(self, id_pro: int):
        for i in self.produtos:
            if i[1].id_pro == id_pro:
                return i[1]

    def add_produto(self, produto: tuple[int, Produto]):
        for i in range(len(self.produtos)):
            if self.produtos[i][1] == produto[1]:
                self.produtos[i] = (self.produtos[i][0] + produto[0], produto[1])
                return
        self.produtos.append(produto)
        self.valor_total += produto[0] * produto[1].valor

    def del_produto(self, id_pro: int):
        for p in range(len(self.produtos)):
            if self.produtos[p][1].id_pro == id_pro:
                self.valor_total -= self.produtos[p][0] * self.produtos[p][1].valor
                self.produtos.pop(p)
                break

    def change_quantidade_pro(self, id_pro: int, quantidade: int):
        for p in range(len(self.produtos)):
            if self.produtos[p][1].id_pro == id_pro:
                self.valor_total -= self.produtos[p][0] * self.produtos[p][1].valor
                self.produtos[p] = (quantidade, self.produtos[p][1])
                self.valor_total += self.produtos[p][0] * self.produtos[p][1].valor
                break

    def __str__(self):
        saida = " "
        saida += "0" * (4 - len(str(self.id_ped))) + str(self.id_ped) + " | "
        saida += str(self.cliente.nome) + ((22 - len(self.cliente.nome)) * " ") + "| "
        saida += self.data + " | "
        saida += "R$" + f"{((100 - self.desconto) / 100) * self.valor_total:.2f}"
        return saida

    def __eq__(self, other):
        if isinstance(other, Pedido):
            return (self.id_ped == other.id_ped) and (self.cliente == other.cliente) and (self.data == other.data)
        return False
