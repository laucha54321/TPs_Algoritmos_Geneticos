import random

def generar_vector(longitud=30):
    """
    Genera un vector (lista) de valores aleatorios.
    
    Args:
        longitud (int): El número de elementos en el vector. Por defecto es 20.
        
    Returns:
        list: Una lista de valores aleatorios.
    """
    return [random.choice([0, 1]) for _ in range(longitud)]

def generar_poblacion(longitud=10):
    pobl = []
    for i in range(longitud):
        pobl.append(generar_vector())
    return pobl
# Ejemplo de uso
poblacion = generar_poblacion()
print(poblacion)