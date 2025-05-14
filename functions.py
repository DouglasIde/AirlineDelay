import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
import yellowbrick
import matplotlib.pyplot as plt

class Functions:

    def __init__(self, df):
        self.df = df

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