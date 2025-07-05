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

# Garantir que os aviões não ocupem o mesmo estacionamento
def avioes_distintos(estacionamentos, modelo):
    var = [estacionamento.var for estacionamento in estacionamentos]
    modelo.AddAllDifferent(var)

# Garantir que todos os aviões estacionem sem faltar nenhum
def todo_aviao_tem_estacionar(total_de_avioes, estacionamentos, modelo):
    vars = {}
    for i in range(1, total_de_avioes + 1):
        for j, estacionamento in enumerate(estacionamentos):
            aviao_i_em_j = modelo.NewBoolVar(f'aviao_{i}_em{j}')
            modelo.Add(estacionamento.var == i).OnlyEnforceIf(aviao_i_em_j)
            modelo.Add(estacionamento.var != i).OnlyEnforceIf(aviao_i_em_j.Not())
            vars[(i,j)] = aviao_i_em_j

    for i in range(1, total_de_avioes + 1):
        modelo.AddExactlyOne([vars[i,j] for j in range(len(estacionamentos))])

# Garantir que determinado estacionamento não receba avioões grandes
def remover_estacionamento(modelo, var_estacionamento, avioes_grandes):
    for aviao in avioes_grandes:
        modelo.Add(var_estacionamento != aviao.k)

def limita_aviao_grande_estacionamento_grande(modelo, estacionamentos, avioes):
    avioes_grandes = [aviao for aviao in avioes if aviao.grande]
    for estacionamento in estacionamentos:
        for aviao in avioes_grandes:
            modelo.Add(estacionamento.var != aviao.k).OnlyEnforceIf(estacionamento.recebe_aviao_grande.Not())

# Um estacionamento só pode receber aviões grandes se seu vizinho também puder receber aviões grandes.
def limita_vizinhos(model, estacionamentos, avioes):
    for estacionamento in estacionamentos:
        if not estacionamento.grande:
            continue
        for vizinho in estacionamento.vizinhos:
            if vizinho.grande:
                model.Add(estacionamento.recebe_aviao_grande == 1).OnlyEnforceIf(vizinho.recebe_aviao_grande)

def limitar_avioes_que_requerem_passport(modelo, estacionamentos, avioes):
    # Verifica quais aviões tem controle de passaporte
    avioes_c_controle = [aviao for aviao in avioes if aviao.requer_controle_passport]

    # Verifica quais estacionamentos não tem controle de passaporte
    estacionamentos_s_controle = [estacionamento for estacionamento in estacionamentos if not estacionamento.tem_controle_passport]

    # Iterando para que estacionamento sem controle não tenha avião com controle
    for estacionamento in estacionamentos_s_controle:
        for aviao in avioes_c_controle:
            modelo.Add(estacionamento.var != aviao.k)
