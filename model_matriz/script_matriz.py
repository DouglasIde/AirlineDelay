from ortools.sat.python import cp_model

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

modelo = cp_model.CpModel()
solucionador = cp_model.CpSolver()

total_avioes = 3
total_estacionamentos = 4

X = [[modelo.NewBoolVar(f'aviao_{i}_em_estacionamento_{j}') for j in range(total_estacionamentos)]
        for i in range(total_avioes)]

for i, linha in enumerate(X):
    print(f"Aviao {i} - {linha}")

for linha_do_aviao in X:
    modelo.AddExactlyOne(linha_do_aviao)

for j in range(total_estacionamentos):
    modelo.AddAtMostOne([X[i][j] for i in range(total_avioes)])

resolve(solucionador, modelo, X)