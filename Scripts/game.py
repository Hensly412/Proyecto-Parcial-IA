# Lógica principal del juego HV Warriors (CON IMAGEN DE FONDO)
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import random
import math
import os
from scripts.config import Config
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.bullet import Bullet
from scripts.game_map import GameMap
from scripts.sound_manager import SoundManager
from scripts.sprite_manager import SpriteManager

class Game:
    """
    Clase principal que maneja la lógica del juego con fondo de imagen
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
        
        # Cargar imagen de fondo
        self.background = None
        self.background_offset_x = 0
        self.background_offset_y = 0
        self.load_background()
        
        print(f"🎮 Game: Componentes inicializados")
        
        # Crear jugador
        start_x = Config.SCREEN_WIDTH // 2
        start_y = Config.SCREEN_HEIGHT - 100
        self.player = Player(start_x, start_y, self.sprite_manager)
        
        print(f"🎮 Game: Player creado")
        
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
        
        # Reproducir música del juego
        self.sound_manager.play_game_music()
    
    def load_background(self):
        """
        Carga la imagen de fondo del juego
        """
        try:
            background_path = os.path.join("assets", "images", "game_background.jpg")
            if os.path.exists(background_path):
                self.background = pygame.image.load(background_path)
                # Hacer la imagen más grande para efecto parallax
                bg_width = int(Config.SCREEN_WIDTH * 1.5)
                bg_height = int(Config.SCREEN_HEIGHT * 1.5)
                self.background = pygame.transform.scale(self.background, (bg_width, bg_height))
                print("✓ Imagen de fondo del juego cargada")
            else:
                print("✗ No se encontró game_background.jpg")
                self.create_default_background()
        except Exception as e:
            print(f"✗ Error cargando imagen de fondo: {e}")
            self.create_default_background()
    
    def create_default_background(self):
        """
        Crea un fondo por defecto con patrón de terreno
        """
        width = int(Config.SCREEN_WIDTH * 1.5)
        height = int(Config.SCREEN_HEIGHT * 1.5)
        self.background = pygame.Surface((width, height))
        
        # Color base terroso
        self.background.fill((101, 67, 33))
        
        # Añadir textura
        for y in range(0, height, 40):
            for x in range(0, width, 40):
                if (x + y) % 80 == 0:
                    pygame.draw.rect(self.background, (80, 50, 20), (x, y, 40, 40))
        
        # Añadir algunos detalles
        for i in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(20, 40)
            pygame.draw.circle(self.background, (80, 50, 20), (x, y), radius)
    
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
        
        # Actualizar efecto parallax del fondo
        self.update_background_parallax()
        
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
    
    def update_background_parallax(self):
        """
        Actualiza el efecto parallax del fondo basado en la posición del jugador
        """
        if self.background:
            # Calcular offset basado en la posición del jugador
            player_x_ratio = self.player.rect.centerx / Config.SCREEN_WIDTH
            player_y_ratio = self.player.rect.centery / Config.SCREEN_HEIGHT
            
            max_offset_x = self.background.get_width() - Config.SCREEN_WIDTH
            max_offset_y = self.background.get_height() - Config.SCREEN_HEIGHT
            
            self.background_offset_x = int(player_x_ratio * max_offset_x * 0.3)  # 0.3 para efecto suave
            self.background_offset_y = int(player_y_ratio * max_offset_y * 0.3)
    
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
        
        # Crear enemigo básico
        try:
            enemy = Enemy(x, y, self.sprite_manager)
            self.enemies.append(enemy)
        except Exception as e:
            print(f"Error creando enemigo: {e}")
            # Crear enemigo mínimo de respaldo
            enemy = Enemy(x, y)
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
        # Dibujar imagen de fondo con efecto parallax
        if self.background:
            self.screen.blit(self.background, (-self.background_offset_x, -self.background_offset_y))
        else:
            self.screen.fill(Config.DARK_GREEN)
        
        # Overlay semi-transparente para el mapa
        map_overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        map_overlay.set_alpha(100)  # Muy transparente
        map_overlay.fill(Config.BLACK)
        self.screen.blit(map_overlay, (0, 0))
        
        # Renderizar mapa con transparencia
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
        Renderiza la interfaz de usuario con mejor diseño
        """
        font = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
        
        # Panel de información con fondo semi-transparente
        panel_width = 250
        panel_height = 170
        panel = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(200)
        panel.fill(Config.BLACK)
        self.screen.blit(panel, (10, 10))
        
        # Borde del panel
        pygame.draw.rect(self.screen, Config.WHITE, (10, 10, panel_width, panel_height), 2)
        
        # Salud del jugador con icono
        health_text = font.render(f"Health: {self.player.health}", True, Config.WHITE)
        self.screen.blit(health_text, (20, 20))
        
        # Puntuación
        score_text = font.render(f"Score: {self.score}", True, Config.YELLOW)
        self.screen.blit(score_text, (20, 60))
        
        # Wave actual
        wave_text = font.render(f"Wave: {self.wave}", True, Config.WHITE)
        self.screen.blit(wave_text, (20, 100))
        
        # Enemigos eliminados
        kills_text = font.render(f"Kills: {self.enemies_killed}", True, Config.WHITE)
        self.screen.blit(kills_text, (20, 140))
        
        # Barra de salud visual mejorada
        health_bar_width = 200
        health_bar_height = 25
        health_percentage = max(0, self.player.health / Config.PLAYER_HEALTH)
        
        # Posición de la barra de salud
        bar_x = Config.SCREEN_WIDTH - health_bar_width - 20
        bar_y = 20
        
        # Fondo de la barra de salud
        health_bar_bg = pygame.Rect(bar_x, bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(self.screen, (50, 0, 0), health_bar_bg)
        pygame.draw.rect(self.screen, Config.WHITE, health_bar_bg, 2)
        
        # Barra de salud actual con gradiente de color
        if health_percentage > 0:
            health_color = Config.GREEN if health_percentage > 0.5 else Config.YELLOW if health_percentage > 0.25 else Config.RED
            health_bar_fg = pygame.Rect(bar_x + 2, bar_y + 2,
                                       int((health_bar_width - 4) * health_percentage), health_bar_height - 4)
            pygame.draw.rect(self.screen, health_color, health_bar_fg)
        
        # Texto de porcentaje de salud
        health_percent_text = font_small.render(f"{int(health_percentage * 100)}%", True, Config.WHITE)
        health_percent_rect = health_percent_text.get_rect(center=(bar_x + health_bar_width // 2, bar_y + health_bar_height // 2))
        self.screen.blit(health_percent_text, health_percent_rect)
    
    def show_game_over(self):
        """
        Muestra la pantalla de game over mejorada
        """
        # Fondo oscuro con transparencia
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(Config.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # Panel central
        panel_width = 600
        panel_height = 400
        panel_x = (Config.SCREEN_WIDTH - panel_width) // 2
        panel_y = (Config.SCREEN_HEIGHT - panel_height) // 2
        
        # Dibujar panel
        panel = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(240)
        panel.fill((20, 20, 20))
        self.screen.blit(panel, (panel_x, panel_y))
        pygame.draw.rect(self.screen, Config.RED, (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Texto de Game Over
        game_over_text = font_large.render("GAME OVER", True, Config.RED)
        game_over_rect = game_over_text.get_rect(center=(Config.SCREEN_WIDTH//2, panel_y + 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Estadísticas finales
        stats_y = panel_y + 150
        final_score_text = font_medium.render(f"Final Score: {self.score}", True, Config.YELLOW)
        final_score_rect = final_score_text.get_rect(center=(Config.SCREEN_WIDTH//2, stats_y))
        self.screen.blit(final_score_text, final_score_rect)
        
        kills_text = font_medium.render(f"Enemies Killed: {self.enemies_killed}", True, Config.WHITE)
        kills_rect = kills_text.get_rect(center=(Config.SCREEN_WIDTH//2, stats_y + 50))
        self.screen.blit(kills_text, kills_rect)
        
        wave_text = font_medium.render(f"Wave Reached: {self.wave}", True, Config.WHITE)
        wave_rect = wave_text.get_rect(center=(Config.SCREEN_WIDTH//2, stats_y + 100))
        self.screen.blit(wave_text, wave_rect)
        
        # Opciones
        options_y = panel_y + panel_height - 80
        restart_text = font_small.render("Press R to Restart", True, Config.YELLOW)
        restart_rect = restart_text.get_rect(center=(Config.SCREEN_WIDTH//2 - 120, options_y))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = font_small.render("Press M for Main Menu", True, Config.YELLOW)
        menu_rect = menu_text.get_rect(center=(Config.SCREEN_WIDTH//2 + 120, options_y))
        self.screen.blit(menu_text, menu_rect)
        
        # Manejar entrada
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return "RESTART"
        elif keys[pygame.K_m]:
            return "MENU"
        
        return None