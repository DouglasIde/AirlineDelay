# Funções do Modelo de Aeroportos e Aviões
from ortools.sat.python import cp_model


# Função que cria os estacionamentos para os aviões
def criar_estacionamento(estacionamentos, total_de_avioes, modelo):
    vars = []
    for i, estacionamento in enumerate(estacionamentos):
        var = modelo.NewIntVar(0, total_de_avioes, f'estacionamento_{i}')
        estacionamento.var = var
        vars.append(var)
    return vars

# Resolve o modelo de otimização e exibe a alocação de aviões nos estacionamentos
def resolve(solucionador, modelo, estacionamentos, avioes):
    status = solucionador.Solve(modelo)
    print(solucionador.StatusName(status))
    if status == cp_model.INFEASIBLE:
        print("Sem solução!!")
        return
    for estacionamento in estacionamentos:
        var = estacionamento.var
        valor = solucionador.Value(var)
        if valor == 0:
            print(f"{var} sem avião!!")
        else:
            aviao = avioes[valor - 1]
            print(f"{estacionamento} tem avião: {valor}, grande = {aviao.grande}")