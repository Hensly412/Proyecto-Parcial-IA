# Árbol de Comportamiento implementado desde cero - HV Warriors
# Autor: Hensly Manuel Vidal Rosario
# Matrícula: 23-MISN-2-007

class BehaviorTree:
    """
    Implementación de Árbol de Comportamiento desde cero
    """
    
    def __init__(self, root):
        self.root = root
    
    def tick(self, context):
        """
        Ejecuta el árbol de comportamiento
        """
        return self.root.execute(context)

class Node:
    """
    Clase base para todos los nodos del árbol de comportamiento
    """
    
    def __init__(self):
        self.children = []
    
    def execute(self, context):
        """
        Ejecuta el nodo. Debe ser implementado por las subclases
        Retorna: SUCCESS, FAILURE, o RUNNING
        """
        raise NotImplementedError
    
    def add_child(self, child):
        """
        Agrega un nodo hijo
        """
        self.children.append(child)

class Selector(Node):
    """
    Nodo Selector: Ejecuta hijos hasta que uno retorne SUCCESS
    """
    
    def execute(self, context):
        for child in self.children:
            result = child.execute(context)
            if result == "SUCCESS":
                return "SUCCESS"
            elif result == "RUNNING":
                return "RUNNING"
        return "FAILURE"

class Sequence(Node):
    """
    Nodo Secuencia: Ejecuta hijos en orden hasta que uno falle
    """
    
    def execute(self, context):
        for child in self.children:
            result = child.execute(context)
            if result == "FAILURE":
                return "FAILURE"
            elif result == "RUNNING":
                return "RUNNING"
        return "SUCCESS"

class Leaf(Node):
    """
    Nodo hoja que ejecuta una función específica
    """
    
    def __init__(self, action_func):
        super().__init__()
        self.action_func = action_func
    
    def execute(self, context):
        return self.action_func(context)

class Condition(Node):
    """
    Nodo condición que evalúa una función booleana
    """
    
    def __init__(self, condition_func):
        super().__init__()
        self.condition_func = condition_func
    
    def execute(self, context):
        if self.condition_func(context):
            return "SUCCESS"
        else:
            return "FAILURE"

class Inverter(Node):
    """
    Nodo que invierte el resultado de su hijo
    """
    
    def __init__(self, child):
        super().__init__()
        self.child = child
    
    def execute(self, context):
        result = self.child.execute(context)
        if result == "SUCCESS":
            return "FAILURE"
        elif result == "FAILURE":
            return "SUCCESS"
        else:
            return result  # RUNNING permanece igual