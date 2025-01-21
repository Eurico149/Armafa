CREATE TABLE produtos(
    id_pro INTEGER PRIMARY KEY,
    nome VARCHAR(36) NOT NULL,
    valor REAL NOT NULL
);

-- excluindo em todos menos o email: -, ., ), (, /, \
CREATE TABLE clientes(
    id_cli INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cep CHAR(8),
    endereco VARCHAR(100),
    uf CHAR(2),
    cidade VARCHAR(40),
    bairro VARCHAR(40),
    cpf_cnpj VARCHAR(14),
    fone VARCHAR(11),
    email VARCHAR(80),
);

-- data: dd/mm/aaaa
CREATE TABLE pedidos(
    id_ped INTEGER PRIMARY KEY,
    id_cli INTEGER NOT NULL,
    data CHAR(10),
    FOREIGN KEY (id_cli) REFERENCES clientes(id_cli),
    CONSTRAINT tamanho_data CHECK LENGTH(data) = 10
);

CREATE TABLE pro_ped(
    id_ped INTEGER NOT NULL,
    id_pro INTEGER NOT NULL,
    valor_individual REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (id_pro) REFERENCES produtos(id_pro),
    FOREIGN KEY (id_ped) REFERENCES pedidos(id_ped),
    CONSTRAINT quantidade_check CHECK quantidade >= 0
);

CREATE VIEW pedido_quantidade_produto AS
SELECT pp.id_ped, pp.id_pro, pro.nome, pp.quantidade, pp.valor_individual
FROM pedidos AS ped, produtos AS pro, pro_ped AS pp
WHERE ped.id_ped=pp.id_ped AND pp.id_pro=pro.id_pro;
