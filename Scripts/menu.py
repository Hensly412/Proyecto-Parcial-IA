# Menú principal - HV Warriors (CON IMAGEN DE FONDO)
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import os
from scripts.config import Config

class Menu:
    """
    Clase del menú principal con soporte para imagen de fondo
    """
    
    def __init__(self, screen, skin_manager=None, sound_manager=None):
        self.screen = screen
        self.sound_manager = sound_manager
        self.selected_option = 0
        self.options = ["Start Game", "Quit"]  # Solo 2 opciones
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 72)
        self.option_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 24)
        
        # Cargar imagen de fondo
        self.background = None
        self.load_background()
        
        # Gamepad
        self.gamepad = None
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
        
        # Reproducir música del menú (con verificación)
        if self.sound_manager and hasattr(self.sound_manager, 'play_menu_music'):
            self.sound_manager.play_menu_music()
    
    def load_background(self):
        """
        Carga la imagen de fondo del menú
        """
        try:
            # Intentar cargar la imagen de fondo
            background_path = os.path.join("assets", "images", "menu_background.jpg")
            if os.path.exists(background_path):
                self.background = pygame.image.load(background_path)
                # Escalar la imagen al tamaño de la pantalla
                self.background = pygame.transform.scale(self.background, 
                                                       (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
                print("✓ Imagen de fondo del menú cargada")
            else:
                print("✗ No se encontró menu_background.jpg")
                self.create_default_background()
        except Exception as e:
            print(f"✗ Error cargando imagen de fondo: {e}")
            self.create_default_background()
    
    def create_default_background(self):
        """
        Crea un fondo por defecto si no hay imagen
        """
        self.background = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        # Crear gradiente verde militar
        for y in range(Config.SCREEN_HEIGHT):
            green_value = int(80 - (y / Config.SCREEN_HEIGHT) * 60)
            color = (0, green_value, 0)
            pygame.draw.line(self.background, color, (0, y), (Config.SCREEN_WIDTH, y))
        
        # Añadir líneas decorativas
        for i in range(0, Config.SCREEN_HEIGHT, 50):
            pygame.draw.line(self.background, (0, 100, 0), (0, i), (Config.SCREEN_WIDTH, i), 2)
    
    def handle_event(self, event):
        """
        Maneja los eventos del menú
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                if self.sound_manager:
                    self.sound_manager.play_sound("menu_select")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                if self.sound_manager:
                    self.sound_manager.play_sound("menu_select")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.sound_manager:
                    self.sound_manager.play_sound("menu_confirm")
                if self.selected_option == 0:
                    return "START"
                elif self.selected_option == 1:
                    return "QUIT"
        
        elif event.type == pygame.JOYBUTTONDOWN:
            if self.gamepad:
                if event.button == 0:  # Botón A
                    if self.sound_manager:
                        self.sound_manager.play_sound("menu_confirm")
                    if self.selected_option == 0:
                        return "START"
                    elif self.selected_option == 1:
                        return "QUIT"
        
        elif event.type == pygame.JOYHATMOTION:
            if self.gamepad and event.hat == 0:
                if event.value[1] == 1:  # Arriba
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    if self.sound_manager:
                        self.sound_manager.play_sound("menu_select")
                elif event.value[1] == -1:  # Abajo
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    if self.sound_manager:
                        self.sound_manager.play_sound("menu_select")
        
        return None
    
    def update(self, dt):
        """
        Actualiza el menú (para animaciones futuras)
        """
        pass
    
    def render(self):
        """
        Renderiza el menú con imagen de fondo
        """
        # Dibujar imagen de fondo
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(Config.BLACK)
        
        # Overlay oscuro semi-transparente para mejorar legibilidad
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        overlay.set_alpha(180)  # 70% opacidad
        overlay.fill(Config.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Título con sombra
        shadow_offset = 3
        title_shadow = self.title_font.render("HV WARRIORS", True, Config.BLACK)
        title_shadow_rect = title_shadow.get_rect(center=(Config.SCREEN_WIDTH//2 + shadow_offset, 
                                                         150 + shadow_offset))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        title_text = self.title_font.render("HV WARRIORS", True, Config.YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.info_font.render("Inspirado en Ikari Warriors", True, Config.WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(Config.SCREEN_WIDTH//2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Opciones del menú con efecto hover
        for i, option in enumerate(self.options):
            # Determinar color y tamaño
            if i == self.selected_option:
                color = Config.YELLOW
                # Añadir indicador de selección
                indicator = "► "
                scale = 1.1
            else:
                color = Config.WHITE
                indicator = "  "
                scale = 1.0
            
            # Renderizar opción
            option_text = self.option_font.render(indicator + option, True, color)
            
            # Aplicar escala si está seleccionado
            if scale > 1.0:
                width = int(option_text.get_width() * scale)
                height = int(option_text.get_height() * scale)
                option_text = pygame.transform.scale(option_text, (width, height))
            
            option_rect = option_text.get_rect(center=(Config.SCREEN_WIDTH//2, 300 + i * 80))
            self.screen.blit(option_text, option_rect)
        
        # Controles con fondo semi-transparente
        controls_bg = pygame.Surface((400, 120))
        controls_bg.set_alpha(128)
        controls_bg.fill(Config.BLACK)
        controls_bg_rect = controls_bg.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT - 100))
        self.screen.blit(controls_bg, controls_bg_rect)
        
        controls_y = Config.SCREEN_HEIGHT - 160
        controls = [
            "Controles:",
            "WASD/Flechas - Mover",
            "Espacio - Disparar",
            "Gamepad compatible"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.info_font.render(control, True, Config.WHITE if i > 0 else Config.YELLOW)
            control_rect = control_text.get_rect(center=(Config.SCREEN_WIDTH//2, controls_y + i * 25))
            self.screen.blit(control_text, control_rect)
        
        # Información del autor
        author_text = self.info_font.render("Por: Hensly Manuel Vidal Rosario (23-MISN-2-007)", True, Config.GRAY)
        author_rect = author_text.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT - 20))
        self.screen.blit(author_text, author_rect)