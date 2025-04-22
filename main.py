import random
from guardarVectores import guardarVectoresJson

def generarVector(longitud=30):
# Genera un vector aleatorio de longitud 30 por defecto
    return [random.choice([0, 1]) for _ in range(longitud)]

def generarPoblacion(longitud=10):
# Utiliza la funcion generarVector para generar una poblacion de vectores, longitud en este caso es el tamaño de la poblacion.
    pobl = []
    for i in range(longitud):
        pobl.append(generarVector())
    return pobl

def cruzarVectores(vect1, vect2):

    posicionSplit = int(random.random() * len(vect1) + 1)
        
    # Separamos los vectores vect1 y vect2 en dos partes (Left y Right)
    vect1Right = vect1[posicionSplit:]
    vect1Left = vect1[:posicionSplit]
    vect2Right = vect2[posicionSplit:]
    vect2Left = vect2[:posicionSplit]

    # Unimos las partes, generando los nuevos vectores hijos que son cruza de sus padres
    vect1Hijo = vect1Left + vect2Right
    vect2Hijo = vect2Left + vect1Right

    print("\n ################# CRUZAR VECTORES #################\n \nPosicion del Split: ", posicionSplit,"\n\nPadre1: ",vect1,"\nPadre2: ", vect2,"\n\nHijo1: ",vect1Hijo,"\nHijo2: ",vect2Hijo,"\n\n")
    return vect1Hijo, vect2Hijo

def crossover(vect1, vect2):
    if(random.random()>0,75):
        ## Aca hacemos el crossover si aplica
        print()
    else:
        return vect1, vect2
    

cruzarVectores(generarVector(),generarVector())