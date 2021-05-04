import pandas as pd
import json as js
import os
import sys

from config import *

bandeira_liquidez_diaria = False
bandeira_cotacao = False
bandeira_ebit = False
bandeira_lucro = False


def super_spaces():
    print("===========================================================================================================")


def spaces():
    print("----------------------------------------------------------------------------------------------------------")


action_counter = 0
falha_liq_roe = 0  # Falha ou na liquidez e/ou no ROE mínimo
falha_action_filter = 0  # Falha no tipo de ação
falha_pl_lpa = 0  # Falha no PL em relação ao LPA
falha_cot_vpa = 0  # Falha da cotação média em relação ao VPA
falha_ebit_rec = 0  # Falha no EBIT ou na tentativa de recuperação
falha_bd = 0  # Falha no banco de dados
falha_min_yield = 0  # Falha no Yield Minimo
falha_ll = 0  # Falha no Lucro líquido ou na tentativa de recuperação
falha_caixa = 0  # Falha no caixa livre
falha_tf = 0  # Falha no teste final de recuperação

try:
    os.remove("ops.txt")
except:
    print("Primeira operação iniciada!")

json_list = os.listdir('JSON/.')  # LISTA TODOS OS ARQUIVOS .JSON DO DIRETÓRIO JSON/
list_acoes = []
data_frame = []

alimenticio = pd.read_csv('CSV/alimenticio.csv', sep=';', header=0)
bancario = pd.read_csv('CSV/bancario.csv', sep=';', header=0)
eletrico = pd.read_csv('CSV/eletrico.csv', sep=';', header=0)
saude = pd.read_csv('CSV/saude.csv', sep=';', header=0)

print("Processo Iniciado!")

sys.stdout = open("ops.txt", "w")

json_volume = js.load(open('CSV/volumes.json'))

