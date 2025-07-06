# Clase de balas - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
from scripts.config import Config

class Bullet:
    """
    Clase que representa una bala
    """
    
    def __init__(self, x, y, dx, dy, damage, owner):
        self.x = x
        self.y = y
        self.dx = dx  # Dirección normalizada
        self.dy = dy
        self.damage = damage
        self.owner = owner  # "player" o "enemy"
        self.speed = Config.BULLET_SPEED
        
        self.rect = pygame.Rect(x, y, Config.BULLET_SIZE, Config.BULLET_SIZE)
        
        # Color según el propietario
        if owner == "player":
            self.color = Config.YELLOW
        else:
            self.color = Config.RED
    
    def update(self, dt):
        """
        Actualiza la posición de la bala
        """
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def is_off_screen(self):
        """
        Verifica si la bala está fuera de la pantalla
        """
        return (self.rect.right < 0 or self.rect.left > Config.SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > Config.SCREEN_HEIGHT)
    
    def render(self, screen):
        """
        Renderiza la bala
        """
        pygame.draw.circle(screen, self.color, self.rect.center, Config.BULLET_SIZE // 2)