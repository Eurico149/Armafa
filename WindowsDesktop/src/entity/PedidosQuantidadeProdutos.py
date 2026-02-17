from sqlalchemy import MetaData, Table


def get_pedido_quantidade_produto_entity(metadata: MetaData, engine) -> Table:

    vw_pedido_quantidade_produto = Table("pedido_quantidade_produto", metadata, autoload_with=engine)

    return vw_pedido_quantidade_produto
