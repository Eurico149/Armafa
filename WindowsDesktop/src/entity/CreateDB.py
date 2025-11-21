from sqlalchemy import text, MetaData, create_engine
from src.entity import get_clientes_entity, get_pedido_quantidade_produto_entity, get_pedidos_entity, get_produtos_entity, get_produtos_pedidos_entity



def create():
    metadata = MetaData()
    engine = create_engine("sqlite:///src/data/dataBase.db")

    produtos = get_produtos_entity(metadata)
    clientes = get_clientes_entity(metadata)
    pedidos = get_pedidos_entity(metadata)
    produtos_pedidos = get_produtos_pedidos_entity(metadata)


    clientes.create(engine)
    produtos.create(engine)
    pedidos.create(engine)
    produtos_pedidos.create(engine)

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE VIEW pedido_quantidade_produto AS
            SELECT pp.id_ped, pp.id_pro, pro.nome, pp.quantidade, pp.valor_individual
            FROM pedidos AS ped
            JOIN pro_ped AS pp ON ped.id_ped = pp.id_ped
            JOIN produtos AS pro ON pp.id_pro = pro.id_pro;
        """))
        conn.commit()
