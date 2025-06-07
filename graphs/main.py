import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
import yellowbrick
import matplotlib.pyplot as plt

from functions import Functions
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor

def gerar_histograma():
    print("Histrograma sendo gerado por Hora de Chegada")
    largura_bin_at = func.calcular_largura_bin(dados, 'arrival_time')
    sns.histplot(data=dados, x='arrival_time', kde=True, binwidth=largura_bin_at)
    plt.show()
    print("Histrograma sendo gerado por Hora de partida")
    largura_bin_at = func.calcular_largura_bin(dados, 'departure_time')
    sns.histplot(data=dados, x='departure_time', kde=True, binwidth=largura_bin_at)
    plt.show()

def avaliar_modelos_dummy(X_train, y_train, X_test, y_test):
    estrategias = ["mean", "median", ("quantile", 0.25), ("constant", 10.0)]
    resultados = {}

    for estrategia in estrategias:
        if isinstance(estrategia, tuple):
            estrategia, valor = estrategia
            if estrategia == 'quantile':
                model_dummy = DummyRegressor(strategy=estrategia, quantile=valor)
            else:
                model_dummy = DummyRegressor(strategy=estrategia, constant=valor)
        else:
            model_dummy = DummyRegressor(strategy=estrategia)

if __name__ == '__main__':

    dados = pd.read_csv('flights.csv')
    print(dados.head())

    # Chamando as funções com FUNC
    func = Functions(dados)

    # Alterando nomes de algumas colunas dos dados
    dados['date'] = pd.to_datetime(dados['year'].astype(str) + '-' + (dados['day'] + 1).astype(str), format='%Y-%j')
    dados['is_weekend'] = dados['date'].dt.weekday.isin([5,6])
    dados['day_name'] = dados['date'].dt.day_name()
    dados['schengen'] = dados['schengen'].replace({'non-schengen': 0, 'schengen': 1})
    dados['is_holiday'] = dados['is_holiday'].replace({False: 0, True: 1})
    dados['is_weekend'] = dados['is_weekend'].replace({False: 0, True: 1})

    # Variaveis para as functions
    variaveis_categoricas = ['airline', 'aircraft_type', 'origin', 'day_name']
    df_encoded = pd.get_dummies(data=dados, columns=variaveis_categoricas, dtype=int)
    df_encoded[['arrival_time', 'departure_time']].corr()
    df_clean = df_encoded.drop(['flight_id', 'departure_time', 'day', 'year', 'date'], axis=1)

    X = df_clean.drop(['delay'], axis=1)
    y = df_clean['delay']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    model_dummy = DummyRegressor()
    model_dummy.fit(X_train, y_train)
    y_pred_dummy = model_dummy.predict(X_test)

    print("""
        1 - Verificar atrasos médios
        2 - Histograma Freedman-Diaconis com Bins
        3 - Distribuição dos valores de atrasos
        4 - Verificar as Métricas de Regressão
    """)

    switch = {
        1: lambda: (func.airline_delay(), func.type_average_delay(), func.holiday_average_delay()),
        2: lambda: gerar_histograma(),
        3: lambda: func.visualizar_delay(dados),
        4: lambda: func.calcular_metricas_regressao(y_test, y_pred_dummy)
    }

    user_choice = int(input("Escolha o que deseja verificar: "))

    if user_choice in switch:
        switch[user_choice]()
    else:
        print("Opção inválida.")




