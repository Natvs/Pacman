import random
class Individual:
    
    def __init__(self, game, sequence_length):
        self.possible_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.sequence = [random.choice(self.possible_moves) for _ in range(sequence_length)]
        print(f"Séquence générée : {self.sequence}")  # Log pour vérifier la diversité des séquences
        self.fitness = self.evaluate(game)

    def evaluate(self, game):
        # Exemple simple d'évaluation : la fitness est basée sur le premier mouvement
        if not self.sequence:
            return 0
    
    # Log pour vérifier quel mouvement est évalué
        print(f"Évaluation de la séquence : {self.sequence}")
    
    # Exemple : on pourrait baser la fitness sur le mouvement (1, 0)
    # Ici, on suppose que le but est de se déplacer vers la droite
        target_move = (1, 0)
        fitness = 1 if self.sequence[0] == target_move else 0
    
        return fitness

    def mutate(self):
        # Appliquer une mutation aléatoire à l'un des mouvements
        index = random.randint(0, self.sequence_length - 1)
        self.moves[index] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def crossover(self, other):
        # Effectuer un croisement entre deux individus (combinaison de leurs séquences de mouvements)
        point = random.randint(0, self.sequence_length)
        child = Individual(None, self.sequence_length)
        child.moves = self.moves[:point] + other.moves[point:]
        return child
