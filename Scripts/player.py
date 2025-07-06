# Clase del jugador - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import math
from scripts.config import Config
from scripts.bullet import Bullet

class Player:
    """
    Clase que representa al jugador
    """
    
    def __init__(self, x, y, sprite_manager, skin_manager=None):
        self.x = x
        self.y = y
        self.sprite_manager = sprite_manager
        self.skin_manager = skin_manager
        self.rect = pygame.Rect(x, y, Config.PLAYER_SIZE, Config.PLAYER_SIZE)
        
        # Rastrear skin actual para detectar cambios
        self.current_skin_name = None
        
        # Estadísticas
        self.health = Config.PLAYER_HEALTH
        self.max_health = Config.PLAYER_HEALTH
        self.speed = Config.PLAYER_SPEED
        
        # Dirección y ángulo
        self.angle = 0  # Ángulo en radianes
        self.facing_direction = 0  # 0=Norte, 1=Este, 2=Sur, 3=Oeste
        
        # Sistema de disparo
        self.shoot_cooldown = 0
        self.shoot_delay = 0.2  # Segundos entre disparos
        
        # Sprites y animación
        self.sprite = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        
        # Cargar sprite del jugador
        self.load_sprite()
    
    def load_sprite(self):
        """
        Carga el sprite del jugador
        """
        # Usar skin manager si está disponible
        if self.skin_manager:
            new_sprite = self.skin_manager.get_player_skin()
            if new_sprite:
                self.sprite = new_sprite
                print(f"🎨 Sprite cargado desde SkinManager: {self.skin_manager.current_player_skin}")
            else:
                print("❌ SkinManager no devolvió sprite")
                self.create_fallback_sprite()
        else:
            print("❌ No hay SkinManager disponible")
            self.create_fallback_sprite()
    
    def create_fallback_sprite(self):
        """
        Crea sprite básico de respaldo
        """
        self.sprite = pygame.Surface((Config.PLAYER_SIZE, Config.PLAYER_SIZE))
        self.sprite.fill(Config.BLUE)
        
        # Agregar detalles al sprite
        pygame.draw.circle(self.sprite, Config.WHITE, 
                         (Config.PLAYER_SIZE//2, Config.PLAYER_SIZE//4), 4)
        pygame.draw.rect(self.sprite, Config.YELLOW,
                        (Config.PLAYER_SIZE//2 - 2, Config.PLAYER_SIZE//2, 4, 8))
        print("🎨 Sprite de respaldo creado")
    
    def update_skin(self):
        """
        Actualiza la skin del jugador (recarga el sprite)
        """
        self.load_sprite()
    
    def update(self, dt):
        """
        Actualiza el estado del jugador
        """
        # Verificar cambios de skin (DETECCIÓN MEJORADA)
        if self.skin_manager:
            current_skin_name = self.skin_manager.current_player_skin
            if current_skin_name != self.current_skin_name:
                print(f"🎨 CAMBIANDO SKIN EN PLAYER: {self.current_skin_name} → {current_skin_name}")
                self.current_skin_name = current_skin_name
                self.load_sprite()
                print(f"🎨 Sprite actualizado para skin: {current_skin_name}")
        
        # Actualizar cooldown de disparo
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        
        # Actualizar animación
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0
        
        # Mantener al jugador dentro de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.x = self.rect.x
        self.y = self.rect.y
    
    def move(self, dx, dy, dt):
        """
        Mueve al jugador en la dirección especificada
        """
        # Normalizar el vector de movimiento
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length
        
        # Calcular nueva posición
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        
        # Actualizar posición y rectángulo
        self.x = new_x
        self.y = new_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Actualizar dirección de cara
        if dx > 0:
            self.facing_direction = 1  # Este
        elif dx < 0:
            self.facing_direction = 3  # Oeste
        elif dy < 0:
            self.facing_direction = 0  # Norte
        elif dy > 0:
            self.facing_direction = 2  # Sur
        
        # Calcular ángulo para disparos
        if dx != 0 or dy != 0:
            self.angle = math.atan2(dy, dx)
    
    def can_shoot(self):
        """
        Verifica si el jugador puede disparar
        """
        return self.shoot_cooldown <= 0
    
    def shoot(self):
        """
        Dispara una bala en la dirección que está mirando el jugador
        """
        if not self.can_shoot():
            return None
        
        # Crear bala
        bullet_x = self.rect.centerx
        bullet_y = self.rect.centery
        
        # Dirección basada en la dirección de cara
        directions = [
            (0, -1),   # Norte
            (1, 0),    # Este
            (0, 1),    # Sur
            (-1, 0)    # Oeste
        ]
        
        dx, dy = directions[self.facing_direction]
        
        bullet = Bullet(bullet_x, bullet_y, dx, dy, Config.BULLET_DAMAGE, "player")
        
        # Activar cooldown
        self.shoot_cooldown = self.shoot_delay
        
        return bullet
    
    def take_damage(self, damage):
        """
        El jugador recibe daño
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        """
        Cura al jugador
        """
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    
    def render(self, screen):
        """
        Renderiza al jugador en la pantalla
        """
        # Verificar skin antes de renderizar (fuerza actualización)
        if self.skin_manager:
            self.sprite = self.skin_manager.get_player_skin()
        
        # Rotar sprite según la dirección
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.facing_direction * 90)
        
        # Centrar el sprite rotado
        sprite_rect = rotated_sprite.get_rect(center=self.rect.center)
        
        screen.blit(rotated_sprite, sprite_rect)
        
        # Renderizar indicador de salud si está herido
        if self.health < self.max_health:
            self.render_health_bar(screen)
    
    def render_health_bar(self, screen):
        """
        Renderiza una barra de salud sobre el jugador
        """
        bar_width = Config.PLAYER_SIZE
        bar_height = 6
        bar_x = self.rect.x
        bar_y = self.rect.y - 10
        
        # Fondo de la barra
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, Config.RED, bg_rect)
        
        # Barra de salud actual
        health_percentage = self.health / self.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
        pygame.draw.rect(screen, Config.GREEN, health_rect)
        
        # Borde
        pygame.draw.rect(screen, Config.WHITE, bg_rect, 1)