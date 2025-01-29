import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from src.model.Cliente import Cliente
from src.model.Pedido import Pedido
from os import startfile, path


class PDF_creator:

    def __init__(self, nome_arquivo: str, cliente: Cliente, pedido: Pedido):
        self._cliente = cliente
        self._pedido = pedido
        self._nome = self._valida_nome(nome_arquivo)
        self._cont = 1
        self._cv = canvas.Canvas(self._nome, pagesize=A4)
        self.__make_pdf()

    def _valida_nome(self, nome_base):
        output_dir = './pdfs'
        os.makedirs(output_dir, exist_ok=True)
        nome_base = os.path.join(output_dir, nome_base)
        nome, extensao = path.splitext(nome_base)
        contador = 1
        nome_unico = nome_base

        while path.exists(nome_unico):
            nome_unico = f"{nome}({contador}){extensao}"
            contador += 1
        return nome_unico

    def __make_pdf(self):
        self._cabecalho()
        self._tabela()
        self.__salvar()

    def _tabela(self):
        largura, altura = A4

        h = 15
        col_l = [40, 250, 60, 100, 104]
        for j in range(len(self._pedido.produtos)+1):
            if j == 37:
                self._cont += 1
                self.__more_pages()
                break
            for i in range(len(col_l)):
                if j == 0:
                    p = ['Código', 'Produto', 'Quantidade', 'Preço Unitário', 'Valor Total']
                else:
                    id_pro = "0" * (4 - len(str(self._pedido.produtos[j-1][1].id_pro))) + str(self._pedido.produtos[j-1][1].id_pro)
                    nome = self._pedido.produtos[j-1][1].nome
                    quantidade = str(self._pedido.produtos[j-1][0])
                    aux_u = f"{self._pedido.produtos[j-1][1].valor:.2f}".replace(".", ",")
                    if len(aux_u) > 6:
                        aux_u = aux_u[0:-6] + "." + aux_u[-6:]
                    valor_unidade = f"R$ {aux_u}"
                    aux_t = f"{(self._pedido.produtos[j-1][0] * self._pedido.produtos[j-1][1].valor):.2f}".replace(".", ",")
                    if len(aux_t) > 6:
                        aux_t = aux_t[0:-6] + "." + aux_t[-6:]
                    valor_total = f"R$ {aux_t}"
                    p = [id_pro, nome, quantidade, valor_unidade, valor_total]

                aux = (0, 0, 0, 0)
                if j == 0:
                    self._cv.setFont("Helvetica-Bold", 10)
                    if i == 0:
                        aux = (5, 0, 0, 0)
                    if i == 4:
                        aux = (0, 5, 0, 0)
                    self._cv.setFillColor(colors.HexColor("#DCDCDC"))
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 181 - j * h, col_l[i], h, aux, fill=1)
                    self._cv.setFillColor(colors.HexColor("#000000"))
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 177 - j * h, p[i])
                    self._cv.setFont("Helvetica", 10)
                elif j == len(self._pedido.produtos) or j == 36:
                    if i == 0:
                        self._cv.drawString(580, 10, str(self._cont))
                        aux = (0, 0, 5, 0)
                    elif i == 4:
                        aux = (0, 0, 0, 5)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 181 - j * h, col_l[i], h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 177 - j * h, p[i])
                else:
                    aux = (0, 0, 0, 0)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 181 - j * h, col_l[i], h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 177 - j * h, p[i])
            if j == len(self._pedido.produtos) or j == 36:
                self._cv.roundRect(470, altura - 199 - j * h, col_l[4], h, (5, 5, 0, 0))
                self._cv.roundRect(470, altura - 199 - (j+1) * h, col_l[4], h, (0, 0, 5, 5))
                st = f"{self._pedido.valor_total:.2f}".replace(".", ",")
                if len(st) > 6:
                    st = st[0:-6] + "." + st[-6:]
                self._cv.drawString(472, altura - 195 - j * h, f"R$ {st}")
                self._cv.drawString(425, altura - 195 - j * h, "SubTotal:")
                vt = f"{self._pedido.valor_total * ((100 - self._pedido.desconto) / 100):.2f}".replace(".", ",")
                if len(vt) > 6:
                    vt = vt[0:-6] + "." + vt[-6:]
                self._cv.drawString(472, altura - 195 - (j+1) * h, f"R$ {vt}")
                self._cv.drawString(443, altura - 195 - (j+1) * h, "Total:")

                self._cv.roundRect(470, altura - 199 - (j+2.5) * h, 30, h, (5, 5, 5, 5))
                self._cv.drawString(472, altura - 195 - (j+2.5) * h, f"{self._pedido.desconto}%")
                self._cv.drawString(439, altura - 195 - (j+2.5) * h, "Desc.:")

                self._cv.roundRect(20, altura - 245 - j * h, 300, 60, (5, 5, 5, 5))
                self._cv.drawString(22, altura - 195 - j * h, "Observações:")

                self._cv.roundRect(20, altura - 280 - j * h, 554, 30, (5, 5, 5, 5))
                self._cv.drawString(22, altura - 269 - j * h, "Vendedor: " + (41 * "_"))
                self._cv.drawString(303, altura - 269 - j * h, "Cliente: " + (41 * "_"))

    def __more_pages(self):
        self._cv.showPage()
        largura, altura = A4
        self._cv.setFont("Helvetica", 10)

        h = 15
        col_l = [40, 250, 60, 100, 104]
        for j in range(37, len(self._pedido.produtos)+1):
            if j != 37 and (j - 37) % 52 == 0:
                self._cont += 1
                self._cv.showPage()
                self._cv.setFont("Helvetica", 10)
            for i in range(len(col_l)):
                id_pro = "0" * (4 - len(str(self._pedido.produtos[j - 1][1].id_pro))) + str(
                    self._pedido.produtos[j - 1][1].id_pro)
                nome = self._pedido.produtos[j - 1][1].nome
                quantidade = str(self._pedido.produtos[j - 1][0])
                aux_u = f"{self._pedido.produtos[j - 1][1].valor:.2f}".replace(".", ",")
                if len(aux_u) > 6:
                    aux_u = aux_u[0:-6] + "." + aux_u[-6:]
                valor_unidade = f"R$ {aux_u}"
                aux_t = f"{(self._pedido.produtos[j - 1][0] * self._pedido.produtos[j - 1][1].valor):.2f}".replace(".",
                                                                                                                   ",")
                if len(aux_t) > 6:
                    aux_t = aux_t[0:-6] + "." + aux_t[-6:]
                valor_total = f"R$ {aux_t}"
                p = [id_pro, nome, quantidade, valor_unidade, valor_total]

                aux = (0, 0, 0, 0)
                if j == len(self._pedido.produtos) or (j - 37) % 52 == 51:
                    if i == 0:
                        self._cv.drawString(580, 10, str(self._cont))
                        aux = (0, 0, 5, 0)
                    elif i == 4:
                        aux = (0, 0, 0, 5)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 44 - ((j - 37) % 52) * h, col_l[i],
                                       h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 40 - ((j - 37) % 52) * h, p[i])
                elif (j - 37) % 52 == 0:
                    if i == 0:
                        aux = (5, 0, 0, 0)
                    if i == 4:
                        aux = (0, 5, 0, 0)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 44 - ((j - 37) % 52) * h, col_l[i],
                                       h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 40 - ((j - 37) % 52) * h, p[i])

                else:
                    aux = (0, 0, 0, 0)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 44 - ((j - 37) % 52) * h, col_l[i],
                                       h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 40 - ((j - 37) % 52) * h, p[i])

    # limeites largura: 20, 574
    def _cabecalho(self):
        largura, altura = A4

        self._cv.setFont("Helvetica", 8)
        self._cv.roundRect(20, altura - 70, 130, 50, 5)
        self._cv.drawString(22, altura - 34, "Salmo 23: ")
        self._cv.drawString(22, altura - 46, "O SENHOR é o meu pastor,")
        self._cv.drawString(22, altura - 58, "nada me faltará.")

        self._cv.roundRect(152, altura - 70, 290, 50, 5)

        text = "Armafa Fabrocação de Ferro LTDA."
        aux = self._centralise(152, 442, text)
        self._cv.drawString(aux, altura - 30, text)

        text = "BR 230 KM 171 SÃO JOSÉ DA MATA CAMPINA GRANDE PB"
        aux = self._centralise(152, 442, text)
        self._cv.drawString(aux, altura - 45, text)

        text = "cassianooricardo@yahoo.com.br"
        aux = self._centralise(152, 442, text)
        self._cv.drawString(aux, altura - 60, text)

        self._cv.setFont("Helvetica-Bold", 11)

        self._cv.setFillColor(colors.HexColor("#DCDCDC"))
        self._cv.roundRect(444, altura - 70, 130, 50, 5, fill=1)
        self._cv.setFillColor(colors.HexColor("#000000"))

        id_ped = str(self._pedido.id_ped)
        text = "PEDIDO Nº" + ("0" * (4 - len(id_ped))) + id_ped
        aux = self._centralise(444, 574, text)
        self._cv.drawString(aux, altura - 40, text)

        text = "DATA: " + self._pedido.data
        aux = self._centralise(444, 574, text)
        self._cv.drawString(aux, altura - 60, text)

        self._cv.roundRect(20, altura - 100, 554, 25, 5)
        self._cv.setFont("Helvetica-Bold", 14)

        text = "PEDIDO DE VENDA"
        aux = self._centralise(20, 574, text)
        self._cv.drawString(aux, altura - 92, text)

        self._cv.setFont("Helvetica", 9)

        self._cv.roundRect(20, altura - 160, 554, 55, 5)

        id_cli = str(self._cliente.id_cli)
        text = "ID_cliente: " + ("0" * (4 - len(id_cli))) + id_cli
        self._cv.drawString(23, altura - 120, text)
        self._cv.drawString(67, altura - 121, 5 * "_")


        self._cv.drawString(100, altura - 120, "Cliente: " + self._cliente.nome)
        self._cv.drawString(131, altura - 121, 50 * "_")

        # cnpj = "20.031.219/0002-46"
        cnpj = self._cliente.cpf_cnpj
        if len(cnpj) == 11:
            cnpj = cnpj[0:3] + "." + cnpj[3:6] + "." + cnpj[6:9] + "-" + cnpj[9:]
        else:
            cnpj = cnpj[0:2] + "." + cnpj[2:5] + "." + cnpj[5:8] + "/" + cnpj[8:12] + "-" + cnpj[12:]
        self._cv.drawString(390, altura - 120, "CPF/CNPJ: " + cnpj)
        self._cv.drawString(438, altura - 121, 26 * "_")

        endereco = self._cliente.endereco
        self._cv.drawString(23, altura - 135, "Endereço: " + endereco)
        self._cv.drawString(66, altura - 136, 43 * "_")

        cep = self._cliente.cep
        if cep != "":
            cep = cep[0:5] + "-" + cep[5:]
        self._cv.drawString(285, altura - 135, "CEP: " + cep)
        self._cv.drawString(308, altura - 136, 12 * "_")

        uf = self._cliente.uf
        self._cv.drawString(372, altura - 135, "UF: " + uf)
        self._cv.drawString(389, altura - 136, 6 * "_")

        cidade = self._cliente.cidade
        self._cv.drawString(424, altura - 135, "Cidade: " + cidade)
        self._cv.drawString(457, altura - 136, 22 * "_")

        bairro = self._cliente.bairro
        self._cv.drawString(23, altura - 150, "Bairro: " + bairro)
        self._cv.drawString(51, altura - 151, 20 * "_")

        telefone = self._cliente.fone
        if len(telefone) == 10:
            telefone = "(" + telefone[0:2] + ") " + telefone[2:6] + "-" + telefone[6:]
        elif len(telefone) == 11:
            telefone = "(" + telefone[0:2] + ") " + telefone[2] + " " + telefone[3:7] + "-" + telefone[7:]
        self._cv.drawString(158, altura - 150, "Fone: " + telefone)
        self._cv.drawString(183, altura - 151, 23 * "_")

        email = self._cliente.email
        self._cv.drawString(305, altura - 150, "e-mail: " + email)
        self._cv.drawString(334, altura - 151, 47 * "_")

    def _centralise(self, largura_inicio, largura_fim, texto):
        text_width = self._cv.stringWidth(texto, "Helvetica")
        return largura_inicio + ((largura_fim - largura_inicio) - text_width) / 2

    def __salvar(self):
        self._cv.save()
        startfile(self._nome)

