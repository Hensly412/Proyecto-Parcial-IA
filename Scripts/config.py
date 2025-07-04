# Configuración del juego HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame

class Config:
    """
    Clase de configuración que contiene todas las constantes del juego
    """
    
    # Configuración de pantalla
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    FPS = 60
    
    # Colores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    DARK_GREEN = (0, 128, 0)
    BROWN = (139, 69, 19)
    
    # Configuración del jugador
    PLAYER_SPEED = 200
    PLAYER_SIZE = 32
    PLAYER_HEALTH = 100
    
    # Configuración de enemigos
    ENEMY_SPEED = 80
    ENEMY_SIZE = 32
    ENEMY_HEALTH = 50
    ENEMY_SPAWN_RATE = 2.0  # segundos
    
    # Configuración de balas
    BULLET_SPEED = 400
    BULLET_SIZE = 8
    BULLET_DAMAGE = 25
    
    # Configuración del mapa
    TILE_SIZE = 32
    MAP_WIDTH = 32
    MAP_HEIGHT = 24
    
    # Configuración de la IA
    BEHAVIOR_TREE_UPDATE_RATE = 0.1  # segundos
    PATHFINDING_UPDATE_RATE = 0.5    # segundos
    ENEMY_SIGHT_RANGE = 150
    ENEMY_ATTACK_RANGE = 100
    
    # Configuración de sonido
    MUSIC_VOLUME = 0.5
    SFX_VOLUME = 0.7
    
    # Controles del gamepad
    GAMEPAD_DEADZONE = 0.2
    
    # Configuración de sprites
    SPRITE_SCALE = 1.0