# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

valor_inicial = 100000

df = pd.read_excel('CSV/indice_cdi.xlsx', usecols="O")  # VALORES DO INDICE CDI
cdi_inq = df["CDI"].tolist()
cdi = cdi_inq.copy()
cdi_string = cdi_inq.copy()

cdi[0] = valor_inicial

for a in range(1, len(cdi_inq)):
    cdi[a] = round((cdi_inq[a] / 100) * cdi[a - 1] + cdi[a - 1], 0)

trimestres = ['2011.1', '2011.2', '2011.3', '2011.4', '2012.1', '2012.2', '2012.3', '2012.4', '2013.1', '2013.2',
              '2013.3', '2013.4', '2014.1', '2014.2', '2014.3', '2014.4', '2015.1', '2015.2', '2015.3', '2015.4',
              '2016.1', '2016.2', '2016.3', '2016.4', '2017.1', '2017.2', '2017.3', '2017.4', '2018.1', '2018.2',
              '2018.3', '2018.4', '2019.1', '2019.2', '2019.3', '2019.4']  # 36 VALORES

FV_trimestres = ['01/04/2011', '01/07/2011', '01/10/2011', '01/01/2012']

FV_Csv = pd.read_csv("CSV/fundValue.csv")
FV_Date = list(FV_Csv['Date'])
FV_Value = list(FV_Csv['Value'])
for a in range(len(FV_Value)):
    FV_Value[a] = FV_Value[a]*1000

# multiple line plot
# plt.plot(trimestres, cdi_corrigido,  marker='', color='red', linewidth=1, label="100% do CDI corrigido")
plt.plot(FV_Date, FV_Value, color='orange', linewidth=2, label="ProTECH")
# plt.plot(trimestres, ironman, color='orange', linewidth=1, label="Iron Man", marker='o')
plt.plot(['04/04/2011', '27/12/2019'], [100000, cdi[len(cdi) - 1]], color='black', linewidth=1, label="100% do CDI")
plt.legend(loc='upper left')
plt.xticks(['04/04/2011', '02/04/2012', '01/04/2013', '01/04/2014', '01/04/2015', '01/04/2016', '03/04/2017', '02/04/2018', '01/04/2019', '27/12/2019'], rotation=60, fontsize=8)
# plt.xticks(['2011.4', '2012.4', '2013.4', '2014.4', '2015.4', '2016.4', '2017.4', '2018.4', '2019.4'], rotation=60, fontsize=8)
plt.yticks(np.arange(100000, 400000, 25000))
plt.title('CDI x ProTECH')
plt.xlabel('Trimestre')
plt.ylabel('Montante acumulado (R$)')
plt.grid()
plt.show()

bovespa = pd.read_csv("CSV/BVSP.csv")
Date = list(bovespa['Date'])
Adj_close = list(bovespa['Adj Close'])
base_adj = Adj_close[0]

Adj_close_prt = []

for looper in range(len(Adj_close)):
    x = ((100 * Adj_close[looper]) / base_adj)
    Adj_close_prt.append(x)

# plt.plot(trimestres, ironman)#, color='purple', linewidth=1, label="Iron Man", marker='o')
plt.plot(Date, Adj_close_prt, color='silver', linewidth=1, label="Bovespa")
plt.legend(loc='upper left')
plt.xticks(
    ['2011-04-01', '2012-04-02', '2013-04-01', '2014-04-01', '2015-04-01', '2016-04-01', '2017-04-03', '2018-04-02',
     '2019-04-01'], rotation=60, fontsize=8)
plt.title('IBOV x Iron Man')
plt.xlabel('Dias')
plt.ylabel('Valorização percentual em relação à ' + Date[0])
plt.grid()
# plt.show()