for year in year_list:
    for quarter in quarter_list:
        super_spaces()
        super_spaces()
        print('Ano: ' + str(year) + ' Trimestre: ' + str(quarter))
        list_acoes.append(str(year) + '-' + str(quarter))
        super_spaces()
        super_spaces()
        volume_list = json_volume[str(year) + '-' + str(quarter)]
        for json_file in json_list:  # INICIA O LOOPING PARA ANÁLISAR TODOS OS ARQUIVOS IMPORTADOS EM JSON_LIST
            if bancario["TICKER"].str.contains(json_file[:-5]).any():  # BANCÁRIO
                qtd_acoes = 3000000  # QUANTIDADE MÍNIMA DE AÇÕES (EM DINHEIRO NEGOCIADO)
                pl_maximo = 10 * 5  # PL MAXIMO
                yield_minimo = 0.04  # YIELD MAXIMO (0.2 = 20%)
                margemEbitMinima = 0  # MARGEM EBIT MÍNIMA (0.2 = 20%)
                roe_minimo = 0.113 / 4  # ROE MINIMO (0.2 = 20%) TRIMESTRAL
                setor = "BANCARIO"
            elif alimenticio["TICKER"].str.contains(json_file[:-5]).any():  # ALIMENTÍCIO
                qtd_acoes = 2000000  # QUANTIDADE MÍNIMA DE AÇÕES
                pl_maximo = 18.5 * 5  # PL MAXIMO
                yield_minimo = 0.02  # YIELD MAXIMO (0.2 = 20%)
                margemEbitMinima = 0.09  # MARGEM EBIT MÍNIMA (0.2 = 20%)
                roe_minimo = 0.112 / 4  # ROE MINIMO (0.2 = 20%) TRIMESTRAL
                setor = "ALIMENTICIO"
            elif eletrico["TICKER"].str.contains(json_file[:-5]).any():  # ELÉTRICO
                qtd_acoes = 1000000  # QUANTIDADE MÍNIMA DE AÇÕES
                pl_maximo = 15 * 5  # PL MAXIMO
                yield_minimo = 0.037  # YIELD MAXIMO (0.2 = 20%)
                margemEbitMinima = 0.189  # MARGEM EBIT MÍNIMA (0.2 = 20%)
                roe_minimo = 0.13 / 4  # ROE MINIMO (0.2 = 20%) TRIMESTRAL
                setor = "ELETRICO"
            elif saude["TICKER"].str.contains(json_file[:-5]).any():  # SAÚDE
                qtd_acoes = 10000000  # QUANTIDADE MÍNIMA DE AÇÕES
                pl_maximo = 25 * 5  # PL MAXIMO
                yield_minimo = 0.01  # YIELD MAXIMO (0.2 = 20%)
                margemEbitMinima = 0.2  # MARGEM EBIT MÍNIMA (0.2 = 20%)
                roe_minimo = 0.1 / 4  # ROE MINIMO (0.2 = 20%) TRIMESTRAL
                setor = "SAUDE"
            else:
                qtd_acoes = 10000000000000  # QUANTIDADE MÍNIMA DE AÇÕES                                  #NÃO CONVEM
                pl_maximo = 0  # PL MAXIMO
                yield_minimo = 1  # YIELD MAXIMO (0.2 = 20%)
                margemEbitMinima = 0.50  # MARGEM EBIT MÍNIMA (0.2 = 20%)
                roe_minimo = 0.015  # ROE MINIMO (0.2 = 20%) TRIMESTRAL
                setor = "FALHOU"
            json_options = js.load(open('JSON/' + json_file))  # ABRE O ARQUIVO
            super_spaces()  # CHAMA FUNÇÃO PRA DEIXAR BONITO
            print("Ficha Técnica: " + json_file + " (" + setor + ")")  # MOSTRA QUAL ARQUIVO ABRIU
            spaces()  # CHAMA FUNÇÃO PRA DEIXAR BONITO

            for year_options in json_options:  # ESSE AQUI É O LOOPING DE FILTRO
                bandeira_liquidez_diaria = False
                bandeira_cotacao = False
                bandeira_ebit = False
                bandeira_lucro = False
                if year_options['year'] == year and year_options['quarter'] == quarter:  # FILTRA ANO E BIMESTRE ESCOLHI
                    action_counter = action_counter + 1
                    print("Ano de " + str(year) + " e trimestre " + str(quarter) + " identificado!")
                    try:
                        if qtd_acoes <= volume_list[str(json_file)[:-5]]:  # LIQUIDEZ DIÁRIA
                            print("[OK] Líquidez corrente")
                            bandeira_liquidez_diaria = True  # BANDEIRA PARA PRÓXIMO BLOCO
                        else:
                            if year_options['roe'] > 0.15 and qtd_acoes / 10 <= volume_list[str(json_file)[:-5]]:
                                print('[OK] ROE MÍNIMO DE 15%')
                                bandeira_liquidez_diaria = True
                            else:
                                print('[FALHA] Liquidez Diária e ROE')
                                falha_liq_roe = falha_liq_roe + 1
                    except KeyError:
                        print('[FALHA] Ação não pertence ao filtro')
                        falha_action_filter = falha_action_filter + 1

                    if 0 < year_options['pl'] <= pl_maximo and bandeira_liquidez_diaria is True:
                        bandeira_liquidez_diaria = False
                        print("[OK] PL máximo")
                        bandeira_cotacao = True
                    elif 0 < year_options['pl'] <= pl_maximo and bandeira_liquidez_diaria is False:
                        print('')
                    else:
                        if year_options['pl'] <= 12 * year_options['lpa']:
                            if year_options['vpa'] * 2 > year_options['cotacao']:
                                print('[OK] VPA e PL')
                                bandeira_cotacao = True
                            else:
                                print('[FALHA] Cotação em relação ao VPA')
                                falha_cot_vpa = falha_cot_vpa + 1
                        else:
                            print('[FALHA] Pl em relação ao LPA')
                            falha_pl_lpa = falha_pl_lpa + 1

                    if yield_minimo < year_options['divYeld'] and bandeira_cotacao is True:
                        bandeira_cotacao = False
                        print("[OK] Yield Mínimo")
                        if year_options[
                            'margEbit'] > margemEbitMinima:  # MARGEM EBIT MAIOR QUE MARGEM EBIT ESTABELECIDA
                            bandeira_ebit = True
                            print('[OK] Margem EBIT Mínima')
                        else:
                            if year_options['capex'] > 0 and year_options['ebit'] != 0 and (
                                    year_options['divBruta'] / year_options['ebit'] < 4):
                                bandeira_ebit = True
                                print('[OK] Recuperação Capex + Db/Ebit')
                            else:
                                print('[FALHA] Margem Ebit Mínima e tentativa de recuperação')
                                falha_ebit_rec = falha_ebit_rec + 1
                    elif year_options == 0:
                        print("[FALHA] O Banco de dados não possuí o dado de Yield para esse ano!")
                        falha_bd = falha_bd + 1
                    elif yield_minimo < year_options['divYeld'] and bandeira_cotacao is False:
                        print('')
                    else:
                        print('[FALHA] Yield Mínimo')
                        falha_min_yield = falha_min_yield + 1

                    if 10 * year_options['receitaLiquida'] > year_options[
                        'divBruta'] > 0 and bandeira_ebit is True:  # DÍVIDA LÍQUIDA MENOR QUE RECEITA
                        bandeira_ebit = False
                        print('[OK] Receita Líquida')
                        for ancestor_year_options in json_options:
                            if ancestor_year_options['year'] == year - 1 and ancestor_year_options[
                                'quarter'] == quarter:
                                if 0 < ancestor_year_options['lucroLiquido'] <= year_options[
                                    'lucroLiquido']:  # LUCRO LÍQUIDO
                                    print('[OK] Lucro Liquido')  # CRESCENTE
                                    bandeira_lucro = True
                                elif ancestor_year_options['fco'] < year_options['fco'] and ancestor_year_options[
                                    'ebit'] < \
                                        year_options['ebit'] and ancestor_year_options['caixaLivre'] < \
                                        year_options['caixaLivre'] and ancestor_year_options['divBruta'] < \
                                        year_options['divBruta']:

                                    print('[OK] Filtros de recuperação!')
                                    bandeira_lucro = True
                                else:
                                    print('[FALHA] Lucro Líquido ou recuperação')
                                    falha_ll = falha_ll + 1
                                break
                    elif year_options['receitaLiquida'] > year_options['divBruta'] > 0 and bandeira_ebit is False:
                        print('')
                    else:
                        print('[FALHA] Caixa Livre')
                        falha_caixa = falha_caixa + 1

                    if bandeira_lucro is True:
                        bandeira_lucro = False
                        if year_options['roe'] > roe_minimo:
                            print('[OK] ROE Mínimo')
                            if year_options['vpa'] > year_options['cotacao']/2:
                                print('[OK] VPA é maior que a cotação média')
                                list_acoes.append(json_file)
                            else:
                                if year_options['fcl'] >= year_options['divBruta'] / 5 and 0 < year_options['capexFco'] < 1:
                                    print('[OK] VPA é maior que a cotação média')
                                    list_acoes.append(json_file)
                                else:
                                    print('[FALHA] Teste Final')
                                    falha_tf = falha_tf + 1
                        else:
                            print('[FALHA] ROE Mínimo')
                            falha_liq_roe = falha_liq_roe + 1
                bandeira_lucro = False
                bandeira_ebit = False
                bandeira_cotacao = False
                bandeira_liquidez_diaria = False
        data_frame.append([list_acoes])
        list_acoes = []

super_spaces()
print("Número total de operações: " + str(action_counter))
super_spaces()
print("Falhas no tipo de ação verificado: " + str(falha_action_filter))
print("Falhas na liquidez e/ou ROE Mínimo: " + str(falha_liq_roe))
print("Falhas no PL em relação ao LPA: " + str(falha_pl_lpa))
print("Falhas na cotaação média em relação ao VPA: " + str(falha_cot_vpa))
print("Falhas no EBIT ou na tentativa de recuperação 1: " + str(falha_ebit_rec))
print("Falhas em relação aos dados do banco de dados: " + str(falha_bd))
print("Falhas em relação ao Yield Máximo: " + str(falha_min_yield))
print("Falhas no lucro líquido ou na tentativa de recuperação 2: " + str(falha_ll))
print("Falhas no caixa livre: " + str(falha_caixa))
print("Falhas no teste de recuperação 3 (final): " + str(falha_tf))
print("")
sys.stdout.close()

df = pd.DataFrame(data_frame)
df.to_excel("Filtradas.xlsx")
