# Debug específico del SkinManager - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
from scripts.skin_manager import SkinManager

def debug_skin_manager():
    """
    Debug específico del SkinManager
    """
    print("🔍 DEBUG ESPECÍFICO DEL SKINMANAGER")
    print("=" * 50)
    
    pygame.init()
    
    # Crear SkinManager
    print("\n1️⃣ Creando SkinManager...")
    skin_manager = SkinManager()
    
    # Verificar estado inicial
    print(f"\n2️⃣ Estado inicial:")
    print(f"   current_player_skin: {skin_manager.current_player_skin}")
    print(f"   Skins disponibles: {list(skin_manager.player_skins.keys())}")
    
    # Probar get_player_skin sin parámetros
    print(f"\n3️⃣ Probando get_player_skin() sin parámetros:")
    sprite = skin_manager.get_player_skin()
    print(f"   Sprite devuelto: {sprite}")
    
    # Cambiar skin
    print(f"\n4️⃣ Cambiando skin a 'fire':")
    success = skin_manager.set_player_skin("fire")
    print(f"   Cambio exitoso: {success}")
    
    # Verificar estado después del cambio
    print(f"\n5️⃣ Estado después del cambio:")
    print(f"   current_player_skin: {skin_manager.current_player_skin}")
    
    # Probar get_player_skin otra vez
    print(f"\n6️⃣ Probando get_player_skin() después del cambio:")
    sprite = skin_manager.get_player_skin()
    print(f"   Sprite devuelto: {sprite}")
    
    # Probar con parámetro específico
    print(f"\n7️⃣ Probando get_player_skin('fire') con parámetro:")
    sprite = skin_manager.get_player_skin("fire")
    print(f"   Sprite devuelto: {sprite}")
    
    # Verificar que las skins son diferentes
    print(f"\n8️⃣ Comparando sprites:")
    default_sprite = skin_manager.get_player_skin("default")
    fire_sprite = skin_manager.get_player_skin("fire")
    
    print(f"   Default sprite: {default_sprite}")
    print(f"   Fire sprite: {fire_sprite}")
    print(f"   Son diferentes: {default_sprite != fire_sprite}")
    
    if default_sprite and fire_sprite:
        # Comparar píxel por píxel (muestra)
        default_color = default_sprite.get_at((16, 16))
        fire_color = fire_sprite.get_at((16, 16))
        print(f"   Color en centro - Default: {default_color}, Fire: {fire_color}")
    
    pygame.quit()

if __name__ == "__main__":
    debug_skin_manager()