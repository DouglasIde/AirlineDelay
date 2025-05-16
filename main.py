import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
import yellowbrick
import matplotlib.pyplot as plt

from functions import Functions

if __name__ == '__main__':

    dados = pd.read_csv('flights.csv')
    print(dados.head())
    print(dados.info())

    # Chamando as funções com FUNC
    func = Functions(dados)

    # Funções com Atrasos Médios
    func.airline_delay()
    func.type_average_delay()
    func.holiday_average_delay()

    # Numéro de Voos por Aeronave



