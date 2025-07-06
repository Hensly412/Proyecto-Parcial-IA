# Clase del enemigo con IA - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import math
import random
from scripts.config import Config
from scripts.bullet import Bullet
from scripts.behavior_tree import BehaviorTree, Selector, Sequence, Leaf, Condition
from scripts.astar import AStar

class Enemy:
    """
    Clase que representa un enemigo con IA avanzada
    """
    
    def __init__(self, x, y, sprite_manager, skin_manager=None):
        self.x = x
        self.y = y
        self.sprite_manager = sprite_manager
        self.skin_manager = skin_manager
        self.rect = pygame.Rect(x, y, Config.ENEMY_SIZE, Config.ENEMY_SIZE)
        
        # Estadísticas
        self.health = Config.ENEMY_HEALTH
        self.max_health = Config.ENEMY_HEALTH
        self.speed = Config.ENEMY_SPEED
        
        # IA y comportamiento
        self.target_pos = None
        self.state = "PATROL"  # PATROL, CHASE, ATTACK, RETREAT
        self.behavior_tree = self.create_behavior_tree()
        self.behavior_timer = 0
        
        # Pathfinding A*
        self.astar = AStar()
        self.path = []
        self.current_path_index = 0
        self.pathfinding_timer = 0
        
        # Sistema de disparo
        self.shoot_cooldown = 0
        self.shoot_delay = 1.5  # Segundos entre disparos
        self.last_shot_time = 0
        
        # Detección del jugador
        self.sight_range = Config.ENEMY_SIGHT_RANGE
        self.attack_range = Config.ENEMY_ATTACK_RANGE
        self.player_detected = False
        self.last_player_pos = None
        
        # Patrullaje
        self.patrol_points = self.generate_patrol_points()
        self.current_patrol_index = 0
        
        # Sprites y animación
        self.sprite = None
        self.facing_direction = 0  # 0=Norte, 1=Este, 2=Sur, 3=Oeste
        self.animation_frame = 0
        self.animation_timer = 0
        
        self.load_sprite()
        
        # Estadísticas
        self.health = Config.ENEMY_HEALTH
        self.max_health = Config.ENEMY_HEALTH
        self.speed = Config.ENEMY_SPEED
        
        # IA y comportamiento
        self.target_pos = None
        self.state = "PATROL"  # PATROL, CHASE, ATTACK, RETREAT
        self.behavior_tree = self.create_behavior_tree()
        self.behavior_timer = 0
        
        # Pathfinding A*
        self.astar = AStar()
        self.path = []
        self.current_path_index = 0
        self.pathfinding_timer = 0
        
        # Sistema de disparo
        self.shoot_cooldown = 0
        self.shoot_delay = 1.5  # Segundos entre disparos
        self.last_shot_time = 0
        
        # Detección del jugador
        self.sight_range = Config.ENEMY_SIGHT_RANGE
        self.attack_range = Config.ENEMY_ATTACK_RANGE
        self.player_detected = False
        self.last_player_pos = None
        
        # Patrullaje
        self.patrol_points = self.generate_patrol_points()
        self.current_patrol_index = 0
        
        # Sprites y animación
        self.sprite = None
        self.facing_direction = 0  # 0=Norte, 1=Este, 2=Sur, 3=Oeste
        self.animation_frame = 0
        self.animation_timer = 0
        
        self.load_sprite()
    
    def load_sprite(self):
        """
        Carga el sprite del enemigo
        """
        # Crear sprite básico
        self.sprite = pygame.Surface((Config.ENEMY_SIZE, Config.ENEMY_SIZE))
        self.sprite.fill(Config.RED)
        
        # Agregar detalles
        pygame.draw.circle(self.sprite, Config.BLACK,
                         (Config.ENEMY_SIZE//2, Config.ENEMY_SIZE//4), 3)
        pygame.draw.rect(self.sprite, Config.GRAY,
                        (Config.ENEMY_SIZE//2 - 2, Config.ENEMY_SIZE//2, 4, 8))
    
    def generate_patrol_points(self):
        """
        Genera puntos de patrullaje aleatorios
        """
        points = []
        for i in range(3):
            x = random.randint(50, Config.SCREEN_WIDTH - 50)
            y = random.randint(50, Config.SCREEN_HEIGHT - 50)
            points.append((x, y))
        return points
    
    def create_behavior_tree(self):
        """
        Crea el árbol de comportamiento del enemigo
        """
        # Condiciones
        player_in_sight = Condition(self.is_player_in_sight)
        player_in_attack_range = Condition(self.is_player_in_attack_range)
        health_low = Condition(self.is_health_low)
        
        # Acciones
        chase_player = Leaf(self.chase_player_action)
        attack_player = Leaf(self.attack_player_action)
        patrol = Leaf(self.patrol_action)
        retreat = Leaf(self.retreat_action)
        
        # Estructura del árbol
        attack_sequence = Sequence()
        attack_sequence.add_child(player_in_attack_range)
        attack_sequence.add_child(attack_player)
        
        chase_sequence = Sequence()
        chase_sequence.add_child(player_in_sight)
        chase_sequence.add_child(chase_player)
        
        retreat_sequence = Sequence()
        retreat_sequence.add_child(health_low)
        retreat_sequence.add_child(retreat)
        
        main_selector = Selector()
        main_selector.add_child(retreat_sequence)
        main_selector.add_child(attack_sequence)
        main_selector.add_child(chase_sequence)
        main_selector.add_child(patrol)
        
        return BehaviorTree(main_selector)
    
    def update(self, dt, player_pos, game_map):
        """
        Actualiza el enemigo
        """
        # Actualizar timers
        self.behavior_timer += dt
        self.pathfinding_timer += dt
        self.shoot_cooldown -= dt
        
        # Ejecutar árbol de comportamiento
        if self.behavior_timer >= Config.BEHAVIOR_TREE_UPDATE_RATE:
            context = {
                'enemy': self,
                'player_pos': player_pos,
                'game_map': game_map,
                'dt': dt
            }
            self.behavior_tree.tick(context)
            self.behavior_timer = 0
        
        # Actualizar pathfinding
        if self.pathfinding_timer >= Config.PATHFINDING_UPDATE_RATE:
            if self.target_pos and self.state in ["CHASE", "RETREAT"]:
                self.update_pathfinding(game_map)
            self.pathfinding_timer = 0
        
        # Mover según el path actual
        self.follow_path(dt)
        
        # Actualizar posición del rectángulo
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def update_pathfinding(self, game_map):
        """
        Actualiza el pathfinding usando A*
        """
        if self.target_pos:
            start = (int(self.x), int(self.y))
            goal = (int(self.target_pos[0]), int(self.target_pos[1]))
            
            self.path = self.astar.find_path(start, goal, game_map)
            self.current_path_index = 0
    
    def follow_path(self, dt):
        """
        Sigue el path calculado por A*
        """
        if not self.path or self.current_path_index >= len(self.path):
            return
        
        target = self.path[self.current_path_index]
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 10:  # Llegó al punto
            self.current_path_index += 1
        else:
            # Mover hacia el punto
            dx /= distance
            dy /= distance
            
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt
            
            # Actualizar dirección de cara
            if abs(dx) > abs(dy):
                self.facing_direction = 1 if dx > 0 else 3
            else:
                self.facing_direction = 2 if dy > 0 else 0
    
    # Condiciones para el árbol de comportamiento
    def is_player_in_sight(self, context):
        """
        Verifica si el jugador está a la vista
        """
        player_pos = context['player_pos']
        distance = self.distance_to_player(player_pos)
        
        if distance <= self.sight_range:
            self.player_detected = True
            self.last_player_pos = player_pos
            return True
        
        return False
    
    def is_player_in_attack_range(self, context):
        """
        Verifica si el jugador está en rango de ataque
        """
        player_pos = context['player_pos']
        distance = self.distance_to_player(player_pos)
        return distance <= self.attack_range
    
    def is_health_low(self, context):
        """
        Verifica si la salud está baja
        """
        return self.health < self.max_health * 0.3
    
    def distance_to_player(self, player_pos):
        """
        Calcula la distancia al jugador
        """
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        return math.sqrt(dx*dx + dy*dy)
    
    # Acciones para el árbol de comportamiento
    def chase_player_action(self, context):
        """
        Persigue al jugador
        """
        player_pos = context['player_pos']
        self.state = "CHASE"
        self.target_pos = player_pos
        return "SUCCESS"
    
    def attack_player_action(self, context):
        """
        Ataca al jugador
        """
        player_pos = context['player_pos']
        self.state = "ATTACK"
        
        if self.can_shoot():
            # Lógica de disparo se maneja en el juego principal
            pass
        
        return "SUCCESS"
    
    def patrol_action(self, context):
        """
        Patrulla por puntos predefinidos
        """
        self.state = "PATROL"
        
        if not self.target_pos or self.distance_to_point(self.target_pos) < 20:
            # Cambiar al siguiente punto de patrulla
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
            self.target_pos = self.patrol_points[self.current_patrol_index]
        
        return "SUCCESS"
    
    def retreat_action(self, context):
        """
        Se retira del jugador
        """
        player_pos = context['player_pos']
        self.state = "RETREAT"
        
        # Calcular posición opuesta al jugador
        dx = self.rect.centerx - player_pos[0]
        dy = self.rect.centery - player_pos[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length > 0:
            dx /= length
            dy /= length
            
            retreat_x = self.rect.centerx + dx * 100
            retreat_y = self.rect.centery + dy * 100
            
            # Mantener dentro de la pantalla
            retreat_x = max(50, min(Config.SCREEN_WIDTH - 50, retreat_x))
            retreat_y = max(50, min(Config.SCREEN_HEIGHT - 50, retreat_y))
            
            self.target_pos = (retreat_x, retreat_y)
        
        return "SUCCESS"
    
    def distance_to_point(self, point):
        """
        Calcula la distancia a un punto
        """
        dx = point[0] - self.rect.centerx
        dy = point[1] - self.rect.centery
        return math.sqrt(dx*dx + dy*dy)
    
    def can_shoot(self):
        """
        Verifica si puede disparar
        """
        return self.shoot_cooldown <= 0
    
    def shoot(self, target_pos):
        """
        Dispara hacia una posición objetivo
        """
        if not self.can_shoot():
            return None
        
        # Calcular dirección
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        length = math.sqrt(dx*dx + dy*dy)
        
        if length > 0:
            dx /= length
            dy /= length
            
            bullet = Bullet(self.rect.centerx, self.rect.centery, 
                           dx, dy, Config.BULLET_DAMAGE, "enemy")
            
            self.shoot_cooldown = self.shoot_delay
            return bullet
        
        return None
    
    def take_damage(self, damage):
        """
        Recibe daño
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def render(self, screen):
        """
        Renderiza el enemigo
        """
        # Rotar sprite según dirección
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.facing_direction * 90)
        sprite_rect = rotated_sprite.get_rect(center=self.rect.center)
        screen.blit(rotated_sprite, sprite_rect)
        
        # Barra de salud si está herido
        if self.health < self.max_health:
            self.render_health_bar(screen)
        
        # Debug: mostrar path si está activo (opcional)
        # if self.path and len(self.path) > 1:
        #     for i in range(len(self.path) - 1):
        #         pygame.draw.line(screen, Config.YELLOW, self.path[i], self.path[i+1], 2)
    
    def render_health_bar(self, screen):
        """
        Renderiza barra de salud sobre el enemigo
        """
        bar_width = Config.ENEMY_SIZE
        bar_height = 4
        bar_x = self.rect.x
        bar_y = self.rect.y - 8
        
        # Fondo
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, Config.RED, bg_rect)
        
        # Salud actual
        health_percentage = self.health / self.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
        pygame.draw.rect(screen, Config.GREEN, health_rect)