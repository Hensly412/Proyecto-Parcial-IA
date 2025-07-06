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
        self.current_music_type = None  # "menu" o "game"
        
        # Configurar volumen
        pygame.mixer.music.set_volume(Config.MUSIC_VOLUME)
        
        # Cargar sonidos básicos (generados programáticamente)
        self.create_basic_sounds()
    
    def create_basic_sounds(self):
        """
        Crea sonidos básicos programáticamente si no hay archivos de audio
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
    
    def detect_file_format(self, filepath):
        """
        Detecta el formato real de un archivo de audio
        """
        try:
            with open(filepath, 'rb') as f:
                header = f.read(12)
                
            # Detectar formato por header
            if header.startswith(b'ID3') or header[6:10] == b'ftyp':
                return 'mp3'
            elif header.startswith(b'OggS'):
                return 'ogg'
            elif header.startswith(b'RIFF') and header[8:12] == b'WAVE':
                return 'wav'
            else:
                # Fallback: usar extensión del archivo
                return filepath.split('.')[-1].lower()
                
        except Exception:
            return filepath.split('.')[-1].lower()
    
    def try_load_music(self, filepath):
        """
        Intenta cargar música detectando automáticamente el formato
        """
        if not os.path.exists(filepath):
            return False
            
        try:
            # Detectar formato real
            real_format = self.detect_file_format(filepath)
            print(f"🔍 Archivo: {os.path.basename(filepath)} - Formato detectado: {real_format}")
            
            # Intentar cargar
            pygame.mixer.music.load(filepath)
            return True
            
        except Exception as e:
            print(f"❌ Error cargando {filepath}: {e}")
            return False
    
    def play_menu_music(self):
        """
        Reproduce música del menú
        """
        if self.current_music_type == "menu":
            return  # Ya está reproduciendo música del menú
        
        # Buscar archivos de música del menú
        menu_files = [
            "assets/music/menu_theme.mp3",
            "assets/music/menu_theme.wav", 
            "assets/music/menu_theme.ogg",
            "assets/music/menu.mp3",
            "assets/music/menu.wav",
            "assets/music/menu.ogg"
        ]
        
        for path in menu_files:
            if os.path.exists(path):
                if self.try_load_music(path):
                    try:
                        pygame.mixer.music.play(-1)  # Loop infinito
                        self.music_playing = True
                        self.current_music_type = "menu"
                        print(f"🎵 Música del menú cargada: {os.path.basename(path)}")
                        return
                    except Exception as e:
                        print(f"❌ Error reproduciendo {path}: {e}")
                        continue
        
        print("⚠️ No se pudo cargar música del menú")
        self.current_music_type = "menu"
    
    def play_game_music(self):
        """
        Reproduce música del juego
        """
        if self.current_music_type == "game":
            return  # Ya está reproduciendo música del juego
        
        # Buscar archivos de música del juego
        game_files = [
            "assets/music/game_theme.mp3",
            "assets/music/game_theme.wav",
            "assets/music/game_theme.ogg", 
            "assets/music/battle.mp3",
            "assets/music/battle.wav",
            "assets/music/battle.ogg",
            "assets/music/game.mp3",
            "assets/music/game.wav",
            "assets/music/game.ogg"
        ]
        
        for path in game_files:
            if os.path.exists(path):
                if self.try_load_music(path):
                    try:
                        pygame.mixer.music.play(-1)  # Loop infinito
                        self.music_playing = True
                        self.current_music_type = "game"
                        print(f"🎵 Música del juego cargada: {os.path.basename(path)}")
                        return
                    except Exception as e:
                        print(f"❌ Error reproduciendo {path}: {e}")
                        continue
        
        print("⚠️ No se pudo cargar música del juego")
        self.current_music_type = "game"
    
    def get_current_music_type(self):
        """
        Obtiene el tipo de música actual
        """
        return self.current_music_type or "Sin música"
    
    def play_sound(self, sound_name):
        """
        Reproduce un sonido
        """
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error reproduciendo sonido {sound_name}: {e}")
    
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