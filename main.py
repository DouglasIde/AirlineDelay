import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
import yellowbrick
import matplotlib.pyplot as plt

from functions import Functions

def gerar_histograma():
    print("Histrograma sendo gerado por Hora de Chegada")
    largura_bin_at = func.calcular_largura_bin(dados, 'arrival_time')
    sns.histplot(data=dados, x='arrival_time', kde=True, binwidth=largura_bin_at)
    plt.show()
    print("Histrograma sendo gerado por Hora de partida")
    largura_bin_at = func.calcular_largura_bin(dados, 'departure_time')
    sns.histplot(data=dados, x='departure_time', kde=True, binwidth=largura_bin_at)
    plt.show()

if __name__ == '__main__':

    dados = pd.read_csv('flights.csv')
    print(dados.head())

    # Chamando as funções com FUNC
    func = Functions(dados)

    print("""
        1 - Verificar atrasos médios
        2 - Histograma Freedman-Diaconis com Bins
    """)

    switch = {
        1: lambda: (func.airline_delay(), func.type_average_delay(), func.holiday_average_delay()),
        2: lambda: gerar_histograma(),
    }

    user_choice = int(input("Escolha o que deseja verificar: "))

    if user_choice in switch:
        switch[user_choice]()
    else:
        print("Opção inválida.")




