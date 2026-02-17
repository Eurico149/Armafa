from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, MetaData, Table


def get_produtos_pedidos_entity(metadata: MetaData) -> Table:

    pedidos = Table(
        "pro_ped",
        metadata,
        Column("id_ped", Integer, ForeignKey("pedidos.id_ped"), primary_key=True, nullable=False),
        Column("id_pro", Integer, ForeignKey("produtos.id_pro"), primary_key=True, nullable=False),
        Column("valor_individual", Float, nullable=False),
        Column("quantidade", Integer, nullable=False),
        CheckConstraint("quantidade >= 0", name="quantidade_check"),
    )

    return pedidos
