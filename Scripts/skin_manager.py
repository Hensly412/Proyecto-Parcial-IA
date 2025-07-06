# Sistema de skins - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import os
from scripts.config import Config

class SkinManager:
    """
    Gestor de skins para el jugador y enemigos
    """
    
    def __init__(self):
        self.player_skins = {}
        self.enemy_skins = {}
        self.current_player_skin = "default"
        self.current_enemy_skin = "default"
        
        print("🎨 Inicializando SkinManager...")
        self.load_all_skins()
        print(f"🎨 SkinManager inicializado. Skins cargadas: {list(self.player_skins.keys())}")
        print(f"🎨 Skin inicial: {self.current_player_skin}")
    
    def load_all_skins(self):
        """
        Carga todas las skins disponibles
        """
        print("🎨 Cargando skins...")
        self.load_player_skins()
        self.load_enemy_skins()
        
        # Asegurar que current_player_skin sea válida
        if self.current_player_skin not in self.player_skins:
            if "default" in self.player_skins:
                self.current_player_skin = "default"
            else:
                # Usar la primera skin disponible
                self.current_player_skin = list(self.player_skins.keys())[0]
        
        print(f"✅ Skins cargadas. Current skin asegurada: {self.current_player_skin}")
    
    def load_player_skins(self):
        """
        Carga las skins del jugador
        """
        # Skin por defecto (azul)
        self.player_skins["default"] = self.create_player_skin(Config.BLUE, Config.WHITE, Config.YELLOW)
        
        # Skin roja (fuego)
        self.player_skins["fire"] = self.create_player_skin((255, 69, 0), Config.YELLOW, (255, 140, 0))
        
        # Skin verde (naturaleza)
        self.player_skins["nature"] = self.create_player_skin((34, 139, 34), Config.WHITE, (154, 205, 50))
        
        # Skin púrpura (mágica)
        self.player_skins["magic"] = self.create_player_skin((138, 43, 226), Config.WHITE, (255, 20, 147))
        
        # Skin dorada (legendaria)
        self.player_skins["golden"] = self.create_player_skin((255, 215, 0), Config.BLACK, (255, 255, 0))
        
        # Skin cyber (tecnológica)
        self.player_skins["cyber"] = self.create_player_skin((0, 255, 255), Config.BLACK, (0, 191, 255))
        
        # Intentar cargar desde archivos
        self.load_player_skins_from_files()
    
    def load_enemy_skins(self):
        """
        Carga las skins de los enemigos
        """
        # Skin por defecto (roja)
        self.enemy_skins["default"] = self.create_enemy_skin(Config.RED, Config.BLACK, Config.GRAY)
        
        # Skin élite (negro)
        self.enemy_skins["elite"] = self.create_enemy_skin(Config.BLACK, Config.RED, Config.YELLOW)
        
        # Skin tanque (gris)
        self.enemy_skins["tank"] = self.create_enemy_skin((105, 105, 105), Config.BLACK, (169, 169, 169))
        
        # Skin rápido (verde)
        self.enemy_skins["fast"] = self.create_enemy_skin((0, 128, 0), Config.WHITE, (144, 238, 144))
        
        # Intentar cargar desde archivos
        self.load_enemy_skins_from_files()
    
    def create_player_skin(self, main_color, detail_color, weapon_color):
        """
        Crea una skin del jugador con colores personalizados
        """
        sprite = pygame.Surface((Config.PLAYER_SIZE, Config.PLAYER_SIZE), pygame.SRCALPHA)
        
        # Cuerpo principal (más visible)
        pygame.draw.circle(sprite, main_color, 
                         (Config.PLAYER_SIZE//2, Config.PLAYER_SIZE//2), 
                         Config.PLAYER_SIZE//2 - 2)
        
        # Cabeza/casco (más grande)
        pygame.draw.circle(sprite, detail_color, 
                         (Config.PLAYER_SIZE//2, Config.PLAYER_SIZE//4), 8)
        
        # Arma (más visible)
        weapon_rect = pygame.Rect(Config.PLAYER_SIZE//2 - 4, 
                                Config.PLAYER_SIZE//2 - 2, 8, 16)
        pygame.draw.rect(sprite, weapon_color, weapon_rect)
        
        # Detalles adicionales (más distintivos)
        pygame.draw.circle(sprite, detail_color, 
                         (Config.PLAYER_SIZE//2 - 8, Config.PLAYER_SIZE//2), 3)
        pygame.draw.circle(sprite, detail_color, 
                         (Config.PLAYER_SIZE//2 + 8, Config.PLAYER_SIZE//2), 3)
        
        # Agregar patrón único según colores
        if main_color == (255, 69, 0):  # Fire skin
            # Agregar llamas
            pygame.draw.polygon(sprite, (255, 140, 0), [
                (Config.PLAYER_SIZE//2, Config.PLAYER_SIZE//4),
                (Config.PLAYER_SIZE//2 - 4, Config.PLAYER_SIZE//4 + 6),
                (Config.PLAYER_SIZE//2 + 4, Config.PLAYER_SIZE//4 + 6)
            ])
        elif main_color == (34, 139, 34):  # Nature skin
            # Agregar hojas
            pygame.draw.ellipse(sprite, (154, 205, 50), 
                              (Config.PLAYER_SIZE//2 - 6, Config.PLAYER_SIZE//4 - 2, 4, 8))
            pygame.draw.ellipse(sprite, (154, 205, 50), 
                              (Config.PLAYER_SIZE//2 + 2, Config.PLAYER_SIZE//4 - 2, 4, 8))
        elif main_color == (255, 215, 0):  # Golden skin
            # Agregar brillo
            for i in range(3):
                pygame.draw.circle(sprite, (255, 255, 255), 
                                 (Config.PLAYER_SIZE//2 + i*3, Config.PLAYER_SIZE//2 + i*3), 1)
        
        # Borde distintivo
        pygame.draw.circle(sprite, Config.BLACK, 
                         (Config.PLAYER_SIZE//2, Config.PLAYER_SIZE//2), 
                         Config.PLAYER_SIZE//2 - 2, 3)
        
        return sprite
    
    def create_enemy_skin(self, main_color, detail_color, weapon_color):
        """
        Crea una skin del enemigo con colores personalizados
        """
        sprite = pygame.Surface((Config.ENEMY_SIZE, Config.ENEMY_SIZE), pygame.SRCALPHA)
        
        # Cuerpo principal
        pygame.draw.circle(sprite, main_color, 
                         (Config.ENEMY_SIZE//2, Config.ENEMY_SIZE//2), 
                         Config.ENEMY_SIZE//2 - 2)
        
        # Ojos
        pygame.draw.circle(sprite, detail_color,
                         (Config.ENEMY_SIZE//2 - 4, Config.ENEMY_SIZE//4), 2)
        pygame.draw.circle(sprite, detail_color,
                         (Config.ENEMY_SIZE//2 + 4, Config.ENEMY_SIZE//4), 2)
        
        # Arma
        weapon_rect = pygame.Rect(Config.ENEMY_SIZE//2 - 2, 
                                Config.ENEMY_SIZE//2, 4, 10)
        pygame.draw.rect(sprite, weapon_color, weapon_rect)
        
        # Borde
        pygame.draw.circle(sprite, Config.BLACK, 
                         (Config.ENEMY_SIZE//2, Config.ENEMY_SIZE//2), 
                         Config.ENEMY_SIZE//2 - 2, 2)
        
        return sprite
    
    def load_player_skins_from_files(self):
        """
        Carga skins del jugador desde archivos
        """
        skin_path = "assets/images/skins/player/"
        if os.path.exists(skin_path):
            for filename in os.listdir(skin_path):
                if filename.endswith(('.png', '.jpg', '.bmp')):
                    skin_name = filename.split('.')[0]
                    try:
                        sprite = pygame.image.load(os.path.join(skin_path, filename))
                        sprite = pygame.transform.scale(sprite, 
                                                      (Config.PLAYER_SIZE, Config.PLAYER_SIZE))
                        self.player_skins[skin_name] = sprite
                    except Exception as e:
                        print(f"Error cargando skin de jugador {filename}: {e}")
    
    def load_enemy_skins_from_files(self):
        """
        Carga skins de enemigos desde archivos
        """
        skin_path = "assets/images/skins/enemy/"
        if os.path.exists(skin_path):
            for filename in os.listdir(skin_path):
                if filename.endswith(('.png', '.jpg', '.bmp')):
                    skin_name = filename.split('.')[0]
                    try:
                        sprite = pygame.image.load(os.path.join(skin_path, filename))
                        sprite = pygame.transform.scale(sprite, 
                                                      (Config.ENEMY_SIZE, Config.ENEMY_SIZE))
                        self.enemy_skins[skin_name] = sprite
                    except Exception as e:
                        print(f"Error cargando skin de enemigo {filename}: {e}")
    
    def get_player_skin(self, skin_name=None):
        """
        Obtiene la skin actual del jugador
        """
        if skin_name is None:
            skin_name = self.current_player_skin
        
        return self.player_skins.get(skin_name, self.player_skins["default"])
    
    def get_enemy_skin(self, skin_name=None):
        """
        Obtiene la skin actual del enemigo
        """
        if skin_name is None:
            skin_name = self.current_enemy_skin
        
        return self.enemy_skins.get(skin_name, self.enemy_skins["default"])
    
    def set_player_skin(self, skin_name):
        """
        Cambia la skin del jugador
        """
        if skin_name in self.player_skins:
            self.current_player_skin = skin_name
            return True
        return False
    
    def set_enemy_skin(self, skin_name):
        """
        Cambia la skin del enemigo
        """
        if skin_name in self.enemy_skins:
            self.current_enemy_skin = skin_name
            return True
        return False
    
    def get_available_player_skins(self):
        """
        Obtiene lista de skins disponibles para el jugador
        """
        return list(self.player_skins.keys())
    
    def get_available_enemy_skins(self):
        """
        Obtiene lista de skins disponibles para enemigos
        """
        return list(self.enemy_skins.keys())
    
    def get_random_enemy_skin(self):
        """
        Obtiene una skin aleatoria para enemigos
        """
        import random
        skin_names = list(self.enemy_skins.keys())
        return random.choice(skin_names)