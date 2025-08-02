from model.functions import loga
from model_matriz.functions import resolve
from ortools.sat.python import cp_model

modelo = cp_model.CpModel()
solucionador = cp_model.CpSolver()

total_avioes = 3
total_estacionamentos = 3
total_tempo = 5

var_a_logar = []

X = [[[modelo.NewBoolVar(f'aviao_{i}_estacionamento_{j}_tempo_{k}')
    for k in range(total_tempo)]
    for j in range(total_estacionamentos)]
    for i in range(total_avioes)]

# Imprime a Estrutura da matriz em 3D (avioes, estacionamentos e tempo)
print(len(X))
print(len(X[0]))
print(len(X[0][0]))

# [RESTRIÇÃO] Um avião tem que estar em algum lugar
for i in range(total_avioes):
    posicao_aviao = [X[i][j][k] for j in range(total_estacionamentos) for k in range(total_tempo)]
    modelo.Add(sum(posicao_aviao) >= 1)

# [RESTRIÇÃO] No estacionamento J no tempo K não pode ter 2 aviões
for j in range(total_estacionamentos):
    for k in range(total_tempo):
        avioes_now = [X[i][j][k] for i in range(total_avioes)]
        modelo.Add(sum(avioes_now) <= 1)

# O avião I tem que ficar no minimo 3 janelas de tempo em Qualquer Estacionamento J
for i in range(total_avioes):
    tudo_aviao = [X[i][j][k] for j in range(total_estacionamentos) for k in range(total_tempo)]
    modelo.Add(sum(tudo_aviao) >= 3)

# [RESTRIÇÃO] Se o avião I ocupou o estacionamento J em algum momento
for i in range(total_avioes):
    for j in range(total_estacionamentos):

        aviao_i_j = modelo.NewBoolVar(f'aviao_{i}_estacionamento_{j}')
        loga(aviao_i_j)
        var_aviao_estacionamento = [X[i][j][k] for k in range(total_tempo)]

        # Verifica se o avião I passou por este estacionamento J
        modelo.Add(sum(var_aviao_estacionamento) > 0).OnlyEnforceIf(aviao_i_j)

        # Se não passou a soma das variaveis é igual a 0
        modelo.Add(sum(var_aviao_estacionamento) == 0).OnlyEnforceIf(aviao_i_j.Not())

resolve(solucionador, modelo, X)