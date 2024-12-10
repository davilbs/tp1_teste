class EstoqueAlimento:
    def __init__(self, vegan=False):
        self.vegan = vegan
        self.alimentos = {}

    def buy_alimento(self, alimento, value=1):
        if alimento not in self.alimentos:
            self.alimentos[alimento] = 0
        self.alimentos[alimento] += value
        return True

    def sell_alimento(self, alimento, value=1):
        if alimento not in self.alimentos:
            return False
        if self.alimentos[alimento] == 0:
            return False
        self.alimentos[alimento] -= value
        return True
    
    def get_alimento(self, alimento):
        return self.alimentos.get(alimento, 0)