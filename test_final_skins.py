# Test final de skins - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import pygame
from scripts.config import Config
from scripts.skin_manager import SkinManager
from scripts.player import Player

def test_final_skins():
    """
    Test final para verificar que las skins se cambian visualmente
    """
    print("🧪 TEST FINAL DE SKINS")
    print("=" * 50)
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Final - Cambio de Skins")
    clock = pygame.time.Clock()
    
    # Crear sistemas
    skin_manager = SkinManager()
    sprite_manager = None
    
    # Crear jugador
    player = Player(400, 300, sprite_manager, skin_manager)
    
    # Lista de skins para ciclar
    skins = skin_manager.get_available_player_skins()
    current_index = 0
    
    font = pygame.font.Font(None, 36)
    
    print(f"🎭 Skins disponibles: {skins}")
    print(f"🎮 Controles: ESPACIO = Cambiar skin, ESC = Salir")
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Cambiar a la siguiente skin
                    current_index = (current_index + 1) % len(skins)
                    new_skin = skins[current_index]
                    
                    print(f"\n🔄 CAMBIANDO SKIN:")
                    print(f"   Índice: {current_index}")
                    print(f"   Nueva skin: {new_skin}")
                    
                    # Cambiar skin en el manager
                    skin_manager.set_player_skin(new_skin)
                    
                    # Forzar actualización del jugador
                    player.current_skin_name = None  # Resetear para forzar detección
                    
                    print(f"   Skin en manager: {skin_manager.current_player_skin}")
                    
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Actualizar jugador
        player.update(dt)
        
        # Renderizar
        screen.fill((100, 100, 100))
        
        # Renderizar jugador (aquí es donde debería cambiar)
        player.render(screen)
        
        # UI
        current_skin = skin_manager.current_player_skin
        skin_text = font.render(f"Skin: {current_skin} ({current_index + 1}/{len(skins)})", True, (255, 255, 255))
        screen.blit(skin_text, (50, 50))
        
        instructions = font.render("ESPACIO = Cambiar skin | ESC = Salir", True, (200, 200, 200))
        screen.blit(instructions, (50, 500))
        
        # Mostrar colores de la skin actual para debug
        if player.sprite:
            try:
                center_color = player.sprite.get_at((16, 16))
                color_text = font.render(f"Color centro: {center_color}", True, (255, 255, 255))
                screen.blit(color_text, (50, 90))
            except:
                pass
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    test_final_skins()