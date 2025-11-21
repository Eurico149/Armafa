from sqlalchemy import Table, Column, Integer, String, MetaData


def get_clientes_entity(metadata: MetaData) -> Table:

    clientes = Table(
        "clientes",
        metadata,
        Column("id_cli", Integer, primary_key=True),
        Column("nome", String(50), nullable=False),
        Column("cep", String(8)),
        Column("endereco", String(100)),
        Column("uf", String(2)),
        Column("cidade", String(40)),
        Column("bairro", String(40)),
        Column("cpf_cnpj", String(14)),
        Column("fone", String(11)),
        Column("email", String(80))
    )

    return clientes