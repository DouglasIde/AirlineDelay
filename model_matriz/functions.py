from ortools.sat.python import cp_model

from model.functions import variaveis_a_logar


# Função com o solucionador do modelo
# Imprime os resultados se a solução for Ótima
def resolve(solucionador, model, X):
    status = solucionador.Solve(model)
    print(f"Status: {status}")

    # Condição para se o modelo for ótimo
    if status == cp_model.OPTIMAL:
        print("OPTIMAL")
        for i, matriz_estacionamento_tempo in enumerate(X):
            for j, tempos in enumerate(matriz_estacionamento_tempo):
                for k, var in enumerate(tempos):
                    value = solucionador.Value(var)
                    if value == 1:
                        print(f"Avião {i} no estacionamento {j} no tempo {k}")
        for var in variaveis_a_logar:
            value = solucionador.Value(var)
            print(f"Variavel {var} = {value}")
    else:
        print("Solução não encontrada!! :(")

