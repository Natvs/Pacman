import pygame
import numpy as np
from collections import deque

class TrainingVisualizer:
    def __init__(self, screen_width=800, screen_height=600, history_length=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.history_length = history_length
        
        # Initialize history trackers
        self.fitness_history = deque(maxlen=history_length)
        self.avg_fitness_history = deque(maxlen=history_length)
        self.generation = 0
        
        # Graph dimensions and positions
        self.graph_width = 300
        self.graph_height = 150
        self.graph_x = screen_width - self.graph_width - 10
        self.graph_y = 10
        
        # Colors
        self.BACKGROUND = (30, 30, 30)
        self.GRAPH_LINE = (0, 255, 0)
        self.AVG_LINE = (255, 165, 0)
        self.TEXT_COLOR = (255, 255, 255)
        
        # Font initialization
        self.font = pygame.font.Font(None, 24)

    def update_stats(self, population):
        # Update fitness histories
        if population:
            best_fitness = max(ind.fitness for ind in population)
            avg_fitness = sum(ind.fitness for ind in population) / len(population)
            self.fitness_history.append(best_fitness)
            self.avg_fitness_history.append(avg_fitness)
        self.generation += 1

    def draw_graph(self, surface):
        # Draw graph background
        pygame.draw.rect(surface, self.BACKGROUND, 
                        (self.graph_x, self.graph_y, self.graph_width, self.graph_height))
        
        if len(self.fitness_history) > 1:
            # Scale values to graph height
            max_fitness = max(max(self.fitness_history), max(self.avg_fitness_history))
            min_fitness = min(min(self.fitness_history), min(self.avg_fitness_history))
            scale = self.graph_height / (max_fitness - min_fitness + 1e-10)
            
            # Draw best fitness line
            points = []
            for i, fitness in enumerate(self.fitness_history):
                x = self.graph_x + (i * self.graph_width // self.history_length)
                y = self.graph_y + self.graph_height - int((fitness - min_fitness) * scale)
                points.append((x, y))
            if len(points) > 1:
                pygame.draw.lines(surface, self.GRAPH_LINE, False, points, 2)
            
            # Draw average fitness line
            avg_points = []
            for i, avg_fitness in enumerate(self.avg_fitness_history):
                x = self.graph_x + (i * self.graph_width // self.history_length)
                y = self.graph_y + self.graph_height - int((avg_fitness - min_fitness) * scale)
                avg_points.append((x, y))
            if len(avg_points) > 1:
                pygame.draw.lines(surface, self.AVG_LINE, False, avg_points, 2)

    def draw_stats(self, surface, current_fitness, best_sequence):
        # Draw generation counter
        gen_text = self.font.render(f"Generation: {self.generation}", True, self.TEXT_COLOR)
        surface.blit(gen_text, (10, 10))
        
        # Draw current fitness
        fitness_text = self.font.render(f"Current Fitness: {current_fitness:.2f}", True, self.TEXT_COLOR)
        surface.blit(fitness_text, (10, 40))
        
        # Draw best sequence
        if best_sequence:
            sequence_text = self.font.render(f"Best Move: {str(best_sequence[0])}", True, self.TEXT_COLOR)
            surface.blit(sequence_text, (10, 70))

    def draw_movement_preview(self, surface, game, best_sequence):
        if not best_sequence:
            return
            
        # Draw movement preview as arrows or dots
        start_x = game.pacman.rect.x
        start_y = game.pacman.rect.y
        
        for i, move in enumerate(best_sequence[:5]):  # Show first 5 moves
            # Calculate preview position
            preview_x = start_x + move[0] * 20 * (i + 1)
            preview_y = start_y + move[1] * 20 * (i + 1)
            
            # Draw preview dot
            color = (0, 255, 0, max(255 - i * 50, 50))  # Fade out with distance
            pygame.draw.circle(surface, color, (preview_x, preview_y), 3)

    def draw(self, surface, game, population, current_fitness, best_sequence):
        # Draw the fitness graph
        self.draw_graph(surface)
        
        # Draw statistics
        self.draw_stats(surface, current_fitness, best_sequence)
        
        # Draw movement preview
        self.draw_movement_preview(surface, game, best_sequence)
