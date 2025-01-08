class Produto:
    def __init__(self, id_pro: int, nome, valor: int):
        self.id_pro = id_pro
        self.nome = nome
        self.valor = valor

    def __str__(self):
        saida = " "
        saida += "0" * (4 - len(str(self.id_pro))) + str(self.id_pro) + " | "
        saida += str(self.nome) + ((37 - len(self.nome)) * " ") + "| "
        saida += "R$" + f"{(self.valor/100):.2f}"
        return saida

    def __eq__(self, other):
        if isinstance(other, Produto):
            return (self.id_pro == other.id_pro) and (self.nome == other.nome) and (self.valor == other.valor)
        return False