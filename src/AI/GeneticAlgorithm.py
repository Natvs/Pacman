# Importation de la classe Individual
from AI.Individual import Individual

import random
import math
class GeneticAlgorithm:
    def __init__(self, game, population_size, sequence_length):
        # Crée une population initiale d'individus
        self.population = [Individual(game, sequence_length) for _ in range(population_size)]

    def select_parents(self):
        # Sélectionner deux parents à partir de la population en fonction de leur fitness
        sorted_population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        return sorted_population[0], sorted_population[1]

    def generate_next_generation(self):
        # Créer une nouvelle génération en croisant et en mutant
        new_population = []
        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child = parent1.crossover(parent2)
            child.mutate()
            new_population.append(child)
        self.population = new_population

    def get_best_move(self):
    # Afficher la fitness de chaque individu
        for ind in self.population:
            print(f"Individu : {ind.sequence} | Fitness : {ind.fitness}")
    
    # Sélectionne le meilleur individu
        best_individual = max(self.population, key=lambda ind: ind.fitness)

    # Vérifie si la séquence est présente
        if not best_individual.sequence:
            print("Erreur : L'individu sélectionné n'a pas de séquence.")
        return (0, 0)

        print(f"Meilleur individu sélectionné : {best_individual.sequence} avec fitness {best_individual.fitness}")
    
    # Retourne le premier mouvement de la séquence
        return best_individual.sequence[0]

