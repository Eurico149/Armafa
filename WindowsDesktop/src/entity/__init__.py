from .ClienteEntity import get_clientes_entity
from .PedidosEntity import get_pedidos_entity
from .PedidosQuantidadeProdutos import get_pedido_quantidade_produto_entity
from .ProdutoPedidoEntity import get_produtos_pedidos_entity
from .ProdutosEntity import get_produtos_entity

__all__ = [
    "get_clientes_entity",
    "get_pedidos_entity",
    "get_pedido_quantidade_produto_entity",
    "get_produtos_pedidos_entity",
    "get_produtos_entity",
]
