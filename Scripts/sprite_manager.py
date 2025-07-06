# Gestor de sprites - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import os
from scripts.config import Config

class SpriteManager:
    """
    Gestor de sprites e imágenes del juego
    """
    
    def __init__(self):
        self.sprites = {}
        self.load_sprites()
    
    def load_sprites(self):
        """
        Carga todos los sprites del juego
        """
        # Intentar cargar sprites desde archivos
        sprite_files = {
            "player": "assets/images/player.png",
            "enemy": "assets/images/enemy.png",
            "bullet": "assets/images/bullet.png"
        }
        
        for name, path in sprite_files.items():
            if os.path.exists(path):
                try:
                    sprite = pygame.image.load(path)
                    sprite = pygame.transform.scale(sprite, 
                                                  (Config.PLAYER_SIZE, Config.PLAYER_SIZE))
                    self.sprites[name] = sprite
                except Exception as e:
                    print(f"Error cargando sprite {name}: {e}")
                    self.sprites[name] = self.create_basic_sprite(name)
            else:
                # Crear sprite básico programáticamente
                self.sprites[name] = self.create_basic_sprite(name)
    
    def create_basic_sprite(self, sprite_type):
        """
        Crea sprites básicos programáticamente
        """
        if sprite_type == "player":
            sprite = pygame.Surface((Config.PLAYER_SIZE, Config.PLAYER_SIZE))
            sprite.fill(Config.BLUE)
            # Agregar detalles
            pygame.draw.circle(sprite, Config.WHITE, 
                             (Config.PLAYER_SIZE//2, Config.PLAYER_SIZE//4), 4)
            pygame.draw.rect(sprite, Config.YELLOW,
                           (Config.PLAYER_SIZE//2 - 2, Config.PLAYER_SIZE//2, 4, 8))
        
        elif sprite_type == "enemy":
            sprite = pygame.Surface((Config.ENEMY_SIZE, Config.ENEMY_SIZE))
            sprite.fill(Config.RED)
            # Agregar detalles
            pygame.draw.circle(sprite, Config.BLACK,
                             (Config.ENEMY_SIZE//2, Config.ENEMY_SIZE//4), 3)
            pygame.draw.rect(sprite, Config.GRAY,
                           (Config.ENEMY_SIZE//2 - 2, Config.ENEMY_SIZE//2, 4, 8))
        
        elif sprite_type == "bullet":
            sprite = pygame.Surface((Config.BULLET_SIZE, Config.BULLET_SIZE))
            sprite.fill(Config.YELLOW)
            pygame.draw.circle(sprite, Config.WHITE, 
                             (Config.BULLET_SIZE//2, Config.BULLET_SIZE//2), 
                             Config.BULLET_SIZE//4)
        
        else:
            # Sprite genérico
            sprite = pygame.Surface((32, 32))
            sprite.fill(Config.GRAY)
        
        return sprite
    
    def get_sprite(self, name):
        """
        Obtiene un sprite por nombre
        """
        return self.sprites.get(name, self.create_basic_sprite("generic"))
    
    def scale_sprite(self, sprite, scale_factor):
        """
        Escala un sprite
        """
        width = int(sprite.get_width() * scale_factor)
        height = int(sprite.get_height() * scale_factor)
        return pygame.transform.scale(sprite, (width, height))
    
    def rotate_sprite(self, sprite, angle):
        """
        Rota un sprite
        """
        return pygame.transform.rotate(sprite, angle)