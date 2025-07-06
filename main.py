# HV Warriors - Proyecto Final IA
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007
# Inspirado en Ikari Warriors

import pygame
import sys
import os
from scripts.game import Game
from scripts.menu import Menu
from scripts.sound_manager import SoundManager
from scripts.config import Config

def main():
    """
    Función principal del juego HV Warriors
    """
    # Inicializar pygame
    pygame.init()
    pygame.mixer.init()
    
    # Configurar la pantalla
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("HV Warriors")
    clock = pygame.time.Clock()
    
    # Inicializar sistemas
    sound_manager = SoundManager()
    menu = Menu(screen, None, sound_manager)  # Sin skin_manager
    game = None
    
    # Estados del juego
    game_state = "MENU"  # MENU, PLAYING, GAME_OVER
    
    running = True
    while running:
        dt = clock.tick(Config.FPS) / 1000.0  # Delta time en segundos
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Manejar eventos según el estado del juego
            if game_state == "MENU":
                action = menu.handle_event(event)
                if action == "START":
                    game = Game(screen)
                    game_state = "PLAYING"
                elif action == "QUIT":
                    running = False
            
            elif game_state == "PLAYING":
                if game:
                    game_result = game.handle_event(event)
                    if game_result == "GAME_OVER":
                        game_state = "GAME_OVER"
                    elif game_result == "QUIT":
                        game_state = "MENU"
        
        # Actualizar y renderizar según el estado
        if game_state == "MENU":
            menu.update(dt)
            menu.render()
        
        elif game_state == "PLAYING":
            if game:
                game_result = game.update(dt)
                if game_result == "GAME_OVER":
                    game_state = "GAME_OVER"
                game.render()
        
        elif game_state == "GAME_OVER":
            # Mostrar pantalla de game over y esperar reinicio
            if game:
                action = game.show_game_over()
                if action == "RESTART":
                    game = Game(screen)
                    game_state = "PLAYING"
                elif action == "MENU":
                    game_state = "MENU"
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()