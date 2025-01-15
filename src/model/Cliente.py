class Cliente:

    def __init__(self, id_cli: int, nome: str, cep: str, endereco: str, uf: str, cidade: str, bairro: str, cpf_cnpj: str, fone: str, email: str):
        self.id_cli = id_cli
        self.nome = nome
        self.cep = cep
        self.endereco = endereco
        self.uf = uf
        self.cidade = cidade
        self.bairro = bairro
        self.cpf_cnpj = cpf_cnpj
        self.fone = fone
        self.email = email

    def __str__(self):
        saida = " "
        saida += "0" * (4 - len(str(self.id_cli))) + str(self.id_cli) + " | "
        saida += self.nome
        return saida

    def __eq__(self, other):
        if isinstance(other, Cliente):
            return (self.cpf_cnpj == other.cpf_cnpj) or (self.id_cli == other.id_cli)
        return False