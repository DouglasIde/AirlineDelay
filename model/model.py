from ortools.sat.python import cp_model

from functions import *
from models.aviao import Aviao
from models.estacionamento import Estacionamento

model = cp_model.CpModel()

# Se for TRUE significa que o avião é grande, FALSE é que é pequeno
avioes = [Aviao(1, True, True), Aviao(2, False, False), Aviao(3, True, True)]

total_de_avioes = len(avioes)

# Se for TRUE significa que o estacionamento é grande, FALSE é que é pequeno
estacionamentos = [Estacionamento(1, total_de_avioes, False, model, True),
                   Estacionamento(2, total_de_avioes, True, model, False),
                   Estacionamento(3, total_de_avioes, True, model, False)]

estacionamentos[2].vizinhos = [estacionamentos[1]]

avioes_distintos(estacionamentos, model)
todo_aviao_tem_estacionar(total_de_avioes, estacionamentos, model)
limita_vizinhos(model, estacionamentos, avioes)
limita_aviao_grande_estacionamento_grande(model, estacionamentos, avioes)

# Limitar os aviões que precisam de controle de passaporte
limitar_avioes_que_requerem_passport(model, estacionamentos, avioes)

solucionador = cp_model.CpSolver()
status = resolve(solucionador, model, estacionamentos, avioes)

print(solucionador.StatusName(status))




