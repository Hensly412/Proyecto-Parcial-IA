# Lógica principal del juego HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import random
import math
from scripts.config import Config
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.bullet import Bullet
from scripts.game_map import GameMap
from scripts.sound_manager import SoundManager
from scripts.sprite_manager import SpriteManager

class Game:
    """
    Clase principal que maneja la lógica del juego
    """
    
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.game_over = False
        self.score = 0
        self.wave = 1
        self.enemies_killed = 0
        
        # Inicializar componentes
        self.sound_manager = SoundManager()
        self.sprite_manager = SpriteManager()
        self.game_map = GameMap()
        
        # Crear jugador
        start_x = Config.SCREEN_WIDTH // 2
        start_y = Config.SCREEN_HEIGHT - 100
        self.player = Player(start_x, start_y, self.sprite_manager)
        
        # Listas de entidades
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        
        # Timers
        self.enemy_spawn_timer = 0
        self.wave_timer = 0
        
        # Configurar gamepad si está disponible
        self.gamepad = None
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
        
        # Reproducir música de fondo
        self.sound_manager.play_music()
    
    def handle_event(self, event):
        """
        Maneja los eventos del juego
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "QUIT"
            elif event.key == pygame.K_SPACE:
                self.player_shoot()
        
        elif event.type == pygame.JOYBUTTONDOWN:
            if self.gamepad and event.button == 0:  # Botón A
                self.player_shoot()
        
        return None
    
    def update(self, dt):
        """
        Actualiza la lógica del juego
        """
        if self.game_over:
            return "GAME_OVER"
        
        # Actualizar controles del jugador
        self.update_player_input(dt)
        
        # Actualizar entidades
        self.player.update(dt)
        
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player.rect.center, self.game_map)
            
            # El enemigo dispara al jugador
            if enemy.can_shoot():
                bullet = enemy.shoot(self.player.rect.center)
                if bullet:
                    self.enemy_bullets.append(bullet)
        
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        for bullet in self.enemy_bullets[:]:
            bullet.update(dt)
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)
        
        # Spawn de enemigos
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= Config.ENEMY_SPAWN_RATE:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
        
        # Detectar colisiones
        self.check_collisions()
        
        # Verificar condiciones de game over
        if self.player.health <= 0:
            self.game_over = True
            return "GAME_OVER"
        
        # Actualizar wave
        self.wave_timer += dt
        if self.wave_timer >= 30:  # Nueva wave cada 30 segundos
            self.wave += 1
            self.wave_timer = 0
        
        return None
    
    def update_player_input(self, dt):
        """
        Actualiza los controles del jugador (teclado y gamepad)
        """
        keys = pygame.key.get_pressed()
        
        # Controles de teclado
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        
        # Controles de gamepad
        if self.gamepad:
            gamepad_x = self.gamepad.get_axis(0)
            gamepad_y = self.gamepad.get_axis(1)
            
            if abs(gamepad_x) > Config.GAMEPAD_DEADZONE:
                dx = gamepad_x
            if abs(gamepad_y) > Config.GAMEPAD_DEADZONE:
                dy = gamepad_y
        
        # Mover jugador
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, dt)
        
        # Disparo automático si se mantiene presionado
        if keys[pygame.K_SPACE] or (self.gamepad and self.gamepad.get_button(0)):
            if self.player.can_shoot():
                self.player_shoot()
    
    def player_shoot(self):
        """
        El jugador dispara una bala
        """
        bullet = self.player.shoot()
        if bullet:
            self.bullets.append(bullet)
            self.sound_manager.play_sound("shoot")
    
    def spawn_enemy(self):
        """
        Genera un nuevo enemigo en una posición aleatoria
        """
        # Generar en los bordes de la pantalla
        side = random.randint(0, 3)
        if side == 0:  # Arriba
            x = random.randint(0, Config.SCREEN_WIDTH)
            y = -Config.ENEMY_SIZE
        elif side == 1:  # Derecha
            x = Config.SCREEN_WIDTH + Config.ENEMY_SIZE
            y = random.randint(0, Config.SCREEN_HEIGHT)
        elif side == 2:  # Abajo
            x = random.randint(0, Config.SCREEN_WIDTH)
            y = Config.SCREEN_HEIGHT + Config.ENEMY_SIZE
        else:  # Izquierda
            x = -Config.ENEMY_SIZE
            y = random.randint(0, Config.SCREEN_HEIGHT)
        
        enemy = Enemy(x, y, self.sprite_manager)
        self.enemies.append(enemy)
    
    def check_collisions(self):
        """
        Verifica las colisiones entre entidades
        """
        # Balas del jugador vs enemigos
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(bullet.damage)
                    self.bullets.remove(bullet)
                    
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.enemies_killed += 1
                        self.score += 100
                        self.sound_manager.play_sound("enemy_death")
                    break
        
        # Balas de enemigos vs jugador
        for bullet in self.enemy_bullets[:]:
            if bullet.rect.colliderect(self.player.rect):
                self.player.take_damage(bullet.damage)
                self.enemy_bullets.remove(bullet)
                self.sound_manager.play_sound("player_hit")
        
        # Enemigos vs jugador (colisión directa)
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.player.take_damage(10)
                enemy.take_damage(25)
    
    def render(self):
        """
        Renderiza todos los elementos del juego
        """
        # Limpiar pantalla
        self.screen.fill(Config.DARK_GREEN)
        
        # Renderizar mapa
        self.game_map.render(self.screen)
        
        # Renderizar entidades
        self.player.render(self.screen)
        
        for enemy in self.enemies:
            enemy.render(self.screen)
        
        for bullet in self.bullets:
            bullet.render(self.screen)
        
        for bullet in self.enemy_bullets:
            bullet.render(self.screen)
        
        # Renderizar UI
        self.render_ui()
    
    def render_ui(self):
        """
        Renderiza la interfaz de usuario
        """
        font = pygame.font.Font(None, 36)
        
        # Salud del jugador
        health_text = font.render(f"Health: {self.player.health}", True, Config.WHITE)
        self.screen.blit(health_text, (10, 10))
        
        # Puntuación
        score_text = font.render(f"Score: {self.score}", True, Config.WHITE)
        self.screen.blit(score_text, (10, 50))
        
        # Wave actual
        wave_text = font.render(f"Wave: {self.wave}", True, Config.WHITE)
        self.screen.blit(wave_text, (10, 90))
        
        # Enemigos eliminados
        kills_text = font.render(f"Kills: {self.enemies_killed}", True, Config.WHITE)
        self.screen.blit(kills_text, (10, 130))
        
        # Barra de salud visual
        health_bar_width = 200
        health_bar_height = 20
        health_percentage = self.player.health / Config.PLAYER_HEALTH
        
        # Fondo de la barra de salud
        health_bar_bg = pygame.Rect(Config.SCREEN_WIDTH - health_bar_width - 10, 10, 
                                   health_bar_width, health_bar_height)
        pygame.draw.rect(self.screen, Config.RED, health_bar_bg)
        
        # Barra de salud actual
        health_bar_fg = pygame.Rect(Config.SCREEN_WIDTH - health_bar_width - 10, 10,
                                   health_bar_width * health_percentage, health_bar_height)
        pygame.draw.rect(self.screen, Config.GREEN, health_bar_fg)
    
    def show_game_over(self):
        """
        Muestra la pantalla de game over y maneja la entrada
        """
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Config.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # Texto de Game Over
        game_over_text = font_large.render("GAME OVER", True, Config.RED)
        game_over_rect = game_over_text.get_rect(center=(Config.SCREEN_WIDTH//2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Estadísticas finales
        final_score_text = font_medium.render(f"Final Score: {self.score}", True, Config.WHITE)
        final_score_rect = final_score_text.get_rect(center=(Config.SCREEN_WIDTH//2, 300))
        self.screen.blit(final_score_text, final_score_rect)
        
        kills_text = font_medium.render(f"Enemies Killed: {self.enemies_killed}", True, Config.WHITE)
        kills_rect = kills_text.get_rect(center=(Config.SCREEN_WIDTH//2, 350))
        self.screen.blit(kills_text, kills_rect)
        
        wave_text = font_medium.render(f"Wave Reached: {self.wave}", True, Config.WHITE)
        wave_rect = wave_text.get_rect(center=(Config.SCREEN_WIDTH//2, 400))
        self.screen.blit(wave_text, wave_rect)
        
        # Opciones
        restart_text = font_small.render("Press R to Restart", True, Config.YELLOW)
        restart_rect = restart_text.get_rect(center=(Config.SCREEN_WIDTH//2, 500))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = font_small.render("Press M for Main Menu", True, Config.YELLOW)
        menu_rect = menu_text.get_rect(center=(Config.SCREEN_WIDTH//2, 540))
        self.screen.blit(menu_text, menu_rect)
        
        # Manejar entrada
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return "RESTART"
        elif keys[pygame.K_m]:
            return "MENU"
        
        return None