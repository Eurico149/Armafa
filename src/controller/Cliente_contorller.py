from src.model.Cliente_repository import Cliente_repository as Cr


class Cliente_controller:

    def get_clientes(self, ref: str):
        if ref.isnumeric():
            return Cr().get_cliente(int(ref))
        return Cr().get_clientes_by_name(ref)
