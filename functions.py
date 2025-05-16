import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
import yellowbrick
import matplotlib.pyplot as plt

class Functions:

    def __init__(self, df):
        self.df = df

    # Atrasos médios por companhia aérea
    def airline_delay(self):
        average_delay = self.df.groupby('airline')['delay'].mean().reset_index()
        sns.barplot(x='airline', y='delay', data=average_delay)
        plt.title("Companhias Aéreas VS Atrasos Médios")
        plt.xlabel('Companhia Aéreas')
        plt.ylabel("Atraso Médio em Minutos")
        plt.show()

        sns.countplot(data=self.df, x='airline')
        plt.title("Número de voos por companhia aérea")
        plt.xlabel("Companhia Aérea")
        plt.ylabel("Número de Voos")
        plt.show()

    # Atrasos médios por tipo de voo
    def type_average_delay(self):
        average_delay = self.df.groupby('schengen')['delay'].mean().reset_index()
        sns.barplot(x='schengen', y='delay', data=average_delay)
        plt.title("Tipo de Voo VS Atrasos Médios")
        plt.xlabel('Tipo de Voo')
        plt.ylabel("Atraso Médio em Minutos")
        plt.show()

        sns.countplot(data=self.df, x='schengen')
        plt.title("Número de voos por tipo de voo")
        plt.xlabel("Companhia Aérea")
        plt.ylabel("Número de Voos")
        plt.show()

    # Atrasos Médios por Feriado
    def holiday_average_delay(self):
        average_delay = self.df.groupby('is_holiday')['delay'].mean().reset_index()
        sns.barplot(x='is_holiday', y='delay', data=average_delay)
        plt.title("Feriados VS Atrasos Médios")
        plt.xlabel('É Feriado?')
        plt.ylabel("Atraso Médio em Minutos")
        plt.show()

    # Numero de Voos por Aeronave
    def flight_numbers_by_ship(self):
        order = self.df['aircraft_type'].value_counts().index
        sns.countplot(data=self.df, x='aircraft_type', order=order)
        sns.countplot(data=self.df, x='aircraft_type')
        plt.title("Número de voos por aeronave")
        plt.xticks(rotation=70)
        plt.xlabel("Tipo de Aeronave")
        plt.ylabel("Número de Voos")
        plt.show()

    def calcular_largura_bin(self, coluna):
        Q75, Q25 = np.percentile(self.df[coluna], [75, 25])
        IQR = Q75 - Q25
        largura_bin = 2 * IQR / np.power(len(self.df[coluna]), -1/3)
        return largura_bin