class Pdf_espelho(PDF_creator):

    def __init__(self, nome: str, cliente: Cliente, pedido: Pedido):
        super().__init__(nome, cliente, pedido)

    def _tabela(self):
        largura, altura = A4

        self._cv.setFont("Helvetica", 14)
        h = 20
        col_l = [60, 400, 94]
        for j in range(len(self._pedido.produtos) + 1):
            if j != 0 and j == 32 :
                self._cont += 1
                self.__more_pages()
                break
            for i in range(len(col_l)):
                if j == 0:
                    p = ['Código', 'Produto', 'Quantidade']
                else:
                    id_pro = "0" * (4 - len(str(self._pedido.produtos[j - 1][1].id_pro))) + str(
                        self._pedido.produtos[j - 1][1].id_pro)
                    nome = self._pedido.produtos[j - 1][1].nome
                    quantidade = str(self._pedido.produtos[j - 1][0])
                    p = [id_pro, nome, quantidade]

                aux = (0, 0, 0, 0)
                if j == 0:
                    self._cv.setFont("Helvetica-Bold", 14)
                    if i == 0:
                        aux = (5, 0, 0, 0)
                    if i == 2:
                        aux = (0, 5, 0, 0)
                    self._cv.setFillColor(colors.HexColor("#DCDCDC"))
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], (altura - 186 - j * h), col_l[i], h, aux,
                                       fill=1)
                    self._cv.setFillColor(colors.HexColor("#000000"))
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 182 - j * h, p[i])
                    self._cv.setFont("Helvetica", 14)
                elif j == len(self._pedido.produtos) or j == 31:
                    if i == 0:
                        self._cv.setFont("Helvetica", 10)
                        self._cv.drawString(580, 10, str(self._cont))
                        self._cv.setFont("Helvetica", 14)
                        aux = (0, 0, 5, 0)
                    elif i == 2:
                        aux = (0, 0, 0, 5)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 186 - j * h, col_l[i], h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 182 - j * h, p[i])
                else:
                    aux = (0, 0, 0, 0)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 186 - j * h, col_l[i], h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 182 - j * h, p[i])

    def __more_pages(self):
        self._cv.showPage()
        largura, altura = A4

        self._cv.setFont("Helvetica", 14)
        h = 20
        col_l = [60, 400, 94]
        for j in range(32, len(self._pedido.produtos) + 1):
            if j != 32 and (j-32) % 39 == 0:
                self._cont += 1
                self._cv.showPage()
            for i in range(len(col_l)):
                id_pro = "0" * (4 - len(str(self._pedido.produtos[j - 1][1].id_pro))) + str(
                    self._pedido.produtos[j - 1][1].id_pro)
                nome = self._pedido.produtos[j - 1][1].nome
                quantidade = str(self._pedido.produtos[j - 1][0])
                p = [id_pro, nome, quantidade]

                aux = (0, 0, 0, 0)
                if j == len(self._pedido.produtos) or (j-32) % 39 == 38:
                    if i == 0:
                        self._cv.setFont("Helvetica", 10)
                        self._cv.drawString(580, 10, str(self._cont))
                        self._cv.setFont("Helvetica", 14)
                        aux = (0, 0, 5, 0)
                    elif i == 2:
                        aux = (0, 0, 0, 5)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 44 - ((j-32) % 39) * h, col_l[i], h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 40 - ((j-32) % 39) * h, p[i])
                elif (j-32) % 39 == 0:
                    self._cv.setFont("Helvetica", 14)
                    if i == 0:
                        aux = (5, 0, 0, 0)
                    if i == 2:
                        aux = (0, 5, 0, 0)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 44 - ((j-32) % 39) * h, col_l[i], h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i],altura - 40 - ((j-32) % 39) * h, p[i])

                else:
                    aux = (0, 0, 0, 0)
                    self._cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 44 - ((j-32) % 39) * h, col_l[i], h, aux)
                    self._cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 40 - ((j-32) % 39) * h, p[i])
