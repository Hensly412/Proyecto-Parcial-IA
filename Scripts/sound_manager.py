# Gestor de sonido - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
import os
from scripts.config import Config

class SoundManager:
    """
    Gestor de sonidos y música del juego
    """
    
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        
        # Configurar volumen
        pygame.mixer.music.set_volume(Config.MUSIC_VOLUME)
        
        # Cargar sonidos básicos (generados programáticamente)
        self.create_basic_sounds()
    
    def create_basic_sounds(self):
        """
        Crea sonidos básicos 
        """
        try:
            # Intentar cargar archivos de sonido reales
            sound_files = {
                "shoot": "assets/sounds/shoot.wav",
                "enemy_death": "assets/sounds/enemy_death.wav",
                "player_hit": "assets/sounds/player_hit.wav"
            }
            
            for name, path in sound_files.items():
                if os.path.exists(path):
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(Config.SFX_VOLUME)
                    self.sounds[name] = sound
                else:
                    # Crear sonido sintético
                    self.sounds[name] = self.create_synthetic_sound(name)
        
        except Exception as e:
            print(f"Error cargando sonidos: {e}")
            # Crear todos los sonidos sintéticamente
            for name in ["shoot", "enemy_death", "player_hit"]:
                self.sounds[name] = self.create_synthetic_sound(name)
    
    def create_synthetic_sound(self, sound_type):
        """
        Crea sonidos sintéticos usando pygame
        """
        try:
            # Crear un array de sonido básico
            import numpy as np
            
            sample_rate = 22050
            duration = 0.1  # 100ms
            
            if sound_type == "shoot":
                # Sonido de disparo - ruido blanco corto
                frequency = 800
                t = np.linspace(0, duration, int(sample_rate * duration))
                wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 10)
            
            elif sound_type == "enemy_death":
                # Sonido de muerte - tono descendente
                start_freq = 400
                end_freq = 100
                t = np.linspace(0, duration * 3, int(sample_rate * duration * 3))
                frequency = start_freq * np.exp(-t * 2)
                wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 2)
            
            elif sound_type == "player_hit":
                # Sonido de golpe - ruido fuerte y corto
                t = np.linspace(0, duration * 0.5, int(sample_rate * duration * 0.5))
                wave = np.random.random(len(t)) * 2 - 1
                wave *= np.exp(-t * 20)
            
            else:
                # Sonido genérico
                t = np.linspace(0, duration, int(sample_rate * duration))
                wave = np.sin(440 * 2 * np.pi * t) * np.exp(-t * 5)
            
            # Convertir a formato de pygame
            wave = (wave * 32767).astype(np.int16)
            wave = np.repeat(wave.reshape(wave.shape[0], 1), 2, axis=1)
            
            sound = pygame.sndarray.make_sound(wave)
            sound.set_volume(Config.SFX_VOLUME)
            return sound
            
        except ImportError:
            # Si numpy no está disponible, crear un sonido silencioso
            return pygame.mixer.Sound(buffer=b'\x00' * 1000)
        except Exception:
            # Crear sonido silencioso como fallback
            return pygame.mixer.Sound(buffer=b'\x00' * 1000)
    
    def play_sound(self, sound_name):
        """
        Reproduce un sonido
        """
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error reproduciendo sonido {sound_name}: {e}")
    
    def play_music(self):
        """
        Reproduce música de fondo
        """
        try:
            music_path = "assets/music/background.mp3"
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)  # Loop infinito
                self.music_playing = True
            else:
                # No hay música, continuamos sin ella
                print("No se encontró música de fondo")
        except Exception as e:
            print(f"Error cargando música: {e}")
    
    def stop_music(self):
        """
        Detiene la música
        """
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def set_music_volume(self, volume):
        """
        Ajusta el volumen de la música
        """
        pygame.mixer.music.set_volume(volume)
    
    def set_sfx_volume(self, volume):
        """
        Ajusta el volumen de los efectos de sonido
        """
        for sound in self.sounds.values():
            sound.set_volume(volume)