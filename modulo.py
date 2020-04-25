# coding: utf-8
# Alguns Valores podem ser conferidos no site:
# https://fazaconta.com/financiamentos-tabela-sac.htm


class MathFin:
    """Classe: Funções para cálculos financeiros e Sistemas de Financiamento::
            Valor Presente (VP)
            Valor Futuro (VF)
            Coversão de Taxa (i)
            Parcelas (PMT)
            Sistema de Amortização Constante (SAC)
            Sistema Francês de Amortização (PRICE)
            Sistema de Amortização Americano (SAA)"""

    def __init__(self, valor, i, n):
        """Valor: Valor a ser trabalhado
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


#================== Programa Principal VP, VF, Conversão de taxa ==================
valor = float(input('Digite o valor a ser trabalhado: '))
i = float(input('Digite a taxa: '))
n = int(input('Digite a quantidade de parcelas: '))
objeto1 = MathFin(valor, i, n)  # instancia o obj á classe

while True:
    pergunta = int(input('Deseja converter a taxa: \n1 - Sim\n2 - Não '))
    if pergunta == 1:
        p1 = int(input('Digite o período atual da taxa (Ex: Taxa anual = 12 (Meses): '))
        p2 = int(input('Digite o período desejado para conversão. Ex: digite: '
                       '1 (P/ pagamentos mensais) | 3 (Pagamentos trimestrais):'))
        objeto1.converter_tax(p1, p2)
        break
    elif pergunta == 2:
        break
    else:
        print('Opção Inválida!')

print(f'\nValor: R${objeto1.valor:.2f} \nTaxa: {objeto1.i:.4f}% \nTempo: {objeto1.n}')

while True:
    pergunta2 = int(input('Escolha a opção desejada: \n1 - Valor Presente (VP)'
                          '\n2 - Valor Futuro (VF)\n3 - Valor da Parcela (PMT)\n4 - Nenhum '))
    if pergunta2 == 1:
        print(f'\nValor presente: R${objeto1.vp():.2f}')
        break
    elif pergunta2 == 2:
        print(f'\nValor futuro: R${objeto1.vf():.2f}')
        break
    elif pergunta2 == 3:
        print(f'PMT: R${objeto1.pmt():.2f}')
        break
    elif pergunta2 == 4:
        break
    else:
        print('Opção Inválida!')


objeto2 = Financiamento(objeto1.valor, objeto1.i, objeto1.n)
while True:
    pergunta3 = int(input('\nDeseja calcular o Financiamento com esse valores?'
                          '\nEscolha o sistema de financiamento:'
                          '\n1 - SAC\n2 - PRICE\n3 - SAA\n4 - Não calcular'))
    if pergunta3 == 1:
        sis = 'Sac'  # variável para printar qual o sistema
        a = objeto2.sac()
        break
    elif pergunta3 == 2:
        sis = 'Price'
        a = objeto2.price()
        break
    elif pergunta3 == 3:
        sis = 'SAA'
        a = objeto2.saa()
        break
    elif pergunta3 == 4:
        a = ' '
        print('Saindo!')
        break
    else:
        print('Opção Inválida!')

if a != ' ':  # se foi calculado o financiamento
    print(f'\nValor: R${objeto1.valor:.2f}\nTaxa: {objeto1.i:.4f}%\nTempo: {objeto1.n}\n')
    for valores in range(len(a)):
        print(f'Parcela {valores + 1}: R${a[valores]:.2f}')  # printa cada parcelas formatada
    print(f'Valor total do Financiamento pelo sistema {sis}: R${sum(a):.2f}')  # valor total do financiamento

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~> Anotações - formas de calculo: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- TABELA: n|Saldo i (Si)|juros (j)|Amortização (AM)|    Parcela (PMT)     |    Saldo f (SD)
- SAC:     |  SD n-1    | Si * i  |     PV / n     |         AM + j       | Si - AM      #AM CONSTANTE
- PRICE:   |  SD n-1    | Si * i  |     PMT-j      |(PV(i/(1-((1+i)*-n))))| Si - AM      #PMT CONSTANTE
- SAA:     |  SD n-1    | Si * i  |   0,0...Si     |         AM + j       | Si - AM
# SAC - AM CONSTANTE, PMT = AM + J
# PRICE - PMT CONSTANTE, AM = PMT - J
# SAA - PAGA JUROS CONSTANTE, PV PAGO NA ULTIMA PMT, AM = 0, NA ULTIMA PMT: AM + SI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
