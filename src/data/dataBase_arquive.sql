-- valor: 1250 == R$12,50
CREATE TABLE produtos(
    id_pro INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor INTEGER NOT NULL
);

-- excluindo em todos menos o email: -, ., ), (, /, \
CREATE TABLE clientes(
    id_cli INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cep CHAR(8),
    endereco VARCHAR(100),
    uf CHAR(2),
    cidade VARCHAR(50),
    bairro VARCHAR(50),
    cpf_cnpj VARCHAR(14),
    fone VARCHAR(11),
    email VARCHAR(80)
);

-- valor_total: 1250 == R$12,50
-- data: dd/mm/aaaa
CREATE TABLE pedidos(
    id_ped INTEGER PRIMARY KEY,
    id_cli INTEGER NOT NULL,
    data CHAR(10),
    FOREIGN KEY (id_cli) REFERENCES clientes(id_cli)
);

-- valor_individual: 1250 == R$12,50
CREATE TABLE pro_ped(
    id_ped INTEGER NOT NULL,
    id_pro INTEGER NOT NULL,
    valor_individual INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (id_pro) REFERENCES produtos(id_pro),
    FOREIGN KEY (id_ped) REFERENCES pedidos(id_ped)
);
