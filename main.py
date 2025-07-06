# HV Warriors - Proyecto Final IA
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007
# Inspirado en Ikari Warriors

import pygame
import sys
import os
from scripts.game import Game
from scripts.menu import Menu
from scripts.skin_menu import SkinMenu
from scripts.skin_manager import SkinManager
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
    skin_manager = SkinManager()
    sound_manager = SoundManager()
    menu = Menu(screen, skin_manager, sound_manager)
    skin_menu = SkinMenu(screen, skin_manager)
    game = None
    
    # Estados del juego
    game_state = "MENU"  # MENU, SKINS, PLAYING, GAME_OVER
    
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
                elif action == "SKINS":
                    game_state = "SKINS"
                elif action == "QUIT":
                    running = False
            
            elif game_state == "SKINS":
                action = skin_menu.handle_event(event)
                if action == "SELECTED":
                    print(f"🎨 MAIN: Skin seleccionada en menú")
                    # Actualizar skin del jugador si está en juego
                    if game and hasattr(game, 'player'):
                        print(f"🎨 MAIN: Forzando actualización del jugador existente")
                        # Resetear el seguimiento de skin para forzar detección
                        game.player.current_skin_name = None
                        # Forzar recarga inmediata
                        game.player.load_sprite()
                        print(f"🎨 MAIN: Player actualizado a skin {game.player.skin_manager.current_player_skin}")
                    game_state = "MENU"
                elif action == "BACK":
                    game_state = "MENU"
            
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
        
        elif game_state == "SKINS":
            skin_menu.update(dt)
            skin_menu.render()
        
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