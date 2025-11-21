from sqlalchemy import Table, Column, Integer, String, MetaData, Float


def get_produtos_entity(metadata: MetaData) -> Table:

    produtos = Table(
        "produtos",
        metadata,
        Column("id_pro", Integer, primary_key=True),
        Column("nome", String(36), nullable=False),
        Column("valor", Float, nullable=False)
    )

    return produtos