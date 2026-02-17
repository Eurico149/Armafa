from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, MetaData, String, Table


def get_pedidos_entity(metadata: MetaData) -> Table:

    pedidos = Table(
        "pedidos",
        metadata,
        Column("id_ped", Integer, primary_key=True),
        Column("id_cli", Integer, ForeignKey("clientes.id_cli"), nullable=False),
        Column("data", String(10), nullable=False),
        Column("desconto", Integer, nullable=False),
        CheckConstraint("LENGTH(data) = 10", name="tamanho_data"),
    )

    return pedidos
