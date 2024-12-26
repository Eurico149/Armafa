-- valor: 1250 == R$12,50
CREATE TABLE produtos(
    id_pro INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    valor INTEGER NOT NULL
);

-- valor_total: 1250 == R$12,50
-- data: dd/mm/aaaa
CREATE TABLE pedidos(
    id_ped INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente VARCHAR(50),
    data CHAR(10),
    valor_total INTEGER NOT NULL
);

CREATE TABLE pro_ped(
    id_ped INTEGER NOT NULL,
    id_pro INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (id_pro) REFERENCES produtos(id_pro),
    FOREIGN KEY (id_ped) REFERENCES pedidos(id_ped)
);
