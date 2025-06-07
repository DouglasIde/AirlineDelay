class Estacionamento:
    def __init__(self, k, total_de_avioes, grande, modelo):
        # Numeração do estacionamento
        self.k = k

        # Qual avião está alocado neste estacionamento
        self.var = modelo.NewIntVar(0, total_de_avioes, f'estacionamento_{k}')

        # Verificar se o estacionamento é grande
        self.grande = grande
        self.vizinhos = []
        self.recebe_aviao_grande = modelo.NewBoolVar(f'recebe_aviao_grande_{k}')
        if not self.grande:
            modelo.Add(self.recebe_aviao_grande == 0)
