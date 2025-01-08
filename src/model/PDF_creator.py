from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from src.model.Cliente import Cliente
from src.model.Pedido import Pedido
from os import startfile


class PDF_creator:

    def __init__(self, nome_arquivo: str, cliente: Cliente, pedido: Pedido):
        self.__cliente = cliente
        self.__pedido = pedido
        self.__nome = nome_arquivo
        self.__cv = canvas.Canvas(nome_arquivo, pagesize=A4)
        self.__make_pdf()

    def __make_pdf(self):
        self.__cabecalho()
        self.__tabela()
        self.__salvar()

    def __tabela(self):
        largura, altura = A4

        h = 15
        col_l = [40, 250, 60, 100, 104]
        for j in range(len(self.__pedido.produtos)):
            for i in range(len(col_l)):
                id_pro = str(self.__pedido.produtos[j][1].id_pro)
                nome = self.__pedido.produtos[j][1].nome
                quantidade = str(self.__pedido.produtos[j][0])
                valor_unidade = "R$"+str(self.__pedido.produtos[j][1].valor / 100)
                valor_total = "R$"+str(self.__pedido.produtos[j][0] * self.__pedido.produtos[j][1].valor / 100)
                p = [id_pro, nome, quantidade, valor_unidade, valor_total]

                aux = (0, 0, 0, 0)
                if j == 0:
                    self.__cv.setFont("Helvetica-Bold", 10)
                    if i == 0:
                        aux = (5, 0, 0, 0)
                    if i == 4:
                        aux = (0, 5, 0, 0)
                    self.__cv.setFillColor(colors.HexColor("#DCDCDC"))
                    self.__cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 181 - j * h, col_l[i], h, aux, fill=1)
                    self.__cv.setFillColor(colors.HexColor("#000000"))
                    self.__cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 177 - j * h, p[i])
                    self.__cv.setFont("Helvetica", 10)
                elif j == len(self.__pedido.produtos)-1:
                    if i == 0:
                        aux = (0, 0, 5, 0)
                    self.__cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 181 - j * h, col_l[i], h, aux)
                    self.__cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 177 - j * h, p[i])
                else:
                    aux = (0, 0, 0, 0)
                    self.__cv.roundRect(20 + sum(col_l[:i + 1]) - col_l[i], altura - 181 - j * h, col_l[i], h, aux)
                    self.__cv.drawString(22 + sum(col_l[:i + 1]) - col_l[i], altura - 177 - j * h, p[i])
            if j == len(self.__pedido.produtos)-1:
                self.__cv.roundRect(470, altura - 196 - j * h, col_l[4], h, (0, 0, 5, 5))
                self.__cv.drawString(472, altura - 192 - j * h, "R$"+str(self.__pedido.valor_total/100))

                self.__cv.roundRect(20, altura - 245 - j * h, 300, 60, (5, 5, 5, 5))
                self.__cv.drawString(22, altura - 195 - j * h, "Observações:")

                self.__cv.roundRect(20, altura - 280 - j * h, 554, 30, (5, 5, 5, 5))
                self.__cv.drawString(22, altura - 269 - j * h, "Vendedor: " + (41 * "_"))
                self.__cv.drawString(303, altura - 269 - j * h, "Cliente: " + (41 * "_"))



    # limeites largura: 20, 574
    def __cabecalho(self):
        largura, altura = A4

        self.__cv.setFont("Helvetica", 8)
        self.__cv.roundRect(20, altura - 70, 130, 50, 5)
        self.__cv.drawString(22, altura - 34, "Salmo 23: ")
        self.__cv.drawString(22, altura - 46, "O SENHOR é o meu pastor,")
        self.__cv.drawString(22, altura - 58, "nada me faltará.")

        self.__cv.roundRect(152, altura - 70, 290, 50, 5)

        text = "Armafa Fabrocação de Ferro LTDA."
        aux = self.__centralise(152, 442, text)
        self.__cv.drawString(aux, altura - 30, text)

        text = "BR 230 KM 171 SÃO JOSÉ DA MATA CAMPINA GRANDE PB"
        aux = self.__centralise(152, 442, text)
        self.__cv.drawString(aux, altura - 45, text)

        text = "cassianooricardo@yahoo.com.br"
        aux = self.__centralise(152, 442, text)
        self.__cv.drawString(aux, altura - 60, text)

        self.__cv.setFont("Helvetica-Bold", 11)

        self.__cv.setFillColor(colors.HexColor("#DCDCDC"))
        self.__cv.roundRect(444, altura - 70, 130, 50, 5, fill=1)
        self.__cv.setFillColor(colors.HexColor("#000000"))

        id_ped = str(self.__pedido.id_ped)
        text = "PEDIDO Nº" + ("0" * (4 - len(id_ped))) + id_ped
        aux = self.__centralise(444, 574, text)
        self.__cv.drawString(aux, altura - 40, text)

        text = "DATA: " + self.__pedido.data
        aux = self.__centralise(444, 574, text)
        self.__cv.drawString(aux, altura - 60, text)

        self.__cv.roundRect(20, altura - 100, 554, 25, 5)
        self.__cv.setFont("Helvetica-Bold", 14)

        text = "PEDIDO DE VENDA"
        aux = self.__centralise(20, 574, text)
        self.__cv.drawString(aux, altura - 92, text)

        self.__cv.setFont("Helvetica", 9)

        self.__cv.roundRect(20, altura - 160, 554, 55, 5)

        id_cli = str(self.__cliente.id_cli)
        text = "ID_cliente: " + ("0" * (4 - len(id_cli))) + id_cli
        self.__cv.drawString(23, altura - 120, text)
        self.__cv.drawString(67, altura - 121, 5 * "_")


        self.__cv.drawString(100, altura - 120, "Cliente: " + self.__cliente.nome)
        self.__cv.drawString(131, altura - 121, 50 * "_")

        # cnpj = "20.031.219/0002-46"
        cnpj = self.__cliente.cpf_cnpj
        cnpj = cnpj[0:2] + "." + cnpj[2:5] + "." + cnpj[5:8] + "/" + cnpj[8:12] + "-" + cnpj[12:]
        self.__cv.drawString(390, altura - 120, "CPF/CNPJ: " + cnpj)
        self.__cv.drawString(438, altura - 121, 26 * "_")

        endereco = self.__cliente.endereco
        self.__cv.drawString(23, altura - 135, "Endereço: " + endereco)
        self.__cv.drawString(66, altura - 136, 43 * "_")

        cep = self.__cliente.cep
        cep = cep[0:5] + "-" + cep[5:]
        self.__cv.drawString(285, altura - 135, "CEP: " + cep)
        self.__cv.drawString(308, altura - 136, 12 * "_")

        uf = self.__cliente.uf
        self.__cv.drawString(372, altura - 135, "UF: " + uf)
        self.__cv.drawString(389, altura - 136, 6 * "_")

        cidade = self.__cliente.cidade
        self.__cv.drawString(424, altura - 135, "Cidade: " + cidade)
        self.__cv.drawString(457, altura - 136, 22 * "_")

        bairro = self.__cliente.bairro
        self.__cv.drawString(23, altura - 150, "Bairro: " + bairro)
        self.__cv.drawString(51, altura - 151, 20 * "_")

        # telefone = "(83) 9 8618-1144"
        telefone = self.__cliente.fone
        telefone = "(" + telefone[0:2] + ") " + telefone[2] + " " + telefone[3:7] + "-" + telefone[7:]
        self.__cv.drawString(158, altura - 150, "Fone: " + telefone)
        self.__cv.drawString(183, altura - 151, 23 * "_")

        email = self.__cliente.email
        self.__cv.drawString(305, altura - 150, "e-mail: " + email)
        self.__cv.drawString(334, altura - 151, 47 * "_")

    def __centralise(self, largura_inicio, largura_fim, texto):
        text_width = self.__cv.stringWidth(texto, "Helvetica")
        return largura_inicio + ((largura_fim - largura_inicio) - text_width) / 2

    def __salvar(self):
        startfile(self.__nome)
        self.__cv.save()