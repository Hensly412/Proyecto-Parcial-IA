# Menú principal - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
from scripts.config import Config

class Menu:
    """
    Clase del menú principal
    """
    
    def __init__(self, screen, skin_manager=None, sound_manager=None):
        self.screen = screen
        self.skin_manager = skin_manager
        self.sound_manager = sound_manager
        self.selected_option = 0
        self.options = ["Start Game", "Select Skin", "Quit"]
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 24)
        
        # Gamepad
        self.gamepad = None
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
        
        # Reproducir música del menú
        if self.sound_manager:
            self.sound_manager.play_menu_music()
    
    def handle_event(self, event):
        """
        Maneja los eventos del menú
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:
                    return "START"
                elif self.selected_option == 1:
                    return "SKINS"
                elif self.selected_option == 2:
                    return "QUIT"
        
        elif event.type == pygame.JOYBUTTONDOWN:
            if self.gamepad:
                if event.button == 0:  # Botón A
                    if self.selected_option == 0:
                        return "START"
                    elif self.selected_option == 1:
                        return "SKINS"
                    elif self.selected_option == 2:
                        return "QUIT"
        
        elif event.type == pygame.JOYHATMOTION:
            if self.gamepad and event.hat == 0:
                if event.value[1] == 1:  # Arriba
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.value[1] == -1:  # Abajo
                    self.selected_option = (self.selected_option + 1) % len(self.options)
        
        return None
    
    def update(self, dt):
        """
        Actualiza el menú
        """
        pass
    
    def render(self):
        """
        Renderiza el menú
        """
        # Fondo
        self.screen.fill(Config.BLACK)
        
        # Título
        title_text = self.title_font.render("HV WARRIORS", True, Config.YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.info_font.render("Inspirado en Ikari Warriors", True, Config.WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(Config.SCREEN_WIDTH//2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Opciones del menú
        for i, option in enumerate(self.options):
            color = Config.YELLOW if i == self.selected_option else Config.WHITE
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(Config.SCREEN_WIDTH//2, 300 + i * 60))
            self.screen.blit(option_text, option_rect)
        
        # Controles
        controls_y = Config.SCREEN_HEIGHT - 160
        controls = [
            "Controles:",
            "WASD/Flechas - Mover",
            "Espacio - Disparar",
            "Gamepad compatible"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.info_font.render(control, True, Config.GRAY)
            control_rect = control_text.get_rect(center=(Config.SCREEN_WIDTH//2, controls_y + i * 25))
            self.screen.blit(control_text, control_rect)
        
        # Información del autor
        author_text = self.info_font.render("Por: Hensly Manuel Vidal Rosario (23-MISN-2-007)", True, Config.GRAY)
        author_rect = author_text.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT - 20))
        self.screen.blit(author_text, author_rect)