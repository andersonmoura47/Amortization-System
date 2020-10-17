

class MathFin:
    """Classe: Funções para cálculos financeiros e Sistemas de Financiamento:
            Valor Presente (VP)
            Valor Futuro (VF)
            Coversão de Taxa (i)
            Parcelas (PMT)
            Sistema de Amortização Constante (SAC)
            Sistema Francês de Amortização (PRICE)
            Sistema de Amortização Americano (SAA)"""

    def __init__(self, valor, i, n):
        """Valor: Valor
            i: Taxa
            n: Tempo"""
        self.valor = valor
        self.i = i
        self.n = n

    def vf(self):
        """Calcula o Valor Futuro
        Retorna o resultado do cálculo"""
        # fv = pv * (1 + i)**n
        cvf = (self.valor * ((1 + (self.i/100)) ** self.n))
        return cvf

    def vp(self):
        """Calcula o Valor Presente
        Retorna o resultado do calculo"""
        # pv = fv / (1 + i)**n
        cvp = (self.valor / ((1 + (self.i/100)) ** self.n))
        return cvp

    def pmt(self):
        """Calcula o valor das parcelas
        Retorna o resultado do calculo"""
        i = self.i / 100  # para efeito de calculo (unitário)
        # pmt = pv * {i / [1 - (1 + i)**-n]}
        pmt = self.valor * (i / (1 - ((1 + i)**(- self.n))))
        return pmt

    def converter_tax(self, PeriodoAtual, PeriodoDesejado):
        """Conversão de taxa
        Período atual ex: 1 (mes)
        Período desejado ex: 12 meses (1 ano)
        """
        # ieq = {[1 + (i/100)] ** (periodo2 / periodo1) - 1} * 100
        self.i = (((1 + (self.i/100)) ** (PeriodoDesejado/PeriodoAtual)) - 1) * 100


class Financiamento(MathFin):
    """Sistemas de Financiamento: SAC, PRICE, SAA"""

    def sac(self):
        """Sistema de Amortização Constante (SAC)
        Retorna a lista de Parcelas
        """
        saldo_inicial = self.valor  # saldo inicial começa com o valor do financiamento
        amortizacao = self.valor / self.n  # amortização constante
        i = self.i / 100  # taxa unitaria
        parcelas = []
        for a in range(self.n):  # loop p/ calcular os valores das parcelas conforme sua quantidade (n)
            juros = saldo_inicial * i
            valor_parcela = amortizacao + juros
            saldo_final = saldo_inicial - amortizacao
            saldo_inicial = saldo_final
            parcelas.append(valor_parcela)
        return parcelas

    def price(self):
        """Sistema Francês de Amortização (PRICE) | Parcelas constantes
        Retorna a lista de Parcelas
        """
        saldo_inicial = self.valor  # saldo inicial começa com o valor do financiamento
        pmt_var = self.pmt()  # calcula e recebe o valor constante da parcela
        i = self.i / 100  # taxa unitária
        parcelas = []
        for a in range(self.n):  # loop p/ calcular os valores das parcelas conforme sua quantidade (n)
            juros = saldo_inicial * i
            amortizacao = pmt_var - juros
            saldo_final = saldo_inicial - amortizacao
            saldo_inicial = saldo_final
            parcelas.append(pmt_var)
        return parcelas

    def saa(self):
        """Sistema de Amortização Americano (SAA) | Pagamento dos juros mesais
        Retorna a lista de Parcelas
        """
        saldo_inicial = self.valor  # saldo inicial começa com o valor do financiamento
        i = self.i / 100  # taxa unitaria
        parcelas = []
        for a in range(self.n):
            juros = saldo_inicial * i
            if (a + 1) != self.n:  # a amortização so é somada na ultima parcelas em que (a = n)
                amortizacao = 0
            else:
                amortizacao = saldo_inicial  # saldo (self.valor) é amortizado na ultima parcela (a = 0)
            pmt_var = amortizacao + juros
            saldo_final = saldo_inicial - amortizacao
            saldo_inicial = saldo_final
            parcelas.append(pmt_var)
        return parcelas

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~> Anotações - formas de calculo: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- TABELA: n|Saldo i (Si)|juros (j)|Amortização (AM)|    Parcela (PMT)     |    Saldo f (SD)
- SAC:     |  SD n-1    | Si * i  |     PV / n     |         AM + j       | Si - AM      #AM CONSTANTE
- PRICE:   |  SD n-1    | Si * i  |     PMT-j      |(PV(i/(1-((1+i)*-n))))| Si - AM      #PMT CONSTANTE
- SAA:     |  SD n-1    | Si * i  |   0,0...Si     |         AM + j       | Si - AM
# SAC - AM CONSTANTE, PMT = AM + J
# PRICE - PMT CONSTANTE, AM = PMT - J
# SAA - PAGA JUROS CONSTANTE, PV PAGO NA ULTIMA PMT, AM = 0, NA ULTIMA PMT: AM + SI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

a = MathFin(1200,5,8)
a.converter_tax(12,1)
#print('Valor: %.2f' %a.vf())
b = Financiamento(40000,8,96)
b.converter_tax(12,1)
#print(sum(b.sac()))
