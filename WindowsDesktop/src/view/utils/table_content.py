def convert_to_table_content(data_type: str, data: list):
    content = {}

    match data_type:

        case "Clientes":
            data.reverse()
            content = {
                "data": [(c.id_cli, c.nome) for c in data],
                "meta": {
                    "table_title": "Clientes",
                    "columns": [
                        {"name": "ID", "width": 35, "location": "center"},
                        {"name": "Nome", "width": "auto", "location": "w"},
                    ]
                }
            }

        case "Produtos":
            data.reverse()

            dto = []
            for p in data:
                texto = f"{p.valor:,.2f}"
                texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
                valor = f"R$ {(10 - len(texto)) * " "}{texto}"
                dto.append((p.id_pro, p.nome, valor))

            content = {
                "data": dto,
                "meta": {
                    "table_title": "Produtos",
                    "columns": [
                        {"name": "ID", "width": 35, "location": "center"},
                        {"name": "Nome", "width": "auto", "location": "w"},
                        {"name": "Valor", "width": 100, "location": "w"}
                    ]
                }
            }

        case "Pedidos":
            data.reverse()

            dto = []
            for p in data:
                texto = f"{p.valor_total:,.2f}"
                texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
                valor_total = f"R$ {(10 - len(texto)) * " "}{texto}"
                dto.append((p.id_ped, p.data, p.cliente.nome, valor_total))

            content = {
                "data": dto,
                "meta": {
                    "table_title": "Pedidos",
                    "columns": [
                        {"name": "ID", "width": 35, "location": "center"},
                        {"name": "Data", "width": 80, "location": "center"},
                        {"name": "Cliente", "width": "auto", "location": "w"},
                        {"name": "Total", "width": 100, "location": "w"}
                    ]
                }
            }

    return content
