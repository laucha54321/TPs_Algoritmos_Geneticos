import random
from guardarVectores import guardarVectoresJson

def generarVector(longitud=30):
    """
    Genera un vector (lista) de valores aleatorios.
    
    Args:
        longitud (int): El número de elementos en el vector. Por defecto es 20.
        
    Returns:
        list: Una lista de valores aleatorios.
    """
    return [random.choice([0, 1]) for _ in range(longitud)]

def generarPoblacion(longitud=10):
    pobl = []
    for i in range(longitud):
        pobl.append(generarVector())
    return pobl

def crossover(vect1, vect2):
    if(random.random()>0,75):
        ## Aca hacemos el crossover si aplica
        print()
    else:
        return vect1, vect2
    
poblacion = generarPoblacion()

guardarVectoresJson(poblacion)

print(poblacion)