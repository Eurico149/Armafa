from src.controller import Cliente_controller, Pedidos_controller, Produto_controller
from src.repository import DBConfig, ProdutoRepository, PedidoRepository, ClienteRepository


class SystemRoot:

    def __init__(self):
        config = DBConfig()
        cliente_repo = ClienteRepository(config)
        pedidos_repo = PedidoRepository(config, cliente_repo)
        produtos_repo = ProdutoRepository(config, pedidos_repo)

        self.__pedidos_controller = Pedidos_controller(pedidos_repo, cliente_repo)
        self.__cliente_controller = Cliente_controller(cliente_repo, pedidos_repo)
        self.__produtos_controller = Produto_controller(produtos_repo, pedidos_repo)

    @property
    def pedidos_controller(self):
        return self.__pedidos_controller

    @property
    def cliente_controller(self):
        return self.__cliente_controller

    @property
    def produtos_controller(self):
        return self.__produtos_controller