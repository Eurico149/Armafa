class Pedido:
    def __init__(self, id_ped: int, cliente: str, valor_total: int, data: str):
        self.id_ped = id_ped
        self.cliente = cliente
        self.valor_total = valor_total
        self.data = data

    def __str__(self):
        saida = " "
        saida += "0" * (4 - len(str(self.id_ped))) + str(self.id_ped) + " | "
        saida += str(self.cliente) + ((25 - len(self.cliente)) * " ") + "| "
        saida += self.data + " | "
        saida += "R$" + f"{(self.valor_total/100):.2f}"
        return saida

    def __eq__(self, other):
        if isinstance(other, Pedido):
            return (self.id_ped == other.id_ped) and (self.cliente == other.cliente) and (self.data == other.data)
        return False
