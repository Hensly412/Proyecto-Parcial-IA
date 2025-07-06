# Algoritmo A* implementado desde cero - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

import math
from scripts.config import Config

class Node:
    """
    Nodo para el algoritmo A*
    """
    
    def __init__(self, position, parent=None):
        self.position = position  # (x, y)
        self.parent = parent
        self.g = 0  # Costo desde el inicio
        self.h = 0  # Heurística al objetivo
        self.f = 0  # Costo total (g + h)
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f

class AStar:
    """
    Implementación del algoritmo A* desde cero
    """
    
    def __init__(self):
        self.grid_size = Config.TILE_SIZE
    
    def heuristic(self, pos1, pos2):
        """
        Calcula la distancia heurística entre dos posiciones (distancia euclidiana)
        """
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return math.sqrt(dx * dx + dy * dy)
    
    def get_neighbors(self, position):
        """
        Obtiene los vecinos válidos de una posición
        """
        x, y = position
        neighbors = []
        
        # 8 direcciones posibles
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dx, dy in directions:
            new_x = x + dx * self.grid_size
            new_y = y + dy * self.grid_size
            
            # Verificar límites de pantalla
            if (0 <= new_x < Config.SCREEN_WIDTH and 
                0 <= new_y < Config.SCREEN_HEIGHT):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    def is_walkable(self, position, game_map=None):
        """
        Verifica si una posición es transitable
        """
        x, y = position
        
        # Verificar límites básicos
        if (x < 0 or x >= Config.SCREEN_WIDTH or 
            y < 0 or y >= Config.SCREEN_HEIGHT):
            return False
        
        # Si hay un mapa del juego, verificar obstáculos
        if game_map:
            grid_x = x // Config.TILE_SIZE
            grid_y = y // Config.TILE_SIZE
            return game_map.is_walkable(grid_x, grid_y)
        
        return True
    
    def reconstruct_path(self, node):
        """
        Reconstruye el camino desde el nodo objetivo hasta el inicio
        """
        path = []
        current = node
        
        while current:
            path.append(current.position)
            current = current.parent
        
        return path[::-1]  # Invertir para obtener el camino del inicio al objetivo
    
    def find_path(self, start, goal, game_map=None):
        """
        Encuentra el camino más corto usando A*
        """
        # Convertir posiciones a coordenadas de grid
        start_grid = (int(start[0] // self.grid_size) * self.grid_size,
                     int(start[1] // self.grid_size) * self.grid_size)
        goal_grid = (int(goal[0] // self.grid_size) * self.grid_size,
                    int(goal[1] // self.grid_size) * self.grid_size)
        
        # Crear nodos de inicio y objetivo
        start_node = Node(start_grid)
        goal_node = Node(goal_grid)
        
        # Listas abiertas y cerradas
        open_list = [start_node]
        closed_list = []
        
        # Diccionario para acceso rápido a nodos en open_list
        open_dict = {start_grid: start_node}
        
        while open_list:
            # Encontrar el nodo con menor f
            current_node = min(open_list, key=lambda n: n.f)
            
            # Mover de open a closed
            open_list.remove(current_node)
            del open_dict[current_node.position]
            closed_list.append(current_node)
            
            # Verificar si llegamos al objetivo
            if current_node == goal_node:
                return self.reconstruct_path(current_node)
            
            # Explorar vecinos
            for neighbor_pos in self.get_neighbors(current_node.position):
                # Verificar si el vecino es transitable
                if not self.is_walkable(neighbor_pos, game_map):
                    continue
                
                # Verificar si ya está en la lista cerrada
                if any(node.position == neighbor_pos for node in closed_list):
                    continue
                
                # Crear nodo vecino
                neighbor_node = Node(neighbor_pos, current_node)
                
                # Calcular costos
                neighbor_node.g = current_node.g + self.heuristic(current_node.position, neighbor_pos)
                neighbor_node.h = self.heuristic(neighbor_pos, goal_grid)
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                
                # Verificar si ya está en open_list con mejor costo
                if neighbor_pos in open_dict:
                    existing_node = open_dict[neighbor_pos]
                    if neighbor_node.g < existing_node.g:
                        # Actualizar el nodo existente
                        existing_node.parent = current_node
                        existing_node.g = neighbor_node.g
                        existing_node.f = neighbor_node.f
                else:
                    # Agregar a open_list
                    open_list.append(neighbor_node)
                    open_dict[neighbor_pos] = neighbor_node
        
        # No se encontró camino
        return []
    
    def smooth_path(self, path):
        """
        Suaviza el camino eliminando puntos innecesarios
        """
        if len(path) <= 2:
            return path
        
        smoothed = [path[0]]
        
        for i in range(1, len(path) - 1):
            current = path[i]
            prev = smoothed[-1]
            next_point = path[i + 1]
            
            # Verificar si podemos ir directamente de prev a next
            if not self.line_of_sight(prev, next_point):
                smoothed.append(current)
        
        smoothed.append(path[-1])
        return smoothed
    
    def line_of_sight(self, start, end, game_map=None):
        """
        Verifica si hay línea de vista directa entre dos puntos
        """
        x0, y0 = start
        x1, y1 = end
        
        # Algoritmo de Bresenham para verificar línea de vista
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        x, y = x0, y0
        
        while True:
            # Verificar si la posición actual es transitable
            if not self.is_walkable((x, y), game_map):
                return False
            
            if x == x1 and y == y1:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        
        return True