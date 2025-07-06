# Menú de selección de skins - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
from scripts.config import Config

class SkinMenu:
    """
    Menú para seleccionar skins del jugador
    """
    
    def __init__(self, screen, skin_manager):
        self.screen = screen
        self.skin_manager = skin_manager
        self.selected_skin_index = 0
        self.available_skins = skin_manager.get_available_player_skins()
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 48)
        self.skin_font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 24)
        
        # Gamepad
        self.gamepad = None
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
    
    def handle_event(self, event):
        """
        Maneja los eventos del menú de skins
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.selected_skin_index = (self.selected_skin_index - 1) % len(self.available_skins)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.selected_skin_index = (self.selected_skin_index + 1) % len(self.available_skins)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Seleccionar skin
                selected_skin = self.available_skins[self.selected_skin_index]
                self.skin_manager.set_player_skin(selected_skin)
                return "SELECTED"
            elif event.key == pygame.K_ESCAPE:
                return "BACK"
        
        elif event.type == pygame.JOYBUTTONDOWN:
            if self.gamepad:
                if event.button == 0:  # Botón A
                    selected_skin = self.available_skins[self.selected_skin_index]
                    self.skin_manager.set_player_skin(selected_skin)
                    return "SELECTED"
                elif event.button == 1:  # Botón B
                    return "BACK"
        
        elif event.type == pygame.JOYHATMOTION:
            if self.gamepad and event.hat == 0:
                if event.value[0] == -1:  # Izquierda
                    self.selected_skin_index = (self.selected_skin_index - 1) % len(self.available_skins)
                elif event.value[0] == 1:  # Derecha
                    self.selected_skin_index = (self.selected_skin_index + 1) % len(self.available_skins)
        
        return None
    
    def update(self, dt):
        """
        Actualiza el menú
        """
        pass
    
    def render(self):
        """
        Renderiza el menú de selección de skins
        """
        # Fondo semitransparente
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(Config.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title_text = self.title_font.render("SELECCIONAR SKIN", True, Config.YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Mostrar skins disponibles
        skin_y = 200
        skin_spacing = 120
        start_x = Config.SCREEN_WIDTH // 2 - (len(self.available_skins) * skin_spacing) // 2
        
        for i, skin_name in enumerate(self.available_skins):
            skin_x = start_x + i * skin_spacing
            
            # Obtener sprite de la skin
            skin_sprite = self.skin_manager.get_player_skin(skin_name)
            
            # Escalar sprite para vista previa
            preview_size = 64
            scaled_sprite = pygame.transform.scale(skin_sprite, (preview_size, preview_size))
            
            # Fondo para la skin
            bg_color = Config.YELLOW if i == self.selected_skin_index else Config.GRAY
            bg_rect = pygame.Rect(skin_x - preview_size//2 - 5, skin_y - 5, 
                                 preview_size + 10, preview_size + 10)
            pygame.draw.rect(self.screen, bg_color, bg_rect, 3)
            
            # Sprite de la skin
            sprite_rect = scaled_sprite.get_rect(center=(skin_x, skin_y + preview_size//2))
            self.screen.blit(scaled_sprite, sprite_rect)
            
            # Nombre de la skin
            name_text = self.skin_font.render(skin_name.upper(), True, 
                                            Config.YELLOW if i == self.selected_skin_index else Config.WHITE)
            name_rect = name_text.get_rect(center=(skin_x, skin_y + preview_size + 30))
            self.screen.blit(name_text, name_rect)
        
        # Descripción de la skin seleccionada
        selected_skin = self.available_skins[self.selected_skin_index]
        descriptions = {
            "default": "Skin clásica del guerrero",
            "fire": "Poder del fuego ardiente",
            "nature": "Armonía con la naturaleza",
            "magic": "Energía mágica ancestral",
            "golden": "Skin legendaria dorada",
            "cyber": "Tecnología del futuro"
        }
        
        description = descriptions.get(selected_skin, "Skin personalizada")
        desc_text = self.info_font.render(description, True, Config.WHITE)
        desc_rect = desc_text.get_rect(center=(Config.SCREEN_WIDTH//2, 400))
        self.screen.blit(desc_text, desc_rect)
        
        # Controles
        controls_y = Config.SCREEN_HEIGHT - 100
        controls = [
            "Izquierda/Derecha - Cambiar skin",
            "Enter/Espacio - Seleccionar",
            "Escape - Volver"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.info_font.render(control, True, Config.GRAY)
            control_rect = control_text.get_rect(center=(Config.SCREEN_WIDTH//2, controls_y + i * 25))
            self.screen.blit(control_text, control_rect)