import pygame
from game2 import Game2
from AI.GeneticAlgorithm import GeneticAlgorithm

def genetic():
    pygame.init()
    
    # Initialiser la fenêtre Pygame (screen)
    screen = pygame.display.set_mode((800, 600))  # Par exemple, une fenêtre de 800x600 pixels
    
    # Initialiser le jeu en passant l'objet screen
    game = Game2(screen)
    clock = pygame.time.Clock()

    # Initialiser l'algorithme génétique
    ga = ga = GeneticAlgorithm(game, population_size=10, sequence_length=10)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Log pour vérifier si le mouvement est valide
        best_move = ga.get_best_move()
        print(f"Best move: {best_move}")
        
        # Vérifier si l'objet pacman existe et mettre à jour la direction
        if hasattr(game, 'pacman') and game.pacman is not None:
            game.pacman.set_direction(best_move)
        else:
            print("Pacman object is missing or invalid.")

        # Mettre à jour et dessiner le jeu
        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    genetic()

