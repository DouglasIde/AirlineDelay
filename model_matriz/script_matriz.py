from ortools.sat.python import cp_model

modelo = cp_model.CpModel()
solucionador = cp_model.CpSolver()

total_avioes = 3
total_estacionamentos = 4

requer_onibus = [0, 1, 0, 1]
distancias = [10, 200, 20, 100]
passageiros = [100, 105, 49]

def resolve(solucionador, modelo, X):
    status = solucionador.Solve(modelo)
    print(f"Status: {status}")

    if status == cp_model.OPTIMAL:
        print("OPTIMAL")

        for i, row in enumerate(X):
            for j, var in enumerate(row):
                valor = solucionador.Value(var)
                if valor == 1:
                    print(f"{var} = {valor}")

    else:
        print("Solução não encontrada! :(")

    print(f"Custo total: {solucionador.ObjectiveValue()}")

def multiplicar_matrizes_item(matriz1, matriz2):
    return [matriz1[i][j] * matriz2[i][j]
            for i in range(total_avioes)
            for j in range(total_estacionamentos)]

custos = []
for i in range(total_avioes):
    custos_do_aviao = []
    for j in range(total_estacionamentos):
        if requer_onibus[j]:
            custo = 500 * distancias[j] * passageiros[i]
        else:
            custo = 100 * distancias[j] * passageiros[i]

        # Adicionar o resultado de custo na lista de custos do avião
        custos_do_aviao.append(custo)
    custos.append(custos_do_aviao)


X = [[modelo.NewBoolVar(f'aviao_{i}_em_estacionamento_{j}') for j in range(total_estacionamentos)]
        for i in range(total_avioes)]

modelo.Minimize(sum(multiplicar_matrizes_item(X, custos)))

for i, linha in enumerate(X):
    print(f"Aviao {i} - {linha}")

for linha_do_aviao in X:
    modelo.AddExactlyOne(linha_do_aviao)

for j in range(total_estacionamentos):
    modelo.AddAtMostOne([X[i][j] for i in range(total_avioes)])

resolve(solucionador, modelo, X)