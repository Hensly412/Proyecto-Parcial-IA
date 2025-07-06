# Mapa del juego - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import random
from scripts.config import Config

class GameMap:
    """
    Clase que maneja el mapa del juego
    """
    
    def __init__(self):
        self.width = Config.MAP_WIDTH
        self.height = Config.MAP_HEIGHT
        self.tile_size = Config.TILE_SIZE
        
        # Generar mapa básico
        self.tiles = self.generate_map()
    
    def generate_map(self):
        """
        Genera un mapa básico con algunos obstáculos
        """
        tiles = []
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Crear obstáculos aleatorios
                if random.random() < 0.1:  # 10% de probabilidad
                    row.append(1)  # Obstáculo
                else:
                    row.append(0)  # Suelo libre
            tiles.append(row)
        
        return tiles
    
    def is_walkable(self, grid_x, grid_y):
        """
        Verifica si una celda es transitable
        """
        if (grid_x < 0 or grid_x >= self.width or 
            grid_y < 0 or grid_y >= self.height):
            return False
        
        return self.tiles[grid_y][grid_x] == 0
    
    def render(self, screen):
        """
        Renderiza el mapa
        """
        for y in range(self.height):
            for x in range(self.width):
                pixel_x = x * self.tile_size
                pixel_y = y * self.tile_size
                
                rect = pygame.Rect(pixel_x, pixel_y, self.tile_size, self.tile_size)
                
                if self.tiles[y][x] == 1:  # Obstáculo
                    pygame.draw.rect(screen, Config.BROWN, rect)
                    pygame.draw.rect(screen, Config.BLACK, rect, 2)
                else:  # Suelo libre
                    pygame.draw.rect(screen, Config.DARK_GREEN, rect)
    
    def get_random_walkable_position(self):
        """
        Obtiene una posición aleatoria que sea transitable
        """
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            if self.is_walkable(x, y):
                return (x * self.tile_size, y * self.tile_size)