from model.functions import loga
from model_matriz.functions import resolve
from ortools.sat.python import cp_model

modelo = cp_model.CpModel()
solucionador = cp_model.CpSolver()

total_avioes = 3
total_estacionamentos = 3
total_tempo = 5

momento_chegada = [1, 2, 0]
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

# Detectar o momento que cada avião decolou
# 1 = Está no estacionamento
# 2 = Está decolando
# 0 = Decolou!
for i in range(total_avioes):
    for j in range(total_estacionamentos):
        for k in range(total_tempo):
            if k > 0 and k < total_tempo - 1:
                aviao_decolou = modelo.NewBoolVar(f'aviao_{i}_estac_{j}_tempo_{k}_partiu_agora')
                loga(aviao_decolou)
                # Indica que o avião decolou!!
                modelo.Add(sum([X[i][j][k-1], X[i][j][k].Not()]) == 2).OnlyEnforceIf(aviao_decolou)
                # Indica que o avião NÃO decolou!!
                modelo.Add(sum([X[i][j][k-1], X[i][j][k].Not()]) != 2).OnlyEnforceIf(aviao_decolou.Not())

                # Se o avião decolou
                for futuro in range(k + 1, total_tempo):
                    # Se o avião decolou ele não volta mais
                    modelo.AddImplication(aviao_decolou, X[i][j][futuro].Not())
            if k < total_tempo - 1:
                aviao_pousou = modelo.NewBoolVar(f'aviao_{i}_estac_{j}_tempo_{k}_pousou_agora')
                loga(aviao_pousou)
                # Indica que o avião pousou!!
                modelo.Add(sum([X[i][j][k+1], X[i][j][k].Not()]) == 2).OnlyEnforceIf(aviao_pousou)
                # Indica que o avião NÃO pousou!!
                modelo.Add(sum([X[i][j][k+1], X[i][j][k].Not()]) != 2).OnlyEnforceIf(aviao_pousou.Not())

                for passado in range(0, k-1):
                    modelo.AddImplication(aviao_pousou, X[i][j][passado].Not())

# Garantir que o avião não chegue antes do tempo exigido
for i in range(total_avioes):
    chegada_aviao = momento_chegada[i]
    for j in range(total_estacionamentos):
        for k in range(chegada_aviao):
            modelo.Add(X[i][j][k] == 0)

# Garantir que o avião Chegue na hora que tem que chegar
for i in range(total_avioes):
    chegada_aviao = momento_chegada[i]
    todos_estacionamentos = [X[i][j][chegada_aviao] for j in range(total_estacionamentos)]
    modelo.Add(sum(todos_estacionamentos) == 1)


resolve(solucionador, modelo, X)