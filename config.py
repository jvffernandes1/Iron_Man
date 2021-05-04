from datetime import datetime

year_list = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]  # ANO
quarter_list = [1, 2, 3, 4]                                               # TRIMESTRE

qtd_acoes = 10000000000000                                           # QUANTIDADE MÍNIMA DE AÇÕES
pl_maximo = 1000                                                     # PL MAXIMO
yield_minimo = 0.20                                                  # YIELD MAXIMO (0.2 = 20%)
margemEbitMinima = 0.50                                              # MARGEM EBIT MÍNIMA (0.2 = 20%)
roe_minimo = 0.05                                                    # ROE MINIMO (0.2 = 20%)
setor = "FALHOU"

# DAQUI PRA BAIXO É PARA OUTROS SCRIPTS / FERRAMENTAS ------------------------------------------------------------------

now = datetime.now()
timestamp = int(datetime.timestamp(now))

site_base = "https://statusinvest.com.br/acoes/"
yahoo_base = "https://br.financas.yahoo.com/quote/"
suno_base = "https://www.sunoresearch.com.br/acoes/"
suno_api_quarter_base = "https://api-analitica.sunoresearch.com.br/api/Indicator/GetIndicatorsQuarter?ticker="
suno_api_base = "https://api-analitica.sunoresearch.com.br/index.html"

segmentos = ['Alimentos', 'Alimentos diversos', 'Alimentos Diversos', 'Bancos', 'Carnes e derivados',
             'Energia Elétrica', 'Energia elétrica', 'Medicamentos e outros produtos', 'Medicamentos e Outros Produtos',
             'Restaurante e Similares', 'Serv.Méd.Hospit..Análises e Diagnósticos',
             'Serviços médico-hospitalares, análises e diag']

govern = ['Novo Mercado', 'Nivel 2', 'Nivel 1']  # 'Tradicional'

span_govern = "ctl00_conteudoPrincipal_lblGovernanca"